# AWS AI Service Decision Matrix

## Amazon Bedrock
- **What it does:** Managed access to multiple foundation models plus Guardrails, Agents, and Knowledge Bases for GenAI apps.
- **Use when:** You need text/image/embedding generation quickly with governance controls and no infrastructure management.
- **Avoid when:** You must train highly customized models from scratch or run workloads fully offline; choose SageMaker instead.
- **Exam traps:** Confusing Bedrock with SageMaker for classical ML; forgetting Guardrails handle moderation, not dataset labeling.
- **Scenario:** Product team prototypes a multilingual chatbot using Anthropic Claude via Bedrock and adds Guardrails to block PII leakage.

## Amazon SageMaker
- **What it does:** End-to-end platform for building, training, tuning, and deploying custom ML models.
- **Use when:** You need full control over data, algorithms, pipelines, or want to operationalize bespoke models at scale.
- **Avoid when:** A pre-trained API already solves the problem or GenAI via Bedrock meets requirements; don’t overbuild.
- **Exam traps:** Picking SageMaker for simple OCR or sentiment tasks that a managed API handles better; ignoring cost/ops overhead.
- **Scenario:** Data scientists train a churn model using SageMaker Studio notebooks, Pipelines, and Model Monitor for drift alerts.

## SageMaker Canvas
- **What it does:** No-code AutoML interface inside SageMaker for business analysts.
- **Use when:** Non-technical users must build quick tabular predictions or share insights without writing code.
- **Avoid when:** Deep customization, advanced feature engineering, or unsupported data types are required.
- **Exam traps:** Mixing up Canvas (no-code) with Studio (full IDE) or Autopilot (automated training under the hood).
- **Scenario:** A finance analyst imports historical transactions into Canvas to forecast monthly revenue without coding.

## SageMaker Ground Truth
- **What it does:** Managed data-labeling service with human workforces and active learning.
- **Use when:** You require scalable, auditable annotation workflows for images, text, or video before training models.
- **Avoid when:** Labels already exist or you only need lightweight reviewers; don’t add extra cost/latency.
- **Exam traps:** Assuming Ground Truth improves model quality itself—it only creates labeled datasets.
- **Scenario:** A computer vision team labels vehicle damage photos via Ground Truth with private contractors.

## Amazon Rekognition
- **What it does:** Pre-trained computer vision API for image and video analysis (labels, faces, moderation, text).
- **Use when:** You need instant object/facial/moderation detection without training.
- **Avoid when:** You must classify highly specialized objects requiring proprietary training—then use SageMaker CV pipelines.
- **Exam traps:** Thinking Rekognition performs OCR everywhere (Textract handles documents) or handles audio.
- **Scenario:** A social media startup scans user uploads for violence using Rekognition Moderation API before publishing.

## Amazon Comprehend
- **What it does:** NLP service for sentiment, entities, key phrases, PII detection, topic modeling.
- **Use when:** You need text analytics quickly or want to build custom classifiers/entities with minimal setup.
- **Avoid when:** Complex summarization/generative writing is required (use Bedrock) or you must process speech/audio directly.
- **Exam traps:** Mixing up Comprehend with Translate (language conversion) or Textract (document OCR).
- **Scenario:** Support team runs Comprehend on tickets to auto-route negative sentiment cases to escalation queues.

## Amazon Transcribe
- **What it does:** Automatic speech-to-text for batch or streaming audio with custom vocabulary and channel features.
- **Use when:** You need transcripts, subtitles, or call analytics from audio/video sources in near real-time.
- **Avoid when:** Goal is text-to-speech (Polly) or translation (Translate); it only outputs text from audio.
- **Exam traps:** Forgetting to mention encryption/compliance for call recordings; confusing streaming vs. batch modes.
- **Scenario:** Contact center streams calls to Transcribe, then pipes transcripts into Comprehend for sentiment tagging.

## Amazon Polly
- **What it does:** Text-to-speech service with neural voices, lexicons, and speech marks.
- **Use when:** Applications require lifelike audio (IVR prompts, accessibility content, e-learning narration).
- **Avoid when:** Task is speech recognition or translation; Polly does not understand input audio.
- **Exam traps:** Mixing Polly with Lex roles (Lex handles conversation logic, Polly just speaks) or ignoring per-character pricing.
- **Scenario:** Training app converts lesson text to multiple languages using Polly neural voices for offline listening.

## Amazon Translate
- **What it does:** Neural machine translation for real-time or batch text conversion with Custom Terminology.
- **Use when:** You must localize content, chats, or documents across many languages quickly.
- **Avoid when:** Use cases need deep text understanding (sentiment/entity) or speech recognition; combine with Comprehend/Transcribe instead.
- **Exam traps:** Forgetting Custom Terminology for brand words; assuming it handles document layout (use Textract first).
- **Scenario:** Global support chat pipeline detects language, translates messages via Translate, and returns localized replies instantly.

## Amazon Lex
- **What it does:** Conversational AI for chatbots/IVR combining ASR and NLU with Lambda integration.
- **Use when:** You need multi-turn dialog with slot elicitation, voice or text channels, and backend fulfillment.
- **Avoid when:** Only narration is needed (Polly) or you want open-ended GenAI responses without dialog management (Bedrock).
- **Exam traps:** Forgetting Lex requires integration for responses (e.g., Connect or custom UI); mixing up with Contact Lens analytics.
- **Scenario:** Retailer builds a returns bot in Lex that captures order numbers and invokes Lambda to create shipping labels.

## Amazon Textract
- **What it does:** Intelligent document processing (IDP) extracting text, tables, and form data from scanned files.
- **Use when:** You must digitize PDFs, forms, or handwriting before downstream NLP/analytics.
- **Avoid when:** Source is native digital text (no OCR needed) or you only need key phrases/sentiment (Comprehend).
- **Exam traps:** Assuming Textract understands context/sentiment; it outputs structured text, not analysis.
- **Scenario:** Insurance company reads claim forms via Textract, stores results in DynamoDB, then routes to underwriters.

## Amazon Kendra
- **What it does:** Intelligent enterprise search service with connectors, relevance tuning, and semantic ranking.
- **Use when:** Employees need natural language search over manuals, FAQs, or repositories, potentially feeding GenAI answers.
- **Avoid when:** Small datasets can be handled by DynamoDB queries or when generative QA via Bedrock Knowledge Bases already meets needs.
- **Exam traps:** Confusing Kendra with OpenSearch indexing, or assuming it auto-generates answers without content sources.
- **Scenario:** Support portal uses Kendra to index PDFs and SharePoint content, surfacing precise answers to technician questions.
