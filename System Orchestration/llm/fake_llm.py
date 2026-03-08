"""
Dummy LLM module - generates natural responses for slot-filling prompts
In production, would use OpenAI, Claude, LLaMA, etc.
"""


class FakeLLM:
    """
    Dummy LLM that generates responses based on templates.
    In real implementation, would call actual LLM API (OpenAI, Hugging Face, etc.)
    """
    
    def __init__(self):
        self.response_templates = {
            "item_name": [
                "I'd like to know - which item are you interested in? We have pizzas, burgers, and more.",
                "Which item would you like to order?",
                "Tell me - are you looking for a pizza, burger, or something else?",
            ],
            "category": [
                "Perfect! Which category interests you - burgers, sides, or buckets?",
                "What category would you like to explore?",
                "Would you like to browse our burgers, sides, or special buckets?",
            ],
            "location_query": [
                "Which location are you looking for? We have branches downtown, at the mall, and near the airport.",
                "Where would you like to find a store?",
                "Are you looking for a specific area or location?",
            ],
            "order_items": [
                "Great! What items would you like to add to your order?",
                "What items would you like to order?",
                "Please tell me what you'd like to order.",
            ],
        }
    
    def generate(self, prompt_dict):
        """
        Generate a response given a prompt dictionary.
        
        Args:
            prompt_dict: {
                "intent": str,
                "slots": dict,
                "missing": list of missing slot names,
                "message": str
            }
        
        Returns:
            str: Generated response
        """
        missing = prompt_dict.get("missing", [])
        
        if not missing:
            return "All information received. Processing your request..."
        
        # Get response template for the first missing slot
        first_missing = missing[0] if missing else None
        
        if first_missing and first_missing in self.response_templates:
            import random
            responses = self.response_templates[first_missing]
            return random.choice(responses)
        
        # Fallback generic response
        return f"I need some information: {', '.join(missing)}. Could you provide those details?"
