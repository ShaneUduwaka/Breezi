from train.trainer import run_training
import subprocess, os

DRIVE_PATH = "/content/drive/MyDrive/whisper_processed_data_newest/"
LOCAL_PATH = "/tmp/whisper_data/"

def sync_data(src, dst):
    print(f"Syncing data from Drive to Local SSD")
    if not os.path.exists(dst):
        os.makedirs(dst)
    subprocess.run(["rsync", "-avz", src, dst], check=True)

sync_data(DRIVE_PATH, LOCAL_PATH)

print ("sync done")
