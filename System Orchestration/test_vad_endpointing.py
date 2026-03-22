import asyncio
import numpy as np
import torch
from system.bootsrap import build_system
from system.audio_pipeline import AudioPipelineManager

async def test_vad_endpointing():
    print("Building system...")
    # We only need the pipeline
    system = build_system(True)
    pipeline = system["pipeline"]
    
    session_id = "test-vad-session"
    await pipeline.start_session(session_id)
    sess = pipeline.sessions[session_id]
    
    # 1. Create a "speech" chunk (dummy loud noise + Silero high prob)
    # We'll mock the vad_model to return 0.95
    original_vad = pipeline.vad_model
    class MockVAD:
        def __init__(self, prob): self.prob = prob
        def __call__(self, tensor, rate):
            class Result:
                def item(self): return self.prob
                def __getattr__(self, name): return lambda: 0.95
            return Result()
    
    pipeline.vad_model = MockVAD(0.95)
    
    print("\n--- TEST: Speech Detection ---")
    # Feed enough chunks to trigger speech_ever_detected
    # VAD_CONSECUTIVE_CHUNKS is 5
    speech_chunk = (np.random.randn(512)*5000).astype(np.int16).tobytes()
    for i in range(10):
        await pipeline.feed_audio_chunk(session_id, speech_chunk)
        
    assert sess["speech_ever_detected"] == True
    assert sess["end_of_turn"] == False
    print("PASS: Speech detected, turn not ended yet.")
    
    print("\n--- TEST: Silence Endpointing ---")
    # Now switch to silence
    pipeline.vad_model = MockVAD(0.01)
    silence_chunk = np.zeros(512, dtype=np.int16).tobytes()
    
    # Needs VAD_SILENCE_CHUNKS = 20
    for i in range(25):
        await pipeline.feed_audio_chunk(session_id, silence_chunk)
        if sess["end_of_turn"]:
            break
            
    assert sess["end_of_turn"] == True
    print(f"PASS: VAD endpoint detected after {i+1} silence chunks!")
    
    print("\nALL VAD TESTS PASSED!")
    
    # Cleanup
    pipeline.vad_model = original_vad
    await pipeline.stop_session(session_id)

if __name__ == "__main__":
    asyncio.run(test_vad_endpointing())
