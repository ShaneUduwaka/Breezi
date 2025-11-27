# Use a lightweight Python base image
FROM python:3.10-slim

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Install system dependencies
# ADDED: libsndfile1 (Required for the 'soundfile' Python library)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python libraries
# We use the CPU version of PyTorch to keep the image size small (approx 300MB vs 4GB)
RUN pip install --no-cache-dir \
    torch torchaudio --index-url https://download.pytorch.org/whl/cpu \
    silero-vad \
    soundfile \
    numpy

# 3. Setup the app
WORKDIR /app
COPY pre-process.py .

# 4. Define the output directories (for documentation purposes)
VOLUME /data/raw_audio
VOLUME /data/final_chunks

# 5. Run the script automatically
ENTRYPOINT ["python", "pre-process.py"]