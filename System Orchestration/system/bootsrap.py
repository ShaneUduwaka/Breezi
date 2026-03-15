import os
import json

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


def load_business_config(json_path):
    """Load business configuration from JSON file"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_system(json_path=None):
    """Build the complete AI Call Agent system with all components"""

    # Use default path if not provided
    if json_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "..", "Business input", "intent.JSON")
        json_path = os.path.abspath(json_path)

    # Load business configuration from JSON
    business_config = load_business_config(json_path)

    # Extract different sections
    intents = business_config.get("intents", {})
    business_data = business_config.get("business_data", {})
    nlu_config = business_config.get("nlu_config", {})

    # memory stores (must be created before handlers so they can be injected)
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    rag_store = RagStore(redis_url)
    context_mem = ContextMemory(redis_url)

    # Initialize handlers with business data and memory references
    initialize_handlers(business_data, rag_store=rag_store, context_memory=context_mem)

    # Create registry with intents from JSON
    registry = IntentRegistry(json_path, handler_mapping=HANDLERS)

    # Initialize components
    llm = FakeLLM()
    orchestrator = DialogOrchestrator(registry, llm)

    # Pass full business config to NLU (includes intents and nlu_config)
    nlu = FakeNLU(business_config)

    stt = DummySTT()
    tts = DummyTTS()

    conversation = ConversationManager(registry, orchestrator, nlu, memory=context_mem)

    return {
        "conversation": conversation,
        "stt": stt,
        "tts": tts,
        "orchestrator": orchestrator,
        "nlu": nlu,
        "registry": registry,
        "llm": llm,
        "business_config": business_config,
        "rag": rag_store,
        "context_memory": context_mem,
    }