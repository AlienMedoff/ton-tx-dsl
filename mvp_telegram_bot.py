import asyncio
import sys
import logging
import os
from datetime import datetime

# Фикс для Windows консоли
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import httpx
import json

# Импортируем TON сервис
from core.blockchain import ton_service

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "8652950916:AAHoJAJRbU58bH6P4ic7gOLRoZwcpp9PJ7k"
AI_SERVER_URL = "http://127.0.0.1:8001"

# Инициализация
bot = Bot(token=BOT_TOKEN)
router = Router()
dp = Dispatcher()

# Настройка клавиатуры
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start"), KeyboardButton(text="/help")],
        [KeyboardButton(text="/status"), KeyboardButton(text="/models")]
    ],
    resize_keyboard=True
)

async def get_ai_response(text, user_id):
    """Стучится в твой локальный Aether API"""
    payload = {
        "message": text,
        "model": "mistral", # По умолчанию используем стабильный Mistral
        "user_id": user_id
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(AI_SERVER_URL + "/ai/chat", json=payload)
            data = response.json()
            ai_response = data.get("response", "AI вернул пустой ответ.")
            
            # МАКСИМАЛЬНАЯ ОЧИСТКА ДЛЯ TELEGRAM
            import re
            
            # Убираем все эмодзи
            cleaned = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)\[\]\{\}"\'\/\\@#\$%\^&\*\+\=\|\~`]', '', ai_response)
            
            # Заменяем проблемные символы
            cleaned = cleaned.replace('{', '(').replace('}', ')')
            cleaned = cleaned.replace('[', '(').replace(']', ')')
            cleaned = cleaned.replace('\\', '/').replace('|', 'I')
            
            # Убираем множественные пробелы
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            print(f"Original: {ai_response[:100]}...")
            print(f"Cleaned: {cleaned[:100]}...")
            print(f"Length: {len(cleaned)} chars")
            
            return cleaned.strip()
        except Exception as e:
            return f"Error: {str(e)}"

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("🚀 Привет! Я Aether Bot. Бэкенд подключен, ИИ готов. Жду твое сообщение!", reply_markup=keyboard)

@dp.message(lambda message: message.text.startswith('/ton'))
async def cmd_ton(message: types.Message):
    """Обработка /ton команд"""
    try:
        # Получаем адрес из команды
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("📝 Использование: /ton <адрес_кошелька>")
            return
        
        address = parts[1]
        
        # Проверяем валидность адреса
        if not await ton_service.validate_address(address):
            await message.answer("❌ Неверный адрес кошелька TON")
            return
        
        # Получаем баланс
        balance = await ton_service.get_balance(address)
        if balance is not None:
            await message.answer(f"💰 Баланс кошелька {address[:10]}...:\n{balance:.6f} TON")
        else:
            await message.answer("❌ Не удалось получить баланс")
            
    except Exception as e:
        logger.error(f"TON command error: {e}")
        await message.answer("❌ Ошибка при обработке запроса")

@dp.message()
async def handle_message(message: types.Message):
    # Игнорируем команды
    if message.text.startswith('/'):
        return
    
    # Показываем, что бот печатает
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        print(f"Bot received: {message.text}")
        response = await get_ai_response(message.text, message.from_user.id)
        print(f"AI responded: {response}")
        print(f"Response length: {len(response)} characters")
        
        if response and len(response.strip()) > 0:
            # Просто отправляем как есть, без всяких разбивок
            await message.answer(response)
            print("Response sent successfully!")
        else:
            await message.answer("AI returned empty response. Please try again.")
            
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        print(f"Error: {e}")
        await message.answer("Error occurred while processing response")

async def main():
    print("=" * 60)
    print("AETHER MVP BOT STARTING...")
    print("=" * 60)
    
    # Сброс кэша Telegram (убивает конфликты)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # ЕДИНСТВЕННАЯ ТОЧКА ЗАПУСКА:
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
