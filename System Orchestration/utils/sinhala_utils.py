"""
Sinhala Language Utilities
Handles Sinhala keyword mapping, numeral conversion, and mixed language support
"""

# Sinhala keyword mappings for intents
SINHALA_KEYWORDS = {
    "start_order": [
        "ඉල්ලුම්",  # order/illum
        "ඔර්ඩර්",   # order (English phonetic)
        "කරන්න",    # do/place
        "ඇණවුම්",   # order
        "පිටුවන්න",  # order
        "ගන්න",     # take/get
        "කිනුවන්න",  # buy
    ],
    "view_menu": [
        "මෙනුව",    # menu
        "න්‍යාපිතය", # food list
        "කෝටි",     # categories
        "කොටස්",    # sections
        "ඉතාමත්",   # items
    ],
    "view_menu_category": [
        "බර්ගර්",   # burger
        "පීසා",     # pizza
        "දෙමුතු",   # sides
        "බාල්දිමේ", # bucket
        "බකට්",     # bucket (English)
        "කෝටිය",    # category
    ],
    "view_menu_item": [
        "විස්තරය",   # details
        "ගැන",      # about
        "කුමක්ද",    # what is
        "මිල",      # price
        "පිරිසම",    # type/kind
    ],
    "view_promotions": [
        "ඉඩ",       # offer/deal
        "පිණිස",    # promotion
        "මිල".replace("", ""), # discount
        "ශුන්‍ය",    # discount
        "විශේෂ",     # special
    ],
    "view_locations": [
        "ස්ථානය",   # location
        "ඉවුරු",     # store/shop
        "දුර",      # distance/near
        "පිහිටීම",   # location
    ],
}

# Numeral conversion (Arabic to Sinhala)
ARABIC_TO_SINHALA_NUMERALS = {
    '0': '0',  # zero (same in both)
    '1': '1',  # one
    '2': '2',  # two
    '3': '3',  # three
    '4': '4',  # four
    '5': '5',  # five
    '6': '6',  # six
    '7': '7',  # seven
    '8': '8',  # eight
    '9': '9',  # nine
}

# Sinhala translations for common responses
SINHALA_TRANSLATIONS = {
    "📋 Our Menu": "📋 අපගේ මෙනුව",
    "Burgers": "බර්ගර්",
    "Buckets": "බකට්",
    "Sides": "දෙමුතු",
    "Promotions available": "ප්‍රවර්ධන ලබා ගත හැකිය",
    "Our menu is currently being updated": "අපගේ මෙනුව දැනට යාවත්කාලීන කරන ලදී",
    "Please check back later": "පසුව නැවත පරීක්ෂා කරන්න",
    "Please specify which category": "කුම කෝටිය තිබේ ඒ කියන්න",
    "Sorry, we don't have a": "ඉන්දිය, අපට නැත",
    "category": "කෝටිය",
    "is currently empty": "දැනට හිස් ය",
    "Please specify which item": "කුම ඉතාමතෙක් තිබේ ඒ කියන්න",
    "Sorry, we don't have": "ඉන්දිය, අපට නැත",
    "on our menu": "අපගේ මෙනුවේ",
    "order started": "ඉල්ලුම ආරම්භ",
    "Order started": "ඉල්ලුම ආරම්භ කරන ලදි",
    "You want": "ඔබ අවශ්‍ය කරන්නේ",
    "Order type": "ඉල්ලුම් වර්ගය",
    "Processing your order": "ඔබගේ ඉල්ලුම ක්‍රියාවලිය කරමින් ඇත",
    "Quantity": "ප්‍රමාණය",
    "I need some information": "මට තොරතුරු අවශ්‍ය ය",
    "Could you provide those details": "ඒ විස්තර ලබා දිය හැකිද",
    "No current promotions": "දැනට ප්‍රවර්ධන නැත",
    "Location information is currently being updated": "ස්ථාන තොරතුරු දැනට යාවත්කාලීන කරන ලි",
    "Our Locations": "අපගේ ස්ථාන",
    "Cached menu from RAG store": "RAG ගබඩා වලින් ගබඩා කරන ලද මෙනුව",
}

def convert_numerals_to_sinhala(text):
    """Convert Arabic numerals to Sinhala numerals"""
    result = text
    for arabic, sinhala in ARABIC_TO_SINHALA_NUMERALS.items():
        result = result.replace(arabic, sinhala)
    return result

def detect_sinhala_content(text):
    """
    Detect if text contains Sinhala script.
    Returns True if Sinhala characters are detected.
    """
    # Sinhala Unicode ranges: U+0D80 to U+0DFF
    for char in text:
        if '\u0D80' <= char <= '\u0DFF':
            return True
    return False

def has_mixed_language(text):
    """Check if text has both Sinhala and English content"""
    has_sinhala = detect_sinhala_content(text)
    has_english = any(char.isalpha() and ord(char) < 128 for char in text)
    return has_sinhala and has_english

def extract_sinhala_words(text):
    """Extract Sinhala words from mixed text"""
    sinhala_words = []
    current_word = ""
    for char in text:
        if '\u0D80' <= char <= '\u0DFF' or char in " \t\n":
            if current_word:
                sinhala_words.append(current_word)
                current_word = ""
            if char not in " \t\n":
                current_word += char
        else:
            current_word += char
    if current_word:
        sinhala_words.append(current_word)
    return sinhala_words

def get_sinhala_keywords_for_intent(intent_name):
    """Get all Sinhala keywords for a specific intent"""
    return SINHALA_KEYWORDS.get(intent_name, [])

def translate_response_to_sinhala(english_response):
    """
    Translate common English phrases to Sinhala in response.
    Keeps English words like pizza, burger, delivery as-is.
    """
    result = english_response
    
    # Apply translations but preserve English food names and technical terms
    english_preserves = ["pizza", "burger", "bucket", "fries", "delivery", "dine-in", "takeout"]
    
    for english, sinhala in SINHALA_TRANSLATIONS.items():
        result = result.replace(english, sinhala)
    
    # Restore preserved English words if they were accidentally translated
    for word in english_preserves:
        if word.lower() not in result.lower():
            # Re-add if it was in original
            if word in english_response.lower():
                result = result.replace(word.lower(), word)
    
    return result

def format_sinhala_response(response_text):
    """
    Format response for Sinhala output:
    1. Translate common phrases to Sinhala
    2. Convert numerals to Sinhala
    3. Keep English food names and technical terms
    """
    # Step 1: Translate phrases
    translated = translate_response_to_sinhala(response_text)
    
    # Step 2: Convert numerals
    with_numerals = convert_numerals_to_sinhala(translated)
    
    return with_numerals
