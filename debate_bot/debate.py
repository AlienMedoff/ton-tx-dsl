import asyncio
import json
import logging
import time
from agents import AGENTS
from memory import get_session, add_to_session, save_debate

logger = logging.getLogger("debate")

async def run_debate(question: str, context: list = None, progress_callback=None) -> dict:
    """Запускает дебаты между агентами"""
    
    logger.info(f"Starting debate: {question[:100]}...")
    
    # Инициализация
    participants = list(AGENTS.keys())
    responses = {}
    
    # Этап 1: Каждый агент анализирует вопрос
    for name, config in AGENTS.items():
        try:
            # Здесь должна быть логика обращения к AI API
            # Для примера - заглушка
            response = f"[{name}] Я бы проанализировал этот вопрос с точки зрения {config['role']}. Мой стиль: {config['style']}."
            responses[name] = response
            
            if progress_callback:
                await progress_callback(name, response)
                
            # Небольшая задержка для симуляции
            await asyncio.sleep(0.5)
            
        except Exception as e:
            logger.error(f"Agent {name} error: {e}")
            responses[name] = f"[{name}] Ошибка: {e}"
    
    # Этап 2: Формирование консенсуса
    consensus = f"КОНСЕНСУС: {' | '.join(responses.values())}"
    
    # Этап 3: Сохранение
    # await save_debate(user_id, question, consensus)
    
    logger.info("Debate completed")
    
    return {
        "question": question,
        "responses": responses,
        "consensus": consensus,
        "participants": participants
    }
