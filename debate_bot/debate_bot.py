import asyncio
import hashlib
import json
import logging
import os
import time
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiohttp import web
import redis.asyncio as aioredis

from debate import run_debate
from agents import AGENTS
from memory import (
    save_debate, get_history,
    add_to_session, get_session,
    archive_session, get_archives, restore_session
)
from hardened_kernel_v2 import SecurityKernel, SecurityMiddleware, sanitize
from core.blockchain import ton_service

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("bot")

# ============================================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================================

ALLOWED_USERS = set(
    int(x) for x in os.getenv("ALLOWED_USERS", "").split(",") if x.strip()
)
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG", "audit.log")

bot    = Bot(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
router = Router()
dp     = Dispatcher()

_start_time   = time.time()
_debate_count = 0
_error_count  = 0

# ============================================================
# AUDIT
# ============================================================

def audit_log(user_id: int, action: str, payload: dict) -> None:
    entry      = {"user_id": user_id, "action": action, "payload": payload, "timestamp": time.time()}
    entry_str  = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry_hash = hashlib.sha256(entry_str.encode()).hexdigest()
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(f"{entry_hash} {entry_str}\n")
    logger.info(f"[audit] {action} user={user_id} -> {entry_hash[:12]}")

# ============================================================
# ALERT — аномалии летят в Telegram
# ============================================================

ALERT_CHAT_ID = os.getenv("ALERT_CHAT_ID")

async def send_alert(text: str) -> None:
    if not ALERT_CHAT_ID:
        return
    try:
        await bot.send_message(
            chat_id=ALERT_CHAT_ID,
            text=f"🚨 *SECURITY ALERT*\n\n{text}",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"[alert] Failed to send: {e}")

# ============================================================
# ПРОПУСКНОЙ КОНТРОЛЬ
# ============================================================

async def access_check(message: Message) -> bool:
    uid = message.from_user.id
    if ALLOWED_USERS and uid not in ALLOWED_USERS:
        audit_log(uid, "ACCESS_DENIED", {"text": (message.text or "")[:50]})
        await message.answer("⛔ Доступ запрещён")
        return False
    return True

# ============================================================
# HANDLERS
# ============================================================

@router.message(CommandStart())
async def start(message: Message):
    uid   = message.from_user.id
    if not await access_check(message): return
    names = " · ".join(f"{cfg['emoji']}{name}" for name, cfg in AGENTS.items())
    audit_log(uid, "START", {})
    await message.answer(
        f"👋 <b>Aether Multi-Agent Hub</b>\n\n"
        f"Агенты: {names}\n\n"
        f"/agents — список агентов\n"
        f"/history — последние дебаты\n"
        f"/archives — архивные сессии\n"
        f"/reset — архивировать и начать заново\n"
        f"/status — статус системы\n"
        f"/ton &lt;адрес&gt; — баланс TON"
    )

@router.message(Command("agents"))
async def agents_cmd(message: Message):
    if not await access_check(message): return
    text = "🤖 <b>Активные агенты:</b>\n\n"
    for name, cfg in AGENTS.items():
        text += f"{cfg['emoji']} <b>{name}</b> — <code>{cfg['model']}</code>\n"
    await message.answer(text)

@router.message(Command("status"))
async def status_cmd(message: Message, kernel: SecurityKernel = None):
    if not await access_check(message): return
    uid     = message.from_user.id
    now     = time.time()
    uptime  = int(now - _start_time)
    h, m    = divmod(uptime // 60, 60)
    context = await get_session(uid)
    # метрики rate limit из Redis
    rl_key  = f"ratelimit:{uid}"
    r       = kernel.redis if kernel else None
    recent  = await r.zcard(rl_key) if r else "?"
    await message.answer(
        f"📊 <b>Статус системы</b>\n\n"
        f"⏱ Аптайм: {h}ч {m}м\n"
        f"💬 Дебатов: {_debate_count}\n"
        f"❌ Ошибок: {_error_count}\n"
        f"📨 Запросов за минуту: {recent}\n"
        f"🤖 Агентов: {len(AGENTS)}\n"
        f"🧠 Сообщений в контексте: {len(context)}"
    )

@router.message(Command("history"))
async def history_cmd(message: Message):
    if not await access_check(message): return
    uid     = message.from_user.id
    history = await get_history(uid)
    if not history:
        await message.answer("📭 История пуста")
        return
    text = "📚 *Последние дебаты:*\n\n"
    for i, item in enumerate(history, 1):
        q     = item["question"][:80]
        short = item["consensus"][:150]
        text += f"*{i}.* {q}...\n_{short}..._\n\n"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@router.message(Command("reset"))
async def reset_cmd(message: Message):
    if not await access_check(message): return
    uid = message.from_user.id
    await archive_session(uid)
    audit_log(uid, "SESSION_ARCHIVED", {})
    await message.answer(
        "📦 Сессия заархивирована.\n"
        "Начинаем с чистого листа.\n"
        "Вернуться: /archives"
    )

@router.message(Command("archives"))
async def archives_cmd(message: Message):
    if not await access_check(message): return
    uid      = message.from_user.id
    archives = await get_archives(uid)
    if not archives:
        await message.answer("📭 Архив пуст")
        return
    text = "🗄 *Архивные сессии:*\n\n"
    for a in archives[-5:]:
        ts   = a["timestamp"]
        dt   = time.strftime("%d.%m.%Y %H:%M", time.localtime(ts))
        text += f"📁 `{ts}` — {dt} ({len(a['messages'])} сообщений)\n"
        text += f"Восстановить: `/restore {ts}`\n\n"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@router.message(Command("restore"))
async def restore_cmd(message: Message):
    if not await access_check(message): return
    uid  = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /restore <timestamp>")
        return
    try:
        ts = int(args[1])
    except ValueError:
        await message.answer("❌ Неверный timestamp")
        return
    ok = await restore_session(uid, ts)
    if ok:
        audit_log(uid, "SESSION_RESTORED", {"timestamp": ts})
        await message.answer("✅ Сессия восстановлена.")
    else:
        await message.answer("❌ Архив не найден")

@router.message(Command("ton"))
async def ton_cmd(message: Message):
    """Команда проверки баланса TON"""
    args = message.text.split()
    if len(args) < 2:
        await message.answer("⚠️ Использование: /ton &lt;адрес_кошелька&gt;")
        return
    
    address = args[1]
    status_msg = await message.answer("⏳ Стучусь в блокчейн TON...")
    
    try:
        balance = await ton_service.get_balance(address)
        
        if balance is not None:
            await status_msg.edit_text(
                f"💰 <b>Баланс кошелька</b>\n\n"
                f"Адрес: <code>{address[:15]}...{address[-6:]}</code>\n"
                f"Баланс: <b>{balance:.6f} TON</b>\n\n"
                f"📊 Данные получены через toncenter.com"
            )
        else:
            await status_msg.edit_text(
                "❌ <b>Ошибка получения баланса</b>\n\n"
                f"Возможные причины:\n"
                f"• Неверный адрес кошелька\n"
                f"• Проблемы с API toncenter.com\n"
                f"• Превышен лимит запросов\n\n"
                f"Попробуйте позже или проверьте адрес."
            )
            
    except Exception as e:
        logger.error(f"TON command error: {e}")
        await status_msg.edit_text(
            f"❌ <b>Критическая ошибка</b>\n\n"
            f"Ошибка: <code>{str(e)}</code>\n\n"
            f"Пожалуйста, сообщите администратору."
        )

@router.message()
async def handle(message: Message):
    global _debate_count, _error_count
    if not await access_check(message): return

    uid      = message.from_user.id
    question = message.text or ""
    context  = await get_session(uid)

    audit_log(uid, "DEBATE_START", {"question": question[:200]})
    status = await message.answer("🔄 Запускаю дебаты...")

    async def on_agent_done(name, answer):
        # НЕ шлём каждый ответ в TG — только консенсус
        # Агенты видны в веб-консоли
        pass

    try:
        result = await run_debate(question, context=context, progress_callback=on_agent_done)
        _debate_count += 1

        await add_to_session(uid, "user", question)
        await add_to_session(uid, "assistant", result["consensus"])
        await save_debate(uid, question, result["consensus"])

        audit_log(uid, "DEBATE_DONE", {"consensus_len": len(result["consensus"])})
        await status.edit_text("✅ Готово")

        # TG лимит — режем консенсус на части по 4000 символов
        consensus = result["consensus"]
        chunks    = [consensus[i:i+4000] for i in range(0, len(consensus), 4000)]
        for idx, chunk in enumerate(chunks):
            prefix = "🎯 <b>КОНСЕНСУС</b>\n\n" if idx == 0 else f"<b>[{idx+1}/{len(chunks)}]</b>\n\n"
            await message.answer(prefix + chunk)

    except Exception as e:
        _error_count += 1
        audit_log(uid, "DEBATE_ERROR", {"error": str(e)})
        await send_alert(f"DEBATE_ERROR\nUser: {uid}\nError: {e}")
        await status.edit_text(f"❌ Ошибка: {e}")

# ============================================================
# HEALTH + METRICS (Prometheus)
# ============================================================

async def healthcheck(request):
    return web.json_response({
        "status": "ok",
        "uptime":  round(time.time() - _start_time),
        "debates": _debate_count,
        "errors": _error_count,
        "agents": list(AGENTS.keys()),
    })

async def metrics(request):
    return web.Response(
        content_type="text/plain",
        text=(
            "# HELP aether_uptime_seconds Bot uptime\n"
            "# TYPE aether_uptime_seconds counter\n"
            f"aether_uptime_seconds {round(time.time() - _start_time)}\n"
            "# HELP aether_debates_total Debates processed\n"
            "# TYPE aether_debates_total counter\n"
            f"aether_debates_total {_debate_count}\n"
            "# HELP aether_errors_total Errors\n"
            "# TYPE aether_errors_total counter\n"
            f"aether_errors_total {_error_count}\n"
            "# HELP aether_agents_total Agents\n"
            "# TYPE aether_agents_total gauge\n"
            f"aether_agents_total {len(AGENTS)}\n"
        )
    )

async def start_health_server():
    app = web.Application()
    app.router.add_get("/health", healthcheck)
    app.router.add_get("/metrics", metrics)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logger.info("Health/metrics on :8080")

# ============================================================
# MAIN
# ============================================================

async def main():
    redis_client = aioredis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379"),
        password=os.getenv("REDIS_PASS"),
        decode_responses=True
    )

    kernel = SecurityKernel(
        secret_key=os.getenv("KERNEL_SECRET", "changeme-32-chars-minimum!!!!!"),
        redis_client=redis_client
    )

    # Monkey-patch _anomaly чтобы алерты летели в TG
    _orig_anomaly = kernel._anomaly
    async def _anomaly_with_alert(agent_id: str, reason: str):
        await _orig_anomaly(agent_id, reason)
        count = await redis_client.get(f"anomaly:{agent_id}") or "?"
        await send_alert(
            f"⚠️ Аномалия\nAgent: `{agent_id}`\nReason: `{reason}`\nCount: {count}"
        )
    kernel._anomaly = _anomaly_with_alert

    # Middleware на роутер
    router.message.middleware(SecurityMiddleware(kernel, os.getenv("KERNEL_SECRET", "")))
    dp.include_router(router)

    logger.info("Aether Bot starting...")
    await asyncio.gather(
        dp.start_polling(bot),
        start_health_server(),
    )

if __name__ == "__main__":
    asyncio.run(main())
