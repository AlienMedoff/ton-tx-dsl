import httpx
import asyncio
import sys

# Фикс для Windows консоли
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

async def test_ai_service():
    """Тестируем AI сервис напрямую"""
    print("Testing AI service...")
    
    payload = {
        "message": "Hello! How are you?",
        "model": "mistral",
        "user_id": 123456789
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8000/ai/chat", json=payload)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', 'Empty response')
                print(f"AI Response: {ai_response}")
                print(f"Response length: {len(ai_response)} characters")
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_service())
