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

Part 1: Action for YOU (The Team Leader) 👮‍♂️
Before you send the guide to your team, you must upload the latest "Auto-Pilot" code to the cloud.

Run these commands in your sinhala_builder folder:

Bash

# 1. Login to Docker
docker login

# 2. Tag your local image with a specific name for the team
docker tag sinhala-builder tevingg/sinhala-autopilot:latest

# 3. Push it to the internet
docker push tevingg/sinhala-autopilot:latest
Part 2: The Team Guide (README.md) 📄
Copy the text below into a file named README.md and send it to your team (via WhatsApp, Discord, or GitHub).

🇱🇰 Sinhala Speech Dataset Workflow
This guide explains how to use our Auto-Pilot Tool to process audio files and how to perform the manual correction for our dataset.

🛠️ Prerequisites
Install Docker Desktop: Download Here

Get the Key: Ask Tevin for the gcp-key.json file.

Get the Audio: Download your batch of audio files assigned to you.

📂 Step 1: Setup Your Folders
Create a main folder named sinhala_project on your computer. Inside it, create exactly these 3 empty folders and paste your key file:

Plaintext

sinhala_project/
├── gcp-key.json         <-- Paste the key file here
├── raw_audio/           <-- Put your WAV/MP3 files here
├── json_cache/          <-- Leave empty (Transcripts saved here)
└── final_dataset/       <-- Leave empty (Results appear here)
🚀 Step 2: Run the Auto-Pilot Tool
Open your Terminal (Mac/Linux) or Command Prompt (Windows).

Navigate to your sinhala_project folder (cd path/to/sinhala_project).

Copy and paste the command below:

Windows Command:

PowerShell

docker run --rm ^
  -v "%cd%\raw_audio:/data/raw_audio" ^
  -v "%cd%\json_cache:/data/json_transcripts" ^
  -v "%cd%\final_dataset:/data/final_dataset" ^
  -v "%cd%\gcp-key.json:/app/gcp-key.json" ^
  -e GCP_PROJECT_ID="elevated-pod-477414-u2" ^
  -e GCP_BUCKET_NAME="elevated-pod-477414-u2-audio" ^
  tevingg/sinhala-autopilot:latest
Mac / Linux Command:

Bash

docker run --rm \
  -v "$PWD/raw_audio:/data/raw_audio" \
  -v "$PWD/json_cache:/data/json_transcripts" \
  -v "$PWD/final_dataset:/data/final_dataset" \
  -v "$PWD/gcp-key.json:/app/gcp-key.json" \
  -e GCP_PROJECT_ID="elevated-pod-477414-u2" \
  -e GCP_BUCKET_NAME="elevated-pod-477414-u2-audio" \
  tevingg/sinhala-autopilot:latest
What will happen?
The tool will scan your raw_audio.

If it finds a file without a transcript, it will auto-upload to Google and buy the transcript.

It will download the JSON transcript to json_cache.

It will save the final chopped audio and the TSV file in final_dataset.

✍️ Step 3: Manual Correction (Human-in-the-Loop)
Once the tool finishes, go to the final_dataset folder. You will see a file named dataset.tsv.

Open dataset.tsv in Excel or Google Sheets.

Listen & Correct:

Play the audio chunk (found in the audio/ folder).

Read the text in the sentence column.

Edit the text if it is wrong.

Critical Rules:

❌ DO NOT change the path column.

❌ DO NOT change the duration column.

✅ ONLY edit the Sinhala text in the sentence column.

📤 Step 4: Submit Your Work
When you are done correcting your batch:

Rename your TSV to include your name (e.g., dataset_tevin.tsv).

Zip the final_dataset folder.

Send the Zip file to Tevin.

❓ Troubleshooting
"Image not found": Make sure you have internet access so Docker can download the tool.

"GCP Credentials missing": Check that gcp-key.json is in the correct folder and named exactly right.

"Docker daemon not running": Open the Docker Desktop app on your computer.

Part 3: Visual Overview
You can also share this diagram with them so they understand the flow:

docker pull <YOUR_DOCKERHUB_USERNAME>/sinhala-preprocessor:latest
