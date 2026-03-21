# Common Confusion Points & Memory Boosters

Use this file whenever a practice question or flashcard feels fuzzy. Each section lists the trap, how to decide quickly, and a tiny scenario so you can rehearse exam wording.

## Vision vs. Documents vs. Text
| Trap | Remember | Scenario Cue |
| --- | --- | --- |
| Rekognition vs. Textract | **Rekognition sees pixels**, handles images/videos for labels, faces, moderation. **Textract reads documents**, pulling text, tables, key-value pairs. | “Moderate user selfies before posting” → Rekognition Moderation. “Digitize insurance form PDFs” → Textract AnalyzeDocument + Comprehend. |
| Textract vs. Comprehend | Textract extracts text; Comprehend interprets it (sentiment, PII, key phrases). | “Need JSON of handwritten claim numbers” → Textract. “Need to auto-route negative claims” → Comprehend Sentiment. |
| Comprehend vs. Translate | Translate swaps language quickly; Comprehend mines meaning. | “Real-time chat translation” → Translate + Custom Terminology. “Find PHI in translated chat logs” → Comprehend PII API. |

## Speech & Conversation Ladder
Memory trick: **“Talk → Text → Think → Talk”**
- **Lex** captures the conversation and controls slots/Lambda hooks.
- **Transcribe** turns speech/audio into text with timestamps.
- **Comprehend** interprets transcripts.
- **Polly** speaks back with neural voices.
Scenario: “Call center wants IVR that collects account IDs, reads answers aloud, stores transcripts, and flags angry calls.” Flow: Lex (bot) → Transcribe (logs) → Comprehend (sentiment) → Polly (voice backs).

## QuickSight vs. QuickSight Q
| Need | Service | Memory Hook |
| --- | --- | --- |
| Build dashboards, schedule emails, embed visuals | Amazon QuickSight | “Dashboards & visuals.” |
| Ask natural-language business questions like “Which region won Q4?” | Amazon QuickSight Q | “Q = Questions.” |
Exam trap: Practice Test 02 Q16 expects you to jump to QuickSight Q even if Stage 2 hasn’t mentioned it yet—review this section before tackling Test 02.

## Data Prep: DataBrew vs. Data Wrangler
| Feature | AWS Glue DataBrew | SageMaker Data Wrangler |
| --- | --- | --- |
| Audience | Analysts needing drag-and-drop cleaning on CSV/Parquet | Data scientists already inside SageMaker Studio |
| Output | Glue Jobs, S3 outputs, share to downstream analytics | Feature engineering flows into SageMaker Pipelines/endpoints |
| Exam clue | Mentions AWS Glue, CSV grooming, no ML context | Talks about SageMaker Studio panels, joins, feature stores |
Scenario: Practice Test 02 Q23 describes merchandising analysts “drag-and-dropping CSVs” → DataBrew, not Data Wrangler.

## GenAI Escalation: Managed API → Bedrock → SageMaker
Decision ladder (say it every time): **Managed API first, Bedrock when you need FM flexibility, SageMaker only when you must own training.**
- Managed APIs (Rekognition, Textract, Comprehend, Kendra) → zero training, fastest answer.
- **Amazon Bedrock** → pick FM, add Guardrails, optionally Agents/Knowledge Bases for RAG.
- **Amazon SageMaker** → fine-tune bespoke models, run pipelines, add Model Monitor/Clarify.
Scenario spark: “Need branded chatbot this week without GPUs” → Bedrock Agents + Guardrails. “Need to train a churn XGBoost with custom features” → SageMaker Studio + Pipelines.

## Responsible AI Checklist (Plan → Protect → Prove)
1. **Plan** – Define policies, data lineage, evaluation metrics. Mention CloudTrail + tagging. (Link to `notes/ai-practitioner/aws-ai-overview.md` Stage 1.)
2. **Protect** – Apply Guardrails (prompt/content filters), Clarify (bias/explainability), encryption at rest/in transit.
3. **Prove** – Monitor with Model Monitor, escalate with Amazon A2I, capture logs in CloudWatch/S3, report via QuickSight dashboards.
Action: copy these rows into your mistakes log whenever you miss a governance question.

## AI/ML Lifecycle Cheat Sheet
| Step | Tools to Name | Exam Trigger |
| --- | --- | --- |
| Data prep | Glue, DataBrew, Data Wrangler, Ground Truth | “Messy CSVs,” “need labeling,” “analyst-friendly prep.” |
| Train/tune | SageMaker Studio/Autopilot/JumpStart | “Need notebooks,” “AutoML,” “custom algorithm.” |
| Deploy | SageMaker endpoints, Bedrock invocations | “Need managed endpoint,” “foundation model API.” |
| Monitor | Model Monitor, CloudWatch, Guardrails, A2I | “Detect drift,” “moderate toxic output,” “route human review.” |
| Iterate | Update features via Feature Store, rerun Data Wrangler → Pipelines | “Need faster retraining cadence.” |

## Scenario Patterns to Memorize
- **QuickSight Q vs. Amazon Q Business:** Q = NL dashboard questions; Amazon Q Business = GenAI chat over enterprise data.
- **AWS Panorama vs. Rekognition Custom Labels:** Panorama = on-prem appliance using existing cameras when cloud connectivity is limited; Rekognition = cloud API/Custom Labels when uploading media is fine.
- **Translate Custom Terminology vs. Polly Lexicons:** Translate handles text translation; use Custom Terminology to lock product slogans. Polly uses lexicons to control pronunciation when reading text.
- **Knowledge Bases vs. Kendra:** Knowledge Bases (Bedrock) = managed RAG ingestion + embeddings feeding FM answers. Kendra = semantic search returning ranked documents; pair them when you need grounded GenAI.

Whenever you miss a question, add a “Trigger word” row here so the confusion is documented once instead of scattered through the repo.
