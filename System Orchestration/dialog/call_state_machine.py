import logging
from enum import Enum

logger = logging.getLogger(__name__)

class CallState(str, Enum):
    GREETING = "GREETING"
    ACTIVE = "ACTIVE"
    WRAPUP = "WRAPUP"
    ENDED = "ENDED"

class CallStateMachine:
    GREETING_MSG = "Hello, this is Breezi! How can I help you today?"
    WRAPUP_MSG = "Is there anything else I can help you with?"
    GOODBYE_MSG = "Thank you for calling Breezi. Goodbye!"

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.state = CallState.GREETING

    def get_proactive_greeting(self) -> str:
        """Fetch the initial greeting proactively and transition state to ACTIVE."""
        if self.state == CallState.GREETING:
            self.state = CallState.ACTIVE
            return self.GREETING_MSG
        return ""

    def handle(self, text: str, conversation_manager) -> tuple[str, bool]:
        """
        Process user text based on the current call state.
        
        Args:
            text: user input
            conversation_manager: the System ConversationManager instance to process NLU/Orchestrator logic
            
        Returns:
            (response_text, should_end_call)
        """
        should_end_call = False
        response = ""

        if self.state == CallState.GREETING:
            # Fallback in case get_proactive_greeting wasn't called
            self.state = CallState.ACTIVE
            response = conversation_manager.handle_active_message(text, self.session_id)
            if conversation_manager.is_state_complete():
                self.state = CallState.WRAPUP
                response += f" {self.WRAPUP_MSG}"
        
        elif self.state == CallState.ACTIVE:
            response = conversation_manager.handle_active_message(text, self.session_id)
            
            if conversation_manager.is_state_complete():
                self.state = CallState.WRAPUP
                response += f" {self.WRAPUP_MSG}"

        elif self.state == CallState.WRAPUP:
            # Check what the user said
            nlu_result = conversation_manager.nlu.parse(text)
            
            if nlu_result.intent == "confirm_end":
                self.state = CallState.ENDED
                response = self.GOODBYE_MSG
                should_end_call = True
            elif nlu_result.intent == "confirm_continue":
                self.state = CallState.ACTIVE
                # Wipe the old IntentState so we can start fresh
                conversation_manager.reset_state(self.session_id)
                response = "Okay, what else can I help you with?"
            else:
                # User asked a new question directly (e.g. "Also where are you located?")
                self.state = CallState.ACTIVE
                conversation_manager.reset_state(self.session_id)
                response = conversation_manager.handle_active_message(text, self.session_id)
                
                if conversation_manager.is_state_complete():
                    self.state = CallState.WRAPUP
                    response += f" {self.WRAPUP_MSG}"

        elif self.state == CallState.ENDED:
            response = self.GOODBYE_MSG
            should_end_call = True

        return response, should_end_call
