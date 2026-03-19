# adapters/call_ingestion/base.py
"""Abstract base class for call ingestion"""

from abc import ABC, abstractmethod
from typing import Optional
import logging


logger = logging.getLogger(__name__)


class CallIngestorBase(ABC):
    """
    Abstract base class for call ingestion adapters
    Implement this for each call source (Twilio, VoIP, WebRTC, etc.)
    """
    
    def __init__(self, config: dict = None):
        """
        Initialize call ingestor
        
        Args:
            config: Provider-specific configuration
        """
        self.config = config or {}
        self.session_id: Optional[str] = None
        self.is_connected = False
    
    @abstractmethod
    async def start_call(self, session_id: str) -> bool:
        """
        Start call and establish connection
        
        Args:
            session_id: Unique call session identifier
            
        Returns:
            bool: True if connection established successfully
        """
        pass
    
    @abstractmethod
    async def receive_audio_chunk(self) -> Optional[bytes]:
        """
        Receive audio chunk from caller
        
        Returns:
            bytes: Audio data, or None if no data available
        """
        pass
    
    @abstractmethod
    async def send_audio_chunk(self, audio_data: bytes) -> bool:
        """
        Send audio chunk back to caller
        
        Args:
            audio_data: Audio bytes to send
            
        Returns:
            bool: True if sent successfully
        """
        pass
    
    @abstractmethod
    async def end_call(self) -> bool:
        """
        End call and cleanup connection
        
        Returns:
            bool: True if ended successfully
        """
        pass
    
    def get_provider_name(self) -> str:
        """Get provider name (e.g., 'twilio', 'custom-voip', 'webrtc')"""
        return self.__class__.__name__.replace("Ingestor", "").lower()
