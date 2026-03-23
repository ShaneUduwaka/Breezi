FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. System Deps
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Install PyTorch (CPU)
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# 3. Install Other Dependancies 
RUN pip install --no-cache-dir \
    silero-vad \
    soundfile \
    numpy \
    google-cloud-speech \
    google-cloud-storage

WORKDIR /app
COPY . .

# Define mount points
VOLUME /data/raw_audio
VOLUME /data/json_transcripts
VOLUME /data/final_dataset

ENTRYPOINT ["python", "main.py"]