from dialog.intent_state import IntentState
import time


class ConversationManager:

    def __init__(self, registry, orchestrator, nlu, memory=None):
        self.registry = registry
        self.orchestrator = orchestrator
        self.nlu = nlu
        # optional ContextMemory instance
        self.memory = memory
        # last-used session id
        self.session_id = None

        self.state = None
        self.language = "english"  # Track detected language (english or sinhala_mixed)

    def handle_message(self, text, session_id: str = None):
        """Process a user utterance with CONTEXT-AWARE NLU.

        ``session_id`` is used to save and load context if a ContextMemory is
        configured.  The method will update the ongoing intent state and then
        invoke the dialog orchestrator.  After the handler response is
        generated the turn is appended to memory along with serialized state.
        Supports both English and Sinhala input with auto-detection.
        
        CONTEXT-AWARE: When current intent has missing slots and NLU detects
        a fallback/default intent, assume continuation and re-extract slot
        values for current intent from the input.
        """

        # maintain session identifier for subsequent calls
        if session_id:
            self.session_id = session_id

        nlu_result = self.nlu.parse(text)
        
        # Track detected language
        if hasattr(nlu_result, 'language'):
            self.language = nlu_result.language

        # CONTEXT-AWARE LOGIC: Check if we should stay in current intent
        fallback_intent = self.nlu.fallback_intent
        should_stay_in_context = (
            self.state is not None and 
            self.state.missing_slots() and  # Current intent has missing slots
            nlu_result.intent == fallback_intent  # NLU detected fallback intent
        )

        if self.state is None or (nlu_result.intent != self.state.intent and not should_stay_in_context):
            # Switch to new intent only if not staying in current context
            intent_def = self.registry.get_intent(nlu_result.intent)

            if not intent_def:
                response = "Sorry, I don't understand."
                self._maybe_append_turn(text, nlu_result, response)
                return response

            self.state = IntentState(nlu_result.intent, intent_def)
        
        # Extract entities from current input (from NLU parsing)
        for slot, value in nlu_result.entities.items():
            self.state.update_slot(slot, value)

        # ADDITIONAL CONTEXT-AWARE EXTRACTION:
        # Try to extract slot values for current intent even if NLU didn't
        # explicitly detect them. This enables natural language slot-filling.
        if self.state.missing_slots():
            self._extract_remaining_slots(text, self.state)

        # Pass language info to orchestrator
        response = self.orchestrator.process(self.state, language=self.language)

        # save conversation state and turn
        self._maybe_append_turn(text, nlu_result, response)

        return response

    def _maybe_append_turn(self, text, nlu_result, response):
        if not self.memory or not self.session_id:
            return

        turn = {
            "input": text,
            "intent": nlu_result.intent,
            "slots": self.state.slots if self.state else {},
            "output": response,
            "timestamp": time.time(),
            "language": self.language,
        }
        try:
            self.memory.append_turn(self.session_id, turn)
            # also persist latest state
            if self.state:
                self.memory.save(self.session_id, self.state.to_dict())
        except Exception:
            # swallow memory errors so conversation continues
            pass

    def _extract_remaining_slots(self, text, state):
        """
        Context-aware slot extraction: Try to extract slot values for the
        current intent even if NLU didn't explicitly detect them.
        
        This enables conversation flow like:
        Turn 1: "I want pizza" → detected intent, entities extracted
        Turn 2: "delivery, 2" → falls back to default intent, but we extract
                               order_type=delivery, quantity_per_item=2
                               for current intent (start_order)
        
        Args:
            text: User input
            state: Current IntentState
        """
        if not state or not state.missing_slots():
            return
        
        intent_def = self.registry.get_intent(state.intent)
        if not intent_def:
            return
        
        slots = intent_def.get("slots", {})
        missing_slots = state.missing_slots()
        text_lower = text.lower()
        
        # Try to fill each missing slot using NLU patterns
        for slot_name in missing_slots:
            if slot_name in slots:
                slot_config = slots[slot_name]
                slot_type = slot_config.get("type", "string")
                
                if slot_type == "enum":
                    # For enum slots, check allowed values (both original and lowercase)
                    allowed_values = slot_config.get("allowed_values", [])
                    for value in allowed_values:
                        if value.lower() in text_lower or value in text:
                            state.update_slot(slot_name, value)
                            break
                
                else:
                    # For string/list slots, use entity patterns
                    pattern_mappings = {
                        "order_items": "item_name",
                        "item_name": "item_name",
                        "category": "category",
                        "location_query": "location_query",
                        "order_type": "order_type",
                        "quantity": "quantity",
                        "quantity_per_item": "quantity"
                    }
                    
                    pattern_name = pattern_mappings.get(slot_name, slot_name)
                    
                    # Get entity patterns from NLU
                    if hasattr(self.nlu, 'entity_patterns'):
                        entity_patterns = self.nlu.entity_patterns.get(pattern_name, [])
                        for pattern in entity_patterns:
                            # Match both original (Sinhala) and lowercase (English)
                            if pattern in text or pattern.lower() in text_lower:
                                if slot_type == "list<string>":
                                    if slot_name not in state.slots or state.slots[slot_name] is None:
                                        state.update_slot(slot_name, [pattern])
                                    elif isinstance(state.slots[slot_name], list):
                                        if pattern not in state.slots[slot_name]:
                                            state.slots[slot_name].append(pattern)
                                else:
                                    state.update_slot(slot_name, pattern)
                                break