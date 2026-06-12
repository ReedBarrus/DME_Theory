#!/usr/bin/env python3
"""DME v0.2 deterministic claim extractor.

Substrates exercised: Structure (parse), Ledger (record). Nothing else.
This implements the v0.2 audit-driven fixes without semantic inference.
"""

from __future__ import annotations

import json
import random
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TAG = "theory-v2.0-pre-grounding"
EXTRACTOR_VERSION = "v0.2"
SAMPLE_SEED = 7

INCLUDE_DIRS = [
    "Core",
    "Grammar",
    "Substrates",
    "Regime_Ecologies",
    "Agentic_Reasoning",
    "Implementation_Orientation",
]
INCLUDE_ROOT_FILES = ["README.md", "MEMORY_INDEX.md"]
EXCLUDE_DIRS = ["Archive", "Meta_Web_Gov_Hub"]

GROUNDING_V0 = REPO / "Grounding" / "v0"
GROUNDING_V0_2 = REPO / "Grounding" / "v0_2"

INSTRUMENT_DOCS = {
    "Core/README.DME.V2.ClaimInventory.md",
    "Core/README.DME.V2.FormalCorrespondenceLedger.md",
    "Implementation_Orientation/README.DME.V2.LanguageAdmissionPrototype.md",
}
INSTRUMENT_NON_COLLAPSE_RE = re.compile(r"non-collapse laws?", re.I)
EXAMPLE_SECTION_RE = re.compile(
    r"(illustrative example|example only|not a populated entry|entry record shape|record shape)",
    re.I,
)
EXAMPLE_LINE_RE = re.compile(
    r"(illustrative example|example only|not a populated entry|example:)",
    re.I,
)
CONTEXT_PREFIX_RE = re.compile(
    r"^(without\b|if absent\b|if missing\b|when missing\b|when absent\b|failure mode\b|if no\b|missing\b|absent\b)",
    re.I,
)

DOCTRINE_TERMS = {
    "identity",
    "scale",
    "envelope",
    "multiscaleidentityenvelope",
    "multiscaleidentity",
    "projection",
    "authority",
    "reference",
    "canon",
    "distinction",
    "constraint",
    "ledger",
    "runtime",
    "attention",
    "agency",
    "decision",
    "consequence",
    "proof",
    "budget",
    "retention",
    "memory",
    "archive",
    "source",
    "structure",
    "token",
    "embedding",
    "feedback",
    "operator",
    "translation",
    "extraction",
    "candidate",
    "corroboration",
    "hypothetical",
    "admitted",
    "opacity",
    "claim",
    "repair",
    "revoke",
    "release",
    "reconcile",
    "admission",
    "inference",
    "path",
    "paths",
    "topology",
    "coherence",
    "governance",
    "provenance",
    "formal",
    "correspondence",
    "recurrence",
    "presheaf",
    "sheaf",
}

OPERATOR_VOCAB = {
    "Accept",
    "Archive",
    "Authorize",
    "Bound",
    "Canonize",
    "Chart",
    "Classify",
    "Compare",
    "Consent",
    "Contest",
    "Declare",
    "DeclareRupture",
    "Determine",
    "Detect",
    "DetectRupture",
    "Differentiate",
    "Echo",
    "Execute",
    "Expose",
    "Ingest",
    "Integrate",
    "Permit",
    "Project",
    "Prove",
    "Reconcile",
    "Record",
    "Reference",
    "Relate",
    "Release",
    "Repair",
    "Revoke",
    "Route",
    "Select",
    "Simulate",
    "Transform",
    "Translate",
}

AXES_EVAL = ["Distinction", "Ledger"]
AXES_OMIT = [
    "Constraint",
    "Identity",
    "Projection",
    "Feedback",
    "Consequence",
    "Proof",
    "Authority",
    "Budget",
]

BLOCKED_USES = ["doctrine_compression", "formal_correspondence", "canon_promotion"]

NC_INLINE = re.compile(r"^(.{1,120}?)\s*(?:!=|≠|â‰ )\s*(.{1,120})$")
NC_ISNOT = re.compile(
    r"\b([A-Z][A-Za-z_/ -]{1,60}?)\s+is not\s+(?:an?\s+|the\s+)?([A-Za-z][A-Za-z_/ -]{1,60}?)(?:[.,;]|$)"
)
NC_IMPLY = re.compile(
    r"\b([A-Za-z_/ -]{2,80}?)\s+does not (?:imply|mean|equal|guarantee)\s+([A-Za-z_/ -]{2,80}?)(?:[.,;]|$)"
)
NC_COLLAPSE = re.compile(
    r"\b([A-Za-z_/ -]{2,80}?)\s+must not be (?:collapsed|confused) (?:with|into)\s+([A-Za-z_/ -]{2,80}?)(?:[.,;]|$)"
)

DEF_TERM_EQ = re.compile(r"^([A-Za-z][A-Za-z_/ ()-]{0,80}?)\s*=\s*$")
DEF_INLINE_EQ = re.compile(r"^([A-Za-z][A-Za-z_/ ()-]{0,80}?)\s*=\s*(.{3,})$")
DEF_LABEL = re.compile(r"^Definition\s*:\s*(.*)$", re.I)

BL_MODAL = re.compile(r"\b(may not|must not|must|never|requires?|only when|only if|cannot)\b", re.I)
CORE_LAW = re.compile(r"^Core law\s*:\s*$", re.I)

ARROW_SPLIT = re.compile(r"\s*(?:→|â†’|->)\s*")
DEP_REF = re.compile(r"(?:defined|specified)\s+(?:later\s+)?in\s+([A-Za-z0-9_./-]+\.md)", re.I)
DEP_DOWNSTREAM = re.compile(r"\bdownstream of\b", re.I)
DEP_LIST_ITEM = re.compile(r"^\s*-\s+([A-Za-z0-9_./ -]+\.md)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")

