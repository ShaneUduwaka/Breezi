"""
Dummy STT/TTS module - Speech to Text / Text to Speech
In production, would use Whisper for STT and actual TTS service
"""


class DummySTT:
    """
    Dummy Speech-to-Text using Whisper (in production)
    For now, just returns a mock transcription
    """
    
    def __init__(self):
        self.mock_audio_responses = [
            "I want to order a pizza",
            "Show me the menu",
            "What burgers do you have",
            "Tell me about the burger",
            "What are your current promotions",
            "Where are your locations",
            "What are your hours",
        ]
        self.current_index = 0
    
    def transcribe(self, audio_data):
        """
        Convert audio to text
        
        Args:
            audio_data: Raw audio bytes/file
            
        Returns:
            str: Transcribed text
        """
        # For demo: cycle through mock responses
        response = self.mock_audio_responses[self.current_index % len(self.mock_audio_responses)]
        self.current_index += 1
        return response
    
    def set_mock_responses(self, responses):
        """Override mock responses for testing"""
        self.mock_audio_responses = responses
        self.current_index = 0


class DummyTTS:
    """
    Dummy Text-to-Speech
    In production, would use Google Cloud TTS, Azure TTS, etc.
    """
    
    def __init__(self):
        self.last_spoken = None
    
    def speak(self, text):
        """
        Convert text to audio and play it
        
        Args:
            text: Text to speak
            
        Returns:
            bool: True if successful
        """
        self.last_spoken = text
        # In real implementation, would synthesize and play audio
        print(f"🔊 [TTS] {text}")
        return True
    
    def get_last_spoken(self):
        """For testing: get what was last spoken"""
        return self.last_spoken
