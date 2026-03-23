
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import spacy
from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span

from .normalizers import normalize_slot_value
from .patterns import LEXICON, build_entity_ruler_patterns, intent_corpus
from .schema import INTENT_DEFINITIONS, SLOT_DEFINITIONS, get_all_slots_for_intent, get_priority_slots


@dataclass
class SlotMatch:
    slot_name: str
    value: str
    start: int
    end: int
    source: str
    score: float = 1.0
    normalized_value: Optional[str] = None


@dataclass
class ParseResult:
    text: str
    intent: str
    intent_confidence: float
    slots: Dict[str, str]
    slot_matches: List[SlotMatch]
    missing_required: List[str]
    missing_priority: List[str]
    follow_up_questions: List[str]
    debug: Dict[str, object] = field(default_factory=dict)


class RestaurantNLUEngine:
    def __init__(self) -> None:
        self.nlp = self._build_nlp()
        self.intent_matcher = self._build_intent_matcher(self.nlp)

    def _build_nlp(self) -> Language:
        try:
            nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer", "textcat"])
        except OSError:
            nlp = spacy.blank("en")
        if "entity_ruler" not in nlp.pipe_names:
            ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
            ruler.add_patterns(build_entity_ruler_patterns())
        return nlp

    def _build_intent_matcher(self, nlp: Language) -> PhraseMatcher:
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        for intent, texts in self._intent_examples_by_intent().items():
            docs = [nlp.make_doc(text) for text in texts]
            matcher.add(intent, docs)
        return matcher

    def _intent_examples_by_intent(self) -> Dict[str, List[str]]:
        data: Dict[str, List[str]] = {}
        for intent, text in intent_corpus():
            data.setdefault(intent, []).append(text)
        return data

    def parse(self, text: str, active_intent: Optional[str] = None) -> ParseResult:
        doc = self.nlp(text)
        intent, confidence, intent_debug = self._predict_intent(doc, active_intent=active_intent)
        slot_matches = self._extract_slots(doc, intent)
        slots = self._merge_slot_matches(slot_matches)
        missing_required, missing_priority = self._find_missing_slots(intent, slots)
        follow_up_questions = self._build_followups(intent, missing_required, missing_priority)
        debug = {
            "intent_candidates": intent_debug,
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "active_intent": active_intent,
        }
        return ParseResult(
            text=text,
            intent=intent,
            intent_confidence=confidence,
            slots=slots,
            slot_matches=slot_matches,
            missing_required=missing_required,
            missing_priority=missing_priority,
            follow_up_questions=follow_up_questions,
            debug=debug,
        )

    def _predict_intent(self, doc: Doc, active_intent: Optional[str] = None) -> Tuple[str, float, Dict[str, float]]:
        scores: Dict[str, float] = {intent: 0.0 for intent in INTENT_DEFINITIONS}

        for match_id, start, end in self.intent_matcher(doc):
            intent = self.nlp.vocab.strings[match_id]
            span_len = max(1, end - start)
            scores[intent] += 1.2 + 0.2 * span_len

        text_lower = doc.text.lower()

        # Heuristic boosts from slots + trigger words
        if any(ent.label_ == "food_item" for ent in doc.ents):
            for intent in [
                "start_new_order", "add_item_to_order", "ask_price_of_item",
                "ask_availability_of_item", "customize_item", "report_missing_item",
                "report_bad_quality", "menu_inquiry",
            ]:
                scores[intent] += 0.25

        if re.search(r"\b(price|cost|how much|කීයද)\b", text_lower):
            scores["ask_price_of_item"] += 2.0

        if re.search(r"\b(available|availability|තියෙනවද)\b", text_lower):
            scores["ask_availability_of_item"] += 2.0

        if re.search(r"\b(track|where is my order)\b", text_lower):
            scores["track_order"] += 2.5

        if re.search(r"\b(cancel|cancelled|cancellation)\b", text_lower):
            scores["cancel_order_before_payment"] += 2.2

        if re.search(r"\b(refund)\b", text_lower):
            scores["refund_request"] += 2.2
            scores["refund_complaint"] += 1.7

        if re.search(r"\b(order|place an order|want to order|want|get me)\b", text_lower):
            scores["start_new_order"] += 1.4

        if re.search(r"\b(deliver|delivered|delivery)\b", text_lower):
            scores["choose_delivery"] += 1.8
            scores["ask_delivery_time_estimate"] += 0.6
            scores["start_new_order"] += 0.6

        if re.search(r"\b(pickup|pick up|takeaway)\b", text_lower):
            scores["choose_pickup"] += 1.8
            scores["change_pickup_time"] += 0.6

        if re.search(r"\b(menu)\b", text_lower):
            scores["menu_inquiry"] += 1.8

        if re.search(r"\b(hours|open|opening)\b", text_lower):
            scores["store_opening_hours"] += 1.8

        if re.search(r"\b(location|where)\b", text_lower):
            scores["store_location"] += 1.2

        if re.search(r"\b(payment failed|failed payment|didn't go through)\b", text_lower):
            scores["payment_failed"] += 2.5

        if re.search(r"\b(points|loyalty)\b", text_lower):
            scores["check_loyalty_points"] += 1.8
            scores["redeem_loyalty_points"] += 0.8

        if re.search(r"\b(manager|callback|call me)\b", text_lower):
            scores["request_manager_callback"] += 2.0

        if re.search(r"\b(catering|event|party)\b", text_lower):
            scores["bulk_catering_order"] += 1.7
            scores["event_booking"] += 1.4

        # Context helps disambiguate short follow-up utterances.
        if active_intent and active_intent in scores:
            scores[active_intent] += 1.5

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, top_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else 0.0

        if top_score <= 0:
            top_intent = "start_new_order" if any(ent.label_ == "food_item" for ent in doc.ents) else "menu_inquiry"
            top_score = 0.4

        confidence = min(0.99, max(0.05, 0.5 + (top_score - second_score) / 6))
        return top_intent, confidence, dict(ranked[:10])

    def _extract_slots(self, doc: Doc, intent: str) -> List[SlotMatch]:
        allowed = set(get_all_slots_for_intent(intent))
        results: List[SlotMatch] = []

        # 1) entity ruler hits
        for ent in doc.ents:
            if ent.label_ in allowed:
                results.append(
                    SlotMatch(
                        slot_name=ent.label_,
                        value=ent.text,
                        normalized_value=normalize_slot_value(ent.label_, ent.text),
                        start=ent.start_char,
                        end=ent.end_char,
                        source="entity_ruler",
                        score=0.95,
                    )
                )

        # 2) regex slots
        for slot_name in allowed:
            definition = SLOT_DEFINITIONS.get(slot_name)
            if not definition:
                continue
            for regex in definition.regexes:
                for m in re.finditer(regex, doc.text, flags=re.IGNORECASE):
                    value = m.group().strip()
                    results.append(
                        SlotMatch(
                            slot_name=slot_name,
                            value=value,
                            normalized_value=normalize_slot_value(slot_name, value),
                            start=m.start(),
                            end=m.end(),
                            source="regex",
                            score=0.90,
                        )
                    )

        # 3) free-text heuristics for specific slots
        results.extend(self._extract_free_text(doc, intent, allowed))

        return self._deduplicate(results)

    def _extract_free_text(self, doc: Doc, intent: str, allowed: set[str]) -> List[SlotMatch]:
        text = doc.text
        results: List[SlotMatch] = []
        lower = text.lower()

        capture_prefixes = {
            "special_request": [
                "with ", "without ", "less ", "extra ", "no ", "please ", "make it ",
                "එක්ක", "නැතුව", "අඩුවෙන්",
            ],
            "instructions": [
                "leave it ", "call me ", "ring the bell", "near ", "next to ", "at the gate",
            ],
            "issue": [
                "because ", "issue is ", "problem is ", "it is ", "it's ", "the issue is ",
            ],
            "reason": [
                "because ", "reason is ", "since ",
            ],
            "message": [
                "feedback: ", "message: ", "i want to say ",
            ],
            "delivery_address": [
                "deliver to ", "send to ", "to ",
            ],
            "landmark": [
                "near ", "next to ", "opposite ", "beside ",
            ],
            "food_preference": [
                "something ", "anything ", "I prefer ", "prefer ",
            ],
            "split": [
                "split ", "half ",
            ],
            "previous": [
                "already ", "previously ", "before ",
            ],
            "resolution": [
                "i want ", "please ", "need a ",
            ],
            "name": [
                "my name is ", "this is ", "name ",
            ],
            "value": [
                "to ", "as ",
            ],
        }

        for slot_name, prefixes in capture_prefixes.items():
            if slot_name not in allowed:
                continue
            for prefix in prefixes:
                idx = lower.find(prefix.lower())
                if idx != -1:
                    start = idx + len(prefix)
                    fragment = text[start:].strip(" .,!?:;")
                    if fragment:
                        results.append(
                            SlotMatch(
                                slot_name=slot_name,
                                value=fragment,
                                normalized_value=normalize_slot_value(slot_name, fragment),
                                start=start,
                                end=len(text),
                                source="free_text",
                                score=0.65,
                            )
                        )
                        break

        # fallback for explicit order ids
        if "order_id" in allowed and "order" in lower:
            if not any(r.slot_name == "order_id" for r in results):
                m = re.search(r"order\s*(?:id)?\s*[:#-]?\s*([A-Z]?\d{3,8})", text, flags=re.I)
                if m:
                    value = m.group(1)
                    results.append(
                        SlotMatch(
                            slot_name="order_id",
                            value=value,
                            normalized_value=normalize_slot_value("order_id", value),
                            start=m.start(1),
                            end=m.end(1),
                            source="heuristic",
                            score=0.88,
                        )
                    )

        return results

    def _deduplicate(self, matches: List[SlotMatch]) -> List[SlotMatch]:
        best: Dict[Tuple[str, int, int, str], SlotMatch] = {}
        for m in matches:
            key = (m.slot_name, m.start, m.end, m.normalized_value or m.value)
            current = best.get(key)
            if current is None or m.score > current.score:
                best[key] = m
        return sorted(best.values(), key=lambda x: (x.start, -x.score))

    def _merge_slot_matches(self, matches: List[SlotMatch]) -> Dict[str, str]:
        merged: Dict[str, Tuple[str, float]] = {}
        for match in matches:
            candidate = match.normalized_value or match.value
            current = merged.get(match.slot_name)
            if current is None or match.score > current[1]:
                merged[match.slot_name] = (candidate, match.score)
        return {slot: value for slot, (value, _score) in merged.items()}

    def _find_missing_slots(self, intent: str, slots: Dict[str, str]) -> Tuple[List[str], List[str]]:
        definition = INTENT_DEFINITIONS[intent]
        missing_required = [slot for slot in definition.required_slots if slot not in slots]
        missing_priority = [slot for slot in get_priority_slots(intent) if slot not in slots]
        return missing_required, missing_priority

    def _build_followups(self, intent: str, missing_required: List[str], missing_priority: List[str]) -> List[str]:
        prompts = {
            "food_item": "Which food item do you want?",
            "quantity": "How many would you like?",
            "delivery_address": "What delivery address should I use?",
            "pickup_time": "What pickup time works for you?",
            "payment_method": "Which payment method do you want to use?",
            "order_id": "Can you share the order ID?",
            "special_request": "What customization would you like?",
            "modification_type": "What change should I make to the item?",
            "issue": "What exactly went wrong?",
            "name": "What name should I use?",
            "phone_number": "What phone number should I use?",
            "event_date": "What is the event date?",
            "event_time": "What is the event time?",
            "headcount": "How many people is this for?",
            "instructions": "Any delivery instructions I should note?",
        }
        queue = []
        for slot in missing_required + [s for s in missing_priority if s not in missing_required]:
            queue.append(prompts.get(slot, f"Please provide {slot.replace('_', ' ')}."))
        return queue
