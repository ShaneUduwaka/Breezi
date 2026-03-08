"""
Templated NLU module - Intent classifier + Entity extractor
Reads all configuration from JSON files, no hardcoded business logic
"""

class NLUResult:
    def __init__(self, intent, entities, confidence=1.0):
        self.intent = intent
        self.entities = entities
        self.confidence = confidence


class FakeNLU:
    """
    Templated NLU that reads intent keywords and entity patterns from JSON.
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
        Uses JSON-configured keywords and patterns
        """
        text_lower = text.lower()

        # Step 1: Classify intent using JSON keywords
        detected_intent = self._detect_intent(text_lower)

        # Step 2: Extract entities using JSON patterns
        entities = self._extract_entities(text_lower, detected_intent)

        return NLUResult(intent=detected_intent, entities=entities)

    def _detect_intent(self, text):
        """Intent detection using JSON-configured keywords with improved specificity"""
        intent_scores = {}

        # First pass: collect all matching keywords
        matching_keywords = []
        for keyword, intent_list in self.intent_keywords.items():
            if keyword in text:
                matching_keywords.append((keyword, intent_list))

        # Score intents based on keyword specificity and exclusivity
        for keyword, intent_list in matching_keywords:
            # Calculate base specificity score
            word_count = len(keyword.split())
            base_score = len(keyword) * word_count

            # Check how many intents this keyword maps to (exclusivity)
            exclusivity_factor = 1.0 / len(intent_list)  # Higher score for exclusive keywords

            # Boost exclusive keywords more significantly
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

        # Return intent with highest score, or fallback
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
            return best_intent

        return self.fallback_intent

    def _extract_entities(self, text, intent):
        """Extract named entities using JSON-configured patterns"""
        entities = {}

        # Get intent definition to understand what slots it expects
        intent_def = self.intents.get(intent, {})
        slots = intent_def.get("slots", {})

        # For each slot in the intent, try to extract values
        for slot_name, slot_config in slots.items():
            slot_type = slot_config.get("type", "string")

            if slot_type == "enum":
                # For enum slots, check allowed values
                allowed_values = slot_config.get("allowed_values", [])
                for value in allowed_values:
                    if value in text:
                        entities[slot_name] = value
                        break

            elif slot_type in ["string", "list<string>"]:
                # Map slot names to appropriate entity patterns
                pattern_mappings = {
                    "order_items": "item_name",
                    "item_name": "item_name",
                    "category": "category",
                    "location_query": "location_query",
                    "order_type": "order_type",
                    "quantity": "quantity",
                    "quantity_per_item": "quantity"
                }

                # Get the pattern name for this slot
                pattern_name = pattern_mappings.get(slot_name, slot_name)

                # Use entity patterns from JSON to extract values
                if pattern_name in self.entity_patterns:
                    patterns = self.entity_patterns[pattern_name]
                    for pattern in patterns:
                        if pattern in text:
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
