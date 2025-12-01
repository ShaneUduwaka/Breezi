import os
import glob
import subprocess
import time
import shutil
import torch
import torchaudio
import soundfile as sf
import numpy as np
from silero_vad import load_silero_vad, get_speech_timestamps
from google.cloud import speech, storage

# --- CONFIGURATION (Env Variables for Docker) ---
# Your team will pass these in via docker run -e
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME")

# Internal Paths
INPUT_DIR = "/data/raw_audio"
CHUNK_DIR = "/data/temp_chunks"  # Intermediate folder
OUTPUT_DIR = "/data/final_transcripts"
SAMPLE_RATE = 16000

# VAD Settings
MIN_DURATION = 3.0
MAX_DURATION = 30.0
VAD_PARAMS = {'min_speech_duration_ms': 250, 'min_silence_duration_ms': 500}

def step_1_chunking():
    print(f"\n[STEP 1] Starting VAD Chunking...")
    print(f"Reading: {INPUT_DIR}")
    
    os.makedirs(CHUNK_DIR, exist_ok=True)
    model = load_silero_vad()
    
    audio_files = []
    for root, _, files in os.walk(INPUT_DIR):
        for f in files:
            if f.lower().endswith(('.wav', '.flac', '.mp3')):
                audio_files.append(os.path.join(root, f))
    
    if not audio_files:
        print("ERROR: No audio files found.")
        return False

    total_chunks = 0
    for long_file in audio_files:
        try:
            print(f"Processing: {os.path.basename(long_file)}")
            audio_data, sr = sf.read(long_file, dtype='float32')
            waveform = torch.from_numpy(audio_data)
            
            # Stereo to Mono
            if waveform.ndim > 1 and waveform.shape[1] > 1:
                waveform = torch.mean(waveform, dim=1)
            if waveform.ndim == 1: waveform = waveform.unsqueeze(0)
            
            # Resample
            if sr != SAMPLE_RATE:
                resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
                waveform = resampler(waveform)

            timestamps = get_speech_timestamps(waveform[0], model, sampling_rate=SAMPLE_RATE, **VAD_PARAMS)
            
            for i, chunk in enumerate(timestamps):
                start = chunk['start'] / SAMPLE_RATE
                end = chunk['end'] / SAMPLE_RATE
                duration = end - start
                
                if duration < MIN_DURATION or duration > MAX_DURATION: continue

                clean_name = os.path.splitext(os.path.basename(long_file))[0].replace(" ", "_")
                out_name = f"{clean_name}_chunk_{i+1:04d}.flac"
                out_path = os.path.join(CHUNK_DIR, out_name)

                subprocess.run([
                    'ffmpeg', '-i', long_file, '-ss', str(start), '-t', str(duration),
                    '-c:a', 'flac', '-ar', str(SAMPLE_RATE), '-ac', '1', '-y', out_path
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                total_chunks += 1
        except Exception as e:
            print(f"Skipping {long_file}: {e}")
            
    print(f"[STEP 1 COMPLETE] Created {total_chunks} valid chunks.")
    return total_chunks > 0

def step_2_google_transcribe():
    print(f"\n[STEP 2] Starting Google Transcription...")
    
    # Auth Check
    if not PROJECT_ID or not BUCKET_NAME:
        print("ERROR: GCP_PROJECT_ID or GCP_BUCKET_NAME not set.")
        return

    key_path = "/app/gcp-key.json"
    if not os.path.exists(key_path):
        print("ERROR: gcp-key.json not found inside container.")
        return
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    
    speech_client = speech.SpeechClient()
    storage_client = storage.Client(project=PROJECT_ID)

    # 1. Upload Chunks to Cloud
    print("Uploading chunks to Google Cloud Storage...")
    bucket = storage_client.get_bucket(BUCKET_NAME)
    local_chunks = glob.glob(os.path.join(CHUNK_DIR, "*.flac"))
    
    uploaded_uris = []
    for local_file in local_chunks:
        blob_name = f"temp_upload/{os.path.basename(local_file)}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_file)
        uploaded_uris.append(f"gs://{BUCKET_NAME}/{blob_name}")
    
    print(f"Uploaded {len(uploaded_uris)} files.")

    # 2. Start Batch Transcription
    print("Sending transcription jobs...")
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=SAMPLE_RATE,
        language_code="si-LK",
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True
    )

    operations = []
    for gcs_uri in uploaded_uris:
        # Unique output path for each file
        base_name = os.path.basename(gcs_uri)
        output_uri = f"gs://{BUCKET_NAME}/transcripts/{base_name}.json"
        
        audio = speech.RecognitionAudio(uri=gcs_uri)
        out_config = speech.TranscriptOutputConfig(gcs_uri=output_uri)
        
        req = speech.LongRunningRecognizeRequest(
            config=config, audio=audio, output_config=out_config
        )
        
        try:
            op = speech_client.long_running_recognize(request=req)
            operations.append(op)
        except Exception as e:
            print(f"Failed to submit {base_name}: {e}")
        time.sleep(0.5) # Rate limit safety

    # 3. Wait for results
    print(f"Waiting for {len(operations)} jobs to finish...")
    for op in operations:
        try:
            op.result(timeout=1800)
        except:
            pass
    
    # 4. Download Results
    print("Downloading transcripts...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    blobs = bucket.list_blobs(prefix="transcripts/")
    for blob in blobs:
        if blob.name.endswith(".json"):
            local_path = os.path.join(OUTPUT_DIR, os.path.basename(blob.name))
            blob.download_to_filename(local_path)
    
    print(f"[STEP 2 COMPLETE] Transcripts saved to {OUTPUT_DIR}")

    # 5. Cleanup Cloud (Optional but Recommended)
    print("Cleaning up cloud bucket...")
    for blob in bucket.list_blobs(prefix="temp_upload/"):
        blob.delete()
    for blob in bucket.list_blobs(prefix="transcripts/"):
        blob.delete()
    print("Cloud bucket cleaned.")

def main():
    if step_1_chunking():
        step_2_google_transcribe()
    else:
        print("Pipeline stopped due to chunking errors.")

if __name__ == "__main__":
    main()