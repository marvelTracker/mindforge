# mindforge

mindforge is a personal learning system and flashcard engine.

The current repo structure stays as-is and currently includes the existing AI Practitioner and ML Engineer Associate tracks.

## Current Layout

- AI Practitioner flashcards: `flashcards/ai-practitioner/`
- AI Practitioner notes: `notes/ai-practitioner/`
- AI Practitioner progress: `progress/ai-practitioner/`
- ML Engineer Associate flashcards: `flashcards/ml-engineer-associate/`
- ML Engineer Associate notes: `notes/ml-engineer-associate/`
- ML Engineer Associate progress: `progress/ml-engineer-associate/`

Current tracks:

- `ai-practitioner`
- `ml-engineer-associate`

## Flashcard Trainer

Script: `flashcards/flashcard_trainer.py`

Dependencies:

- Python 3.9+
- Optional: `colorama` for colored terminal output

How to run:

```bash
python3 flashcards/flashcard_trainer.py
```

Example commands:

```bash
python3 flashcards/flashcard_trainer.py
python3 flashcards/flashcard_trainer.py --certification ai-practitioner --topics bedrock-model-tuning --limit 10
python3 flashcards/flashcard_trainer.py --certification ml-engineer-associate
```

Expected output:

```text
Available certifications:
1. AI Practitioner
2. ML Engineer Associate
Choose a number: 1
```

How certification selection works:

1. The trainer first asks you to choose a certification track.
2. It loads topics only from that certification’s flashcard folder.
3. It writes progress only to that certification’s progress folder.
4. After track selection, the existing topic menu, study modes, scoring, and progress behavior continue as before.

Study modes preserved for AI Practitioner:

- Standard
- Incorrect-only
- Weak-cards
- Review-again
- Newly added

## Notes

AI Practitioner study notes live under `notes/ai-practitioner/`.

ML Engineer Associate study notes live under `notes/ml-engineer-associate/`.

## Practice Tests

The practice test quiz remains unchanged:

```bash
python3 practice_tests_quiz.py
```
