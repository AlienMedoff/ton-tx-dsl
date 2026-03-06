# 🤖 Aether Debate Bot

Многоагентная система с дебатами между AI моделями.

## 🚀 Возможности

- 🧠 **Многоагентные дебаты** - Mistral, Groq, Gemini, Claude
- 🔒 **Безопасность** - SecurityKernel с аномалиями
- 🧠 **Управление сессиями** - Redis для хранения контекста
- 📊 **Метрики** - Prometheus + Health endpoint
- 🗄️ **Аривирование** - Сохранение и восстановление сессий
- ⚠️ **Алерты** - Telegram уведомления о проблемах

## 🛠️ Установка

```bash
# Клонируем
git clone <repository>
cd debate_bot

# Устанавливаем зависимости
pip install -r requirements.txt

# Настраиваем
cp .env.example .env
# Редактируем .env с токенами и настройками

# Запускаем
python debate_bot.py
```

## ⚙️ Конфигурация

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ALLOWED_USERS=834545801
ALERT_CHAT_ID=your_alert_chat_id
REDIS_URL=redis://localhost:6379
REDIS_PASS=your_redis_password
KERNEL_SECRET=changeme-32-chars-minimum!!!!!
AUDIT_LOG=audit.log
```

## 📋 Команды

- `/start` - Запуск бота
- `/agents` - Список активных агентов
- `/history` - История дебатов
- `/archives` - Архивные сессии
- `/restore <timestamp>` - Восстановление сессии
- `/reset` - Архивация текущей сессии
- `/status` - Статус системы

## 🔍 Эндпоинты

- `GET /health` - Health check
- `GET /metrics` - Prometheus метрики

## 🏗️ Архитектура

```
┌─────────────────┐
│  Telegram Bot  │
├─────────────────┤
│  SecurityKernel │
├─────────────────┤
│  Redis Storage  │
├─────────────────┤
│  AI Agents      │
└─────────────────┘
```

## 🔒 Безопасность

- Rate limiting
- Input sanitization
- Anomaly detection
- Audit logging
- Session management

## 📊 Мониторинг

- Uptime tracking
- Error counting
- Rate limiting metrics
- Agent performance

---

**Создано для Aether Multi-Agent System** 🚀
