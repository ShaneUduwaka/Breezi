import pandas as pd
import os
import shutil
import subprocess
from tqdm import tqdm
from pathlib import Path

# --- CONFIGURATION (EDIT THIS) ---
# Define where you want the final clean dataset to be created
OUTPUT_DIR = "C:/Breezi/Final_Dataset" 

# List your datasets here. 
# "name": A short tag to prefix files (e.g., "lec", "team1").
# "tsv_path": Path to the metadata file.
# "audio_root": The folder where the audio paths in the TSV are relative to. 
#               (For the lecturer data, this is likely the folder containing 'asr_sinhala')
SOURCES = [
    # 1. The Lecturer's 80h Data
    {
        "name": "lec",
        "tsv_path": "C:/Path/To/Lecturer/test.tsv",  # CHANGE THIS
        "audio_root": "C:/Path/To/Lecturer",         # CHANGE THIS (Parent of 'asr_sinhala')
        "type": "lecturer"                           # Special flag for the weird folder structure
    },
    # 2. Teammate 1 Data
    {
        "name": "team1",
        "tsv_path": "C:/Path/To/Team1/dataset.tsv",  # CHANGE THIS
        "audio_root": "C:/Path/To/Team1",            # CHANGE THIS
        "type": "standard"
    },
    # Add blocks for Team 2, 3, 4...
]

# --- SETUP ---
FINAL_AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
FINAL_MANIFEST = os.path.join(OUTPUT_DIR, "metadata.tsv")
os.makedirs(FINAL_AUDIO_DIR, exist_ok=True)

def get_duration(file_path):
    """Get duration using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error', 
        '-show_entries', 'format=duration', 
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except:
        return None

def process_lecturer_row(row, source_config):
    """Handles the specific weirdness of the lecturer's TSV."""
    # Lecturer TSV has 'sentence' and 'file_path' (e.g., ./asr_sinhala/data/d7/d72a.flac)
    rel_path = row['file_path']
    # Fix slashes
    rel_path = rel_path.replace('./', '').replace('/', os.sep)
    
    full_path = os.path.join(source_config['audio_root'], rel_path)
    return full_path, row['sentence']

def process_standard_row(row, source_config):
    """Handles standard TSV (path, sentence)."""
    # Assuming standard TSV has 'path' or 'file_name'
    if 'path' in row:
        rel_path = row['path']
    elif 'file_name' in row:
        rel_path = row['file_name']
    elif 'location' in row: # Handle the JSON format
        # If it points to a JSON, find the FLAC
        json_path = row['location']
        rel_path = json_path.replace('.json', '') # Rough guess, might need adjustment
        # Use absolute path if provided in 'location'
        if os.path.isabs(rel_path):
            return rel_path, row['sentence']
        
    full_path = os.path.join(source_config['audio_root'], rel_path)
    return full_path, row['sentence']

def main():
    final_records = []
    
    print(f"--- Starting Grand Unification ---")
    print(f"Target: {OUTPUT_DIR}")

    for source in SOURCES:
        print(f"\nProcessing Source: {source['name']} ({source['type']})")
        
        try:
            df = pd.read_csv(source['tsv_path'], sep='\t')
        except Exception as e:
            print(f"ERROR: Could not read {source['tsv_path']}. Skipping. ({e})")
            continue

        success_count = 0
        
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            try:
                # 1. Resolve Path
                if source['type'] == 'lecturer':
                    original_path, sentence = process_lecturer_row(row, source)
                else:
                    original_path, sentence = process_standard_row(row, source)

                if not os.path.exists(original_path):
                    # Try one desperate fallback for lecturer data (sometimes paths are slightly off)
                    continue

                # 2. Define New Filename (Prefix to avoid collision)
                # e.g. "lec_002ae344.flac"
                original_name = os.path.basename(original_path)
                new_filename = f"{source['name']}_{original_name}"
                new_full_path = os.path.join(FINAL_AUDIO_DIR, new_filename)

                # 3. Copy Audio
                shutil.copy2(original_path, new_full_path)

                # 4. Get Duration (Re-calculate to be safe)
                duration = get_duration(new_full_path)
                if duration is None:
                    print(f"Warning: Corrupt audio {original_path}")
                    os.remove(new_full_path)
                    continue

                # 5. Add to Record
                # We store the RELATIVE path for the final TSV (cleaner)
                final_records.append({
                    'path': f"audio/{new_filename}", 
                    'duration': duration, 
                    'sentence': sentence
                })
                success_count += 1
                
            except Exception as e:
                # print(f"Failed row {idx}: {e}")
                pass
        
        print(f"--> Successfully migrated {success_count} files from {source['name']}")

    # --- Save Final Manifest ---
    if final_records:
        print("\n--- Saving Metadata ---")
        final_df = pd.DataFrame(final_records)
        final_df.to_csv(FINAL_MANIFEST, sep='\t', index=False)
        print(f"SUCCESS! Final dataset at: {OUTPUT_DIR}")
        print(f"Total Files: {len(final_df)}")
        print(f"Columns: {list(final_df.columns)}")
    else:
        print("\nCRITICAL FAILURE: No files were processed. Check your paths in 'SOURCES'.")

if __name__ == "__main__":
    main()