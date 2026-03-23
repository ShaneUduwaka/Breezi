import asyncio
import os
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

async def test_google_apis():
    from adapters.tts_client import TTSClient
    from adapters.stt_client import STTClient

    print("Initializing TTS...")
    tts = TTSClient(provider="google")
    await tts.connect()
    print("Synthesizing Sinhala Text...")
    audio_data = await tts.synthesize_file(
        text="ආයුබෝවන්, කෙහොමද ඔබට?", 
        output_path="sinhala_test.wav", 
        language="si-LK"
    )
    print("✅ TTS Output saved to sinhala_test.wav")

    print("\nInitializing STT...")
    stt = STTClient(provider="google")
    await stt.connect()
    print("Transcribing Sinhala Audio...")
    transcript = await stt.transcribe_file(
        audio_file_path="sinhala_test.wav",
        language="si-LK"
    )
    print(f"✅ STT Transcript: {transcript}")

if __name__ == "__main__":
    asyncio.run(test_google_apis())
