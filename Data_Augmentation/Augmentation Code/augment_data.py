import pandas as pd
import subprocess
import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import sys

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TSV = os.path.join(BASE_DIR, 'test_data.tsv')
OUTPUT_TSV = os.path.join(BASE_DIR, 'dataset_augmented.tsv')
OUTPUT_AUDIO_DIR = os.path.join(BASE_DIR, 'augmented_audio')

SPEED_FACTORS = [0.9, 1.1] 
SAMPLE_RATE = 16000
NUM_WORKERS = max(1, cpu_count() - 2)

# Ensure output directory exists
os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)

def get_audio_duration(file_path):
    """Get duration of audio file using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error', 
        '-show_entries', 'format=duration', 
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        return None

def find_audio_path(json_path):
    """
    Tries to find the actual audio file based on the JSON path in the TSV.
    Strategy: 
    1. Strip .json (Result: .../Json/file.flac)
    2. Replace 'Json' folder with 'Audio' (Result: .../Audio/file.flac)
    """
    # Base assumption: file is .../chunk_xxx.flac.json -> .../chunk_xxx.flac
    base_audio = json_path.replace('.json', '') # Strips trailing .json
    
    candidates = [
        base_audio,                                      # Same folder
        base_audio.replace('Json', 'Audio'),             # Parallel Audio folder
        base_audio.replace('Json', 'wav'),               # Parallel wav folder
        base_audio.replace('Json', 'flac'),              # Parallel flac folder
    ]
    
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def process_row(args):
    """
    Worker function to process a single row (Original + Augmentations).
    """
    idx, row = args
    json_path = row['location']
    sentence = row['sentence']
    
    # 1. Find the source audio
    original_audio_path = find_audio_path(json_path)
    if not original_audio_path:
        # Fail silently or log? Let's just return None for now to avoid breaking flow
        return []

    # 2. Get Original Duration (since it's missing in TSV)
    orig_duration = get_audio_duration(original_audio_path)
    if not orig_duration:
        return []

    results = []
    
    # Add Original Entry (Normalizing path structure)
    results.append({
        'path': original_audio_path,
        'duration': orig_duration,
        'sentence': sentence,
        'type': 'original'
    })
    
    # 3. Create Augmentations
    filename = os.path.basename(original_audio_path)
    name, ext = os.path.splitext(filename)
    
    for speed in SPEED_FACTORS:
        # Define new path in our local 'augmented_audio' folder
        new_filename = f"{name}_sp{speed}{ext}"
        new_path = os.path.join(OUTPUT_AUDIO_DIR, new_filename)
        
        # Calculate expected new duration
        new_duration = orig_duration / speed

        # FFmpeg Command
        new_rate = int(SAMPLE_RATE * speed)
        cmd = [
            'ffmpeg', '-y', '-v', 'error',
            '-i', original_audio_path,
            '-af', f'asetrate={new_rate},aresample={SAMPLE_RATE}',
            new_path
        ]
        
        try:
            # Run conversion
            subprocess.run(cmd, check=True)
            
            results.append({
                'path': new_path,
                'duration': new_duration,
                'sentence': sentence,
                'type': 'augmented'
            })
        except subprocess.CalledProcessError:
            pass # Skip failed augmentations

    return results

def main():
    print(f"--- Loading {INPUT_TSV} ---")
    try:
        df = pd.read_csv(INPUT_TSV, sep='\t')
    except FileNotFoundError:
        print(f"Error: Could not find {INPUT_TSV}. Make sure file is in {BASE_DIR}")
        return

    print(f"Found {len(df)} rows. finding audio and processing...")
    
    tasks = []
    for idx, row in df.iterrows():
        tasks.append((idx, row))
            
    all_rows = []
    
    # Use Multiprocessing
    with Pool(NUM_WORKERS) as pool:
        # We use imap to get results as they finish
        for result_batch in tqdm(pool.imap_unordered(process_row, tasks), total=len(tasks)):
            if result_batch:
                all_rows.extend(result_batch)
            
    # Save Final TSV
    print("--- Saving new manifest ---")
    final_df = pd.DataFrame(all_rows)
    
    # Reorder columns nicely
    if not final_df.empty:
        final_df = final_df[['path', 'duration', 'sentence', 'type']]
        final_df.to_csv(OUTPUT_TSV, sep='\t', index=False)
        print(f"Done! Saved to: {OUTPUT_TSV}")
        print(f"Total Audio Files: {len(final_df)} (Original + Augmented)")
        print(f"Augmented audio stored in: {OUTPUT_AUDIO_DIR}")
    else:
        print("Error: No audio files were processed. Check if your paths in 'location' column are correct.")

if __name__ == '__main__':
    main()