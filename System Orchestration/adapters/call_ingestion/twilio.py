# adapters/call_ingestion/twilio.py
"""Twilio call ingestion adapter"""

from typing import Optional
import logging
from .base import CallIngestorBase


logger = logging.getLogger(__name__)


class TwilioIngestor(CallIngestorBase):
    """
    Twilio call ingestion via Media Streams
    
    Receives audio over WebSocket from Twilio
    Configuration:
        - account_sid: Twilio account SID
        - auth_token: Twilio auth token
        - webhook_url: URL for receiving webhook
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.websocket = None
        self.stream_sid = None
    
    async def start_call(self, session_id: str) -> bool:
        """Start Twilio Media Streams connection"""
        try:
            self.session_id = session_id
            logger.info(f"🎤 Twilio: Starting call session {session_id}")
            # Twilio connection would be established via webhook
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"❌ Twilio: Failed to start call: {e}")
            return False
    
    async def receive_audio_chunk(self) -> Optional[bytes]:
        """Receive audio from Twilio WebSocket"""
        try:
            if not self.websocket:
                return None
            
            # In production, receive from WebSocket
            # message = await self.websocket.recv()
            # return extract_audio_from_message(message)
            return None
        except Exception as e:
            logger.error(f"❌ Twilio: Error receiving audio: {e}")
            return None
    
    async def send_audio_chunk(self, audio_data: bytes) -> bool:
        """Send audio back to Twilio"""
        try:
            if not self.websocket:
                return False
            
            # In production, send via WebSocket to Twilio
            # await self.websocket.send(encode_audio_to_message(audio_data))
            return True
        except Exception as e:
            logger.error(f"❌ Twilio: Error sending audio: {e}")
            return False
    
    async def end_call(self) -> bool:
        """End Twilio call"""
        try:
            logger.info(f"📞 Twilio: Ending call session {self.session_id}")
            if self.websocket:
                await self.websocket.close()
            self.is_connected = False
            return True
        except Exception as e:
            logger.error(f"❌ Twilio: Error ending call: {e}")
            return False
