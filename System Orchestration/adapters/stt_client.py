# adapters/stt_client.py
"""Multi-provider Speech-to-Text client"""

from typing import AsyncGenerator, Optional
import logging


logger = logging.getLogger(__name__)


class STTResult:
    """STT transcription result"""
    def __init__(self, text: str, confidence: float, is_final: bool):
        self.text = text
        self.confidence = confidence
        self.is_final = is_final


class STTClient:
    """
    Multi-provider STT client
    Supports: Google Cloud Speech, AWS Transcribe, Azure Speech
    """
    
    def __init__(self, provider: str = "google", config: dict = None):
        """
        Initialize STT client
        
        Args:
            provider: STT provider (google, aws, azure)
            config: Provider-specific configuration
        """
        self.provider = provider
        self.config = config or {}
        self.is_connected = False
    
    async def connect(self) -> bool:
        """Connect to STT service"""
        try:
            logger.info(f"🎙️ Connecting to {self.provider} STT...")
            # In production: Initialize provider-specific client
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"❌ STT connection failed: {e}")
            return False
    
    async def transcribe_stream(
        self,
        audio_stream: AsyncGenerator[bytes, None],
        session_id: str,
        language: str = "en-US"
    ) -> AsyncGenerator[STTResult, None]:
        """
        Real-time streaming transcription
        
        Args:
            audio_stream: Async generator yielding audio chunks
            session_id: Call session ID
            language: Language code (e.g., en-US, si-LK)
            
        Yields:
            STTResult: Incremental transcription results
        """
        try:
            logger.debug(f"🎙️ Starting STT stream for session {session_id}")
            
            # In production: Stream audio to provider and yield results
            # For now, placeholder
            async for audio_chunk in audio_stream:
                if not audio_chunk:
                    continue
                
                # Send to provider and receive partial results
                # result = await self._send_chunk_to_provider(audio_chunk)
                # if result:
                #     yield result
                pass
        
        except Exception as e:
            logger.error(f"❌ STT transcription error: {e}")
    
    async def transcribe_file(
        self,
        audio_file_path: str,
        language: str = "en-US"
    ) -> str:
        """Transcribe complete audio file"""
        try:
            logger.debug(f"🎙️ Transcribing file: {audio_file_path}")
            # In production: Send entire file to provider
            # result = await self._send_file_to_provider(audio_file_path, language)
            # return result.text
            return ""
        except Exception as e:
            logger.error(f"❌ STT file transcription error: {e}")
            return ""
    
    async def close(self):
        """Close STT connection"""
        logger.info(f"🎙️ Closing {self.provider} STT connection")
        self.is_connected = False