raw_entries = []
stats = defaultdict(int)


def norm_term(text: str) -> str:
    text = text.strip().strip('"\'`*.,;:()[]')
    text = re.sub(r"\s+", " ", text)
    return text.lower().replace(" ", "_")


def first_words(text: str, count: int = 8) -> str:
    return norm_term(" ".join(text.split()[:count]))


def has_terminal_punctuation(text: str) -> bool:
    return bool(text) and text[-1] in ".!?"


def looks_like_heading_fragment(text: str) -> bool:
    if not text:
        return False
    if text.endswith(":"):
        return True
    if re.match(r"^\d+(\.\d+)*\s+[A-Z]", text):
        return True
    return False


def looks_like_list_intro(text: str) -> bool:
    lower = text.lower()
    return lower.endswith(":") or lower.startswith(("examples", "status", "next test", "blocked uses"))


def overlaps(a_start: int, a_end: int, b_start: int, b_end: int) -> int:
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    return max(0, end - start + 1)


def block_char_span(offsets, start_line: int, end_line: int, end_text: str):
    return [offsets[start_line - 1], offsets[end_line - 1] + len(end_text)]


def infer_use_mention_flag(source_file: str, section_context: str, explicit_example: bool = False) -> str:
    if source_file not in INSTRUMENT_DOCS:
        return "asserted"
    if INSTRUMENT_NON_COLLAPSE_RE.search(section_context):
        return "instrument_self_assertion"
    if explicit_example or EXAMPLE_SECTION_RE.search(section_context):
        return "example"
    return "unknown"


def enrich_support_fields(entry: dict) -> None:
    blocked = list(entry.get("blocked_uses", []))
    use_flag = entry.get("use_mention_flag", "asserted")
    if entry.get("context_sensitive"):
        entry["support_status"] = "structurally_supported"
        blocked.extend(BLOCKED_USES)
        entry["notes"] = "Distinction axis demoted: assertion is conditional on context_prefix and is not standalone doctrine."
    elif use_flag in {"example", "mentioned", "unknown"}:
        entry["support_status"] = "structurally_supported"
        blocked.extend(BLOCKED_USES)
    else:
        entry["support_status"] = "partially_admitted"
    if blocked:
        entry["blocked_uses"] = sorted(set(blocked))


def make_raw_entry(
    claim_type: str,
    source_file: str,
    line_start: int,
    line_end: int,
    char_start: int,
    char_end: int,
    verbatim_span: str,
    normalized_terms,
    scale_band: str,
    section_context: str,
    in_fenced_block: bool,
    extraction_method: str,
    notes: str = "",
    extra: dict | None = None,
):
    entry = {
        "claim_type": claim_type,
        "source_file": source_file,
        "line_range": [line_start, line_end],
        "char_span": [char_start, char_end],
        "source_snapshot": TAG,
        "verbatim_span": verbatim_span,
        "normalized_terms": normalized_terms,
        "scale_band": scale_band,
        "section_context": section_context,
        "in_fenced_block": in_fenced_block,
        "evaluated_axes": list(AXES_EVAL),
        "omitted_axes": list(AXES_OMIT),
        "opacity_status": "partially_supported",
        "support_status": "partially_admitted",
        "recurrence_refs": [],
        "extraction_method": extraction_method,
        "notes": notes,
        "use_mention_flag": "asserted",
    }
    if extra:
        entry.update(extra)
    enrich_support_fields(entry)
    raw_entries.append(entry)
    return entry


def should_accept_bl_modal(text: str, in_fenced_block: bool, explicit_label: bool = False) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    lower = stripped.lower()
    if not explicit_label and re.match(r"^(what|which|where|how|why)\b", lower):
        return False
    if looks_like_heading_fragment(stripped) or looks_like_list_intro(stripped):
        return False
    if re.match(r"^[-*]\s+", stripped):
        return False
    if re.match(r"^\d+[\).]\s+", stripped):
        return False
    first_token = stripped.split()[0].strip('"\'`*.,;:()[]')
    starts_well = stripped[0].isupper() or first_token.lower() in DOCTRINE_TERMS
    if not starts_well:
        return False
    if has_terminal_punctuation(stripped):
        return True
    if in_fenced_block:
        if stripped.endswith(":"):
            return False
        if len(stripped.split()) >= 4:
            return True
    return False


def is_contextual_prefix(text: str) -> bool:
    stripped = text.strip()
    if not stripped.endswith(":"):
        return False
    prefix = stripped[:-1].strip()
    return bool(CONTEXT_PREFIX_RE.match(prefix))


def parse_def_label_body(lines, start_index: int):
    line_start = start_index + 1
    line_text = lines[start_index].rstrip()
    match = DEF_LABEL.match(line_text.strip())
    if not match:
        return None
    inline_body = match.group(1).strip()
    if inline_body:
        return {
            "line_start": line_start,
            "line_end": line_start,
            "body": inline_body,
            "next_index": start_index + 1,
        }

    cursor = start_index + 1
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1
    if cursor >= len(lines):
        stats["def_label_rejected_no_body"] += 1
        return None
    probe = lines[cursor].rstrip()
    if probe.lstrip().startswith("```"):
        fence_body = []
        fence_line_start = cursor + 1
        cursor += 1
        while cursor < len(lines) and not lines[cursor].lstrip().startswith("```"):
            fence_body.append(lines[cursor].rstrip())
            cursor += 1
        if not fence_body:
            stats["def_label_rejected_no_body"] += 1
            return None
        return {
            "line_start": line_start,
            "line_end": fence_line_start + len(fence_body) - 1,
            "body": "\n".join(fence_body),
            "next_index": start_index + 1,
            "body_from_fence": True,
        }

    para_lines = []
    para_start = cursor + 1
    while cursor < len(lines):
        candidate = lines[cursor].rstrip()
        if not candidate.strip() or candidate.lstrip().startswith("```") or HEADING_RE.match(candidate.strip()):
            break
        para_lines.append(candidate.strip())
        cursor += 1
    if not para_lines:
        stats["def_label_rejected_no_body"] += 1
        return None
    return {
        "line_start": line_start,
        "line_end": para_start + len(para_lines) - 1,
        "body": "\n".join(para_lines),
        "next_index": start_index + 1,
        "body_from_fence": False,
    }


