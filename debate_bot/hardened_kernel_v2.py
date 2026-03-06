import asyncio
import hashlib
import hmac
import json
import logging
import time
from typing import Callable, Any, Dict

logger = logging.getLogger("security")

class SecurityKernel:
    """Ядро безопасности для многоагентной системы"""
    
    def __init__(self, secret_key: str, redis_client=None):
        self.secret_key = secret_key.encode()
        self.redis_client = redis_client
        self._anomaly_callbacks = []
        
    def _anomaly(self, agent_id: str, reason: str, severity: str = "medium"):
        """Внутренний метод для аномалий"""
        anomaly_data = {
            "agent_id": agent_id,
            "reason": reason,
            "severity": severity,
            "timestamp": time.time(),
            "hash": self._hash_event(agent_id, reason)
        }
        
        # Логируем
        logger.warning(f"ANOMALY: {anomaly_data}")
        
        # Сохраняем в Redis если доступно
        if self.redis_client:
            anomaly_key = f"anomaly:{agent_id}"
            loop = asyncio.get_event_loop()
            loop.create_task(self._redis_client.incr(anomaly_key))
            loop.create_task(self._redis_client.expire(anomaly_key, 3600))  # 1 час
        
        # Вызываем коллбэки
        for callback in self._anomaly_callbacks:
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(callback(agent_id, reason))
            except Exception as e:
                logger.error(f"Anomaly callback error: {e}")
    
    def _hash_event(self, agent_id: str, reason: str) -> str:
        """Хеширование события"""
        payload = f"{agent_id}:{reason}:{time.time()}"
        return hmac.new(self.secret_key, payload.encode(), hashlib.sha256).hexdigest()
    
    def add_anomaly_callback(self, callback: Callable):
        """Добавляет коллбэк для аномалий"""
        self._anomaly_callbacks.append(callback)
    
    async def validate_agent_response(self, agent_id: str, response: str) -> Dict[str, Any]:
        """Валидация ответа агента"""
        issues = []
        
        # Проверка длины
        if len(response) > 10000:
            issues.append("response_too_long")
        
        # Проверка на инъекции
        dangerous_patterns = ["<script>", "javascript:", "eval(", "exec("]
        for pattern in dangerous_patterns:
            if pattern.lower() in response.lower():
                issues.append(f"dangerous_pattern_{pattern}")
        
        # Проверка на подозрительные ссылки
        if "http://" in response.lower() or "https://" in response.lower():
            issues.append("suspicious_urls")
        
        # Проверка частоты сообщений
        if self.redis_client:
            rate_key = f"rate:{agent_id}"
            loop = asyncio.get_event_loop()
            loop.create_task(self._redis_client.incr(rate_key))
            loop.create_task(self._redis_client.expire(rate_key, 60))  # 1 минута
            
            # Получаем текущее значение
            current_rate = await self.redis_client.get(rate_key)
            if int(current_rate or 0) > 10:  # больше 10 сообщений в минуту
                issues.append("rate_limit_exceeded")
                loop.create_task(self._anomaly(agent_id, "Too many messages", "high"))
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "response_length": len(response),
            "timestamp": time.time()
        }
    
    def sanitize_input(self, input_text: str) -> str:
        """Очистка входных данных"""
        if not input_text:
            return ""
        
        # Базовая очистка
        sanitized = input_text.strip()
        
        # Удаление опасных символов
        dangerous_chars = ['<', '>', '&', '"', "'", '\x00']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Ограничение длины
        if len(sanitized) > 5000:
            sanitized = sanitized[:5000] + "...[truncated]"
        
        return sanitized

class SecurityMiddleware:
    """Middleware для безопасности"""
    
    def __init__(self, kernel: SecurityKernel, secret: str):
        self.kernel = kernel
        self.secret = secret
        
    async def __call__(self, handler, message, *args, **kwargs):
        """Оборачивание хендлера"""
        user_id = message.from_user.id
        
        # Валидация входных данных (без перезаписи frozen объекта)
        sanitized_text = self.kernel.sanitize_input(message.text or "")
        
        # НЕ перезаписываем message.text - просто проверяем
        if sanitized_text != message.text:
            # Логируем попытку инъекции
            logger.warning(f"Input sanitization detected for user {user_id}")
        
        if hasattr(message, 'from_user') and message.from_user:
            agent_id = f"tg_user_{user_id}"
            
            # Здесь может быть дополнительная логика проверки
            # Например, проверка на спам, флуд и т.д.
            
            # Логируем активность
            if self.kernel.redis_client:
                activity_key = f"activity:{user_id}"
                await self.kernel.redis_client.incr(activity_key)
                await self.kernel.redis_client.expire(activity_key, 3600)  # 1 час
        
        # Вызываем оригинальный хендлер
        return await handler(message, *args, **kwargs)

def sanitize(text: str) -> str:
    """Глобальная функция очистки"""
    if not text:
        return ""
    
    # Базовая очистка
    sanitized = text.strip()
    
    # Удаление HTML тегов
    import re
    sanitized = re.sub(r'<[^>]+>', '', sanitized)
    
    # Удаление опасных символов
    dangerous_chars = ['<', '>', '&', '"', "'", '\x00']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Ограничение длины
    if len(sanitized) > 5000:
        sanitized = sanitized[:5000] + "...[truncated]"
    
    return sanitized
