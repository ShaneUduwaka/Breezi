"""
Templated NLU module - Intent classifier + Entity extractor
Supports English and Sinhala with mixed language input
Reads all configuration from JSON files, no hardcoded business logic
"""

from utils.sinhala_utils import (
    SINHALA_KEYWORDS,
    detect_sinhala_content,
    extract_sinhala_words,
)


class NLUResult:
    def __init__(self, intent, entities, confidence=1.0, language="english"):
        self.intent = intent
        self.entities = entities
        self.confidence = confidence
        self.language = language  # Track the detected language


class FakeNLU:
    """
    Templated NLU that reads intent keywords and entity patterns from JSON.
    Supports mixed English and Sinhala language input.
    Completely generic - works for any business by changing JSON files.
    """

    def __init__(self, business_config):
        """
        Initialize NLU with business configuration from JSON

        Args:
            business_config: dict containing nlu_config and intents from JSON
        """
        self.nlu_config = business_config.get("nlu_config", {})
        self.intents = business_config.get("intents", {})
        self.entity_patterns = self.nlu_config.get("entity_patterns", {})
        self.fallback_intent = self.nlu_config.get("fallback_intent", "global_browse")

        # Build keyword-to-intent mapping from JSON
        self.intent_keywords = {}
        for intent_name, intent_data in self.intents.items():
            keywords = intent_data.get("nlu_keywords", [])
            for keyword in keywords:
                if keyword not in self.intent_keywords:
                    self.intent_keywords[keyword] = []
                self.intent_keywords[keyword].append(intent_name)

    def parse(self, text):
        """
        Parse user input and return intent + entities
        Supports both English and Sinhala (including mixed input)
        Uses JSON-configured keywords and patterns
        """
        text_lower = text.lower()
        
        # Detect language
        has_sinhala = detect_sinhala_content(text)
        language = "sinhala_mixed" if has_sinhala else "english"

        # Step 1: Classify intent using JSON keywords (English + Sinhala)
        detected_intent = self._detect_intent(text_lower, text, has_sinhala)

        # Step 2: Extract entities using JSON patterns (pass both original and lowercased for proper matching)
        entities = self._extract_entities(text, text_lower, detected_intent)

        return NLUResult(intent=detected_intent, entities=entities, language=language)

    def _detect_intent(self, text, original_text, has_sinhala):
        """Intent detection using JSON-configured keywords with Sinhala support"""
        intent_scores = {}

        # First pass: collect English keyword matches
        matching_keywords = []
        for keyword, intent_list in self.intent_keywords.items():
            if keyword in text:
                matching_keywords.append((keyword, intent_list))

        # Score intents based on English keywords
        for keyword, intent_list in matching_keywords:
            # Calculate base specificity score
            word_count = len(keyword.split())
            base_score = len(keyword) * word_count

            # Check how many intents this keyword maps to (exclusivity)
            exclusivity_factor = 1.0 / len(intent_list)

            if len(intent_list) == 1:
                exclusivity_factor = 2.0  # Double score for exclusive keywords
            else:
                exclusivity_factor = 0.5   # Half score for shared keywords

            specificity_score = base_score * exclusivity_factor

            # Each keyword match gives weighted points to all intents it maps to
            for intent in intent_list:
                if intent not in intent_scores:
                    intent_scores[intent] = 0
                intent_scores[intent] += specificity_score

        # Second pass: if Sinhala detected, also check Sinhala keywords
        if has_sinhala:
            for intent_name, sinhala_keywords in SINHALA_KEYWORDS.items():
                for sinhala_keyword in sinhala_keywords:
                    if sinhala_keyword in original_text:
                        if intent_name not in intent_scores:
                            intent_scores[intent_name] = 0
                        # Give good score to Sinhala matches (slightly less than exclusive English)
                        intent_scores[intent_name] += 1.5

        # Return intent with highest score, or fallback
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
            return best_intent

        return self.fallback_intent

    def _extract_entities(self, text, text_lower, intent):
        """Extract named entities using JSON-configured patterns
        
        Args:
            text: Original text (for Sinhala pattern matching)
            text_lower: Lowercased text (for English pattern matching) 
            intent: The detected intent
        """
        entities = {}

        # Get intent definition to understand what slots it expects
        intent_def = self.intents.get(intent, {})
        slots = intent_def.get("slots", {})

        # For each slot in the intent, try to extract values
        for slot_name, slot_config in slots.items():
            slot_type = slot_config.get("type", "string")
            
            # Use extraction_key from JSON to map to entity patterns
            # Falls back to slot_name if extraction_key not defined
            extraction_key = slot_config.get("extraction_key", slot_name)

            if slot_type == "enum":
                # For enum slots, check allowed values (case-insensitive for English, exact for Sinhala)
                allowed_values = slot_config.get("allowed_values", [])
                for value in allowed_values:
                    if value.lower() in text_lower or value in text:
                        entities[slot_name] = value
                        break

            elif slot_type in ["string", "list<string>"]:
                # Use extraction_key from JSON configuration (TEMPLATE-DRIVEN)
                # This makes it fully configurable without hardcoding
                pattern_name = extraction_key

                # Use entity patterns from JSON to extract values
                if pattern_name in self.entity_patterns:
                    patterns = self.entity_patterns[pattern_name]
                    
                    # Special handling for delivery_address (multi-part extraction)
                    if extraction_key == "delivery_address":
                        # Try to find address patterns 
                        # Look for any text that contains address keywords
                        address_found = False
                        for pattern in patterns:
                            if pattern in text or pattern.lower() in text_lower:
                                # Found an address keyword, now try to extract the full address
                                # For now, just mark that we found an address-related text
                                # In a real system, you'd use NER or regex for full address extraction
                                words = text.split()
                                # Look for pattern (like "street", "avenue") and get surrounding context
                                for i, word in enumerate(words):
                                    if word.lower() == pattern.lower() or pattern in word.lower():
                                        # Extract surrounding words as likely address components
                                        start = max(0, i - 3)  # Get up to 3 words before
                                        end = min(len(words), i + 2)  # Get up to 2 words after
                                        detected_address = " ".join(words[start:end])
                                        if slot_name not in entities:
                                            entities[slot_name] = detected_address
                                            address_found = True
                                            break
                                if address_found:
                                    break
                    else:
                        # Regular pattern matching for non-address strings
                        for pattern in patterns:
                            # Match both original (Sinhala) and lowercase (English) text
                            if pattern in text or pattern.lower() in text_lower:
                                if slot_type == "list<string>":
                                    # For lists, collect all matches
                                    if slot_name not in entities:
                                        entities[slot_name] = []
                                    if pattern not in entities[slot_name]:
                                        entities[slot_name].append(pattern)
                                else:
                                    # For single strings, take first match
                                    if slot_name not in entities:
                                        entities[slot_name] = pattern
                                break

        return entities