def process_fenced_block(
    source_file: str,
    fence_lines,
    section_context: str,
    offsets,
    is_meta: bool,
    is_core_law: bool = False,
    explicit_example: bool = False,
    leading_context_prefix: str | None = None,
    skip_definitions: bool = False,
):
    if not fence_lines:
        return

    use_flag = infer_use_mention_flag(source_file, section_context, explicit_example)
    first_line = fence_lines[0][0]
    last_line = fence_lines[-1][0]
    last_text = fence_lines[-1][1]

    if is_meta:
        active_relation = None
        for line_number, text in fence_lines:
            stripped = text.strip()
            key_match = re.match(r"^\s*(related|depends_on)\s*:\s*$", text)
            if key_match:
                active_relation = "related_to" if key_match.group(1) == "related" else "depends_on"
                continue
            item_match = DEP_LIST_ITEM.match(text)
            if active_relation and item_match:
                target = item_match.group(1).strip()
                make_raw_entry(
                    "DEP",
                    source_file,
                    line_number,
                    line_number,
                    offsets[line_number - 1],
                    offsets[line_number - 1] + len(text),
                    text.strip(),
                    [norm_term(Path(source_file).name), norm_term(Path(target).name), active_relation],
                    "document",
                    section_context,
                    True,
                    f"pattern:DEP-meta-{active_relation};extractor:{EXTRACTOR_VERSION}",
                    extra={"relation_type": active_relation, "use_mention_flag": use_flag},
                )
                stats[f"dep_{active_relation}"] += 1
                continue
            if stripped and not text.startswith("  "):
                active_relation = None
        return

    if is_core_law:
        body = "\n".join(text for _, text in fence_lines)
        make_raw_entry(
            "BL",
            source_file,
            first_line,
            last_line,
            offsets[first_line - 1],
            offsets[last_line - 1] + len(last_text),
            body,
            [first_words(body, 12)],
            "sentence/doctrine_law",
            section_context,
            True,
            f"pattern:BL-corelaw-block;extractor:{EXTRACTOR_VERSION}",
            extra={"use_mention_flag": use_flag},
        )
        stats["bl_corelaw_blocks"] += 1

    current_context_prefix = leading_context_prefix
    index = 0
    while index < len(fence_lines):
        line_number, text = fence_lines[index]
        stripped = text.strip()
        if not stripped:
            current_context_prefix = None
            index += 1
            continue

        if stripped.endswith(":"):
            current_context_prefix = stripped

        match = NC_INLINE.match(stripped)
        if match and not stripped.startswith("="):
            make_raw_entry(
                "NC",
                source_file,
                line_number,
                line_number,
                offsets[line_number - 1],
                offsets[line_number - 1] + len(text),
                stripped,
                [norm_term(match.group(1)), norm_term(match.group(2)), "non_equivalence"],
                "sentence/doctrine_law",
                section_context,
                True,
                f"pattern:NC-symbol;extractor:{EXTRACTOR_VERSION}",
                extra={"use_mention_flag": use_flag},
            )
            stats["nc_fenced"] += 1
            index += 1
            continue

        match = DEF_TERM_EQ.match(stripped)
        if match and not skip_definitions:
            body_lines = []
            cursor = index + 1
            body_end_line = line_number
            while cursor < len(fence_lines) and fence_lines[cursor][1].strip():
                body_lines.append(fence_lines[cursor][1].strip())
                body_end_line = fence_lines[cursor][0]
                cursor += 1
            if body_lines:
                make_raw_entry(
                    "DEF",
                    source_file,
                    line_number,
                    body_end_line,
                    offsets[line_number - 1],
                    offsets[body_end_line - 1] + len(fence_lines[cursor - 1][1]),
                    stripped + "\n" + "\n".join(body_lines),
                    [norm_term(match.group(1)), "defined_as", first_words(" ".join(body_lines))],
                    "sentence",
                    section_context,
                    True,
                    f"pattern:DEF-block;extractor:{EXTRACTOR_VERSION}",
                    extra={"use_mention_flag": use_flag},
                )
                index = cursor
                continue

        match = DEF_INLINE_EQ.match(stripped)
        if match and not skip_definitions:
            make_raw_entry(
                "DEF",
                source_file,
                line_number,
                line_number,
                offsets[line_number - 1],
                offsets[line_number - 1] + len(text),
                stripped,
                [norm_term(match.group(1)), "defined_as", first_words(match.group(2))],
                "sentence",
                section_context,
                True,
                f"pattern:DEF-inline;extractor:{EXTRACTOR_VERSION}",
                extra={"use_mention_flag": use_flag},
            )
            index += 1
            continue

        if any(token in stripped for token in ("→", "â†’", "->")):
            chain_lines = [stripped]
            chain_end_line = line_number
            cursor = index + 1
            while cursor < len(fence_lines) and fence_lines[cursor][1].strip().startswith(("→", "â†’", "->")):
                chain_lines.append(fence_lines[cursor][1].strip())
                chain_end_line = fence_lines[cursor][0]
                cursor += 1
            full_chain = " ".join(chain_lines)
            elements = [elem.strip() for elem in ARROW_SPLIT.split(full_chain) if elem.strip()]
            operators = []
            for element in elements:
                token = element.split()[0].strip("():,")
                token = token.split("(")[0].strip()
                if token in OPERATOR_VOCAB:
                    operators.append(token)
            if len(elements) >= 2 and len(operators) >= 2:
                make_raw_entry(
                    "OP",
                    source_file,
                    line_number,
                    chain_end_line,
                    offsets[line_number - 1],
                    offsets[chain_end_line - 1] + len(fence_lines[cursor - 1][1]),
                    full_chain,
                    [norm_term(op) for op in operators],
                    "span",
                    section_context,
                    True,
                    f"pattern:OP-chain;extractor:{EXTRACTOR_VERSION}",
                    notes=f"{len(operators)}/{len(elements)} elements in operator vocab",
                    extra={"use_mention_flag": use_flag},
                )
                stats["op_admitted"] += 1
                index = cursor
                continue
            if len(elements) >= 2:
                stats["op_chains_nonvocab"] += 1
                index = cursor
                continue

        if not is_core_law and BL_MODAL.search(stripped):
            if should_accept_bl_modal(stripped, in_fenced_block=True):
                extra = {"use_mention_flag": use_flag}
                if current_context_prefix and is_contextual_prefix(current_context_prefix):
                    extra["context_prefix"] = current_context_prefix
                    extra["context_sensitive"] = True
                    stats["context_sensitive_entries"] += 1
                make_raw_entry(
                    "BL",
                    source_file,
                    line_number,
                    line_number,
                    offsets[line_number - 1],
                    offsets[line_number - 1] + len(text),
                    stripped,
                    [first_words(stripped, 10)],
                    "sentence/doctrine_law",
                    section_context,
                    True,
                    f"pattern:BL-modal;extractor:{EXTRACTOR_VERSION}",
                    extra=extra,
                )
            else:
                stats["bl_modal_rejected_shape"] += 1

        for regex, pattern_id in (
            (NC_ISNOT, "NC-isnot"),
            (NC_IMPLY, "NC-imply"),
            (NC_COLLAPSE, "NC-collapse"),
        ):
            match = regex.search(stripped)
            if match:
                make_raw_entry(
                    "NC",
                    source_file,
                    line_number,
                    line_number,
                    offsets[line_number - 1],
                    offsets[line_number - 1] + len(text),
                    stripped,
                    [norm_term(match.group(1)), norm_term(match.group(2)), "non_equivalence"],
                    "sentence/doctrine_law",
                    section_context,
                    True,
                    f"pattern:{pattern_id};extractor:{EXTRACTOR_VERSION}",
                    extra={"use_mention_flag": use_flag},
                )
                break
        index += 1


