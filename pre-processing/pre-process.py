import torch
import torchaudio
import soundfile as sf
import numpy as np
from silero_vad import load_silero_vad, get_speech_timestamps
import os
import subprocess
import glob

# --- Configuration (Internal Paths) ---
INPUT_DIR = "/data/raw_audio"
OUTPUT_DIR = "/data/final_chunks"
SAMPLE_RATE = 16000 # 16kHz

# --- Filtering Rules ---
MIN_DURATION_SEC = 3.0   # Discard anything shorter than 3s (noise/coughs)
MAX_DURATION_SEC = 30.0  # Discard anything longer than 30s

vad_params = {
    'min_speech_duration_ms': 250,
    'min_silence_duration_ms': 500
}

def main():
    print("\n--- Sinhala Pre-Processing Pipeline (Chunk & Filter) ---")
    print(f"Reading from: {INPUT_DIR}")
    print(f"Saving to:    {OUTPUT_DIR}")
    print(f"Filter Rules: {MIN_DURATION_SEC}s - {MAX_DURATION_SEC}s")

    print("\n1. Loading Silero VAD model (CPU)...")
    model = load_silero_vad()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Find all audio files recursively
    audio_files = []
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(('.wav', '.flac', '.mp3')):
                audio_files.append(os.path.join(root, file))
    
    if not audio_files:
        print(f"ERROR: No audio files found in '{INPUT_DIR}'.")
        print("Did you mount the volume correctly? Check your docker run command.")
        return

    print(f"Found {len(audio_files)} audio files to process.\n")
    
    global_chunk_counter = 1
    total_kept = 0
    total_skipped = 0

    for long_file_path in audio_files:
        long_file_name = os.path.basename(long_file_path)
        print(f"--- Processing: {long_file_name} ---")

        try:
            # 1. Load Audio (Safe Method)
            audio_data, original_sample_rate = sf.read(long_file_path, dtype='float32')
            waveform = torch.from_numpy(audio_data)

            # 2. Stereo to Mono (for VAD detection)
            if waveform.ndim > 1 and waveform.shape[1] > 1:
                waveform = torch.mean(waveform, dim=1)
            
            if waveform.ndim == 1:
                waveform = waveform.unsqueeze(0)

            # 3. Resample (for VAD detection)
            if original_sample_rate != SAMPLE_RATE:
                resampler = torchaudio.transforms.Resample(original_sample_rate, SAMPLE_RATE)
                waveform = resampler(waveform)
            
            # 4. Detect Speech
            speech_timestamps = get_speech_timestamps(
                waveform[0],
                model,
                sampling_rate=SAMPLE_RATE,
                **vad_params
            )

            if not speech_timestamps:
                print("  > No speech found. Skipping.")
                continue

            file_kept_count = 0
            
            for i, chunk in enumerate(speech_timestamps):
                start_time_sec = chunk['start'] / SAMPLE_RATE
                end_time_sec = chunk['end'] / SAMPLE_RATE
                duration_sec = end_time_sec - start_time_sec
                
                # 5. Filter Duration
                if duration_sec < MIN_DURATION_SEC or duration_sec > MAX_DURATION_SEC:
                    total_skipped += 1
                    continue 

                # 6. Export
                # Unique filename: originalName_chunk_001.flac
                clean_name = os.path.splitext(long_file_name)[0].replace(" ", "_")
                output_filename = f"{clean_name}_chunk_{i+1:04d}.flac"
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                # ffmpeg: Cut, Resample to 16k, Force Mono
                subprocess.run([
                    'ffmpeg',
                    '-i', long_file_path,
                    '-ss', str(start_time_sec),
                    '-t', str(duration_sec),
                    '-c:a', 'flac',
                    '-ar', str(SAMPLE_RATE),
                    '-ac', '1',  # FORCE MONO
                    '-y', output_path
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                global_chunk_counter += 1
                total_kept += 1
                file_kept_count += 1

            print(f"  > Finished. Kept {file_kept_count} chunks.\n")

        except Exception as e:
            print(f"!!!!!!!! FAILED to process {long_file_name}: {e} !!!!!!!!")

    print("\n--- JOB COMPLETE! ---")
    print(f"Total Chunks Created: {total_kept}")
    print(f"Total 'Junk' Skipped: {total_skipped}")

if __name__ == "__main__":
    main()