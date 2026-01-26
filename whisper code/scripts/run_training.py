from train.trainer import run_training

LOCAL_PATH = "/tmp/whisper_data"
OUTPUT_DIR = "./whisper-sinhala-english-v5"

run_training(local_path=LOCAL_PATH, output_dir=OUTPUT_DIR)
