# utils.py
import json
import os
import csv
import config
import re

def clean_filename(filename):
    """Removes special chars to help with fuzzy matching."""
    # Remove extension
    base = filename.rsplit('.', 1)[0] 
    # Remove everything except letters, numbers, and Sinhala chars
    # We also remove underscores to make comparison easier
    clean = re.sub(r'[^a-zA-Z0-9\u0d80-\u0dff]', '', base)
    return clean

def find_fuzzy_json(expected_filename):
    """
    Tries to find the JSON file even if Google renamed it.
    It looks for:
    1. Exact match
    2. Fuzzy match (same chunk number + matching alphanumeric characters)
    """
    json_dir = config.INPUT_JSON_DIR
    
    # 1. Try Exact Match First (Fastest)
    full_path = os.path.join(json_dir, expected_filename)
    if os.path.exists(full_path):
        return full_path

    # 2. Fuzzy Match
    # expected: "My_Video_|_Title_chunk_0001.flac.json"
    
    # Extract the chunk part (e.g., "_chunk_0001")
    if "_chunk_" not in expected_filename:
        return None
        
    base_part, chunk_part = expected_filename.split('_chunk_', 1)
    chunk_identifier = "chunk_" + chunk_part.split('.')[0] # "chunk_0001"
    
    # Clean up our base name (remove | ? # etc)
    target_skeleton = clean_filename(base_part)

    # List all files in the JSON directory
    try:
        available_files = os.listdir(json_dir)
    except FileNotFoundError:
        return None

    for f in available_files:
        if not f.endswith('.json'): 
            continue
            
        # Optimization: The file MUST contain the same chunk number
        if chunk_identifier not in f:
            continue
            
        # Check if the text part matches
        f_base = f.split('_chunk_', 1)[0]
        f_skeleton = clean_filename(f_base)
        
        # If the "skeletons" match, we found it!
        if target_skeleton in f_skeleton or f_skeleton in target_skeleton:
            # print(f"DEBUG: Fuzzy match found! {expected_filename} -> {f}")
            return os.path.join(json_dir, f)

    return None

def get_transcript_from_json(json_path):
    """Reads the Google JSON and extracts the Sinhala text."""
    if not json_path or not os.path.exists(json_path):
        return None

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'results' in data:
            for result in data['results']:
                if 'alternatives' in result:
                    return result['alternatives'][0]['transcript']
        return None
    except Exception:
        return None

def load_existing_tsv(tsv_path):
    processed_files = set()
    if os.path.exists(tsv_path):
        with open(tsv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)
            for row in reader:
                if len(row) > 0:
                    processed_files.add(row[0])
    return processed_files