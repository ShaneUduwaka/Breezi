# audio/audio_gateway.py
"""
Real-time bidirectional audio streaming gateway
Handles audio chunks from various sources and routes to STT/TTS
"""

import asyncio
from typing import Dict, Optional, Callable
import logging
from .audio_buffer import AudioBuffer, AudioFrame


logger = logging.getLogger(__name__)


class AudioStreamingGateway:
    """
    Manages real-time audio streaming:
    - Receives audio from various call sources
    - Routes to STT for transcription
    - Receives response from TTS
    - Sends audio back to caller
    """
    
    def __init__(self):
        self.active_sessions: Dict[str, 'AudioSession'] = {}
        self.incoming_callbacks: Dict[str, Callable] = {}
        self.outgoing_callbacks: Dict[str, Callable] = {}
    
    async def create_session(self, session_id: str) -> 'AudioSession':
        """Create new audio session"""
        session = AudioSession(session_id)
        self.active_sessions[session_id] = session
        logger.info(f"📍 Created audio session: {session_id}")
        return session
    
    async def get_session(self, session_id: str) -> Optional['AudioSession']:
        """Get existing audio session"""
        return self.active_sessions.get(session_id)
    
    async def handle_incoming_audio(self, session_id: str, audio_chunk: bytes):
        """
        Handle incoming audio from caller
        Routes to inbound callback (typically STT service)
        """
        session = await self.get_session(session_id)
        if not session:
            logger.warning(f"⚠️ Session not found: {session_id}")
            return
        
        # Create audio frame
        frame = AudioFrame(data=audio_chunk)
        
        # Add to buffer
        await session.incoming_buffer.add_frame(frame)
        
        # Trigger callback if registered
        if session_id in self.incoming_callbacks:
            callback = self.incoming_callbacks[session_id]
            await callback(frame)
    
    async def handle_outgoing_audio(self, session_id: str, audio_chunk: bytes):
        """
        Handle outgoing audio from TTS
        Queues for sending back to caller
        """
        session = await self.get_session(session_id)
        if not session:
            logger.warning(f"⚠️ Session not found: {session_id}")
            return
        
        # Create audio frame
        frame = AudioFrame(data=audio_chunk)
        
        # Add to outbound queue
        await session.outgoing_buffer.add_frame(frame)
        
        # Trigger callback if registered
        if session_id in self.outgoing_callbacks:
            callback = self.outgoing_callbacks[session_id]
            await callback(frame)
    
    def register_incoming_callback(self, session_id: str, callback: Callable):
        """Register callback for incoming audio"""
        self.incoming_callbacks[session_id] = callback
    
    def register_outgoing_callback(self, session_id: str, callback: Callable):
        """Register callback for outgoing audio"""
        self.outgoing_callbacks[session_id] = callback
    
    async def get_incoming_frame(self, session_id: str) -> Optional[AudioFrame]:
        """Get next incoming audio frame"""
        session = await self.get_session(session_id)
        if session:
            return await session.incoming_buffer.get_frame()
        return None
    
    async def get_outgoing_frame(self, session_id: str) -> Optional[AudioFrame]:
        """Get next outgoing audio frame"""
        session = await self.get_session(session_id)
        if session:
            return await session.outgoing_buffer.get_frame()
        return None
    
    async def close_session(self, session_id: str):
        """Close audio session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            if session_id in self.incoming_callbacks:
                del self.incoming_callbacks[session_id]
            if session_id in self.outgoing_callbacks:
                del self.outgoing_callbacks[session_id]
            logger.info(f"🔴 Closed audio session: {session_id}")
    
    def get_session_stats(self, session_id: str) -> dict:
        """Get session statistics"""
        session = self.active_sessions.get(session_id)
        if not session:
            return {}
        
        return {
            "session_id": session_id,
            "incoming_buffer": session.incoming_buffer.get_stats(),
            "outgoing_buffer": session.outgoing_buffer.get_stats(),
            "created_at": session.created_at
        }


class AudioSession:
    """Represents a single audio session between app and caller"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.incoming_buffer = AudioBuffer(buffer_size_ms=250)  # STT input
        self.outgoing_buffer = AudioBuffer(buffer_size_ms=250)  # TTS output
        self.created_at = asyncio.get_event_loop().time()
        self.metadata = {}
