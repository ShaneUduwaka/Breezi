# docker/mock-stt/mock_stt.py
"""Mock STT service for development"""

from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)


# Simulate STT responses
MOCK_TRANSCRIPTIONS = {
    "pizza": {"text": "I want to order a pizza", "confidence": 0.95},
    "delivery": {"text": "delivery 2 pieces", "confidence": 0.92},
    "order": {"text": "order burger and fries", "confidence": 0.88},
}


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "mock-stt"}), 200


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Mock transcription endpoint
    Simulates Google Cloud Speech-to-Text API
    """
    try:
        data = request.get_json()
        
        # For demo: Look for keywords in request
        search_text = data.get('audio_content', '').lower()
        
        # Find matching mock response
        for keyword, response in MOCK_TRANSCRIPTIONS.items():
            if keyword in search_text:
                return jsonify({
                    "results": [
                        {
                            "alternatives": [
                                {
                                    "transcript": response["text"],
                                    "confidence": response["confidence"]
                                }
                            ]
                        }
                    ]
                }), 200
        
        # Default response
        return jsonify({
            "results": [
                {
                    "alternatives": [
                        {
                            "transcript": "mock transcription",
                            "confidence": 0.85
                        }
                    ]
                }
            ]
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/stream', methods=['POST'])
def stream_transcribe():
    """Mock streaming transcription endpoint"""
    try:
        data = request.get_json()
        
        return jsonify({
            "result": {
                "alternatives": [
                    {
                        "transcript": "streaming mock transcription",
                        "confidence": 0.80
                    }
                ],
                "is_final": False
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🎙️ Mock STT Service running on port 8002")
    app.run(host='0.0.0.0', port=8002, debug=True)
