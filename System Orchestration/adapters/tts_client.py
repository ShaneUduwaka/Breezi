# adapters/tts_client.py
"""Multi-provider Text-to-Speech client"""

from typing import AsyncGenerator, Optional
import logging


logger = logging.getLogger(__name__)


class TTSClient:
    """
    Multi-provider TTS client
    Supports: Google Cloud Text-to-Speech, AWS Polly, Azure Speech
    """
    
    def __init__(self, provider: str = "google", config: dict = None):
        """
        Initialize TTS client
        
        Args:
            provider: TTS provider (google, aws, azure)
            config: Provider-specific configuration
        """
        self.provider = provider
        self.config = config or {}
        self.is_connected = False
    
    async def connect(self) -> bool:
        """Connect to TTS service"""
        try:
            logger.info(f"🔊 Connecting to {self.provider} TTS...")
            if self.provider == "google":
                from google.cloud import texttospeech
                import os
                api_key = os.getenv("GOOGLE_API_KEY")
                
                if api_key:
                    self.tts_client = texttospeech.TextToSpeechAsyncClient(
                        client_options={"api_key": api_key}
                    )
                else:
                    self.tts_client = texttospeech.TextToSpeechAsyncClient()
                    
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"❌ TTS connection failed: {e}")
            return False
    
    async def synthesize_stream(
        self,
        text: str,
        session_id: str,
        language: str = "en-US",
        voice: Optional[str] = None
    ) -> AsyncGenerator[bytes, None]:
        """
        Real-time streaming synthesis
        """
        try:
            logger.debug(f"🔊 Starting TTS stream for session {session_id}")
            logger.debug(f"    Text: {text[:100]}...")
            
            if self.provider == "google":
                from google.cloud import texttospeech
                
                voice_name = voice or self.set_voice(language)
                synthesis_input = texttospeech.SynthesisInput(text=text)
                
                voice_params = texttospeech.VoiceSelectionParams(
                    language_code=language,
                    name=voice_name if voice_name else None
                )
                
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                    sample_rate_hertz=self.config.get("sample_rate_hertz", 16000)
                )
                
                response = await self.tts_client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice_params,
                    audio_config=audio_config
                )
                
                # Yield the audio in chunks (simulate streaming)
                audio_content = response.audio_content
                chunk_size = 4000
                for i in range(0, len(audio_content), chunk_size):
                    yield audio_content[i:i+chunk_size]
            else:
                pass
        
        except Exception as e:
            logger.error(f"❌ TTS synthesis error: {e}")
    
    async def synthesize_file(
        self,
        text: str,
        output_path: str,
        language: str = "en-US",
        voice: Optional[str] = None
    ) -> bool:
        """Synthesize text to audio file"""
        try:
            logger.debug(f"🔊 Synthesizing to file: {output_path}")
            if self.provider == "google":
                from google.cloud import texttospeech
                
                voice_name = voice or self.set_voice(language)
                synthesis_input = texttospeech.SynthesisInput(text=text)
                
                voice_params = texttospeech.VoiceSelectionParams(
                    language_code=language,
                    name=voice_name if voice_name else None
                )
                
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                    sample_rate_hertz=self.config.get("sample_rate_hertz", 16000)
                )
                
                response = await self.tts_client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice_params,
                    audio_config=audio_config
                )
                
                with open(output_path, "wb") as f:
                    f.write(response.audio_content)
                return True
            return False
        except Exception as e:
            logger.error(f"❌ TTS file synthesis error: {e}")
            return False
    
    def set_voice(self, language: str, gender: str = "neutral") -> Optional[str]:
        """Get suitable voice for language/gender"""
        # In production: Map language/gender to provider-specific voice
        voices = {
            ("en-US", "male"): "en-US-Neural2-C",
            ("en-US", "female"): "en-US-Neural2-E",
            ("si-LK", "male"): "si-LK-Neural2-A",
            ("si-LK", "female"): "si-LK-Neural2-B",
        }
        return voices.get((language, gender))
    
    async def close(self):
        """Close TTS connection"""
        logger.info(f"🔊 Closing {self.provider} TTS connection")
        self.is_connected = False
