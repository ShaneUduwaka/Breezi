import os
import datetime
from mutagen import File


def get_total_audio_duration(root_folder):
    total_seconds = 0
    file_count = 0

    # These are the extensions the script will look for
    # Add more if you have specific formats like .ogg or .m4a
    audio_extensions = ('.mp3', '.wav', '.flac', '.m4a', '.aac', '.wma')

    print(f"Scanning '{root_folder}'... please wait.")

    # Walk through all folders and subfolders
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(audio_extensions):
                file_path = os.path.join(dirpath, filename)

                try:
                    # Load the file using mutagen
                    audio = File(file_path)

                    # If mutagen successfully reads the file
                    if audio is not None and audio.info is not None:
                        total_seconds += audio.info.length
                        file_count += 1

                except Exception as e:
                    print(f"Could not read file {filename}: {e}")

    # Convert total seconds into a readable format (HH:MM:SS)
    total_duration = str(datetime.timedelta(seconds=int(total_seconds)))

    return total_duration, file_count, total_seconds


# --- CONFIGURATION ---
# Replace this path with the actual path to your main folder
folder_path = r'C:\Users\YourName\Documents\Audiofiles'

if os.path.exists(folder_path):
    duration_str, count, seconds = get_total_audio_duration(folder_path)

    print("-" * 30)
    print(f"Total Audio Files Found: {count}")
    print(f"Total Duration (HH:MM:SS): {duration_str}")
    print(f"Total Seconds: {seconds:.2f}")
    print("-" * 30)
else:
    print("The folder path you provided does not exist.")