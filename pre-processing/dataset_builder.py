import torch
import torchaudio
import soundfile as sf
import numpy as np
from silero_vad import load_silero_vad, get_speech_timestamps
import os
import subprocess
import json
import csv

# --- Configuration ---
# Docker Internal Paths
INPUT_RAW_DIR = "/data/raw_audio"        # Where your long wav/mp3 files are
INPUT_JSON_DIR = "/data/json_transcripts" # Where your 806 JSON files are
OUTPUT_DIR = "/data/final_dataset"       # Where we save the FLACs + CSV

SAMPLE_RATE = 16000
MIN_DURATION = 3.0
MAX_DURATION = 30.0
VAD_PARAMS = {'min_speech_duration_ms': 250, 'min_silence_duration_ms': 500}

def get_transcript_from_json(json_path):
    """Reads the Google JSON and extracts the Sinhala text."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Handle Google Cloud 'LongRunningRecognize' output format
        # It usually puts results in a list
        if 'results' in data:
            for result in data['results']:
                if 'alternatives' in result:
                    # Return the first (most confident) transcript
                    return result['alternatives'][0]['transcript']
        return None
    except Exception as e:
        print(f"Error reading JSON {json_path}: {e}")
        return None

def main():
    print("\n--- Sinhala Dataset Builder (Stitch & Verify) ---")
    
    # 1. Setup
    model = load_silero_vad()
    os.makedirs(os.path.join(OUTPUT_DIR, "audio"), exist_ok=True)
    
    csv_data = [] # To store [filename, sentence]
    
    # 2. Find Raw Audio
    audio_files = []
    for root, _, files in os.walk(INPUT_RAW_DIR):
        for f in files:
            if f.lower().endswith(('.wav', '.flac', '.mp3')):
                audio_files.append(os.path.join(root, f))
    
    print(f"Found {len(audio_files)} raw audio files.")
    
    # 3. Process
    for long_file in audio_files:
        clean_name = os.path.splitext(os.path.basename(long_file))[0].replace(" ", "_")
        print(f"Processing: {clean_name}...")
        
        try:
            # Load & VAD (Same logic as before)
            audio, sr = sf.read(long_file, dtype='float32')
            waveform = torch.from_numpy(audio)
            if waveform.ndim > 1: waveform = torch.mean(waveform, dim=1)
            if waveform.ndim == 1: waveform = waveform.unsqueeze(0)
            if sr != SAMPLE_RATE:
                resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
                waveform = resampler(waveform)

            timestamps = get_speech_timestamps(waveform[0], model, sampling_rate=SAMPLE_RATE, **VAD_PARAMS)
            
            for i, chunk in enumerate(timestamps):
                # Calculate Duration
                start = chunk['start'] / SAMPLE_RATE
                end = chunk['end'] / SAMPLE_RATE
                duration = end - start
                
                if duration < MIN_DURATION or duration > MAX_DURATION: continue
                
                # --- THE MATCHING LOGIC ---
                # 1. Determine the expected filename (Old Format)
                chunk_filename = f"{clean_name}_chunk_{i+1:04d}.flac"
                
                # 2. Determine expected JSON filename
                # Google script saved it as: {audio_filename}.json
                expected_json_name = f"{chunk_filename}.json"
                json_full_path = os.path.join(INPUT_JSON_DIR, expected_json_name)
                
                # 3. Check if we have a transcript for this chunk
                if os.path.exists(json_full_path):
                    # YES! We have a match.
                    transcript_text = get_transcript_from_json(json_full_path)
                    
                    if transcript_text:
                        # 4. Save the Audio Chunk
                        out_audio_path = os.path.join(OUTPUT_DIR, "audio", chunk_filename)
                        subprocess.run([
                            'ffmpeg', '-i', long_file, '-ss', str(start), '-t', str(duration),
                            '-c:a', 'flac', '-ar', str(16000), '-ac', '1', '-y', out_audio_path
                        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        
                        # 5. Add to CSV List
                        # WhisperX expects: audio_path, sentence
                        csv_data.append([f"audio/{chunk_filename}", transcript_text])
                        # print(f"  > Match found: {chunk_filename}")
                    else:
                        print(f"  > JSON exists but empty text: {expected_json_name}")
                # If JSON doesn't exist, we skip the chunk (silently ignore junk)

        except Exception as e:
            print(f"Failed to process {clean_name}: {e}")

    # 4. Write CSV
    print(f"\nWriting metadata.csv with {len(csv_data)} entries...")
    csv_path = os.path.join(OUTPUT_DIR, "metadata.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["file_name", "sentence"]) # Header
        writer.writerows(csv_data)
        
    print("--- SUCCESS! Dataset Ready. ---")

if __name__ == "__main__":
    main()