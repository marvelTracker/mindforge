# Flashcard Addition Workflow

Use this playbook whenever you add or refresh cards so every deck stays focused, beginner-friendly, and aligned with the current learning track.

## Standard Process
1. **Pick the skill gap:** Review the latest misses in `mistakes/` and identify the weakest topic (e.g., Bedrock fine-tuning). This keeps additions laser-focused on actual needs.
2. **Collect trusted source notes:** Pull concise bullets from AWS docs or internal notes, then simplify wording into beginner-ready language before drafting cards.
3. **Draft with the template (below):** Feed the Codex prompt with topic, question style, and traps to avoid; let it output structured CSV rows.
4. **Validate schema + tone:** Ensure every row includes `id`, `question`, `answer`, `topic`, and (optionally) `difficulty`. Leave the `id` blank if you want the trainer to assign a UUID, or paste a generated UUIDv4 if you are scripting the CSV yourself.
5. **Check duplicates/conflicts:** Search existing CSVs inside the target certification folder and remove or merge overlaps so learners are not drilled twice on the same fact.
6. **Save + document:** Place the CSV in the correct certification folder under `flashcards/`, update `README.md` if you introduce a new deck, and note study order guidance inside the matching `notes/<certification>/` folder when needed.
7. **Test in trainer:** Run `python3 flashcards/flashcard_trainer.py --certification "<certification>" --topics "<topic>" --limit 5` to ensure topic detection, difficulty display, and study flow work.

Memory trick: Think “**Capture → Craft → Check → Coach**” (collect material, craft cards, check schema, coach via trainer) to keep the workflow quick.

## Reusable Codex Prompt Template
```
You are a curriculum designer + study coach for a personal learning system.
Goal: generate flashcards for the <TOPIC_NAME> topic in the <CERTIFICATION_NAME> track.
Constraints:
- Format output as CSV rows with columns id,question,answer,topic[,difficulty]. Leave the `id` field blank (`,,`) if you want the trainer to auto-fill UUIDs on save.
- Use plain, exam-focused wording, 1 idea per card.
- Highlight traps where services look similar.
- Provide short scenario-style questions when relevant.
Topic details: <paste distilled notes or recent misses>
Number of cards needed: <N>
Difficulty guidance: easy = definition/single fact, medium = comparison/process/cost, hard = nuanced RL/distillation/pricing/judge model reasoning.
Return only CSV rows; do not include backticks.
```

## Required Schema
| Column | Required | Notes |
| --- | --- | --- |
| `id` | Yes | Stable UUIDv4 string per card. Leave blank while drafting and the trainer will assign + persist it automatically. |
| `question` | Yes | Write in plain language, focus on one concept, and call out context (e.g., “Where must Bedrock fine-tuning data live?”). |
| `answer` | Yes | Short, concrete phrasing that a beginner can read aloud; include AWS service names explicitly. |
| `topic` | Yes | Follows the naming rules below (kebab-case, exam domain specific). |
| `difficulty` | Optional | Accepts `easy`, `medium`, or `hard`. Leave blank to let the trainer auto-assign. |

CSV tips:
- Keep commas inside quotes.
- UTF-8 encoding only.
- When appending to combined decks, maintain alphabetical ordering by topic to reduce merge conflicts.

## Topic Naming Rules
- Use lowercase kebab-case (e.g., `bedrock-model-tuning`, `governance-guardrails`).
- Names should map directly to a study slice from `notes/` or the exam blueprint.
- Avoid vague tags like `misc` or `general`; instead, spell out the AWS service or scenario focus.
- When introducing a new topic, mention it once in `README.md` so learners know it exists.

## Difficulty Auto-Assignment Rules
The trainer enforces these heuristics when `difficulty` is omitted:
- **Easy:** direct definitions, single-fact recall, straightforward “What is…?” service identification.
- **Medium:** comparisons, process flows, cost/usage trade-offs, multi-step explanations (trigger words like “why/how/when/where” or “trade-off”).
- **Hard:** reinforcement learning, reward functions, judge/distillation language, nuanced pricing mode choices, scenario reasoning that weighs two or more services.

If the auto-label feels off, set the `difficulty` column manually—otherwise the heuristic keeps things consistent without extra work.

## Duplicate Handling Rules
- Before saving, search for matching or similar questions inside the track folder: `rg -n "fine-tuning" flashcards/ai-practitioner/*.csv`.
- Deduplicate by either removing the new row or rephrasing it to highlight a different exam trap.
- When the concept is necessary twice (e.g., responsible AI vs. governance views), adjust the question framing and topic tag so the intent differs clearly.
- After edits, rerun the trainer to confirm only one card per intent appears under each topic.

## Example: bedrock-model-tuning
1. **Context:** Missed several questions about Bedrock fine-tuning storage and pricing.
2. **Prompt Input (summary):** Use the template with notes covering S3 data location, supervised vs. reinforcement workflows, and inference billing models.
3. **CSV Row Output:**
   ```
   "a507388fd3664977939e32fae1849c4b","Where must the training data for Bedrock fine-tuning be stored?","The training data must be stored in Amazon S3.","bedrock-model-tuning","Medium"
   ```
4. **Trainer Test:** `python3 flashcards/flashcard_trainer.py --certification ai-practitioner --topics bedrock-model-tuning --limit 3`
5. **Documentation:** Mention the new deck in `README.md` under Flashcard Trainer CLI so students know to target it next.

Likely exam trap to highlight in this topic: mixing on-demand inference with provisioned throughput pricing—always spell out both models inside at least one hard card.
