# AWS Certified AI Practitioner – Core Overview

Use this file as your Stage 0–4 compass. Each section mirrors the order you should learn so you never wonder "what now?".

## Stage Anchors at a Glance
| Stage | When to read this section | Files to pair with | Proof of progress |
| --- | --- | --- | --- |
| 0 | Day 1 orientation | `README.md`, this intro | Snapshot the exam facts from memory |
| 1 | Same day, after glossary | `mistakes/` log template | 3-line "still confused" list filed |
| 2 | After service flashcards unlock | `notes/ai-practitioner/services-comparison.md` | Build 6-row service fit table |
| 3 | When Bedrock vs SageMaker starts to blur | `notes/ai-practitioner/service-decision-matrix.md`, `diagrams/` | Draw decision ladder or bullet summary |
| 4 | Once you can name Guardrails/Clarify | `notes/ai-practitioner/responsible-ai-checklist.md` | Guardrail checklist draft |
| 5 | During every practice loop | `practice-tests/`, `mistakes/` | Logged rationale for last 5 Qs |

---

## Stage 0 – Orientation Snapshot (10 minutes)
- **Exam basics:** 65 questions · 90 minutes · score range 100–1000 · pass at 700. Say it aloud so it sticks.
- **Domain weights:** AI/ML Concepts 24%, AWS AI Services 38%, Implementation/Ops 20%, Responsible AI 18%. Visual cue: **"24-38-20-18" → looks like a descending staircase.**
- **Mindset:** Target 85% on practice, tag every miss inside `mistakes/DATE-topic.md`, and keep loops short.
- *Scenario spark:* "Learning lead must brief execs on exam format in a stand-up." If you can answer without notes, you own Stage 0.

## Stage 1 – Core Concepts + Responsible AI Basics (Half Day)
- **Plain-language ladder:** AI (goal) → ML (learning using data) → DL (neural nets handling unstructured data).
- **Learning types cheat:** *Supervised = labeled answers, Unsupervised = find patterns, Reinforcement = feedback loop.*
- **Metrics mantra:** Classification → Accuracy/F1, Regression → RMSE/MAE, Forecasting → MAPE, Imbalanced → Precision/Recall, GenAI → human review + safety note.
- **Workflow story:** Business goal → data prep → feature engineering → train/tune → evaluate → deploy → monitor → retrain. Mention the order when a question says "first" or "next".
- **Responsible AI starter:** Remember **"Plan → Protect → Prove"** (policy, Guardrails/Clarify, monitoring + A2I). Note it inside your Stage 1 mistake log.
- *Scenario:* "Healthcare chatbot must redact PHI and explain answers" → Guardrails + Clarify + Model Monitor + A2I. If that flow feels smooth, move to Stage 2.

## Stage 2 – Managed AI API Ladder (Half Day)
- **Rule:** Default to the simplest managed API before escalating.
- **Grouped cheat sheet:**
  - *Vision:* Rekognition = moderation/labels; Textract = OCR/structured forms.
  - *Text:* Comprehend = sentiment/entities/PII; Translate = language swap; Kendra = semantic search.
  - *Speech:* Transcribe = speech→text; Polly = text→speech; Lex = conversational bot melding ASR + Lambda; memory trick **"Talk → Text → Think → Talk"** (Lex captures, Transcribe logs, Comprehend interprets, Polly replies).
  - *Docs:* Textract → Comprehend → Bedrock (if summarizing) is the safe order.
- **Action:** Fill the 6-row table described in your study flow using `notes/ai-practitioner/services-comparison.md` plus this section.
- **Trap radar:** Translate ≠ Comprehend (translation vs sentiment); Rekognition ≠ Textract (images vs documents). Bold these in your table.
- *Scenario:* "Need to moderate user images now" → Rekognition moderation before any Bedrock custom idea.

## Stage 3 – Bedrock vs SageMaker vs Managed APIs (Half Day)
- **Decision ladder (memorize the yes/no path):**
  1. *Can a named API solve it?* → Use Rekognition, Textract, Comprehend, etc.
  2. *Need GenAI without servers?* → Amazon Bedrock + Guardrails, optionally Agents + Knowledge Bases for RAG.
  3. *Need full ML control or custom training?* → Amazon SageMaker (Studio, Pipelines, Autopilot, Canvas, Feature Store, Model Registry).
- **Memory hook:** **"API → Bedrock → Builder"** = easiest to hardest.
- **Exam trap:** Picking SageMaker for a rapid GenAI pilot when Bedrock already meets needs, or forgetting Bedrock Guardrails only moderate prompts/responses (not dataset labeling—that’s Ground Truth).
- **Action:** Sketch the decision tree described in Stage 3 and paste/commit it under `diagrams/`.
- *Scenario:* "Marketing wants a branded chatbot without managing GPUs" → Bedrock Agents + Guardrails wins.

## Stage 4 – Responsible Workflow Toolkit (2–3 hours)
- **Guard the flow:** Guardrails (prompt/content filters) → Clarify (bias/explain) → Model Monitor (drift) → A2I (human review) → CloudWatch/IAM for audit.
- **Supporting cast:** Ground Truth (annotation), Feature Store (shared features), Data Wrangler (visual prep inside Studio), Model Registry (approvals), QuickSight Q (exec NL BI), Panorama (edge CV) — reference `notes/ai-practitioner/service-decision-matrix.md` for cues.
- **Checklist reminder:** Build `notes/ai-practitioner/responsible-ai-checklist.md` with Step, Tool, Why, Evidence; cite this overview for definitions.
- **Trap:** Guardrails protect Bedrock flows; Model Monitor watches SageMaker endpoints. Mention both when the question references "runtime toxic output".
- *Scenario:* "Contact center bot returns toxic summaries" → update Guardrails block list, review Model Monitor metrics, escalate via A2I.

## Stage 5 – Daily Practice Loop (Forever)
1. Flashcards for yesterday’s weakest tag (Core Concepts → Service Fit → Responsible AI).
2. Re-read only the note section tied to a recent miss (use headings in this file + `notes/ai-practitioner/services-comparison.md`).
3. Answer 5–10 practice questions. For Stage 1 learners use Test 01 Section A; Stage 2 go to Section B, etc. (see `practice-tests/test-01.md` for stages).
4. Log: `Question → Wrong pick → Correct reasoning → Trigger word` inside `mistakes/DATE-topic.md`.
5. Upgrade flashcards or diagrams when the same confusion appears twice.

Lock in these staged checkpoints before opening deep SageMaker labs. Clarity beats coverage—advance only when each scenario here feels boringly easy.
