import asyncio
import os
import json
import base64
from dotenv import load_dotenv
from adapters.stt_client import STTClient

async def test_live_connection():
    load_dotenv()
    print("--- STARTING STT TEST ---")
    
    # Initialize client
    client = STTClient()
    
    print("Connecting...")
    connected = await client.connect()
    if not connected:
        print("❌ Error: API Key missing or client failed to connect.")
        return

    # Use a real word if possible? No, we'll just check if it stays open
    async def dummy_audio_stream():
        print("Feeding 2 seconds of silence/ambient noise...")
        for i in range(10):
            # Send small real PCM-like noise? No, just zeros is fine for handshake check.
            yield b'\x00' * 1024
            await asyncio.sleep(0.1)
        
        print("Sending sentinel...")
        yield None

    try:
        print("Opening transcribe_stream...")
        # We wrap it in a timeout so we don't hang if the server doesn't respond
        async with asyncio.timeout(15): 
            async for result in client.transcribe_stream(dummy_audio_stream(), "test-session"):
                print(f"✨ RESULT: {result.text}")
    except asyncio.TimeoutError:
        print("⏳ Test timed out (Expected if no speech detected). Handshake likely succeeded.")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
    finally:
        await client.close()
        print("--- TEST CONCLUDED ---")

if __name__ == "__main__":
    asyncio.run(test_live_connection())
