import aiohttp
import os
import asyncio
from dotenv import load_dotenv

load_dotenv('secrets/.env')

async def get_ton_balance(address: str):
    # Берем базовый URL из .env
    base_url = os.getenv("TON_API_URL", "https://toncenter.com/api/v2")
    
    # Используем другой метод - getWalletInformation
    url = f"{base_url}/getWalletInformation"
    
    # Передаем адрес кошелька в параметрах
    params = {"address": address}
    
    # Ставим таймаут, чтобы ничего не зависало (твоя мышка скажет спасибо)
    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                
                if data.get("ok"):
                    # Баланс приходит в nanoTON. Делим на 1 млрд, чтобы получить нормальные TON
                    balance_nano = int(data["result"]["balance"])
                    balance_ton = balance_nano / 1_000_000_000
                    return round(balance_ton, 4)
                else:
                    print(f"Ошибка API: {data.get('error')}")
                    return None
                    
        except Exception as e:
            print(f"Ошибка соединения: {e}")
            return None

async def test():
    print("Тестируем Mainnet адреса...")
    
    # Mainnet API - без ключа
    base_url = "https://toncenter.com/api/v2"
    
    # Простой адрес без спецсимволов
    test_wallet = "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE"
    
    print(f"Тестируем адрес: {test_wallet[:15]}...")
        
    url = f"{base_url}/getAddressInformation"
    params = {"address": test_wallet}
        
    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                    
                print(f"Status: {resp.status}")
                print(f"Response: {data}")
                    
                if data.get("ok"):
                    balance_nano = int(data["result"]["balance"])
                    balance_ton = balance_nano / 1_000_000_000
                    print(f"ПОБЕДА! Баланс: {balance_ton:.6f} TON")
                else:
                    print(f"Ошибка: {data}")
                        
        except Exception as e:
            print(f"Ошибка соединения: {e}")

if __name__ == "__main__":
    asyncio.run(test())
