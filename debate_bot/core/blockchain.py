import aiohttp
import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv('debate_bot/.env')

logger = logging.getLogger("blockchain")

class TonService:
    """TON блокчейн сервис для debate bot"""
    
    def __init__(self):
        self.api_url = os.getenv("TON_API_URL", "https://toncenter.com/api/v2")
        self.api_key = os.getenv("TON_API_KEY")
        self.logger = logging.getLogger("blockchain")
        
        if not self.api_url:
            self.logger.error("TON_API_URL not found in .env")
            raise ValueError("TON_API_URL must be set in .env")
        
        if not self.api_key:
            self.logger.warning("TON_API_KEY not found - using public API (rate limited)")
    
    async def get_balance(self, address: str) -> Optional[float]:
        """Получить баланс адреса в TON"""
        url = f"{self.api_url}/getAddressInformation"
        params = {"address": address}
        
        # Заголовки только если есть ключ
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params, headers=headers) as resp:
                    data = await resp.json()
                    
                    if data.get("ok"):
                        balance_nano = int(data["result"]["balance"])
                        balance_ton = balance_nano / 1_000_000_000
                        return round(balance_ton, 6)
                    else:
                        self.logger.error(f"TON API Error: {data}")
                        return None
        except Exception as e:
            self.logger.error(f"TON API Connection Error: {e}")
            return None
    
    async def validate_address(self, address: str) -> bool:
        """Проверить валидность адреса"""
        url = f"{self.api_url}/validateAddress"
        params = {"address": address}
        
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params, headers=headers) as resp:
                    data = await resp.json()
                    return data.get("ok", False) and data.get("valid", False)
        except Exception as e:
            self.logger.error(f"TON API Validation Error: {e}")
            return False

# Глобальный экземпляр
ton_service = TonService()
