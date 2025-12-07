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

Step 2: Run the Auto-Pilot Tool
Open your Terminal (Mac/Linux) or Command Prompt (Windows).

You can just navigate to your sinhala_project folder (e.g., cd Documents/sinhala_project).

Copy and paste the command below based on your OS:
