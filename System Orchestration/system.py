#!/usr/bin/env python3
"""
Breezi Production System - Unified Architecture
Supports both production (STT input) and testing (terminal input) modes
with identical internal processing pipeline

Usage:
    python system.py --mode testing      # Interactive terminal mode
    python system.py --mode production   # Production mode with STT
"""

import os
import sys
import json
import argparse
import logging
from typing import Optional, Tuple
from enum import Enum

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system
from system.conversation_manager import ConversationManager
from system.audio_io import DummySTT, DummyTTS
from utils.test_data_loader import TestDataLoader


class SystemMode(Enum):
    """System operating modes"""
    TESTING = "testing"      # Terminal input for testing
    PRODUCTION = "production"  # STT pipeline input


class InputProvider:
    """Abstract base for input providers"""
    
    def get_input(self) -> Tuple[str, str]:
        """
        Get user input
        Returns: (text, language_code)
        """
        raise NotImplementedError
    
    def shutdown(self):
        """Cleanup resources"""
        pass


class TerminalInputProvider(InputProvider):
    """Testing mode: Read input from terminal"""
    
    def __init__(self):
        self.session_id = "terminal_session"
        self.turn_count = 0
    
    def get_input(self) -> Tuple[str, str]:
        """Get input from terminal"""
        print("\n" + "="*70)
        print(f"📥 TURN {self.turn_count + 1}")
        print("="*70)
        
        # Get user input
        user_input = input("👤 You: ").strip()
        
        if not user_input:
            return None, None
        
        # Detect language (simple heuristic)
        language = self._detect_language(user_input)
        
        self.turn_count += 1
        return user_input, language
    
    @staticmethod
    def _detect_language(text: str) -> str:
        """
        Detect language from text
        Simple heuristic: check for Sinhala characters
        """
        # Sinhala Unicode range: U+0D80 to U+0DFF
        for char in text:
            if '\u0D80' <= char <= '\u0DFF':
                return "si"  # Sinhala
        return "en"  # English


class STTInputProvider(InputProvider):
    """Production mode: Read input from STT pipeline"""
    
    def __init__(self, stt_client, config: dict = None):
        """
        Args:
            stt_client: Configured STT client
            config: STT configuration
        """
        self.stt_client = stt_client
        self.config = config or {}
        self.session_id = self.config.get("session_id", "stt_session")
        self.turn_count = 0
        
        logging.info(f"📞 STT Input Provider initialized for {self.config.get('source', 'audio_input')}")
    
    def get_input(self) -> Tuple[str, str]:
        """Get input from STT pipeline"""
        try:
            # Read audio and convert to text
            result = self.stt_client.transcribe_audio(
                duration=self.config.get("duration", 5)
            )
            
            if not result or not result.get("text"):
                logging.warning("⚠️ No speech detected")
                return None, None
            
            text = result.get("text", "")
            language = result.get("language", "en")
            confidence = result.get("confidence", 0.0)
            
            logging.info(f"🎤 Transcribed ({confidence:.1%}): {text} [{language}]")
            
            self.turn_count += 1
            return text, language
            
        except Exception as e:
            logging.error(f"❌ STT Error: {e}")
            return None, None


class OutputHandler:
    """Abstract base for output handlers"""
    
    def output(self, text: str, language: str = "en"):
        """Output response"""
        raise NotImplementedError
    
    def shutdown(self):
        """Cleanup resources"""
        pass


class TerminalOutputHandler(OutputHandler):
    """Testing mode: Output to terminal"""
    
    def output(self, text: str, language: str = "en"):
        """Print response to terminal"""
        print(f"\n🤖 Bot: {text}\n")


class TTSOutputHandler(OutputHandler):
    """Production mode: Output via TTS"""
    
    def __init__(self, tts_client, config: dict = None):
        """
        Args:
            tts_client: Configured TTS client
            config: TTS configuration
        """
        self.tts_client = tts_client
        self.config = config or {}
        
        logging.info(f"🔊 TTS Output Handler initialized")
    
    def output(self, text: str, language: str = "en"):
        """Synthesize and play response"""
        try:
            # Synthesize speech
            result = self.tts_client.synthesize_speech(
                text=text,
                language=language
            )
            
            if result.get("success"):
                logging.info(f"🔊 Playing audio response ({language})")
            else:
                logging.error(f"❌ TTS Error: {result.get('error')}")
                # Fallback: print to terminal
                print(f"🤖 Bot: {text}\n")
                
        except Exception as e:
            logging.error(f"❌ TTS Error: {e}")
            # Fallback: print to terminal
            print(f"🤖 Bot: {text}\n")


