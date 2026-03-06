import json
import os
import redis.asyncio as aioredis
import logging

logger = logging.getLogger("memory")

# Redis клиент
redis_client = None

async def init_redis():
    """Инициализация Redis"""
    global redis_client
    try:
        redis_client = aioredis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379"),
            password=os.getenv("REDIS_PASS"),
            decode_responses=True
        )
        await redis_client.ping()
        logger.info("Redis connected")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        redis_client = None

async def get_session(user_id: int) -> list:
    """Получает текущую сессию"""
    if not redis_client:
        return []
    
    try:
        session_data = await redis_client.get(f"session:{user_id}")
        if session_data:
            return json.loads(session_data)
        return []
    except Exception as e:
        logger.error(f"Get session error: {e}")
        return []

async def add_to_session(user_id: int, role: str, content: str):
    """Добавляет сообщение в сессию"""
    if not redis_client:
        return
    
    try:
        session = await get_session(user_id)
        session.append({"role": role, "content": content, "timestamp": time.time()})
        
        # Ограничиваем размер сессии
        if len(session) > 50:
            session = session[-50:]
        
        await redis_client.setex(f"session:{user_id}", 3600, json.dumps(session))
    except Exception as e:
        logger.error(f"Add to session error: {e}")

async def save_debate(user_id: int, question: str, consensus: str):
    """Сохраняет дебату"""
    if not redis_client:
        return
    
    try:
        debate_data = {
            "question": question,
            "consensus": consensus,
            "timestamp": time.time()
        }
        
        # Добавляем в историю
        history_key = f"history:{user_id}"
        history = await redis_client.lrange(history_key, 0, -1)
        history.append(debate_data)
        
        # Храним только последние 100 дебатов
        if len(history) > 100:
            history = history[-100:]
        
        await redis_client.delete(history_key)
        for item in history:
            await redis_client.rpush(history_key, json.dumps(item))
        
        logger.info(f"Debate saved for user {user_id}")
    except Exception as e:
        logger.error(f"Save debate error: {e}")

async def get_history(user_id: int) -> list:
    """Получает историю дебатов"""
    if not redis_client:
        return []
    
    try:
        history_data = await redis_client.lrange(f"history:{user_id}", 0, -1)
        return [json.loads(item) for item in history_data]
    except Exception as e:
        logger.error(f"Get history error: {e}")
        return []

async def archive_session(user_id: int):
    """Аривирует текущую сессию"""
    if not redis_client:
        return
    
    try:
        session = await get_session(user_id)
        if session:
            archive_key = f"archives:{user_id}"
            await redis_client.rpush(archive_key, json.dumps({
                "session": session,
                "timestamp": time.time()
            }))
            
            # Удаляем текущую сессию
            await redis_client.delete(f"session:{user_id}")
            
            logger.info(f"Session archived for user {user_id}")
    except Exception as e:
        logger.error(f"Archive session error: {e}")

async def get_archives(user_id: int) -> list:
    """Получает архив сессий"""
    if not redis_client:
        return []
    
    try:
        archives_data = await redis_client.lrange(f"archives:{user_id}", 0, -1)
        return [json.loads(item) for item in archives_data]
    except Exception as e:
        logger.error(f"Get archives error: {e}")
        return []

async def restore_session(user_id: int, timestamp: int):
    """Восстанавливает сессию из архива"""
    if not redis_client:
        return False
    
    try:
        archives_data = await redis_client.lrange(f"archives:{user_id}", 0, -1)
        
        for item in archives_data:
            archive = json.loads(item)
            if archive["timestamp"] == timestamp:
                # Восстанавливаем сессию
                await redis_client.setex(f"session:{user_id}", 3600, json.dumps(archive["session"]))
                
                # Удаляем из архива
                await redis_client.lrem(f"archives:{user_id}", 1, item)
                
                logger.info(f"Session restored for user {user_id}")
                return True
        
        return False
    except Exception as e:
        logger.error(f"Restore session error: {e}")
        return False
