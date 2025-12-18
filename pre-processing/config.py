import os

# Docker Internal Paths
INPUT_RAW_DIR = "/data/raw_audio"
INPUT_JSON_DIR = "/data/json_transcripts"
OUTPUT_DIR = "/data/final_dataset"

# Audio Settings
SAMPLE_RATE = 16000
MIN_DURATION = 3.0
MAX_DURATION = 30.0

# VAD Settings
VAD_PARAMS = {
    'min_speech_duration_ms': 250,
    'min_silence_duration_ms': 500
}

# Output Filenames
TSV_NAME = "dataset.tsv"
AUDIO_SUBFOLDER = "audio"

# Google Cloud Settings (Read from Docker ENV)
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME")