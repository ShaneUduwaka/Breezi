
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .extractor import ParseResult, RestaurantNLUEngine
from .schema import INTENT_DEFINITIONS


@dataclass
class DialogueState:
    active_intent: Optional[str] = None
    slots: Dict[str, str] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)

    def update(self, parse_result: ParseResult) -> None:
        self.active_intent = parse_result.intent
        self.slots.update(parse_result.slots)
        self.history.append(parse_result.text)


class DialogueManager:
    def __init__(self, engine: Optional[RestaurantNLUEngine] = None) -> None:
        self.engine = engine or RestaurantNLUEngine()
        self.state = DialogueState()

    def handle(self, text: str) -> Dict[str, object]:
        parsed = self.engine.parse(text, active_intent=self.state.active_intent)

        # Contextual intents can inherit existing slots.
        merged_slots = dict(self.state.slots)
        merged_slots.update(parsed.slots)
        parsed.slots = merged_slots

        definition = INTENT_DEFINITIONS[parsed.intent]
        parsed.missing_required = [s for s in definition.required_slots if s not in parsed.slots]
        parsed.missing_priority = [s for s in definition.priority_slots if s not in parsed.slots]
        parsed.follow_up_questions = self.engine._build_followups(
            parsed.intent, parsed.missing_required, parsed.missing_priority
        )

        self.state.update(parsed)

        action = self._choose_action(parsed)
        response = self._build_response(parsed, action)

        return {
            "intent": parsed.intent,
            "intent_confidence": parsed.intent_confidence,
            "slots": parsed.slots,
            "missing_required": parsed.missing_required,
            "follow_up_questions": parsed.follow_up_questions,
            "action": action,
            "response": response,
            "debug": parsed.debug,
        }

    def _choose_action(self, parsed: ParseResult) -> str:
        definition = INTENT_DEFINITIONS[parsed.intent]
        if parsed.missing_required:
            return "ask_followup"
        if definition.kind == "question":
            return "answer_query"
        if definition.kind == "support":
            return "create_support_ticket"
        return "execute_transaction"

    def _build_response(self, parsed: ParseResult, action: str) -> str:
        if action == "ask_followup":
            return parsed.follow_up_questions[0]
        if action == "answer_query":
            return f"I understood this as '{parsed.intent}'. I have enough information to answer or call the lookup layer."
        if action == "create_support_ticket":
            return f"I understood '{parsed.intent}' and captured the issue details. You can now route this to the support workflow."
        return f"I understood '{parsed.intent}' and captured the required information. This is ready for your backend action layer."