def process_prose_line(source_file: str, line_number: int, text: str, section_context: str, offsets, explicit_example: bool = False):
    stripped = text.strip()
    if not stripped:
        return

    use_flag = infer_use_mention_flag(source_file, section_context, explicit_example)
    char_start = offsets[line_number - 1]
    char_end = char_start + len(text)

    for match in DEP_REF.finditer(stripped):
        target = match.group(1)
        make_raw_entry(
            "DEP",
            source_file,
            line_number,
            line_number,
            char_start,
            char_end,
            stripped,
            [norm_term(Path(source_file).name), norm_term(Path(target).name), "forward_ref"],
            "document",
            section_context,
            False,
            f"pattern:DEP-forward_ref;extractor:{EXTRACTOR_VERSION}",
            extra={"relation_type": "forward_ref", "use_mention_flag": use_flag},
        )
        stats["dep_forward_ref"] += 1

    if DEP_DOWNSTREAM.search(stripped):
        make_raw_entry(
            "DEP",
            source_file,
            line_number,
            line_number,
            char_start,
            char_end,
            stripped,
            [first_words(stripped, 6), "downstream_of"],
            "document",
            section_context,
            False,
            f"pattern:DEP-downstream_of;extractor:{EXTRACTOR_VERSION}",
            extra={"relation_type": "downstream_of", "use_mention_flag": use_flag},
        )
        stats["dep_downstream_of"] += 1

    for regex, pattern_id in (
        (NC_IMPLY, "NC-imply"),
        (NC_COLLAPSE, "NC-collapse"),
        (NC_ISNOT, "NC-isnot"),
    ):
        match = regex.search(stripped)
        if match:
            make_raw_entry(
                "NC",
                source_file,
                line_number,
                line_number,
                char_start,
                char_end,
                stripped,
                [norm_term(match.group(1)), norm_term(match.group(2)), "non_equivalence"],
                "sentence/doctrine_law",
                section_context,
                False,
                f"pattern:{pattern_id};extractor:{EXTRACTOR_VERSION}",
                extra={"use_mention_flag": use_flag},
            )
            return

    if "!=" in stripped or "≠" in stripped or "â‰ " in stripped:
        match = NC_INLINE.match(stripped)
        if match:
            make_raw_entry(
                "NC",
                source_file,
                line_number,
                line_number,
                char_start,
                char_end,
                stripped,
                [norm_term(match.group(1)), norm_term(match.group(2)), "non_equivalence"],
                "sentence/doctrine_law",
                section_context,
                False,
                f"pattern:NC-symbol;extractor:{EXTRACTOR_VERSION}",
                extra={"use_mention_flag": use_flag},
            )
            return