class BreeziFAQSystem:
    """
    Production-Ready Breezi System
    Unified architecture supporting testing and production modes
    """
    
    def __init__(self, mode: SystemMode, config_path: str = "Business input/intent.JSON"):
        """
        Initialize the system
        
        Args:
            mode: SystemMode.TESTING or SystemMode.PRODUCTION
            config_path: Path to business configuration
        """
        self.mode = mode
        self.config_path = config_path
        
        # Setup logging
        self._setup_logging()
        
        # Load configuration
        self.config = self._load_config()
        
        # Build core system components
        self.system = build_system()
        self.conversation = self.system["conversation"]
        self.nlu = self.system["nlu"]
        
        # Setup input/output based on mode
        self.input_provider = self._create_input_provider()
        self.output_handler = self._create_output_handler()
        
        # Session tracking
        self.session_id = self.input_provider.session_id
        self.is_running = False
        
        self._print_startup_banner()
    
    def _setup_logging(self):
        """Configure logging"""
        log_level = logging.DEBUG if self.mode == SystemMode.TESTING else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _load_config(self) -> dict:
        """Load business configuration from JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logging.info(f"✅ Configuration loaded: {config['business_config']['name']}")
            return config
        except FileNotFoundError:
            logging.error(f"❌ Config file not found: {self.config_path}")
            sys.exit(1)
    
    def _create_input_provider(self) -> InputProvider:
        """Create input provider based on mode"""
        if self.mode == SystemMode.TESTING:
            return TerminalInputProvider()
        else:
            # Production: use STT pipeline
            stt_client = self.system.get("stt_client")
            return STTInputProvider(stt_client)
    
    def _create_output_handler(self) -> OutputHandler:
        """Create output handler based on mode"""
        if self.mode == SystemMode.TESTING:
            return TerminalOutputHandler()
        else:
            # Production: use TTS pipeline
            tts_client = self.system.get("tts_client")
            return TTSOutputHandler(tts_client)
    
    def _print_startup_banner(self):
        """Print system startup banner"""
        print("\n" + "="*70)
        print("🚀 BREEZI SYSTEM - PRODUCTION READY")
        print("="*70)
        print(f"Mode: {'🧪 TESTING' if self.mode == SystemMode.TESTING else '📞 PRODUCTION'}")
        print(f"Business: {self.config['business_config']['name']}")
        print(f"Type: {self.config['business_config']['type']}")
        print(f"Intents: {len(self.config['intents'])}")
        print(f"Menu Categories: {len(self.config['business_data']['menu']['categories'])}")
        print("="*70)
        
        if self.mode == SystemMode.TESTING:
            print("\n📝 Interactive Testing Mode")
            print("   • Type natural language questions")
            print("   • Type 'exit' or 'quit' to end session")
            print("   • Type 'menu' to see available options")
            print("   • All processing uses production pipeline\n")
        else:
            print("\n📞 Production Mode")
            print("   • Listening for STT input")
            print("   • Responses via TTS")
            print("   • Real-time conversation\n")
    
    def run(self):
        """Run the system in interactive mode"""
        self.is_running = True
        
        print("⏳ System ready. Processing inputs...\n")
        
        try:
            while self.is_running:
                # Get input
                user_input, language = self.input_provider.get_input()
                
                if user_input is None:
                    if self.mode == SystemMode.TESTING:
                        continue
                    else:
                        # In production, continue listening
                        continue
                
                # Check for exit commands (testing mode only)
                if self.mode == SystemMode.TESTING:
                    if user_input.lower() in ['exit', 'quit', 'q']:
                        print("\n👋 Goodbye!")
                        break
                    elif user_input.lower() == 'menu':
                        self._show_menu()
                        continue
                
                # Process through conversation pipeline (SAME FOR BOTH MODES)
                logging.debug(f"Processing: '{user_input}' (language: {language})")
                response = self._process_user_input(user_input, language)
                
                # Output response
                self.output_handler.output(response, language)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  System stopped by user")
        finally:
            self.shutdown()
    
    def _process_user_input(self, user_input: str, language: str) -> str:
        """
        Process user input through the system pipeline
        This is IDENTICAL for both testing and production modes
        
        Pipeline:
        1. NLU: Parse intent and entities
        2. Conversation Manager: Maintain state and context
        3. Dialog Orchestrator: Generate response
        4. Handler: Execute business logic
        """
        
        # Step 1: Parse with NLU
        logging.debug(f"→ NLU Processing...")
        nlu_result = self.nlu.parse(user_input)
        logging.debug(f"  Intent: {nlu_result.intent}")
        logging.debug(f"  Entities: {nlu_result.entities}")
        
        # Step 2: Handle through conversation manager
        # This maintains slot-filling, context awareness, and multi-turn state
        logging.debug(f"→ Conversation Manager...")
        response = self.conversation.handle_message(
            text=user_input,
            session_id=self.session_id
        )
        
        logging.debug(f"  Response: {response[:100]}...")
        
        return response
    
    def _show_menu(self):
        """Display menu options (testing mode only)"""
        print("\n" + "="*70)
        print("📋 AVAILABLE COMMANDS")
        print("="*70)
        print("Natural language examples:")
        print("  • 'I want to order a pizza'")
        print("  • 'Show me the menu'")
        print("  • 'Tell me about burgers'")
        print("  • 'What are your hours?'")
        print("  • 'I want delivery to 123 Main Street'")
        print("\nSystem commands:")
        print("  • 'menu' - Show this menu")
        print("  • 'exit' or 'quit' - Exit the system")
        print("="*70 + "\n")
    
    def shutdown(self):
        """Graceful shutdown"""
        self.is_running = False
        self.input_provider.shutdown()
        self.output_handler.shutdown()
        print("\n✅ System shutdown complete\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Breezi Production System - Testing and Production Modes"
    )
    
    parser.add_argument(
        '--mode',
        choices=['testing', 'production'],
        default='testing',
        help='System mode: testing (terminal input) or production (STT input)'
    )
    
    parser.add_argument(
        '--config',
        default='Business input/intent.JSON',
        help='Path to business configuration JSON'
    )
    
    args = parser.parse_args()
    
    # Select mode
    mode = SystemMode.TESTING if args.mode == 'testing' else SystemMode.PRODUCTION
    
    # Initialize and run system
    system = BreeziFAQSystem(mode=mode, config_path=args.config)
    system.run()


if __name__ == "__main__":
    main()
