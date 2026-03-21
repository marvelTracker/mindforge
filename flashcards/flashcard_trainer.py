#!/usr/bin/env python3
"""CLI flashcard trainer for AWS certification prep.

Dependencies:
    - Python 3.9+ (uses only csv, argparse, random, pathlib, collections).
How to run:
    $ python3 flashcards/flashcard_trainer.py
Example commands:
    # Pick a certification and drill everything from that track
    $ python3 flashcards/flashcard_trainer.py --limit 10
    # Skip the certification prompt and filter from the CLI
    $ python3 flashcards/flashcard_trainer.py --certification ai-practitioner --topics "bedrock-model-tuning"
Expected output:
    Available certifications:
    1. AI Practitioner
    2. ML Engineer Associate
    Choose a number: 1
    Available topics (25 cards total):
    0. All topics (25 cards)
    1. bedrock-model-tuning (25 cards)
    Choose a number: 1
    Loaded 25 cards for topic 'bedrock-model-tuning'.
    Card 1/25 | Topic: bedrock-model-tuning | Difficulty: Easy
    Q: What is the purpose of fine-tuning a model in Amazon Bedrock?
    (press Enter to reveal the answer...)
    A: Fine-tuning adapts a copy...
    Session score: 20/25 correct (80.0%) | Focus on the misses listed below.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import shutil
import textwrap
import uuid
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

try:
    from colorama import Fore as ColoramaFore
    from colorama import Style as ColoramaStyle
    from colorama import init as colorama_init
except ImportError:
    ColoramaFore = None
    ColoramaStyle = None
    colorama_init = None


def _fallback_palette():
    class _Plain:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ""
        RESET_ALL = ""

    return _Plain()


if ColoramaFore and ColoramaStyle and colorama_init:
    colorama_init(autoreset=True)
    Fore = ColoramaFore
    Style = ColoramaStyle
    COLOR_ENABLED = True
else:
    Fore = _fallback_palette()
    Style = _fallback_palette()
    COLOR_ENABLED = False

DEFAULT_SOURCE = Path(__file__).resolve().parent
CSV_HEADERS = ["id", "question", "answer", "topic", "difficulty"]
REPO_ROOT = DEFAULT_SOURCE.parent
INCORRECT_RULE_NOTE = "cards whose last result was incorrect"
WEAK_RULE_NOTE = "cards with accuracy < 80% and at least one incorrect attempt"
CARD_LABELS = ["WHAT", "WHY", "HOW", "EXAM TRAP", "EXAMPLE"]
SECTION_PATTERN = re.compile(rf"(?mi)^\s*({'|'.join(CARD_LABELS)})\s*:\s*")


@dataclass(frozen=True)
class CertificationConfig:
    key: str
    label: str
    flashcards_dir: Path
    notes_dir: Path
    progress_dir: Path


CERTIFICATIONS: Dict[str, CertificationConfig] = {
    "ai-practitioner": CertificationConfig(
        key="ai-practitioner",
        label="AI Practitioner",
        flashcards_dir=REPO_ROOT / "flashcards" / "ai-practitioner",
        notes_dir=REPO_ROOT / "notes" / "ai-practitioner",
        progress_dir=REPO_ROOT / "progress" / "ai-practitioner",
    ),
    "ml-engineer-associate": CertificationConfig(
        key="ml-engineer-associate",
        label="ML Engineer Associate",
        flashcards_dir=REPO_ROOT / "flashcards" / "ml-engineer-associate",
        notes_dir=REPO_ROOT / "notes" / "ml-engineer-associate",
        progress_dir=REPO_ROOT / "progress" / "ml-engineer-associate",
    ),
}


class SessionAbort(Exception):
    """Raised when the user cancels with Ctrl+C."""


def safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except KeyboardInterrupt:
        raise SessionAbort from None


class Palette:
    topic = Fore.LIGHTCYAN_EX if COLOR_ENABLED else ""
    difficulty = {
        "easy": Fore.LIGHTGREEN_EX if COLOR_ENABLED else "",
        "medium": Fore.LIGHTYELLOW_EX if COLOR_ENABLED else "",
        "hard": Fore.LIGHTRED_EX if COLOR_ENABLED else "",
    }
    header = Fore.LIGHTMAGENTA_EX if COLOR_ENABLED else ""
    prompt = Fore.LIGHTBLUE_EX if COLOR_ENABLED else ""
    positive = Fore.LIGHTGREEN_EX if COLOR_ENABLED else ""
    negative = Fore.LIGHTRED_EX if COLOR_ENABLED else ""
    section = Fore.LIGHTCYAN_EX if COLOR_ENABLED else ""
    border = Fore.MAGENTA if COLOR_ENABLED else ""
    info = Fore.LIGHTWHITE_EX if COLOR_ENABLED else ""
    accent = Fore.LIGHTBLUE_EX if COLOR_ENABLED else ""


def colorize(text: str, color: str | None) -> str:
    if not COLOR_ENABLED or not color:
        return text
    reset = Style.RESET_ALL if COLOR_ENABLED else ""
    return f"{color}{text}{reset}"


HARD_KEYWORDS = (
    "reinforcement",
    "reward function",
    "judge model",
    "distillation",
    "teacher model",
    "on-demand inference",
    "provisioned throughput",
    "pricing mode",
    "scenario",
)

MEDIUM_KEYWORDS = (
    "trade-off",
    "tradeoff",
    "process",
    "steps",
    "goal",
    "use case",
    "cost",
    "expensive",
    "pairs",
    "data must",
)

MEDIUM_PREFIXES = (
    "how",
    "why",
    "when",
    "where",
    "which",
    "what are",
    "what type",
    "what format",
    "what is the role",
    "what is the trade-off",
)


@dataclass
class Flashcard:
    card_id: str
    question: str
    answer: str
    topic: str
    difficulty: str = "Unknown"


def _contains_keyword(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def assign_difficulty(question: str, answer: str) -> str:
    """Return easy|medium|hard based on simple, exam-focused cues."""

    merged_text = f"{question} {answer}".lower()
    lowered_question = question.lower().strip()

    if _contains_keyword(merged_text, HARD_KEYWORDS):
        return "hard"

    if _contains_keyword(merged_text, MEDIUM_KEYWORDS):
        return "medium"

    if any(lowered_question.startswith(prefix) for prefix in MEDIUM_PREFIXES):
        return "medium"

    return "easy"


def collect_csv_paths(target: Path) -> List[Path]:
    """Return every CSV file referenced by --file (single file or entire folder)."""

    if target.is_file():
        return [target]

    if target.is_dir():
        csv_files = sorted(path for path in target.glob("*.csv") if path.is_file())
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found inside {target}")
        return csv_files

    raise FileNotFoundError(f"Flashcard source not found: {target}")


def load_flashcards_from_file(csv_path: Path) -> tuple[List[Flashcard], int]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Flashcard file not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return [], 0

        missing = {field for field in ("question", "answer", "topic") if field not in reader.fieldnames}
        if missing:
            raise ValueError(f"CSV {csv_path.name} is missing required columns: {', '.join(sorted(missing))}")

        cards: List[Flashcard] = []
        auto_assigned = 0
        rows_for_persist = []
        header_has_id = "id" in reader.fieldnames
        needs_write = not header_has_id

        for row in reader:
            question = (row.get("question") or "").strip()
            answer = (row.get("answer") or "").strip()
            topic = (row.get("topic") or "Uncategorized").strip() or "Uncategorized"
            card_id = (row.get("id") or "").strip()
            if not card_id:
                card_id = uuid.uuid4().hex
                needs_write = True
            difficulty_raw = (row.get("difficulty") or "").strip()
            if difficulty_raw:
                difficulty = difficulty_raw.title()
            else:
                difficulty = assign_difficulty(question, answer).title()
                auto_assigned += 1
            if question and answer:
                rows_for_persist.append(
                    {
                        "id": card_id,
                        "question": question,
                        "answer": answer,
                        "topic": topic,
                        "difficulty": difficulty,
                    }
                )
                cards.append(
                    Flashcard(
                        card_id=card_id,
                        question=question,
                        answer=answer,
                        topic=topic,
                        difficulty=difficulty,
                    )
                )

        if needs_write:
            persist_rows_to_csv(csv_path, rows_for_persist)

        return cards, auto_assigned


def persist_rows_to_csv(csv_path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        return
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def load_flashcards(target: Path) -> tuple[List[Flashcard], int]:
    cards: List[Flashcard] = []
    auto_assigned = 0
    for csv_path in collect_csv_paths(target):
        file_cards, file_auto = load_flashcards_from_file(csv_path)
        cards.extend(file_cards)
        auto_assigned += file_auto
    if not cards:
        raise ValueError(
            "No flashcards found. Add CSVs to the selected certification folder or point --file to a populated CSV."
        )
    return cards, auto_assigned


def filter_by_topics(cards: Iterable[Flashcard], topics: Iterable[str] | None) -> List[Flashcard]:
    if not topics:
        return list(cards)
    normalized = {topic.strip().lower() for topic in topics if topic.strip()}
    return [card for card in cards if card.topic.lower() in normalized]


def looks_like_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (ValueError, TypeError):
        return False


def blank_progress_record() -> Dict[str, float]:
    return {
        "times_seen": 0,
        "times_correct": 0,
        "times_incorrect": 0,
        "times_review_again": 0,
        "accuracy": 0.0,
        "priority_score": 0.0,
        "last_reviewed_at": None,
        "last_result": None,
        "needs_review": False,
        "last_review_flagged_at": None,
    }


def compute_accuracy(times_correct: int, times_seen: int) -> float:
    if not times_seen:
        return 0.0
    return round(times_correct / times_seen, 3)


def compute_priority_score(record: Dict[str, float]) -> float:
    accuracy = record.get("accuracy") or 0.0
    times_incorrect = record.get("times_incorrect") or 0
    return round(times_incorrect * 2 + (1 - accuracy) * 5, 2)


def merge_progress(base: Dict[str, float], incoming: Dict[str, float]) -> Dict[str, float]:
    combined = blank_progress_record()
    combined["times_seen"] = (base.get("times_seen") or 0) + (incoming.get("times_seen") or 0)
    combined["times_correct"] = (base.get("times_correct") or 0) + (incoming.get("times_correct") or 0)
    combined["times_incorrect"] = (base.get("times_incorrect") or 0) + (incoming.get("times_incorrect") or 0)
    combined["times_review_again"] = (base.get("times_review_again") or 0) + (incoming.get("times_review_again") or 0)
    combined["accuracy"] = compute_accuracy(combined["times_correct"], combined["times_seen"])
    combined["priority_score"] = compute_priority_score(combined)
    combined["last_reviewed_at"] = incoming.get("last_reviewed_at") or base.get("last_reviewed_at")
    combined["last_result"] = incoming.get("last_result") or base.get("last_result")
    combined["needs_review"] = incoming.get("needs_review", False) or base.get("needs_review", False)
    combined["last_review_flagged_at"] = incoming.get("last_review_flagged_at") or base.get("last_review_flagged_at")
    return combined


class ProgressTracker:
    def __init__(self, topic: str, cards: List[Flashcard], progress_dir: Path) -> None:
        self.topic = topic
        self.cards = cards
        progress_dir.mkdir(parents=True, exist_ok=True)
        self.path = progress_dir / f"{topic}.json"
        self.records: Dict[str, Dict[str, float]] = self._load_existing()

    def _load_existing(self) -> Dict[str, Dict[str, float]]:
        if not self.path.exists():
            return {}
        try:
            with self.path.open(encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError:
            return {}

        if not data:
            return {}

        needs_migration = any(not looks_like_uuid(key) for key in data.keys())
        if not needs_migration:
            return self._normalize_records(data)

        migrated = self._migrate_records(data)
        normalized = self._normalize_records(migrated)
        self._write(normalized)
        print(f"Migrated flashcard progress for topic '{self.topic}' to stable IDs.")
        return normalized

    def _normalize_records(self, records: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """Repair legacy progress (missing times_incorrect or swapped counts) and ensure metrics stay consistent."""
        dirty = False
        normalized: Dict[str, Dict[str, float]] = {}
        for card_id, record in records.items():
            cleaned, changed = self._sanitize_record(record)
            normalized[card_id] = cleaned
            dirty = dirty or changed
        if dirty:
            self._write(normalized)
        return normalized

    def _sanitize_record(self, record: Dict[str, float]) -> tuple[Dict[str, float], bool]:
        cleaned = dict(record)
        changed = False

        def _extract_int(key: str) -> int:
            value = cleaned.get(key)
            if isinstance(value, (int, float)):
                return int(value)
            if isinstance(value, str):
                try:
                    return int(float(value.strip()))
                except ValueError:
                    return 0
            return 0

        times_seen = max(_extract_int("times_seen"), 0)
        times_correct = max(min(_extract_int("times_correct"), times_seen), 0)
        inferred_incorrect = max(times_seen - times_correct, 0)
        times_incorrect = inferred_incorrect
        times_review_again = _extract_int("times_review_again")

        if cleaned.get("times_seen") != times_seen or cleaned.get("times_correct") != times_correct:
            changed = True
        if cleaned.get("times_incorrect") != times_incorrect:
            changed = True
        if cleaned.get("times_review_again") != times_review_again:
            changed = True

        cleaned["times_seen"] = times_seen
        cleaned["times_correct"] = times_correct
        cleaned["times_incorrect"] = times_incorrect
        cleaned["times_review_again"] = times_review_again
        cleaned["accuracy"] = compute_accuracy(times_correct, times_seen)
        cleaned["priority_score"] = compute_priority_score(cleaned)

        if "last_result" not in cleaned:
            cleaned["last_result"] = None
            changed = True
        if "needs_review" not in cleaned:
            cleaned["needs_review"] = False
            changed = True
        if "last_review_flagged_at" not in cleaned:
            cleaned["last_review_flagged_at"] = None
            changed = True

        return cleaned, changed

    def _migrate_records(self, records: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        migrated = dict(records)
        question_to_id: Dict[str, str] = {}
        for card in self.cards:
            question_to_id.setdefault(card.question, card.card_id)

        for key in list(records.keys()):
            if looks_like_uuid(key):
                continue
            card_id = question_to_id.get(key)
            if not card_id:
                continue
            incoming = migrated.pop(key)
            if card_id in migrated:
                migrated[card_id] = merge_progress(migrated[card_id], incoming)
            else:
                migrated[card_id] = incoming
        return migrated

    def update(self, card_id: str, result: str) -> None:
        record = self.records.setdefault(card_id, blank_progress_record())
        record["times_seen"] += 1
        result = result.lower()
        if result == "correct":
            record["times_correct"] += 1
            record["needs_review"] = False
        elif result == "incorrect":
            record["times_incorrect"] += 1
            record["needs_review"] = True
        elif result == "review":
            record["times_review_again"] += 1
            record["needs_review"] = True
            record["last_review_flagged_at"] = datetime.now(timezone.utc).isoformat()
        record["last_result"] = result
        record["accuracy"] = compute_accuracy(int(record["times_correct"]), int(record["times_seen"]))
        record["priority_score"] = compute_priority_score(record)
        record["last_reviewed_at"] = datetime.now(timezone.utc).isoformat()

    def save(self) -> None:
        self._write(self.records)

    def _write(self, data: Dict[str, Dict[str, float]]) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)

    def get_record(self, card_id: str) -> Dict[str, float] | None:
        return self.records.get(card_id)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Terminal flashcard trainer that keeps the study session exam-focused.",
    )
    parser.add_argument(
        "--file",
        help="Optional path to a flashcard CSV or folder. Defaults to the selected certification folder.",
    )
    parser.add_argument(
        "--certification",
        choices=sorted(CERTIFICATIONS.keys()),
        help="Certification track to study. If omitted, the trainer prompts first.",
    )
    parser.add_argument(
        "--topics",
        nargs="*",
        help="Optional list of topic names to drill (exact match, case-insensitive).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Only run the first N cards after filtering/shuffling.",
    )
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="Preserve CSV order instead of randomizing.",
    )
    parser.add_argument(
        "--color-test",
        action="store_true",
        help="Print sample colored output (if supported) and exit.",
    )
    return parser.parse_args()


def display_certification_menu() -> List[CertificationConfig]:
    certifications = list(CERTIFICATIONS.values())
    print("\nAvailable certifications:")
    for idx, certification in enumerate(certifications, start=1):
        print(f"{idx}. {certification.label}")
    return certifications


def prompt_for_certification_choice(certifications: List[CertificationConfig]) -> CertificationConfig:
    while True:
        selection = safe_input("Choose a number: ").strip()
        if selection.isdigit():
            idx = int(selection)
            if 1 <= idx <= len(certifications):
                chosen = certifications[idx - 1]
                print(f"Studying certification track: {chosen.label}")
                return chosen
        print("Please enter a valid certification number from the menu.")


def resolve_certification(selection: str | None) -> CertificationConfig:
    if selection:
        return CERTIFICATIONS[selection]
    certifications = display_certification_menu()
    return prompt_for_certification_choice(certifications)


def display_topics_menu(topic_counts: Counter) -> List[str]:
    if not topic_counts:
        print("No topic labels found; running the full deck.")
        return []

    topics = sorted(topic_counts.keys(), key=str.lower)
    total_cards = sum(topic_counts.values())
    print("\nAvailable topics ({} cards total):".format(total_cards))
    print(f"0. All topics ({total_cards} cards)")
    for idx, topic in enumerate(topics, start=1):
        print(f"{idx}. {topic} ({topic_counts[topic]} cards)")
    return topics


def prompt_for_topic_choice(topics: List[str]) -> List[str] | None:
    if not topics:
        return None

    while True:
        selection = safe_input("Choose a number (0 for all topics): ").strip().lower()
        if selection in {"", "0"}:
            print("Studying every topic to reinforce broad recall.")
            return None
        if selection.isdigit():
            idx = int(selection)
            if 1 <= idx <= len(topics):
                chosen = topics[idx - 1]
                print(f"Focusing on topic: {chosen}")
                return [chosen]
        print("Please enter a valid number from the menu so spacing stays simple.")


def describe_selection(topics: List[str] | None) -> str:
    if not topics:
        return "all topics"
    if len(topics) == 1:
        return f"topic '{topics[0]}'"
    return ", ".join(sorted(topics))


def get_terminal_width() -> int:
    return max(70, shutil.get_terminal_size(fallback=(100, 20)).columns)


def wrap_text(text: str, width: int, indent: int = 0) -> str:
    indent_str = " " * indent
    wrapped = textwrap.fill(text.strip(), width=width, subsequent_indent=indent_str, initial_indent=indent_str)
    return wrapped


def wrap_bullet(text: str, width: int, prefix: str = "  • ") -> str:
    clean = text.strip()
    if not clean:
        return ""
    return textwrap.fill(
        clean,
        width=width,
        initial_indent=prefix,
        subsequent_indent=" " * len(prefix),
    )


def wrap_preserving_indent(text: str, width: int) -> str:
    stripped = text.rstrip()
    if not stripped:
        return ""
    leading_spaces = len(stripped) - len(stripped.lstrip(" "))
    indent = " " * leading_spaces
    return textwrap.fill(
        stripped.lstrip(),
        width=width,
        initial_indent=indent,
        subsequent_indent=indent,
    )


def parse_structured_answer(answer: str) -> List[tuple[str, str]]:
    """Split an answer into (SECTION, body) tuples if WHAT/WHY/HOW/EXAMPLE markers exist."""
    matches = list(SECTION_PATTERN.finditer(answer))
    if not matches:
        return []

    sections: List[tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(answer)
        body = answer[start:end].strip()
        sections.append((match.group(1).upper(), body))
    return sections


def format_answer(answer: str, width: int, label_color: str | None = None) -> str:
    """Format an answer so each WHAT/WHY/HOW/EXAMPLE block stands out."""
    sections = parse_structured_answer(answer)
    if not sections:
        return wrap_text(answer, width)

    lines: List[str] = []
    for idx, (label, body) in enumerate(sections):
        if idx:
            lines.append("")
        label_line = label
        if label_color:
            label_line = colorize(label_line, label_color)
        lines.append(label_line)
        lines.append("")
        paragraphs = [chunk for chunk in re.split(r"\n\s*\n", body.strip()) if chunk.strip()]
        for p_idx, paragraph in enumerate(paragraphs):
            for line_idx, raw_line in enumerate(paragraph.splitlines()):
                line = raw_line.rstrip()
                if not line.strip():
                    continue
                if re.match(r"^\s*-\s+", line):
                    indent = len(line) - len(line.lstrip(" "))
                    bullet_text = line.lstrip()[2:]
                    bullet_prefix = " " * indent + "- "
                    lines.append(wrap_bullet(bullet_text, width, prefix=bullet_prefix))
                else:
                    lines.append(wrap_preserving_indent(line, width))
                if line_idx != len(paragraph.splitlines()) - 1 and not line.strip().endswith(":"):
                    continue
            if p_idx != len(paragraphs) - 1:
                lines.append("")
    return "\n".join(lines).rstrip()


def prompt_for_study_mode() -> str:
    print(
        "\nChoose study mode:\n"
        "1. Standard (default full deck)\n"
        "2. Incorrect-only review (last attempt wrong)\n"
        "3. Weak-cards review (still weak overall)\n"
        "4. Review-again mode (manually flagged)\n"
        "5. Newly added (no study history yet)"
    )
    while True:
        choice = safe_input("Mode number [1]: ").strip() or "1"
        if choice == "1":
            return "standard"
        if choice == "2":
            return "incorrect-only"
        if choice == "3":
            return "weak-cards"
        if choice == "4":
            return "review-again"
        if choice == "5":
            return "new-cards"
        print("Please enter 1, 2, 3, 4, or 5 so the trainer knows which mode to run.")


def is_incorrect_only_candidate(record: Dict[str, float] | None) -> bool:
    """Return True if the most recent attempt for the card was incorrect."""
    if not record:
        return False
    last = (record.get("last_result") or "").lower()
    return last == "incorrect"


def is_weak_card_candidate(record: Dict[str, float] | None) -> bool:
    """Return True if the card is still weak (recent miss or incorrect count >= correct count)."""
    if not record:
        return False
    if is_incorrect_only_candidate(record):
        return True
    times_incorrect = record.get("times_incorrect") or 0
    times_correct = record.get("times_correct") or 0
    return times_incorrect > 0 and times_incorrect >= times_correct


def filter_incorrect_only(cards: List[Flashcard], trackers: Dict[str, ProgressTracker]) -> List[Flashcard]:
    filtered: List[Flashcard] = []
    for card in cards:
        tracker = trackers.get(card.topic)
        if not tracker:
            continue
        record = tracker.get_record(card.card_id)
        if is_incorrect_only_candidate(record):
            filtered.append(card)
    return filtered


def filter_weak_cards(cards: List[Flashcard], trackers: Dict[str, ProgressTracker]) -> List[Flashcard]:
    filtered: List[Flashcard] = []
    for card in cards:
        tracker = trackers.get(card.topic)
        if not tracker:
            continue
        record = tracker.get_record(card.card_id)
        if is_weak_card_candidate(record):
            filtered.append(card)
    return filtered


def filter_review_again(cards: List[Flashcard], trackers: Dict[str, ProgressTracker]) -> List[Flashcard]:
    filtered: List[Flashcard] = []
    for card in cards:
        tracker = trackers.get(card.topic)
        if not tracker:
            continue
        record = tracker.get_record(card.card_id)
        if record and record.get("needs_review"):
            filtered.append(card)
    return filtered


def is_new_card(card: Flashcard, tracker: ProgressTracker | None) -> bool:
    if not tracker:
        return True
    record = tracker.get_record(card.card_id)
    if not record:
        return True
    times_seen = record.get("times_seen") or 0
    return times_seen == 0


def filter_new_cards(cards: List[Flashcard], trackers: Dict[str, ProgressTracker]) -> List[Flashcard]:
    filtered: List[Flashcard] = []
    for card in cards:
        tracker = trackers.get(card.topic)
        if is_new_card(card, tracker):
            filtered.append(card)
    return filtered


def prompt_new_cards_scope(max_cards: int) -> int | None:
    if max_cards <= 0:
        return None
    print(
        "\nStudy scope for newly added cards:\n"
        "1. All new cards\n"
        "2. Limit number of new cards"
    )
    while True:
        choice = safe_input("Scope number [1]: ").strip() or "1"
        if choice == "1":
            return None
        if choice == "2":
            while True:
                quantity = safe_input(f"How many new cards (1-{max_cards})? ").strip()
                if quantity.isdigit():
                    value = int(quantity)
                    if 1 <= value <= max_cards:
                        return value
                print("Enter a number within the available range so the limit stays valid.")
        print("Please choose 1 or 2 so the trainer knows how many new cards to load.")


def build_border_line(left: str, fill: str, right: str, width: int) -> str:
    inner = max(width - 2, 0)
    return left + fill * inner + right


def announce_color_mode() -> None:
    status = "enabled" if COLOR_ENABLED else "disabled"
    message = f"[Color mode {status}] Install colorama for richer colors." if not COLOR_ENABLED else "[Color mode enabled]"
    print(colorize(message, Palette.accent))


def demo_color_mode() -> None:
    samples = [
        colorize("Topic sample", Palette.topic),
        colorize("Difficulty sample", Palette.difficulty.get("hard")),
        colorize("Header sample", Palette.header),
        colorize("Prompt sample", Palette.prompt),
        colorize("Positive sample", Palette.positive),
        colorize("Negative sample", Palette.negative),
    ]
    print("\n".join(samples))


def run_session(cards: List[Flashcard], trackers: Dict[str, ProgressTracker], selection_label: str) -> None:
    if not cards:
        print("No flashcards matched the selected filters. Add cards or adjust your topic list.")
        return

    total = len(cards)
    correct = 0
    misses: List[Flashcard] = []
    review_again = 0
    term_width = get_terminal_width()
    body_width = min(term_width - 8, 100)

    try:
        for idx, card in enumerate(cards, start=1):
            print()
            print(colorize(build_border_line("╔", "═", "╗", term_width), Palette.border))
            title = f" Card {idx}/{total} "
            inner_width = max(term_width - 4, 0)
            print(colorize(f"║ {title.center(inner_width)} ║", Palette.border))
            print(colorize(build_border_line("╟", "─", "╢", term_width), Palette.border))

            topic_label = colorize("Topic:", Palette.header)
            topic_value = colorize(card.topic, Palette.topic)
            topic_line = f"{topic_label} {topic_value}"
            difficulty_color = Palette.difficulty.get(card.difficulty.lower(), "")
            difficulty_label = colorize("Difficulty:", Palette.header)
            difficulty_value = colorize(card.difficulty, difficulty_color)
            info_line = f"{topic_line}  |  {difficulty_label} {difficulty_value}"
            print(info_line)
            print(colorize("─" * term_width, Palette.border))

            question_block = wrap_text(card.question, body_width)
            print(colorize("QUESTION", Palette.header))
            print(f"{question_block}\n")

            safe_input(colorize("➤ Press Enter to reveal the answer...", Palette.prompt))
            answer_block = format_answer(card.answer, body_width, Palette.section)
            print(colorize("\nANSWER", Palette.header))
            print(answer_block + "\n")

            while True:
                response = safe_input(
                    colorize("How did you do? [c] correct  [i] incorrect  [r] review again  [q] quit: ", Palette.prompt)
                ).strip().lower()
                if response in {"c", "correct"}:
                    correct += 1
                    tracker = trackers.get(card.topic)
                    if tracker:
                        tracker.update(card.card_id, "correct")
                    print(colorize("✅ Nice! Logged as correct.", Palette.positive))
                    break
                if response in {"i", "incorrect"}:
                    misses.append(card)
                    tracker = trackers.get(card.topic)
                    if tracker:
                        tracker.update(card.card_id, "incorrect")
                    print(colorize("⚠️  Marked incorrect — it will return in review modes.", Palette.negative))
                    break
                if response in {"r", "review"}:
                    review_again += 1
                    tracker = trackers.get(card.topic)
                    if tracker:
                        tracker.update(card.card_id, "review")
                    print(colorize("🔁 Flagged for review again. Keep it on the radar.", Palette.prompt))
                    break
                if response in {"q", "quit"}:
                    raise SessionAbort
                print("Please respond with c, i, r, or q so the score stays accurate.")

            asked_so_far = correct + len(misses) + review_again
            accuracy_so_far = (correct / asked_so_far * 100) if asked_so_far else 0.0
            remaining = total - asked_so_far
            progress_line = (
                f"Progress: ✅ {correct} | ❌ {len(misses)} | 🔁 {review_again} | "
                f"Accuracy: {accuracy_so_far:.0f}% | Remaining: {remaining}"
            )
            print(colorize(progress_line, Palette.prompt))
            print(colorize(build_border_line("╚", "═", "╝", term_width), Palette.border))
    except SessionAbort:
        print("\nSession interrupted. Calculating score with the cards answered so far...")

    asked = correct + len(misses) + review_again
    accuracy = (correct / asked * 100) if asked else 0.0
    print("\n" + "=" * 60)
    print(f"Session score: {correct}/{asked} correct ({accuracy:.1f}%)")
    print(f"Breakdown → ✅ {correct} | ❌ {len(misses)} | 🔁 {review_again}")

    if misses:
        print("\nCards to revisit (focus on exam traps and similar service confusions):")
        for card in misses:
            print(f"- {card.topic}: {card.question} -> {card.answer}")
    else:
        print("Streak locked in -- log this win inside mistakes/ and move to a short practice test.")

    print("Memory trick: Pair similar language services with 'Talk -> Text -> Think -> Talk' (Lex, Transcribe, Comprehend, Polly).")
    print("Likely trap: Mixing Bedrock (managed GenAI APIs) with SageMaker (builder workflow). Spot that phrasing whenever a question emphasizes speed over custom control.")

    remaining_review = 0
    remaining_incorrect = 0
    for tracker in trackers.values():
        for record in tracker.records.values():
            if record.get("needs_review"):
                remaining_review += 1
            if (record.get("last_result") or "").lower() == "incorrect":
                remaining_incorrect += 1

    print(
        f"Status for {selection_label}: "
        f"{remaining_review} card(s) still flagged 🔁 | {remaining_incorrect} card(s) currently incorrect ❗"
    )


def main() -> None:
    args = parse_args()
    if args.color_test:
        announce_color_mode()
        demo_color_mode()
        return

    certification = resolve_certification(args.certification)
    target_path = Path(args.file).expanduser() if args.file else certification.flashcards_dir

    try:
        cards, auto_assigned = load_flashcards(target_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}")
        if not args.file:
            print(
                f"Study tip: add CSV flashcards under {certification.flashcards_dir} "
                f"to activate the {certification.label} track."
            )
        return
    announce_color_mode()
    print(f"{len(cards)} cards loaded for {certification.label}, {auto_assigned} auto-assigned difficulty values.")

    topic_counts = Counter(card.topic for card in cards)
    topics = display_topics_menu(topic_counts)
    selected_topics = args.topics
    if not selected_topics:
        selected_topics = prompt_for_topic_choice(topics)

    cards = filter_by_topics(cards, selected_topics)
    selection_label = describe_selection(selected_topics)
    print(f"\nLoaded {len(cards)} cards for {selection_label}.\n")

    topic_cards: Dict[str, List[Flashcard]] = {}
    for card in cards:
        topic_cards.setdefault(card.topic, []).append(card)
    progress_trackers = {
        topic: ProgressTracker(topic, topic_cards[topic], certification.progress_dir) for topic in topic_cards
    }

    study_mode = prompt_for_study_mode()
    skip_shuffle = False
    if study_mode == "incorrect-only":
        cards = filter_incorrect_only(cards, progress_trackers)
        selection_label = describe_selection(selected_topics)
        print(
            f"\nIncorrect-only mode active: cards with last_result = incorrect. "
            f"Loaded {len(cards)} card(s) for {selection_label}.\n"
        )
        if not cards:
            print("Nothing to review yet. Run a standard session first to build incorrect history.")
            for tracker in progress_trackers.values():
                tracker.save()
            return
    elif study_mode == "weak-cards":
        cards = filter_weak_cards(cards, progress_trackers)
        selection_label = describe_selection(selected_topics)
        print(
            f"\nWeak-cards mode active: last result incorrect OR incorrect count >= correct count. "
            f"Loaded {len(cards)} reinforcement card(s) for {selection_label}.\n"
        )
        if not cards:
            print("No weak cards detected right now. Keep logging misses to unlock this mode.")
            for tracker in progress_trackers.values():
                tracker.save()
            return
    elif study_mode == "review-again":
        cards = filter_review_again(cards, progress_trackers)
        selection_label = describe_selection(selected_topics)
        print(
            f"\nReview-again mode active: cards flagged manually for follow-up. "
            f"Loaded {len(cards)} card(s) for {selection_label}.\n"
        )
        if not cards:
            print("Nothing is flagged for review right now. Use 'r' during a session to flag cards.")
            for tracker in progress_trackers.values():
                tracker.save()
            return
    elif study_mode == "new-cards":
        cards = filter_new_cards(cards, progress_trackers)
        selection_label = describe_selection(selected_topics)
        print(
            f"\nNewly added mode active: cards with no study history. "
            f"Found {len(cards)} new card(s) for {selection_label}.\n"
        )
        if not cards:
            print("No new cards found. Add more flashcards or choose another mode to keep momentum.")
            for tracker in progress_trackers.values():
                tracker.save()
            return
        limit = prompt_new_cards_scope(len(cards))
        if limit is not None:
            cards = cards[:limit]
            print(f"\nStudying the first {len(cards)} new card(s) based on CSV order.\n")
        skip_shuffle = True

    if not args.no_shuffle and not skip_shuffle:
        random.shuffle(cards)
    if args.limit is not None:
        cards = cards[: max(args.limit, 0)]
    run_session(cards, progress_trackers, selection_label)
    for tracker in progress_trackers.values():
        tracker.save()


if __name__ == "__main__":
    try:
        main()
    except SessionAbort:
        print("\nSession cancelled by user (Ctrl+C). No changes were saved beyond completed cards.")
