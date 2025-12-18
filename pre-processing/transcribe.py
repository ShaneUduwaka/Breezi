import os
import time
from google.cloud import speech, storage
import config

def transcribe_chunk(local_audio_path, chunk_filename):
    """
    Uploads a single audio chunk to GCS and transcribes it.
    Returns the transcript text or None.
    """
    project_id = config.GCP_PROJECT_ID
    bucket_name = config.GCP_BUCKET_NAME

    if not project_id or not bucket_name:
        print("ERROR: GCP credentials missing in config.")
        return None

    # 1. Setup Clients
    # Implicitly uses /app/gcp-key.json via GOOGLE_APPLICATION_CREDENTIALS
    storage_client = storage.Client(project=project_id)
    speech_client = speech.SpeechClient()

    # 2. Upload to Cloud
    bucket = storage_client.bucket(bucket_name)
    blob_name = f"temp_auto_pilot/{chunk_filename}"
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_audio_path)
    gcs_uri = f"gs://{bucket_name}/{blob_name}"

    # 3. Transcribe
    audio = speech.RecognitionAudio(uri=gcs_uri)
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=config.SAMPLE_RATE,
        language_code="si-LK",
        enable_automatic_punctuation=True
    )

    try:
        # We use synchronous recognize for single chunks (simpler/faster for short audio)
        # For longer batches, LongRunning is better, but this is fine for auto-pilot
        operation = speech_client.long_running_recognize(config=recognition_config, audio=audio)
        response = operation.result(timeout=300)

        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        # 4. Cleanup Cloud File (Save money)
        blob.delete()
        
        return transcript

    except Exception as e:
        print(f"  > Google API Error: {e}")
        return None