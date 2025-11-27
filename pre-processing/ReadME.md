# Sinhala Audio Pre-Processing Pipeline

This tool automatically processes raw audio files for the Sinhala ASR project. It is packaged in a Docker container to ensure it runs exactly the same on everyone's computer.

## What This Does
1.  **Reads** long-form audio files (MP3, WAV, FLAC) from your computer.
2.  **Detects** speech using Silero VAD.
3.  **Filters** the audio:
    * **Removes** silence.
    * **Removes** junk shorter than 3 seconds (noise/coughs).
    * **Removes** clips longer than 30 seconds.
4.  **Converts** valid chunks to **16kHz Mono FLAC**.
5.  **Saves** the clean chunks back to your computer.

---

## 🚀 How to Use (For Teammates)

### Prerequisite
You must have **Docker Desktop** installed and running.

### Step 1: Get the Tool
Open your terminal (CMD/PowerShell) and run:
```bash
docker pull <YOUR_DOCKERHUB_USERNAME>/sinhala-preprocessor:latest