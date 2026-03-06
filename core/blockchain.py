import aiohttp
import os
import logging
from typing import Optional, Dict, Any

class TonService:
    def __init__(self):
        self.api_url = os.getenv("TON_API_URL")
        self.api_key = os.getenv("TON_API_KEY")
        self.logger = logging.getLogger("blockchain")
        
        # Для публичного API ключ не обязателен
        if not self.api_url:
            self.logger.error("TON_API_URL not found in .env")
            raise ValueError("TON_API_URL must be set in .env")
        
        if not self.api_key:
            self.logger.warning("TON_API_KEY not found - using public API (rate limited)")

    async def get_balance(self, address: str) -> Optional[float]:
        """Получить баланс адреса в TON"""
        # API Toncenter v2: /api/v2/getAddressInformation
        url = f"{self.api_url}/getAddressInformation"
        params = {"address": address}
        
        # Заголовки только если есть ключ
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=headers) as resp:
                    data = await resp.json()
                    if data.get("ok"):
                        # Возвращаем баланс в nanoTON (раздели на 10^9 для TON)
                        balance_nano = int(data["result"]["balance"])
                        return balance_nano / 1_000_000_000
                    else:
                        self.logger.error(f"TON API Error: {data}")
                        return None
            except Exception as e:
                self.logger.error(f"TON API Connection Error: {e}")
                return None

    async def get_transaction_info(self, address: str, limit: int = 10) -> Optional[Dict[str, Any]]:
        """Получить информацию о транзакциях"""
        url = f"{self.api_url}/getTransactions"
        params = {"address": address, "limit": limit}
        
        # Заголовки только если есть ключ
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=headers) as resp:
                    data = await resp.json()
                    if data.get("ok"):
                        return data["result"]
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
        
        # Заголовки только если есть ключ
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=headers) as resp:
                    data = await resp.json()
                    return data.get("ok", False) and data.get("valid", False)
            except Exception as e:
                self.logger.error(f"TON API Validation Error: {e}")
                return False

    async def get_masterchain_info(self) -> Optional[Dict[str, Any]]:
        """Получить информацию о мастерчейне"""
        url = f"{self.api_url}/masterchainInfo"
        
        # Заголовки только если есть ключ
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as resp:
                    data = await resp.json()
                    if data.get("ok"):
                        return data["result"]
                    else:
                        self.logger.error(f"TON API Error: {data}")
                        return None
            except Exception as e:
                self.logger.error(f"TON API Connection Error: {e}")
                return None

# Глобальный экземпляр
ton_service = TonService()
