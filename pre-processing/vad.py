# vad.py
import torch
import torchaudio
import soundfile as sf
from silero_vad import load_silero_vad, get_speech_timestamps
import config

def load_model():
    print("Loading Silero VAD Model...")
    return load_silero_vad()

def process_audio(file_path, model):
    """
    Reads audio, converts to mono, resamples, and returns timestamps.
    """
    try:
        # Read audio
        audio, sr = sf.read(file_path, dtype='float32')
        waveform = torch.from_numpy(audio)

        # Convert to Mono
        if waveform.ndim > 1:
            waveform = torch.mean(waveform, dim=1)
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)

        # Resample if needed
        if sr != config.SAMPLE_RATE:
            resampler = torchaudio.transforms.Resample(sr, config.SAMPLE_RATE)
            waveform = resampler(waveform)

        # Get timestamps
        timestamps = get_speech_timestamps(
            waveform[0], 
            model, 
            sampling_rate=config.SAMPLE_RATE, 
            **config.VAD_PARAMS
        )
        
        return timestamps
    except Exception as e:
        print(f"Error processing audio {file_path}: {e}")
        return []