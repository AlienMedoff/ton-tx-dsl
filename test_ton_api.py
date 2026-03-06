import asyncio
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv('secrets/.env')

async def test_ton_api():
    """Тестируем TON API с Public Toncenter"""
    
    print("TON API Test - Public Toncenter")
    api_key = os.getenv("TON_API_KEY")
    api_url = os.getenv("TON_API_URL")
    
    if api_key:
        print(f"API Key: {api_key[:10]}...{api_key[-10:]}")
    else:
        print("API Key: None (публичный режим)")
    
    print(f"API URL: {api_url}")
    
    if not api_url:
        print("TON API URL не найден в .env!")
        return
    
    # Тестовый адрес (можно заменить на свой)
    test_address = "EQCD39vsKjSzbLwqGzjwB5yCghXcMq5r8e5mK2pUqjXQ7Y8"  # Реальный тестовый адрес
    
    try:
        from core.blockchain import ton_service
        
        print(f"\nТестируем адрес: {test_address}")
        
        # Проверяем валидность адреса
        is_valid = await ton_service.validate_address(test_address)
        print(f"Адрес валиден: {is_valid}")
        
        if is_valid:
            # Получаем баланс
            balance = await ton_service.get_balance(test_address)
            if balance is not None:
                print(f"Баланс: {balance:.6f} TON")
            else:
                print("Не удалось получить баланс")
        
        # Получаем инфо о мастерчейне
        masterchain = await ton_service.get_masterchain_info()
        if masterchain:
            print(f"Мастерчейн: {masterchain.get('last', {}).get('seqno', 'N/A')}")
        
        print("\nTON API работает!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Проверь ключи и подключение к интернету")

if __name__ == "__main__":
    asyncio.run(test_ton_api())
