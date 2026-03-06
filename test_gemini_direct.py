import asyncio
import httpx

async def test_gemini():
    """Тестируем Gemini напрямую через AI сервис"""
    print("Testing Gemini through AI service...")
    
    payload = {
        "message": "Hello! How are you?",
        "model": "gemini",
        "user_id": 123456789
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8001/ai/chat", json=payload)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Gemini Response: {data.get('response', 'No response')}")
                print(f"Processing time: {data.get('processing_time', 'N/A')}s")
                print(f"Tokens used: {data.get('tokens_used', 'N/A')}")
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
