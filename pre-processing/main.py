import os
import csv
import subprocess
import json
import config
import vad
import utils
import transcribe  # Import our new module

def main():
    print("\n--- Sinhala Auto-Pilot Pipeline ✈️ ---")
    
    # 1. Setup
    model = vad.load_model()
    audio_out_dir = os.path.join(config.OUTPUT_DIR, config.AUDIO_SUBFOLDER)
    os.makedirs(audio_out_dir, exist_ok=True)
    
    tsv_path = os.path.join(config.OUTPUT_DIR, config.TSV_NAME)
    existing_entries = utils.load_existing_tsv(tsv_path)
    
    # Ensure Google Credentials are visible
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/gcp-key.json"

    # 2. Open TSV
    file_exists = os.path.exists(tsv_path)
    with open(tsv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        if not file_exists:
            writer.writerow(["path", "duration", "sentence"])

        # 3. Scan Files
        for root, _, files in os.walk(config.INPUT_RAW_DIR):
            for f in files:
                if f.lower().endswith(('.wav', '.flac', '.mp3')):
                    long_file_path = os.path.join(root, f)
                    clean_name = os.path.splitext(f)[0].replace(" ", "_")
                    
                    print(f"\nScanning: {clean_name}")
                    timestamps = vad.process_audio(long_file_path, model)
                    
                    for i, chunk in enumerate(timestamps):
                        start = chunk['start'] / config.SAMPLE_RATE
                        end = chunk['end'] / config.SAMPLE_RATE
                        duration = end - start
                        
                        if duration < config.MIN_DURATION or duration > config.MAX_DURATION:
                            continue

                        chunk_filename = f"{clean_name}_chunk_{i+1:04d}.flac"
                        tsv_path_entry = f"{config.AUDIO_SUBFOLDER}/{chunk_filename}"
                        physical_save_path = os.path.join(audio_out_dir, chunk_filename)
                        
                        # Optimization: If in TSV and Audio exists, skip
                        if tsv_path_entry in existing_entries and os.path.exists(physical_save_path):
                            continue

                        # --- THE AUTO-PILOT LOGIC ---
                        transcript_text = None
                        
                        # 1. Try to find existing JSON locally (Free)
                        expected_json_name = f"{chunk_filename}.json"
                        found_json_path = utils.find_fuzzy_json(expected_json_name)

                        if found_json_path:
                            # print(f"  > Found local JSON: {expected_json_name}")
                            transcript_text = utils.get_transcript_from_json(found_json_path)
                        
                        else:
                            # 2. JSON Missing -> Transcribe via Google ($$$)
                            print(f"  > Missing JSON for {chunk_filename}. Transcribing...")
                            
                            # We must extract the chunk to a temp file first
                            temp_chunk_path = f"/tmp/{chunk_filename}"
                            subprocess.run([
                                'ffmpeg', '-i', long_file_path, '-ss', str(start), '-t', str(duration),
                                '-c:a', 'flac', '-ar', str(config.SAMPLE_RATE), '-ac', '1', '-y', temp_chunk_path
                            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                            # Call Google
                            transcript_text = transcribe.transcribe_chunk(temp_chunk_path, chunk_filename)
                            
                            # Save the JSON locally so we never pay again
                            if transcript_text:
                                save_json_path = os.path.join(config.INPUT_JSON_DIR, expected_json_name)
                                with open(save_json_path, 'w', encoding='utf-8') as jf:
                                    json.dump({'results': [{'alternatives': [{'transcript': transcript_text}]}]}, jf, ensure_ascii=False)
                            
                            # Clean temp file
                            if os.path.exists(temp_chunk_path):
                                os.remove(temp_chunk_path)

                        # --- SAVE & WRITE ---
                        if transcript_text:
                            # Save Final FLAC (If not already there)
                            if not os.path.exists(physical_save_path):
                                subprocess.run([
                                    'ffmpeg', '-i', long_file_path, 
                                    '-ss', str(start), '-t', str(duration),
                                    '-c:a', 'flac', '-ar', str(config.SAMPLE_RATE), 
                                    '-ac', '1', '-y', physical_save_path
                                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            
                            writer.writerow([tsv_path_entry, f"{duration:.2f}", transcript_text])
                            print(f"  > Processed: {chunk_filename}")
                        else:
                            print(f"  > Skipped {chunk_filename} (No Transcript)")

    print("\n--- JOB COMPLETE ---")

if __name__ == "__main__":
    main()