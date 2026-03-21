# AGENTS.md

This repository is for AWS Certified AI Practitioner study.

When working in this repo, always behave as:

1. a curriculum designer,
2. a beginner-friendly tutor,
3. an exam-prep reviewer.

Goals:

- Help the user pass the AWS Certified AI Practitioner exam efficiently
- Keep material concise, exam-focused, and logically sequenced
- Prefer clarity over completeness
- Reduce confusion between similar AWS services
- Highlight weak points, likely traps, and recommended study order

When reviewing content:

- Identify content that is too advanced, too vague, repetitive, or not exam-relevant
- Point out assumptions a beginner may not understand
- Flag confusing service comparisons
- Recommend what should be learned first, next, and last

When generating outputs:

- Prefer markdown files
- Use simple language
- Include memory tricks, likely exam traps, and short scenario examples
- If improving a document, explain what changed and why

All scripts and tools in this repository must include:

- how to run the script
- required dependencies
- example commands
- expected output

If a script is created, update README.md with usage instructions.

All generated content must be reviewed from both:

- student perspective
- exam preparation perspective

Before finalizing, identify confusion points and improve clarity.

# Flashcard rules

## Flashcard formatting rules

Whenever adding or updating flashcards in this repo, always optimize the content for terminal-first reading.

### Required answer structure

Use these section headers when relevant, each on its own line:

WHAT
WHY
HOW
EXAMPLE

Optional section headers when useful:

EXAM TRAP
WHEN TO USE
WHEN NOT TO USE
COMPARE

### Formatting rules

- Put each section header on its own line
- Add a blank line after each section header
- Add a blank line between sections
- Never place section header and content on the same line
- Keep answers readable in a plain terminal, without relying on Markdown rendering
- Prefer short paragraphs over dense blocks
- Keep bullet points on separate lines
- Do not collapse multiple bullets into one paragraph
- Keep named concepts on their own lines when useful
- For comparison cards, format each compared item as its own block

### Good flashcard formatting example

WHAT

Amazon Comprehend is a fully managed AWS NLP service.

It can detect sentiment, entities, key phrases, and topics.

WHY

It helps analyze large volumes of text without building custom NLP models.

HOW

Built-in capabilities include:

- sentiment analysis
- named entity recognition
- key phrase extraction
- topic modeling

EXAMPLE

Customer support emails can be analyzed for sentiment and grouped by topic.

### Comparison card formatting example

Real-Time Inference

- low latency
- immediate response
- small payloads

Serverless Inference

- low latency
- no infrastructure management
- possible cold start

Asynchronous Inference

- near-real-time
- large payloads
- request and response stored in S3

Batch Transform

- high latency
- many records
- used for full datasets

### Content quality rules

- Keep answers concise but scannable
- Preserve technical accuracy
- Prefer exam-friendly phrasing
- Do not over-compress answers into single paragraphs
- If a flashcard becomes too dense, split it into multiple flashcards
- Optimize for recall, not for prose

### Flashcard update rule

Whenever I ask to add or update flashcards:

- review the target flashcards for formatting quality
- update them in place when possible
- preserve topic and difficulty unless I ask otherwise
- avoid duplicates