def parse_file(source_file: str):
    path = REPO / source_file
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    offsets = []
    cursor = 0
    for line in lines:
        offsets.append(cursor)
        cursor += len(line) + 1

    heading_chain = []
    seen_first_fence = False
    core_law_pending = False
    example_hint_pending = False
    pending_context_prefix = None
    skip_next_def_fence = False

    def section_context():
        return " > ".join(item[1] for item in heading_chain) or "(root)"

    index = 0
    while index < len(lines):
        raw = lines[index].rstrip()
        stripped = raw.strip()
        line_number = index + 1

        if raw.lstrip().startswith("```"):
            fence_lines = []
            fence_start = line_number
            index += 1
            while index < len(lines) and not lines[index].lstrip().startswith("```"):
                fence_lines.append((index + 1, lines[index].rstrip()))
                index += 1
            block_is_meta = (not seen_first_fence) and any(
                re.match(r"\s*(status|schema posture|folder|source_snapshot|population_status)\s*:", fence_text)
                for _, fence_text in fence_lines
            )
            seen_first_fence = True
            process_fenced_block(
                source_file,
                fence_lines,
                section_context(),
                offsets,
                is_meta=block_is_meta,
                is_core_law=core_law_pending,
                explicit_example=example_hint_pending,
                leading_context_prefix=pending_context_prefix,
                skip_definitions=skip_next_def_fence,
            )
            core_law_pending = False
            example_hint_pending = False
            pending_context_prefix = None
            skip_next_def_fence = False
            if index < len(lines) and lines[index].lstrip().startswith("```"):
                index += 1
            continue

        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            level = len(heading_match.group(1))
            while heading_chain and heading_chain[-1][0] >= level:
                heading_chain.pop()
            heading_chain.append((level, heading_match.group(2).strip()))
            example_hint_pending = False
            core_law_pending = False
            index += 1
            continue

        if CORE_LAW.match(stripped):
            core_law_pending = True
            process_prose_line(source_file, line_number, raw, section_context(), offsets, explicit_example=example_hint_pending)
            index += 1
            continue

        if EXAMPLE_LINE_RE.search(stripped):
            example_hint_pending = True

        if stripped.endswith(":") and is_contextual_prefix(stripped):
            pending_context_prefix = stripped

        def_body = parse_def_label_body(lines, index)
        if def_body:
            use_flag = infer_use_mention_flag(source_file, section_context(), example_hint_pending)
            verbatim = raw.strip() + "\n" + def_body["body"]
            make_raw_entry(
                "DEF",
                source_file,
                def_body["line_start"],
                def_body["line_end"],
                offsets[def_body["line_start"] - 1],
                offsets[def_body["line_end"] - 1] + len(lines[def_body["line_end"] - 1].rstrip()),
                verbatim,
                [first_words(def_body["body"]), "definition_label"],
                "sentence",
                section_context(),
                False,
                f"pattern:DEF-label-body;extractor:{EXTRACTOR_VERSION}",
                extra={"use_mention_flag": use_flag},
            )
            if def_body.get("body_from_fence"):
                skip_next_def_fence = True

        process_prose_line(source_file, line_number, raw, section_context(), offsets, explicit_example=example_hint_pending)
        index += 1


def load_v0_entries():
    old_entries = []
    path = GROUNDING_V0 / "claim_inventory.jsonl"
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                old_entries.append(json.loads(line))
    return old_entries


def parse_claim_id(claim_id: str):
    prefix, claim_type, serial = claim_id.split("-")
    return claim_type, int(serial)


def normalized_verbatim(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("â‰ ", "!=").replace("≠", "!=")).strip().lower()


def score_match(new_entry: dict, old_entry: dict) -> tuple:
    overlap = overlaps(
        new_entry["line_range"][0],
        new_entry["line_range"][1],
        old_entry["line_range"][0],
        old_entry["line_range"][1],
    )
    verbatim_equal = int(normalized_verbatim(new_entry["verbatim_span"]) == normalized_verbatim(old_entry["verbatim_span"]))
    new_terms = {term for term in new_entry.get("normalized_terms", []) if term}
    old_terms = {term for term in old_entry.get("normalized_terms", []) if term}
    shared_terms = len(new_terms & old_terms)
    old_span = old_entry["line_range"][1] - old_entry["line_range"][0]
    return (overlap, verbatim_equal, shared_terms, -old_span, -parse_claim_id(old_entry["claim_id"])[1])


