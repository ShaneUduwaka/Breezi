import asyncio
import sounddevice as sd
import numpy as np
import sys
import queue

from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

from system.bootsrap import build_system
from system.audio_pipeline import AudioPipelineManager

# STT expects 16kHz Mono 16-bit PCM
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = 'int16'
SESSION_ID = "mic_session"

async def run_hardware_test():
    print("Building Breezi system...")
    system = build_system()
    
    # Must wait to ensure STT/TTS connections happen
    stt = system["stt_client"]
    tts = system["tts_client"]
    await stt.connect()
    await tts.connect()
    print("\U0001F3A4 System connected to Google Cloud services.")
    
    pipeline = AudioPipelineManager(system)
    await pipeline.start_session(SESSION_ID)
    
    # We use sync Queues for python-sounddevice callback communication
    loop = asyncio.get_running_loop()

    def audio_callback(indata, frames, time, status):
        """This runs on a separate thread from PyAudio/sounddevice."""
        if status:
            print(status, file=sys.stderr)
        # Convert numpy array to raw bytes
        raw_bytes = indata.tobytes()
        # Feed safely to asyncio loop
        asyncio.run_coroutine_threadsafe(pipeline.feed_audio_chunk(SESSION_ID, raw_bytes), loop)

    print("\U0001F3A4 Starting microphone stream (Press Ctrl+C to stop)...")
    
    try:
        # Start input stream for microphone
        in_stream = sd.InputStream(
            samplerate=SAMPLE_RATE, 
            channels=CHANNELS, 
            dtype=DTYPE, 
            callback=audio_callback,
            blocksize=int(SAMPLE_RATE * 0.1) # 100ms chunks
        )
        in_stream.start()

        # Build speaker player loop
        out_stream = sd.OutputStream(
            samplerate=16000, # Matched with TTSClient configuration
            channels=1,
            dtype='int16'
        )
        out_stream.start()

        print("📢 Talk into your microphone in Sinhala!")
        
        async for output_chunk in pipeline.get_audio_stream(SESSION_ID):
            # Play the returning chunks!
            chunk_array = np.frombuffer(output_chunk, dtype=np.int16)
            # Use to_thread to prevent blocking the async event loop!
            await asyncio.to_thread(out_stream.write, chunk_array)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await pipeline.stop_session(SESSION_ID)
        in_stream.stop()
        in_stream.close()
        out_stream.stop()
        out_stream.close()
        print("Test concluded.")

if __name__ == "__main__":
    asyncio.run(run_hardware_test())
