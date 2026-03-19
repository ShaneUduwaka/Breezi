import os
import json
import logging
from typing import Optional, Dict, Any

from dialog.IntentRegistry import IntentRegistry
from dialog.dialog_orchestrator import DialogOrchestrator
from system.conversation_manager import ConversationManager
from system.audio_io import DummySTT, DummyTTS

from handlers.handler_mapping import HANDLERS
from handlers.order_handlers import initialize_handlers
from llm.fake_llm import FakeLLM
from nlu.fake_nlu import FakeNLU

# memory stores
from memory.rag_store import RagStore
from memory.context_memory import ContextMemory

# Phase 1: Audio & Call Components
from audio import AudioStreamingGateway
from adapters.call_ingestion import (
    CallIngestorBase,
    TwilioIngestor,
    CustomVoIPIngestor,
    WebRTCIngestor
)
from adapters.stt_client import STTClient
from adapters.tts_client import TTSClient


logger = logging.getLogger(__name__)


def load_business_config(json_path):
    """Load business configuration from JSON file"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_call_ingestor(ingestor_type: str, config: Dict[str, Any] = None) -> CallIngestorBase:
    """
    Factory function to create call ingestor based on type
    
    Args:
        ingestor_type: Type of ingestor (twilio, custom_voip, webrtc)
        config: Provider-specific configuration
    
    Returns:
        CallIngestorBase: Configured call ingestor instance
    """
    config = config or {}
    ingestor_type = ingestor_type.lower()
    
    logger.info(f"📞 Creating call ingestor: {ingestor_type}")
    
    if ingestor_type == "twilio":
        return TwilioIngestor(config)
    elif ingestor_type == "custom_voip":
        return CustomVoIPIngestor(config)
    elif ingestor_type == "webrtc":
        return WebRTCIngestor(config)
    elif ingestor_type == "mock":
        # Return mock ingestor for development
        logger.warning("⚠️ Using MOCK call ingestor for development")
        return TwilioIngestor(config)  # Use as placeholder
    else:
        raise ValueError(f"Unknown ingestor type: {ingestor_type}")


def create_stt_client(provider: str, config: Dict[str, Any] = None) -> Optional[STTClient]:
    """
    Factory function to create STT client
    
    Args:
        provider: STT provider (google, aws, azure, mock)
        config: Provider-specific configuration
    
    Returns:
        STTClient: Configured STT client instance
    """
    config = config or {}
    provider = provider.lower()
    
    # If mock mode, return configured mock client
    if provider == "mock":
        logger.warning("⚠️ Using MOCK STT client for development")
        return STTClient(provider="google", config=config)
    
    logger.info(f"🎙️ Creating STT client: {provider}")
    return STTClient(provider=provider, config=config)


def create_tts_client(provider: str, config: Dict[str, Any] = None) -> Optional[TTSClient]:
    """
    Factory function to create TTS client
    
    Args:
        provider: TTS provider (google, aws, azure, mock)
        config: Provider-specific configuration
    
    Returns:
        TTSClient: Configured TTS client instance
    """
    config = config or {}
    provider = provider.lower()
    
    # If mock mode, return configured mock client
    if provider == "mock":
        logger.warning("⚠️ Using MOCK TTS client for development")
        return TTSClient(provider="google", config=config)
    
    logger.info(f"🔊 Creating TTS client: {provider}")
    return TTSClient(provider=provider, config=config)


def get_environmental_config() -> Dict[str, Any]:
    """
    Load Breezi configuration from environment variables
    Falls back to sensible defaults
    """
    return {
        "call_ingestion_type": os.getenv("CALL_INGESTION_TYPE", "mock"),
        "stt_provider": os.getenv("STT_PROVIDER", "mock"),
        "tts_provider": os.getenv("TTS_PROVIDER", "mock"),
        "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }



def build_system(json_path=None, use_phase1=True):
    """
    Build the complete AI Call Agent system with all components
    
    Args:
        json_path: Path to intent.JSON (optional, uses default if None)
        use_phase1: Whether to include Phase 1 audio/call components (default: True)
    
    Returns:
        dict: Complete system with all initialized components
    """

    # Use default path if not provided
    if json_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "..", "Business input", "intent.JSON")
        json_path = os.path.abspath(json_path)

    logger.info("="*70)
    logger.info("🚀 BREEZI SYSTEM INITIALIZATION")
    logger.info("="*70)

    # Load business configuration from JSON
    logger.info("📋 Loading business configuration...")
    business_config = load_business_config(json_path)
    logger.info("✅ Business config loaded")

    # Extract different sections
    intents = business_config.get("intents", {})
    business_data = business_config.get("business_data", {})
    nlu_config = business_config.get("nlu_config", {})

    # memory stores (must be created before handlers so they can be injected)
    logger.info("🧠 Initializing memory stores...")
    rag_store = RagStore()
    context_mem = ContextMemory()
    logger.info("✅ Memory stores initialized")

    # Initialize handlers with business data and memory references
    logger.info("🔧 Initializing handlers...")
    initialize_handlers(business_data, rag_store=rag_store, context_memory=context_mem)
    logger.info("✅ Handlers initialized")

    # Create registry with intents from JSON
    logger.info("📚 Creating intent registry...")
    registry = IntentRegistry(json_path, handler_mapping=HANDLERS)
    logger.info("✅ Intent registry created")

    # Initialize core components
    logger.info("🔌 Initializing core components...")
    llm = FakeLLM()
    orchestrator = DialogOrchestrator(registry, llm)

    # Pass full business config to NLU (includes intents and nlu_config)
    nlu = FakeNLU(business_config)
    conversation = ConversationManager(registry, orchestrator, nlu, memory=context_mem)
    logger.info("✅ Core components initialized")

    # Build system dictionary
    system = {
        "conversation": conversation,
        "orchestrator": orchestrator,
        "nlu": nlu,
        "registry": registry,
        "llm": llm,
        "business_config": business_config,
        "rag": rag_store,
        "context_memory": context_mem,
    }

    # ============= PHASE 1: Audio Gateway & Call Integration =============
    if use_phase1:
        logger.info("\n📞 PHASE 1: Audio & Call Components")
        logger.info("-"*70)
        
        # Load environment-based configuration
        env_config = get_environmental_config()
        logger.debug(f"Environment config: {env_config}")
        
        # Initialize Audio Gateway (real-time bidirectional audio)
        logger.info("🎵 Initializing audio gateway...")
        audio_gateway = AudioStreamingGateway()
        system["audio_gateway"] = audio_gateway
        logger.info("✅ Audio gateway initialized")
        
        # Initialize Call Ingestor (supports Twilio, Custom VoIP, WebRTC)
        logger.info(f"📞 Initializing call ingestor ({env_config['call_ingestion_type']})...")
        call_ingestor_config = {
            "account_sid": os.getenv("TWILIO_ACCOUNT_SID"),
            "auth_token": os.getenv("TWILIO_AUTH_TOKEN"),
            "server_host": os.getenv("VOIP_SERVER_HOST", "localhost"),
            "server_port": os.getenv("VOIP_SERVER_PORT", 5060),
            "use_fastrtc": os.getenv("USE_FASTRTC", "false").lower() == "true",
        }
        call_ingestor = create_call_ingestor(
            env_config["call_ingestion_type"],
            config=call_ingestor_config
        )
        system["call_ingestor"] = call_ingestor
        logger.info(f"✅ Call ingestor initialized: {call_ingestor.get_provider_name()}")
        
        # Initialize STT Client (multi-provider)
        logger.info(f"🎙️ Initializing STT client ({env_config['stt_provider']})...")
        stt_config = {
            "google_api_key": os.getenv("GOOGLE_CLOUD_STT_KEY"),
            "aws_region": os.getenv("AWS_STT_REGION", "us-east-1"),
            "azure_key": os.getenv("AZURE_STT_KEY"),
            "language": os.getenv("STT_LANGUAGE", "en-US"),
        }
        stt_client = create_stt_client(
            env_config["stt_provider"],
            config=stt_config
        )
        system["stt_client"] = stt_client
        logger.info(f"✅ STT client initialized: {env_config['stt_provider']}")
        
        # Initialize TTS Client (multi-provider)
        logger.info(f"🔊 Initializing TTS client ({env_config['tts_provider']})...")
        tts_config = {
            "google_api_key": os.getenv("GOOGLE_CLOUD_TTS_KEY"),
            "aws_region": os.getenv("AWS_TTS_REGION", "us-east-1"),
            "azure_key": os.getenv("AZURE_TTS_KEY"),
            "language": os.getenv("TTS_LANGUAGE", "en-US"),
        }
        tts_client = create_tts_client(
            env_config["tts_provider"],
            config=tts_config
        )
        system["tts_client"] = tts_client
        logger.info(f"✅ TTS client initialized: {env_config['tts_provider']}")
        
        # Keep old dummy clients for backward compatibility
        system["stt"] = DummySTT()
        system["tts"] = DummyTTS()
        
        logger.info("-"*70)
        logger.info("✅ Phase 1 components ready")
    
    logger.info("="*70)
    logger.info("✅ SYSTEM INITIALIZATION COMPLETE")
    logger.info("="*70 + "\n")
    
    return system