def assign_stable_ids(entries_v0_2, entries_v0_1):
    old_by_key = defaultdict(list)
    old_ceiling = defaultdict(int)
    for old in entries_v0_1:
        key = (old["source_file"], old["claim_type"])
        old_by_key[key].append(old)
        claim_type, serial = parse_claim_id(old["claim_id"])
        old_ceiling[claim_type] = max(old_ceiling[claim_type], serial)

    next_serial = defaultdict(int, old_ceiling)
    for old_list in old_by_key.values():
        old_list.sort(key=lambda entry: entry["claim_id"])

    crosswalk = {
        old["claim_id"]: {
            "status": "superseded_no_successor",
            "v0_2_id": None,
            "reason": "No deterministic v0.2 successor matched on source_file, claim_type, and line-range overlap.",
        }
        for old in entries_v0_1
    }
    consumed_old = set()

    indexed_entries = list(enumerate(entries_v0_2))
    indexed_entries.sort(
        key=lambda item: (
            item[1]["claim_type"],
            item[1]["source_file"],
            -(item[1]["line_range"][1] - item[1]["line_range"][0]),
            item[1]["line_range"][0],
            item[1]["line_range"][1],
            item[0],
        )
    )

    for _, entry in indexed_entries:
        key = (entry["source_file"], entry["claim_type"])
        candidates = []
        for old in old_by_key.get(key, []):
            overlap = overlaps(
                entry["line_range"][0],
                entry["line_range"][1],
                old["line_range"][0],
                old["line_range"][1],
            )
            if overlap > 0 and old["claim_id"] not in consumed_old:
                candidates.append((score_match(entry, old), old))
        candidates.sort(key=lambda item: item[0], reverse=True)

        if candidates:
            top_score = candidates[0][0]
            matched_old = [
                candidate[1]
                for candidate in candidates
                if candidate[0] == top_score
                or (candidate[0][0] == top_score[0] and candidate[0][0] > 0)
            ]
            keeper = min(matched_old, key=lambda old: parse_claim_id(old["claim_id"])[1])
            entry["claim_id"] = keeper["claim_id"]
            consumed_old.add(keeper["claim_id"])
            crosswalk[keeper["claim_id"]] = {
                "status": "preserved",
                "v0_2_id": keeper["claim_id"],
                "reason": "Deterministic v0.2 match preserved via source_file, claim_type, overlapping line_range, and supporting verbatim/term similarity.",
            }
            absorbed = []
            for old in matched_old:
                if old["claim_id"] == keeper["claim_id"]:
                    continue
                consumed_old.add(old["claim_id"])
                absorbed.append(old["claim_id"])
                crosswalk[old["claim_id"]] = {
                    "status": "merged_into",
                    "v0_2_id": keeper["claim_id"],
                    "reason": f"Merged into {keeper['claim_id']} after deterministic overlap match; absorbed into cleaner v0.2 capture.",
                }
            if absorbed:
                entry["supersedes"] = absorbed
        else:
            claim_type = entry["claim_type"]
            next_serial[claim_type] += 1
            entry["claim_id"] = f"CLAIM-{claim_type}-{next_serial[claim_type]:04d}"
            crosswalk[entry["claim_id"]] = {
                "status": "new_in_v0_2",
                "v0_2_id": entry["claim_id"],
                "reason": "No prior v0.1 entry matched deterministically; allocated above the v0.1 type ceiling.",
            }

    return entries_v0_2, crosswalk, dict(next_serial)


def build_recurrence(entries_v0_2):
    term_map = defaultdict(list)
    skip_terms = {
        "non_equivalence",
        "defined_as",
        "definition_label",
        "related_to",
        "depends_on",
        "forward_ref",
        "downstream_of",
    }
    id_to_entry = {entry["claim_id"]: entry for entry in entries_v0_2}
    for entry in entries_v0_2:
        for term in entry["normalized_terms"]:
            if term and term not in skip_terms:
                term_map[term].append(entry["claim_id"])
    for term, claim_ids in term_map.items():
        if len(claim_ids) > 1:
            for claim_id in claim_ids:
                refs = [other for other in claim_ids if other != claim_id]
                id_to_entry[claim_id]["recurrence_refs"] = sorted(set(id_to_entry[claim_id]["recurrence_refs"]) | set(refs))[:50]

    cross_document = {}
    for term, claim_ids in term_map.items():
        if len(claim_ids) <= 1:
            continue
        files = sorted({id_to_entry[claim_id]["source_file"] for claim_id in claim_ids})
        cross_document[term] = {
            "count": len(claim_ids),
            "files": files,
            "n_files": len(files),
            "claim_ids": sorted(claim_ids),
        }

    duplicate_nc = defaultdict(list)
    for entry in entries_v0_2:
        if entry["claim_type"] != "NC":
            continue
        key = re.sub(r"\s+", " ", entry["verbatim_span"].replace("â‰ ", "!=").replace("≠", "!=")).strip().lower()
        duplicate_nc[key].append(entry["claim_id"])
    duplicate_nc = {key: value for key, value in duplicate_nc.items() if len(value) > 1}

    return cross_document, duplicate_nc


def load_fcl_001_refs():
    ledger_path = REPO / "Core" / "README.DME.V2.FormalCorrespondenceLedger.md"
    text = ledger_path.read_text(encoding="utf-8", errors="replace")
    start = text.find("### FCL-001")
    end = text.find("### FCL-002")
    if start == -1:
        return []
    segment = text[start:end if end != -1 else None]
    return sorted(set(re.findall(r"CLAIM-[A-Z]+-\d{4}", segment)))


def validate_fcl_refs(entries_v0_2, crosswalk):
    live_ids = {entry["claim_id"] for entry in entries_v0_2}
    dangling = []
    resolutions = {}
    for claim_id in load_fcl_001_refs():
        if claim_id in live_ids:
            resolutions[claim_id] = claim_id
            continue
        target = crosswalk.get(claim_id, {}).get("v0_2_id")
        if target and target in live_ids:
            resolutions[claim_id] = target
            continue
        dangling.append(claim_id)
    if dangling:
        raise SystemExit(
            "FCL-001 validation failed: dangling claim references -> " + ", ".join(dangling)
        )
    return {"passed": True, "dangling_fcl_refs": [], "resolutions": resolutions}


def corpus_files():
    files = []
    for dirname in INCLUDE_DIRS:
        root = REPO / dirname
        for path in sorted(root.rglob("*.md")):
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            files.append(path.relative_to(REPO).as_posix())
    for filename in INCLUDE_ROOT_FILES:
        path = REPO / filename
        if path.exists():
            files.append(path.relative_to(REPO).as_posix())
    return sorted(dict.fromkeys(files))


