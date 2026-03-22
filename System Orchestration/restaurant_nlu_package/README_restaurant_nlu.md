
# Restaurant NLU package

This package gives you a strong starter architecture for a restaurant assistant:

- `schema.py`:
  - normalized slot and intent definitions
  - required vs optional vs priority slots
- `patterns.py`:
  - lexicon values
  - EntityRuler patterns
  - intent example utterances
  - synonym maps
- `normalizers.py`:
  - canonicalization of slot values
- `extractor.py`:
  - spaCy pipeline
  - EntityRuler extraction
  - regex extraction
  - free-text fallback
  - heuristic intent routing
- `dialogue.py`:
  - stateful conversation manager
  - follow-up question generation
- `run_demo.py`:
  - example runner

## Install

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

## Run

```bash
python run_demo.py
```

## Accuracy notes

This code is designed for high controllability and strong early accuracy, not for fully open-domain understanding.
To increase accuracy further:

1. expand `LEXICON`
2. add Sinhala variants and transliterated variants
3. improve intent examples
4. add slot-specific regexes
5. add a trained intent classifier after you collect data
6. add a date/time normalizer such as `dateparser`
7. connect the action layer to real APIs
