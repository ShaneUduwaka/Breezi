# adapters/__init__.py
"""Service adapters for external integrations"""

from .call_ingestion import CallIngestorBase
from .stt_client import STTClient
from .tts_client import TTSClient

__all__ = ["CallIngestorBase", "STTClient", "TTSClient"]