def write_jsonl(path: Path, records):
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_manifest(corpus, entries_v0_2, relation_counts, use_mention_counts, crosswalk, fcl_validation):
    id_counts = Counter(info["status"] for info in crosswalk.values())
    return {
        "source_snapshot": TAG,
        "extractor_version": EXTRACTOR_VERSION,
        "corpus_scope": {
            "included_dirs": INCLUDE_DIRS,
            "included_root_files": INCLUDE_ROOT_FILES,
            "excluded_dirs": EXCLUDE_DIRS,
            "n_files": len(corpus),
        },
        "counts_by_type": dict(sorted(Counter(entry["claim_type"] for entry in entries_v0_2).items())),
        "total_entries": len(entries_v0_2),
        "status_ceiling": "partially_admitted unless context/use_mention lowers support",
        "v0_2_fixes": [
            "core-law block capture",
            "BL-modal sentence-shape filter",
            "negation-context guard",
            "use_mention_flag",
            "DEF-label body attachment",
            "DEP relation typing",
        ],
        "rejection_counts": {
            "bl_modal_rejected_shape": stats["bl_modal_rejected_shape"],
            "def_label_rejected_no_body": stats["def_label_rejected_no_body"],
        },
        "context_sensitive_entries": stats["context_sensitive_entries"],
        "use_mention_counts": dict(sorted(use_mention_counts.items())),
        "dep_relation_counts": dict(sorted(relation_counts.items())),
        "op_chains_rejected_nonvocab": stats["op_chains_nonvocab"],
        "sample_seed": SAMPLE_SEED,
        "id_stability": {
            "prior_inventory": "Grounding/v0/claim_inventory.jsonl",
            "crosswalk": "Grounding/v0_2/id_crosswalk.json",
            "fcl_reference_validation": "passed" if fcl_validation["passed"] else "failed",
            "dangling_fcl_refs": fcl_validation["dangling_fcl_refs"],
        },
        "id_counts": {
            "preserved": id_counts.get("preserved", 0),
            "merged_into": id_counts.get("merged_into", 0),
            "superseded_no_successor": id_counts.get("superseded_no_successor", 0),
            "new_in_v0_2": id_counts.get("new_in_v0_2", 0),
        },
        "bl_validation_sample_size": min(15, sum(1 for entry in entries_v0_2 if entry["claim_type"] == "BL")),
    }


def build_populated_summary(
    manifest,
    entries_v0_2,
    cross_document,
    duplicate_nc,
    old_manifest,
    relation_counts,
    use_mention_counts,
    crosswalk,
):
    counts = manifest["counts_by_type"]
    old_counts = old_manifest.get("counts_by_type", {})
    total_delta = manifest["total_entries"] - old_manifest.get("total_entries", 0)
    bl_delta = counts.get("BL", 0) - old_counts.get("BL", 0)
    def_delta = counts.get("DEF", 0) - old_counts.get("DEF", 0)

    sorted_terms = sorted(cross_document.items(), key=lambda item: (-item[1]["count"], item[0]))[:20]
    sorted_nc = sorted(duplicate_nc.items(), key=lambda item: (-len(item[1]), item[0]))[:20]

    rng = random.Random(SAMPLE_SEED)
    bl_entries = [entry for entry in entries_v0_2 if entry["claim_type"] == "BL"]
    sample_size = min(15, len(bl_entries))
    sampled_bl = rng.sample(bl_entries, sample_size) if sample_size else []
    sampled_bl.sort(key=lambda entry: entry["claim_id"])

    preserved = manifest["id_counts"]["preserved"]
    merged = manifest["id_counts"]["merged_into"]
    retired = manifest["id_counts"]["superseded_no_successor"]
    new_ids = manifest["id_counts"]["new_in_v0_2"]

    def build_audit_note(entry: dict) -> str:
        notes = []
        if entry.get("context_sensitive"):
            notes.append("context-sensitive demotion applied")
        if entry.get("use_mention_flag") != "asserted":
            notes.append(f"use_mention={entry.get('use_mention_flag')}")
        if "BL-corelaw-block" in entry.get("extraction_method", ""):
            notes.append("core-law block capture")
        elif "BL-modal" in entry.get("extraction_method", ""):
            notes.append("modal shape-filtered BL")
        if not notes:
            notes.append("clean asserted BL candidate")
        return "; ".join(notes)

    lines = [
        "# DME V2 - Claim Inventory (POPULATED, v0.2)",
        "",
        "```text",
        "status: grounding instrument / POPULATED",
        f"source_snapshot: {TAG}",
        "extraction_method: extractor v0.2, deterministic pattern grammar",
        "population_status: populated - derived record, append-only",
        "ledger_file: claim_inventory.jsonl (canonical; this doc is a projection of it)",
        "```",
        "",
        "## 1. Run Summary",
        "",
        "```text",
        f"corpus: {manifest['corpus_scope']['n_files']} active-doctrine files",
        "  included: Core, Grammar, Substrates, Regime_Ecologies,",
        "            Agentic_Reasoning, Implementation_Orientation,",
        "            README.md, MEMORY_INDEX.md",
        "  excluded: Archive (active != archive), Meta_Web_Gov_Hub (non-DME)",
        "",
        f"total entries:          {manifest['total_entries']}",
        f"  BL    {counts.get('BL', 0)}",
        f"  DEP   {counts.get('DEP', 0)}",
        f"  DEF   {counts.get('DEF', 0)}",
        f"  NC    {counts.get('NC', 0)}",
        f"  OP    {counts.get('OP', 0)}",
        "",
        f"cross-entry recurrent terms: {len(cross_document)}",
        f"duplicate verbatim NC laws:  {len(duplicate_nc)}",
        f"context-sensitive entries:   {manifest['context_sensitive_entries']}",
        f"use_mention counts:         {dict(sorted(use_mention_counts.items()))}",
        f"BL modal shape rejects:     {manifest['rejection_counts']['bl_modal_rejected_shape']}",
        f"DEF label rejects:          {manifest['rejection_counts']['def_label_rejected_no_body']}",
        f"status ceiling:             {manifest['status_ceiling']}",
        "```",
        "",
        "## 2. Counts by Type",
        "",
        "```text",
        *[
            f"{claim_type:>3}  {counts.get(claim_type, 0)}"
            for claim_type in sorted(counts.keys())
        ],
        "```",
        "",
        "## 3. Comparison Against v0.1",
        "",
        "```text",
        f"total entries delta: {total_delta:+d}  ({old_manifest.get('total_entries', 0)} -> {manifest['total_entries']})",
        f"BL count delta:      {bl_delta:+d}  ({old_counts.get('BL', 0)} -> {counts.get('BL', 0)})",
        f"DEF count delta:     {def_delta:+d}  ({old_counts.get('DEF', 0)} -> {counts.get('DEF', 0)})",
        "DEP relation typing summary:",
        *[f"  {relation}: {count}" for relation, count in sorted(relation_counts.items())],
        f"use_mention counts: {dict(sorted(use_mention_counts.items()))}",
        f"context_sensitive count: {manifest['context_sensitive_entries']}",
        "ID stability crosswalk:",
        f"  preserved: {preserved}",
        f"  merged_into: {merged}",
        f"  superseded_no_successor: {retired}",
        f"  new_in_v0_2: {new_ids}",
        "```",
        "",
        "## 4. Most Recurrent Terms",
        "",
        "```text",
        *[
            f"{term:45s} {info['count']:4d} entries / {info['n_files']:2d} files"
            for term, info in sorted_terms
        ],
        "```",
        "",
        "## 5. Most Repeated NC Laws",
        "",
        "```text",
        *[
            f"{len(claim_ids):3d}x  {law}"
            for law, claim_ids in sorted_nc
        ],
        "```",
        "",
        "## 6. BL Cleanliness Re-sample",
        "",
        f"```text\nsample_seed: {SAMPLE_SEED}",
        *[
            "\n".join([
                f"claim_id: {entry['claim_id']}",
                f"source_file: {entry['source_file']}",
                f"line_range: {entry['line_range'][0]}-{entry['line_range'][1]}",
                f"verbatim_span: {entry['verbatim_span'].replace(chr(10), ' / ')[:220]}",
                f"context_sensitive: {str(entry.get('context_sensitive', False)).lower()}",
                f"use_mention_flag: {entry.get('use_mention_flag', 'unknown')}",
                f"audit_note: {build_audit_note(entry)}",
            ])
            for entry in sampled_bl
        ],
        "```",
        "",
        "## 7. Known v0.2 Limits",
        "",
        "```text",
        "v0.2 remains deterministic Structure + Ledger only",
        "modal coverage is conservative and still syntax-bound",
        "use_mention_flag resolves instrument/example contamination, not full pragmatics",
        "context annotation preserves conditional meaning but does not resolve it",
        "paraphrased non-collapse laws and inference-dependent claims remain out of scope",
        "```",
        "",
        "## 8. Non-Collapse Laws",
        "",
        "```text",
        "v0.2 improvement != semantic understanding",
        "context annotation != resolved meaning",
        "use_mention flag != deletion",
        "related_to != depends_on",
        "cleaner BL != doctrine truth",
        "renumbering != transformation",
        "crosswalk != deletion",
        "merged entry != erased provenance",
        "retired ID != forgotten claim",
        "ID stability != semantic equivalence",
        "```",
        "",
    ]
    return "\n".join(lines)


