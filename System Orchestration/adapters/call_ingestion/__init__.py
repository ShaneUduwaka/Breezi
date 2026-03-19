# adapters/call_ingestion/__init__.py
"""Call ingestion adapters for different call sources"""

from .base import CallIngestorBase
from .twilio import TwilioIngestor
from .custom_voip import CustomVoIPIngestor
from .webrtc import WebRTCIngestor

__all__ = [
    "CallIngestorBase",
    "TwilioIngestor",
    "CustomVoIPIngestor",
    "WebRTCIngestor"
]
