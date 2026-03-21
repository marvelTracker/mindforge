# AWS AI Service Comparison Cheat Sheet

Tie every service back to your current study stage. Stay inside your current stage until each scenario below feels automatic.

| Stage | Service | Use When | Skip When | Memory Hook | Likely Trap |
| --- | --- | --- | --- | --- | --- |
| 2 | **Amazon Bedrock (Intro)** | You need foundation-model text/images/embeddings, Guardrails, Agents, or Knowledge Bases without infrastructure. | You truly must train or host bespoke models yourself—defer to SageMaker later. | *"Bedrock = GenAI API with safety on."* | Thinking Bedrock trains vision models or handles OCR; it only hosts foundation models + governance. |
| 3 | **Amazon SageMaker** | Full ML lifecycle: notebooks, training, tuning, deployment, pipelines, governance. | A managed API or Bedrock already solves the need faster. | *"SageMaker = builder workspace."* | Picking SageMaker for quick OCR/sentiment tasks or ignoring extra ops cost. |
| 2 | **Amazon Rekognition** | Instant object/face/moderation detection in images/videos. | Document OCR or hand-written forms → Textract; needing bespoke classes → SageMaker CV. | *"Rekognition sees pixels."* | Assuming it reads PDFs or audio. |
| 2 | **Amazon Textract** | Extract text, tables, key-value pairs from scans/PDFs before further NLP. | You already have clean digital text or just need sentiment/entities. | *"Textract reads forms."* | Expecting it to summarize/analyze meaning (hand off to Comprehend/Bedrock). |
| 2 | **Amazon Comprehend** | Sentiment, key phrases, entities, PII, custom classifiers/entities over text. | Needs translation (Translate) or audio (Transcribe first). | *"Comprehend understands words."* | Mixing Comprehend vs Translate; forgetting it can redact PII. |
| 2 | **Amazon Transcribe** | Speech→text (batch/streaming, medical, call analytics). | Text→speech (Polly) or open-ended bots (Lex). | *"Transcribe hears voices."* | Not mentioning channel separation/compliance for contact center prompts. |
| 2 | **Amazon Polly** | Text→speech with neural voices, lexicons, speech marks. | Speech recognition or translation tasks. | *"Polly speaks back."* | Ignoring per-character pricing or lexicon support. |
| 2 | **Amazon Translate** | Fast language translation with Custom Terminology for brand terms. | Need deep text analytics (Comprehend) or audio translation (pair with Transcribe). | *"Translate swaps language."* | Forgetting Custom Terminology to lock slogans. |
| 2 | **Amazon Lex** | Multi-turn chat/voice bots with slot elicitation + Lambda fulfillment + Amazon Connect. | Need narration only (Polly) or free-form GenAI (Bedrock). | *"Lex runs the conversation."* | Skipping Lambda/Connect mention in IVR questions. |
| 2 | **Amazon Kendra** | Semantic search across PDFs, SharePoint, Confluence; pair with Bedrock for grounded answers. | Tiny dataset or you only need embeddings (Bedrock Knowledge Bases/OpenSearch). | *"Kendra searches knowledge."* | Assuming it creates content without indexed sources. |
| 4 | **SageMaker Ground Truth** | Large-scale labeling with private/vendor workforces + active learning before model training. | Labels already exist or you just need light review (A2I). | *"Ground Truth labels data."* | Expecting it to improve model accuracy automatically. |
| 4 | **Amazon Augmented AI (A2I)** | Add human review loops to low-confidence predictions. | Data labeling from scratch (Ground Truth). | *"A2I = human safety net."* | Thinking it trains models; it only routes reviews. |
| 4 | **SageMaker Clarify** | Bias + explainability checks (pre/post deployment). | Replacing Guardrails for prompt filtering (different scope). | *"Clarify explains & debiases."* | Mixing Clarify with Model Monitor responsibilities. |
| 4 | **SageMaker Model Monitor** | Detect data/model drift on SageMaker endpoints with alerts. | Guarding Bedrock prompts (use Guardrails). | *"Model Monitor watches live traffic."* | Forgetting to mention CloudWatch alarms or baseline capture. |
| 4 | **SageMaker Feature Store** | Share curated features online/offline across teams. | One-off experiments with no reuse. | *"Feature Store = single source of features."* | Treating it like general object storage. |
| 4 | **SageMaker Data Wrangler** | Visual data prep/joins/quality checks inside Studio before training or Canvas. | Tiny datasets that Excel can handle. | *"Data Wrangler = drag/drop prep."* | Ignoring that it exports pipelines/jobs. |
| 5 | **Amazon QuickSight Q** | Executives ask natural-language BI questions over curated dashboards. | Need ML predictions (use Canvas/SageMaker) or raw SQL queries. | *"QuickSight Q = NL BI."* | Thinking it trains ML models. |
| 6 | **AWS Panorama** | Run computer-vision apps entirely on-prem with existing IP cameras. | Cloud inference or non-vision workloads. | *"Panorama = edge CV appliance."* | Choosing it when latency/cloud connectivity is fine (Rekognition might be easier). |
| 6 | **Amazon OpenSearch Service (Vector engine)** | Managed vector store for RAG/semantic search feeding Bedrock. | Simple keyword search (Kendra might suffice) or you just need embeddings stored in DynamoDB. | *"OpenSearch vectors recall context."* | Forgetting IAM/VPC controls for sensitive embeddings.

### How to Use This Table
- **Stage-first rule:** Only study rows up to your current stage. Highlight the next two services you plan to tackle so focus stays narrow.
- **Trigger words:** Add the “Trigger word to remember” from your mistakes log into the Memory Hook column when you miss a service again.
- **Scenario tie-in:** Copy one scenario per service into `diagrams/` or your personal sheet so practice questions feel familiar.
- **Upgrade path:** When you advance to Stage 4 or higher, append any niche service (QuickSight Q, Panorama) you see on Test 02 so the study flow stays aligned.