def main():
    corpus = corpus_files()
    for source_file in corpus:
        parse_file(source_file)

    old_entries = load_v0_entries()
    entries_v0_2, crosswalk, _ = assign_stable_ids(raw_entries, old_entries)
    entries_v0_2.sort(key=lambda entry: (entry["claim_type"], parse_claim_id(entry["claim_id"])[1]))

    cross_document, duplicate_nc = build_recurrence(entries_v0_2)

    relation_counts = Counter(
        entry.get("relation_type", "unspecified")
        for entry in entries_v0_2
        if entry["claim_type"] == "DEP"
    )
    use_mention_counts = Counter(entry.get("use_mention_flag", "unknown") for entry in entries_v0_2)

    fcl_validation = validate_fcl_refs(entries_v0_2, crosswalk)

    GROUNDING_V0_2.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__), GROUNDING_V0_2 / "extract_v0_2.py")

    manifest = build_manifest(corpus, entries_v0_2, relation_counts, use_mention_counts, crosswalk, fcl_validation)
    old_manifest = json.loads((GROUNDING_V0 / "run_manifest.json").read_text(encoding="utf-8"))
    populated_summary = build_populated_summary(
        manifest,
        entries_v0_2,
        cross_document,
        duplicate_nc,
        old_manifest,
        relation_counts,
        use_mention_counts,
        crosswalk,
    )

    write_jsonl(GROUNDING_V0_2 / "claim_inventory.jsonl", entries_v0_2)
    with (GROUNDING_V0_2 / "recurrence_map.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "terms": dict(sorted(cross_document.items(), key=lambda item: (-item[1]["count"], item[0]))),
                "duplicate_nc_laws": duplicate_nc,
            },
            handle,
            indent=1,
            ensure_ascii=False,
        )
    with (GROUNDING_V0_2 / "run_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    with (GROUNDING_V0_2 / "ClaimInventory.POPULATED.v0_2.md").open("w", encoding="utf-8") as handle:
        handle.write(populated_summary)
    with (GROUNDING_V0_2 / "id_crosswalk.json").open("w", encoding="utf-8") as handle:
        json.dump(crosswalk, handle, indent=2, ensure_ascii=False)

    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
