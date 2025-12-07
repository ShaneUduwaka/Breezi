# 🇱🇰 Sinhala Speech Dataset Workflow

This guide explains how to use our **Auto-Pilot Tool** to process audio files and how to perform the manual correction for our dataset.

## 🛠️ Prerequisites

1.  **Install Docker Desktop:** [Download Here](https://www.docker.com/products/docker-desktop/)
2.  **Get the Key:** Ask Tevin for the `gcp-key.json` file.
3.  **Get the Audio:** Download your batch of audio files assigned to you.

---

## 📂 Step 1: Setup Your Folders

Create a main folder named `sinhala_project` on your computer. Inside it, create exactly these 3 empty folders and paste your key file:

```text
sinhala_project/
├── gcp-key.json         <-- Paste the key file here
├── raw_audio/           <-- Put your WAV/MP3 files here
├── json_cache/          <-- Leave empty (Transcripts saved here)
└── final_dataset/       <-- Leave empty (Results appear here)
```
## 🚀 Step 2: Run the Auto-Pilot Tool
Open your Terminal (Mac/Linux) or Command Prompt (Windows).

Navigate to your sinhala_project folder (e.g., cd Documents/sinhala_project).

Copy and paste the command below based on your OS:

```text

docker run --rm ^
  -v "%cd%\raw_audio:/data/raw_audio" ^
  -v "%cd%\json_cache:/data/json_transcripts" ^
  -v "%cd%\final_dataset:/data/final_dataset" ^
  -v "%cd%\gcp-key.json:/app/gcp-key.json" ^
  -e GCP_PROJECT_ID="elevated-pod-477414-u2" ^
  -e GCP_BUCKET_NAME="elevated-pod-477414-u2-audio" ^
  sinhala-autopilot
```

```text
docker run --rm \
  -v "$PWD/raw_audio:/data/raw_audio" \
  -v "$PWD/json_cache:/data/json_transcripts" \
  -v "$PWD/final_dataset:/data/final_dataset" \
  -v "$PWD/gcp-key.json:/app/gcp-key.json" \
  -e GCP_PROJECT_ID="elevated-pod-477414-u2" \
  -e GCP_BUCKET_NAME="elevated-pod-477414-u2-audio" \
  sinhala-autopilot
```

### ⏳ What happens next?
The tool scans your raw_audio folder.

If it finds a file without a transcript, it automatically uploads it to Google and gets the transcript.

It downloads the JSON transcript to json_cache.

It cuts the audio and saves the final files + TSV in final_dataset

## ✍️ Step 3: Manual Correction (Human-in-the-Loop)
Once the tool finishes, go to the final_dataset folder. You will see a file named dataset.tsv.

Open dataset.tsv in Excel or Google Sheets.

Listen & Correct:

Play the audio chunk (found in the audio/ folder).

Read the text in the sentence column.

Edit the text if it is wrong.

⚠️ Critical Rules
❌ DO NOT change the path column.

❌ DO NOT change the duration column.

✅ ONLY edit the Sinhala text in the sentence column.

## 📤 Step 4: Submit Your Work
When you are done correcting your batch:

Rename your TSV to include your name (e.g., dataset_YOUR_NAME.tsv).

Zip the final_dataset folder.

Send the Zip file to Tevin.

## ❓ Troubleshooting

```text
Error Message,Solution
"Image not found" --- Make sure you have internet access so Docker can download the tool.
"GCP Credentials missing" --- Check that gcp-key.json is in the correct folder and named exactly right.
"Docker daemon not running" --- Open the Docker Desktop app on your computer.
"Volume not found" --- "Make sure you created the folders (raw_audio, json_cache, etc.) exactly as spelt in Step 1."
```
