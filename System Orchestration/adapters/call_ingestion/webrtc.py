# adapters/call_ingestion/webrtc.py
"""WebRTC call ingestion adapter (FastRTC integration)"""

from typing import Optional
import logging
from .base import CallIngestorBase


logger = logging.getLogger(__name__)


class WebRTCIngestor(CallIngestorBase):
    """
    WebRTC call ingestion (peer-to-peer audio)
    Can use FastRTC or native WebRTC APIs
    
    Configuration:
        - ice_servers: STUN/TURN servers list
        - use_fastrtc: Whether to use FastRTC library
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.peer_connection = None
        self.audio_track = None
    
    async def start_call(self, session_id: str) -> bool:
        """Start WebRTC peer connection"""
        try:
            self.session_id = session_id
            logger.info(f"🎤 WebRTC: Starting call session {session_id}")
            
            # In production: Initialize WebRTC peer connection
            # if self.config.get("use_fastrtc"):
            #     from fastrtc import RTCPeerConnection
            #     self.peer_connection = RTCPeerConnection()
            # else:
            #     # Use native WebRTC APIs
            #     pass
            
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"❌ WebRTC: Failed to start call: {e}")
            return False
    
    async def receive_audio_chunk(self) -> Optional[bytes]:
        """Receive audio from WebRTC peer"""
        try:
            if not self.peer_connection:
                return None
            
            # In production: Receive from WebRTC audio track
            # audio_frame = await self.audio_track.recv()
            # return audio_frame.to_bytes()
            return None
        except Exception as e:
            logger.error(f"❌ WebRTC: Error receiving audio: {e}")
            return None
    
    async def send_audio_chunk(self, audio_data: bytes) -> bool:
        """Send audio to WebRTC peer"""
        try:
            if not self.peer_connection or not self.audio_track:
                return False
            
            # In production: Send to WebRTC audio track
            # audio_frame = AudioFrame.from_bytes(audio_data)
            # await self.audio_track.send(audio_frame)
            return True
        except Exception as e:
            logger.error(f"❌ WebRTC: Error sending audio: {e}")
            return False
    
    async def end_call(self) -> bool:
        """End WebRTC call"""
        try:
            logger.info(f"📞 WebRTC: Ending call session {self.session_id}")
            if self.peer_connection:
                await self.peer_connection.close()
            self.is_connected = False
            return True
        except Exception as e:
            logger.error(f"❌ WebRTC: Error ending call: {e}")
            return False
