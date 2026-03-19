# docker/mock-tts/mock_tts.py
"""Mock TTS service for development"""

from flask import Flask, request, jsonify, send_file
from io import BytesIO
import json

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "mock-tts"}), 200


@app.route('/synthesize', methods=['POST'])
def synthesize():
    """
    Mock text-to-speech synthesis
    Simulates Google Cloud Text-to-Speech API
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'en-US')
        
        # Return mock audio metadata
        return jsonify({
            "audioContent": "base64_encoded_mock_audio",
            "audioConfig": {
                "audioEncoding": "LINEAR16",
                "sampleRateHertz": 16000,
                "languageCode": language
            },
            "metadata": {
                "text_processed": text,
                "duration_seconds": len(text.split()) * 0.5
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/synthesize-stream', methods=['POST'])
def synthesize_stream():
    """Mock streaming synthesis"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        # Return streaming audio chunks
        return jsonify({
            "audioChunks": [
                {"data": "mock_chunk_1"},
                {"data": "mock_chunk_2"},
                {"data": "mock_chunk_3"},
            ],
            "metadata": {
                "text_processed": text,
                "stream_active": False
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🔊 Mock TTS Service running on port 8003")
    app.run(host='0.0.0.0', port=8003, debug=True)
