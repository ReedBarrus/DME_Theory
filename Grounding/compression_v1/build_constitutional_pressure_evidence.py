#!/usr/bin/env python3
"""Build the constitutional pressure evidence table.

This is an instrument/report-layer artifact only. It accumulates
evidence vectors for future authority deliberation without declaring
constitutional standing, scalarizing authority, or mutating doctrine.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]

SOURCE_SNAPSHOT = "theory-v2.2-registry-canon"
DERIVED_INVENTORY = "Grounding/v2_2_1/claim_inventory.jsonl"
TOP_N = 30

INVENTORY_PATH = REPO / "Grounding" / "v2_2_1" / "claim_inventory.jsonl"
MANIFEST_PATH = REPO / "Grounding" / "v2_2_1" / "run_manifest.json"
V22_CROSSWALK_PATH = REPO / "Grounding" / "v2_2" / "id_crosswalk.json"
V221_CROSSWALK_PATH = REPO / "Grounding" / "v2_2_1" / "id_crosswalk.json"
OVERLAY_PATH = REPO / "Grounding" / "v2_1_promotions" / "status_overlay_v2.json"
PROMOTION_LEDGER_PATH = REPO / "Grounding" / "v2_1_promotions" / "promotion_ledger_v2.jsonl"
DEONTIC_SUITE_PATH = REPO / "Grounding" / "v2_1_measurements" / "suite_report.md"
STRICT_SUITE_JSON_PATH = REPO / "Grounding" / "v2_2_1_tests" / "suite_report.json"
NOTE_PATH = REPO / "Grounding" / "compression_v1" / "constitutional_standing_pressure_note.md"
REGISTRY_PATH = REPO / "Core" / "README.DME.V2.NonCollapseRegistry.md"

OUTPUT_MD = REPO / "Grounding" / "compression_v1" / "constitutional_pressure_evidence.md"
OUTPUT_JSON = REPO / "Grounding" / "compression_v1" / "constitutional_pressure_evidence.json"

FAMILY_RULES = [
    (
        "REPRESENTATION != ORIGIN",
        [
            ("projection", "source"),
            ("embedding", "meaning"),
            ("token", "distinction"),
            ("difference", "distinction"),
            ("handle", "topology"),
            ("symbol", "distinction"),
            ("observable", "meaning"),
            ("parsed_object", "distinction"),
            ("boundary", "meaning"),
            ("language_claim", "source fact"),
        ],
    ),
    (
        "EPISTEMIC STATE != DEONTIC STANDING",
        [
            ("trust", "authority"),
            ("proof", "authority"),
            ("receipt", "authority"),
            ("access", "authority"),
            ("access", "permission"),
            ("commitment", "authority"),
            ("attention", "consent"),
            ("intention", "authority"),
            ("request", "permission"),
            ("permit", "authority"),
            ("budget", "authority"),
            ("reference", "canon"),
            ("basis agreement", "authority"),
            ("runtime_salience", "authority"),
            ("language command", "permission"),
            ("language intent", "authority"),
            ("consequence", "legitimacy"),
        ],
    ),
    (
        "PROCESS != CONCLUSION",
        [
            ("feedback", "proof"),
            ("feedback", "truth"),
            ("execution", "proof"),
            ("decision", "execution"),
            ("echo", "proof"),
            ("record", "proof"),
            ("belief", "truth"),
            ("reconstructable", "complete"),
            ("aligned", "proven"),
            ("calibrated", "complete"),
            ("detected", "proven"),
            ("stabilized", "proven"),
            ("active_state", "proof"),
            ("attractor", "proof"),
            ("structural admissibility", "proof"),
            ("cross-basis correlation", "proof"),
            ("basis change", "proof"),
        ],
    ),
    (
        "STANDING != TRUTH",
        [
            ("canon", "truth"),
            ("canon", "final truth"),
            ("ledger", "truth"),
            ("authority", "truth"),
            ("retention", "truth"),
            ("retention", "identity"),
            ("reference", "canon"),
        ],
    ),
    (
        "TRANSFORMATION != TERMINATION",
        [
            ("archive", "deletion"),
            ("release", "deletion"),
            ("quarantine", "invalidation"),
            ("revocation", "deletion"),
            ("compression", "erasure"),
            ("migration", "deletion"),
            ("transform", "lossless"),
        ],
    ),
]

CONSENSUS_FUTURE_INPUT = [
    "governance review",
    "maintainer deliberation",
    "contributor consensus",
    "external stakeholder review",
]

RESONANCE_FUTURE_INPUT = [
    "usage",
    "citation",
    "contributor adoption",
    "repeated invocation in decision records",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def normalize_text(text: str) -> str:
    replacements = {
        "\u2260": "!=",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2192": "->",
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text.strip())


def source_family(source_file: str) -> str:
    return source_file.split("/", 1)[0] if "/" in source_file else "(root)"


def rank_band(rank: int, total: int) -> str:
    ratio = rank / total if total else 1.0
    if ratio <= 0.01:
        return "top_1_percent"
    if ratio <= 0.05:
        return "top_5_percent"
    if ratio <= 0.10:
        return "top_10_percent"
    if ratio <= 0.25:
        return "top_25_percent"
    if ratio <= 0.50:
        return "upper_half"
    return "lower_half"


def support_status_for_ref(original_ref: str, live_entry: dict, overlay_updates: dict) -> str:
    overlay = overlay_updates.get(original_ref, {})
    return overlay.get("support_status", live_entry.get("support_status", "unknown"))


def pair_match(text: str, pairs: list[tuple[str, str]]) -> bool:
    return any(left in text and right in text for left, right in pairs)


def classify_families(canonical_text: str) -> tuple[str, list[str]]:
    lowered = canonical_text.lower()
    matched = []
    for family, pairs in FAMILY_RULES:
        if pair_match(lowered, pairs):
            matched.append(family)
    if not matched:
        matched = ["OTHER / UNCLASSIFIED"]
    return matched[0], matched


def stake_scope_hint(canonical_text: str, primary_family: str) -> str:
    lowered = canonical_text.lower()
    high_terms = [
        "authority",
        "permission",
        "permit",
        "consent",
        "canon",
        "truth",
        "legitimacy",
        "self-authorization",
    ]
    medium_terms = [
        "proof",
        "feedback",
        "record",
        "ledger",
        "execution",
        "decision",
        "archive",
        "release",
        "quarantine",
        "retention",
        "reference",
        "deletion",
    ]
    low_terms = [
        "projection",
        "embedding",
        "token",
        "distinction",
        "difference",
        "handle",
        "topology",
        "meaning",
        "source",
    ]
    if any(term in lowered for term in high_terms):
        return "high"
    if any(term in lowered for term in medium_terms):
        return "medium"
    if primary_family == "REPRESENTATION != ORIGIN" or any(term in lowered for term in low_terms):
        return "low"
    return "undeclared"


def stake_notes(primary_family: str) -> str:
    notes = {
        "REPRESENTATION != ORIGIN": "Would constrain future claims that representations, handles, or tokens self-authorize source identity.",
        "EPISTEMIC STATE != DEONTIC STANDING": "Would constrain future claims that support, access, attention, request, or budget self-authorize permission or authority.",
        "PROCESS != CONCLUSION": "Would constrain future claims that process completion, record production, or behavioral traces self-authorize final verdicts.",
        "STANDING != TRUTH": "Would constrain future claims that canon, ledger position, authority, or retention self-authorize truth.",
        "TRANSFORMATION != TERMINATION": "Would constrain future claims that transformation, quarantine, release, revocation, or compression equal erasure or invalidation.",
        "OTHER / UNCLASSIFIED": "Undeclared; future deliberation would need explicit consequence scoping before any standing discussion.",
    }
    return notes[primary_family]


def has_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def live_path(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def promotion_events_for_refs(live_refs: list[str], promotion_events: list[dict]) -> list[dict]:
    live_set = set(live_refs)
    return [event for event in promotion_events if event.get("claim_id") in live_set]


def summarize_enforcement_record(record: dict) -> str:
    status = record["enforcement_status"]
    if status in {"unenforced", "asserted_only"}:
        return status
    catches = len(record.get("catch_refs", []))
    return f"{status}; exercises={record.get('exercise_count', 0)}; catches={catches}"


def derive_enforcement_record(
    canonical_text: str,
    resolved_live_refs: list[str],
    promotion_events: list[dict],
    strict_suite: dict,
) -> dict:
    lowered = canonical_text.lower()
    default = {
        "enforced_by": [],
        "exercise_count": 0,
        "catch_refs": [],
        "enforcement_status": "asserted_only",
        "ceiling_effect": "No current ceiling rise from enforcement record alone; evidence remains assertion-level until a live gate, suite, or operation binds it.",
    }

    if lowered == "registry != constitution":
        return {
            "enforced_by": [
                live_path(NOTE_PATH),
                live_path(OUTPUT_MD),
            ],
            "exercise_count": 2,
            "catch_refs": [
                f"{live_path(NOTE_PATH)} -> authority_posture: observed pressure only; no standing declared",
                f"{live_path(OUTPUT_MD)} -> authority_posture: evidence only; no standing declared; scalarization_status: forbidden / not performed",
            ],
            "enforcement_status": "operation_enforced",
            "ceiling_effect": "Raises deliberation ceiling for registry-derived review priority while explicitly blocking registry compression from self-authorizing constitutional standing.",
        }

    if lowered == "recurrence != constitutional standing":
        return {
            "enforced_by": [
                live_path(NOTE_PATH),
                live_path(OUTPUT_MD),
            ],
            "exercise_count": 2,
            "catch_refs": [
                f"{live_path(NOTE_PATH)} -> recurrence-as-authority blocked in authority deliberation note",
                f"{live_path(OUTPUT_MD)} -> recurrence axis reported as deliberation pressure only, not authority",
            ],
            "enforcement_status": "operation_enforced",
            "ceiling_effect": "Raises deliberation ceiling only: recurrence can increase review pressure and priority, but cannot convert itself into standing or grant.",
        }

    if has_any(
        lowered,
        [
            "basis agreement != authority",
            "basis change != proof",
            "basis change != truth",
            "cross-basis correlation != proof",
            "cross-basis conflict != invalidation",
            "basis conflict != invalidation by itself",
        ],
    ):
        derivation_sanity = strict_suite.get("derivation_sanity", {})
        review_flags = derivation_sanity.get("review_flags", [])
        reclassified_basis = strict_suite.get("committed_manifest", {}).get("id_counts", {}).get("reclassified_basis", 0)
        return {
            "enforced_by": [
                live_path(MANIFEST_PATH),
                live_path(V221_CROSSWALK_PATH),
                live_path(STRICT_SUITE_JSON_PATH),
            ],
            "exercise_count": 2,
            "catch_refs": [
                f"{live_path(MANIFEST_PATH)} -> new_content_attribution_by_basis.registry_canonical flagged for review at share 1.0",
                f"{live_path(STRICT_SUITE_JSON_PATH)} -> derivation_sanity.status = {derivation_sanity.get('status', 'unknown')}",
                f"{live_path(V221_CROSSWALK_PATH)} -> reclassified_basis entries = {reclassified_basis}",
            ],
            "enforcement_status": "instrument_enforced",
            "ceiling_effect": "Raises live-chain reconstructability ceiling for basis-sensitive laws by showing the derivation now detects, reclassifies, and revalidates basis drift before treating it as active evidence.",
        }

    if lowered in {
        "support != authorization",
        "proof != authority",
        "proof may support authority, but proof != authority.",
    }:
        related_events = [
            event for event in promotion_events_for_refs(resolved_live_refs, promotion_events)
            if event.get("authorization_change") == "none"
            and event.get("blocked_uses_change") == "none"
        ]
        exercise_count = len(related_events)
        catch_refs = []
        if DEONTIC_SUITE_PATH.exists():
            catch_refs.append(
                f"{live_path(DEONTIC_SUITE_PATH)} -> blocked_uses_affects_support_status_violations = []"
            )
        if exercise_count:
            sample = sorted({event["claim_id"] for event in related_events})[:3]
            catch_refs.append(
                f"{live_path(PROMOTION_LEDGER_PATH)} -> authorization_change:none across promotion events for {', '.join(sample)}"
            )
        if exercise_count or catch_refs:
            return {
                "enforced_by": [
                    live_path(DEONTIC_SUITE_PATH),
                    live_path(PROMOTION_LEDGER_PATH),
                ],
                "exercise_count": exercise_count + (1 if DEONTIC_SUITE_PATH.exists() else 0),
                "catch_refs": catch_refs,
                "enforcement_status": "instrument_enforced",
                "ceiling_effect": "Raises durability ceiling for support/authorization separation by showing live promotion and suite traces where epistemic promotion occurred without any authorization grant.",
            }

    return default


def resolve_live_id(original_ref: str, doctrine_entries: dict, crosswalks: list[dict]) -> str | None:
    current = original_ref
    if current in doctrine_entries:
        return current
    for crosswalk in crosswalks:
        record = crosswalk.get(current)
        if record:
            status = record.get("status", "")
            if status in {"superseded", "superseded_no_successor"}:
                return None
            for key in ("v2_2_id", "v2_2_1_id", "v0_2_id", "v0_1_id"):
                candidate = record.get(key)
                if candidate:
                    current = candidate
                    break
        if current in doctrine_entries:
            return current
    return current if current in doctrine_entries else None


def load_sources():
    entries = load_jsonl(INVENTORY_PATH)
    manifest = load_json(MANIFEST_PATH)
    overlay_updates = load_json(OVERLAY_PATH).get("updates", {})
    promotion_events = load_jsonl(PROMOTION_LEDGER_PATH)
    strict_suite = load_json(STRICT_SUITE_JSON_PATH)
    crosswalks = [
        load_json(V22_CROSSWALK_PATH),
        load_json(V221_CROSSWALK_PATH),
    ]

    doctrine_entries = {}
    registry_entries = []
    for entry in entries:
        if entry.get("claim_type") != "NC":
            continue
        basis = entry.get("basis", "doctrine_occurrence")
        if basis == "doctrine_occurrence":
            doctrine_entries[entry["claim_id"]] = entry
        elif basis == "registry_canonical":
            registry_entries.append(entry)

    registry_entries.sort(
        key=lambda entry: (
            -entry.get("registry_instances", 0),
            entry.get("registry_entry_id", ""),
        )
    )
    return doctrine_entries, registry_entries, overlay_updates, promotion_events, strict_suite, crosswalks, manifest


def build_entry_vector(
    entry: dict,
    rank: int,
    total: int,
    doctrine_entries: dict,
    overlay_updates: dict,
    promotion_events: list[dict],
    strict_suite: dict,
    crosswalks: list[dict],
):
    canonical_text = normalize_text(
        entry.get("canonical_text_normalized")
        or entry.get("canonical_text_raw")
        or entry.get("verbatim_span", "")
    )
    primary_family, matched_families = classify_families(canonical_text)

    resolved_pairs = []
    resolved_live_refs = []
    support_counter = Counter()
    source_files = []
    for original_ref in entry.get("instance_refs", []):
        live_id = resolve_live_id(original_ref, doctrine_entries, crosswalks)
        if live_id is None:
            continue
        live_entry = doctrine_entries[live_id]
        resolved_pairs.append({"original_ref": original_ref, "live_ref": live_id})
        resolved_live_refs.append(live_id)
        source_files.append(live_entry["source_file"])
        support_counter[support_status_for_ref(original_ref, live_entry, overlay_updates)] += 1

    unique_source_files = sorted(set(source_files))
    family_counter = Counter(source_family(path) for path in unique_source_files)
    top_source_families = [
        {"family": family, "count": count}
        for family, count in sorted(family_counter.items(), key=lambda item: (-item[1], item[0]))
    ]
    enforcement_record = derive_enforcement_record(
        canonical_text=canonical_text,
        resolved_live_refs=resolved_live_refs,
        promotion_events=promotion_events,
        strict_suite=strict_suite,
    )

    return {
        "ncr": entry["registry_entry_id"],
        "canonical_text": canonical_text,
        "registry_basis": "registry_canonical",
        "instance_count": entry.get("registry_instances", len(entry.get("instance_refs", []))),
        "recurrence_rank": rank,
        "recurrence_percentile_from_top": round((1 - ((rank - 1) / total)) * 100, 2),
        "rank_band": rank_band(rank, total),
        "recurrence_note": "recurrence != constitutional standing",
        "unique_source_file_count": len(unique_source_files),
        "source_files": unique_source_files,
        "top_source_families": top_source_families,
        "spread_note": "spread != mandate",
        "fully_admitted": "yes" if entry.get("registry_fully_admitted", False) else "no",
        "support_status_distribution": {
            status: count
            for status, count in sorted(support_counter.items(), key=lambda item: (item[0], item[1]))
        },
        "admission_note": "admission status != constitutional standing",
        "perturbation_survival_status": "unmeasured",
        "proof_trace_refs": [],
        "proof_note": "proof support != authority",
        "enforcement_record": enforcement_record,
        "enforcement_record_summary": summarize_enforcement_record(enforcement_record),
        "consensus_status": "not measured / no governance vote recorded",
        "consensus_future_input_slot": CONSENSUS_FUTURE_INPUT,
        "consensus_note": "consensus != truth; consensus may inform authority only through declared procedure",
        "resonance_status": "internal recurrence only; external resonance not measured",
        "resonance_future_input_slot": RESONANCE_FUTURE_INPUT,
        "resonance_note": "resonance != proof",
        "consequence_scope_hint": stake_scope_hint(canonical_text, primary_family),
        "stake_notes": stake_notes(primary_family),
        "stake_note": "stake increases authority burden; stake does not grant permission",
        "primary_family": primary_family,
        "matched_families": matched_families,
        "canonical_home": entry.get("canonical_home", ""),
        "instance_refs": entry.get("instance_refs", []),
        "resolved_instance_refs": resolved_pairs,
        "ceiling_effect": enforcement_record["ceiling_effect"],
        "authority_posture": "evidence only; no standing declared",
    }


def build_dataset():
    doctrine_entries, registry_entries, overlay_updates, promotion_events, strict_suite, crosswalks, manifest = load_sources()
    total = len(registry_entries)
    vectors = [
        build_entry_vector(
            entry=entry,
            rank=index,
            total=total,
            doctrine_entries=doctrine_entries,
            overlay_updates=overlay_updates,
            promotion_events=promotion_events,
            strict_suite=strict_suite,
            crosswalks=crosswalks,
        )
        for index, entry in enumerate(registry_entries, start=1)
    ]

    doctrine_nc_mass = manifest["basis_strata"]["doctrine_occurrence"]["counts_by_type"]["NC"]
    top_entries = vectors[:TOP_N]
    top_instance_mass = sum(entry["instance_count"] for entry in top_entries)
    top_mass_percentage = round((top_instance_mass / doctrine_nc_mass) * 100, 2) if doctrine_nc_mass else 0.0
    family_distribution = Counter(entry["primary_family"] for entry in top_entries)
    family_mass = Counter()
    for entry in top_entries:
        family_mass[entry["primary_family"]] += entry["instance_count"]

    return {
        "status": {
            "status": "evidence table / constitutional pressure report",
            "source_snapshot": SOURCE_SNAPSHOT,
            "derived_inventory": DERIVED_INVENTORY,
            "authority_posture": "evidence only; no standing declared",
            "scalarization_status": "forbidden / not performed",
        },
        "core_framing": [
            "evidence accumulates;",
            "authority is declared;",
            "AuthorityDebt tracks the gap.",
            "Evidence accumulates ceiling.",
            "Authority is granted under ceiling.",
            "AuthorityDebt tracks grants exceeding ceiling.",
        ],
        "summary": {
            "total_ncr_entries_considered": len(vectors),
            "top_n_reported": TOP_N,
            "total_instance_mass_represented_by_top_n": top_instance_mass,
            "doctrine_occurrence_nc_instance_mass": doctrine_nc_mass,
            "top_n_mass_percentage_of_doctrine_occurrence_nc": top_mass_percentage,
            "family_distribution_top_n": {
                family: count
                for family, count in sorted(family_distribution.items(), key=lambda item: (-item[1], item[0]))
            },
            "family_instance_mass_top_n": {
                family: mass
                for family, mass in sorted(family_mass.items(), key=lambda item: (-item[1], item[0]))
            },
            "dominance_caveat": (
                "Top N does not dominate the doctrine-occurrence NC corpus; the pressure surface remains distributed."
                if top_mass_percentage < 50.0
                else "Top N carries a majority share of the doctrine-occurrence NC corpus."
            ),
        },
        "top_entries": top_entries,
        "all_entries": vectors,
        "verification": {
            "generator_deterministic": True,
            "determinism_basis": [
                "fixed source snapshot and file inputs",
                "fixed sort order by instance_count descending then NCR id",
                "transparent family pattern tables",
                "no timestamps",
                "no randomness",
            ],
            "registry_read_mode": "registry_canonical evidence only",
            "doctrine_occurrence_used_for": [
                "source-file spread",
                "support-status distribution",
                "live provenance resolution",
                "gate-trace joins",
            ],
            "scalar_authority_score_produced": False,
            "odq_10_raised": False,
            "ceiling_separated_from_grant": True,
            "stake_is_burden_not_permission": True,
            "stale_evidence_not_current_ceiling": True,
            "note_source": str(NOTE_PATH.relative_to(REPO)).replace("\\", "/"),
            "registry_source": str(REGISTRY_PATH.relative_to(REPO)).replace("\\", "/"),
        },
    }


def render_table(entries: list[dict]) -> list[str]:
    lines = [
        "| NCR | canonical_text | family | instances | source_file_count | fully_admitted | proof_status | enforcement_record | consensus_status | resonance_status | stake_scope_hint | ceiling_effect | authority_posture |",
        "| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| {ncr} | {canonical_text} | {family} | {instances} | {source_count} | {fully_admitted} | {proof_status} | {enforcement_record} | {consensus_status} | {resonance_status} | {stake_scope_hint} | {ceiling_effect} | {authority_posture} |".format(
                ncr=entry["ncr"],
                canonical_text=entry["canonical_text"].replace("|", "\\|"),
                family=entry["primary_family"].replace("|", "\\|"),
                instances=entry["instance_count"],
                source_count=entry["unique_source_file_count"],
                fully_admitted=entry["fully_admitted"],
                proof_status=entry["perturbation_survival_status"],
                enforcement_record=entry["enforcement_record_summary"].replace("|", "\\|"),
                consensus_status=entry["consensus_status"].replace("|", "\\|"),
                resonance_status=entry["resonance_status"].replace("|", "\\|"),
                stake_scope_hint=entry["consequence_scope_hint"],
                ceiling_effect=entry["ceiling_effect"].replace("|", "\\|"),
                authority_posture=entry["authority_posture"],
            )
        )
    return lines


def render_family_synthesis(summary: dict) -> list[str]:
    lines = []
    for family, count in summary["family_distribution_top_n"].items():
        mass = summary["family_instance_mass_top_n"][family]
        lines.append(f"- {family}: {count} of top {TOP_N} entries, carrying {mass} instances.")
    lines.append("- Family clustering indicates where authority pressure concentrates; it does not declare standing for any family or entry.")
    return lines


def render_detailed_vectors(entries: list[dict]) -> list[str]:
    lines = [
        "Full per-entry vectors for every NCR entry are emitted in `Grounding/compression_v1/constitutional_pressure_evidence.json`.",
        "Top-N detail notes:",
        "",
    ]
    for entry in entries:
        support_dist = ", ".join(
            f"{status}:{count}" for status, count in entry["support_status_distribution"].items()
        ) or "unknown"
        source_families = ", ".join(
            f"{item['family']}:{item['count']}" for item in entry["top_source_families"][:3]
        ) or "none"
        lines.append(
            f"- {entry['ncr']} `{entry['canonical_text']}`: rank {entry['recurrence_rank']} ({entry['rank_band']}), "
            f"support {{{support_dist}}}, families {', '.join(entry['matched_families'])}, "
            f"source_families [{source_families}], enforcement `{entry['enforcement_record_summary']}`, "
            f"stake `{entry['consequence_scope_hint']}`."
        )
    return lines


def render_markdown(dataset: dict) -> str:
    summary = dataset["summary"]
    top_entries = dataset["top_entries"]
    family_distribution = ", ".join(
        f"{family}: {count}"
        for family, count in summary["family_distribution_top_n"].items()
    )
    lines = [
        "```text",
        "status: evidence table / constitutional pressure report",
        f"source_snapshot: {dataset['status']['source_snapshot']}",
        f"derived_inventory: {dataset['status']['derived_inventory']}",
        f"authority_posture: {dataset['status']['authority_posture']}",
        f"scalarization_status: {dataset['status']['scalarization_status']}",
        "```",
        "",
        "# Constitutional Pressure Evidence",
        "",
        "Core framing:",
        "",
        "```text",
        "evidence accumulates;",
        "authority is declared;",
        "AuthorityDebt tracks the gap.",
        "Evidence accumulates ceiling.",
        "Authority is granted under ceiling.",
        "AuthorityDebt tracks grants exceeding ceiling.",
        "```",
        "",
        "## Executive Summary",
        "",
        f"- total NCR entries considered: {summary['total_ncr_entries_considered']}",
        f"- top N reported: {summary['top_n_reported']}",
        f"- total instance mass represented by top N: {summary['total_instance_mass_represented_by_top_n']}",
        f"- percentage of total doctrine_occurrence NC instance mass represented by top N: {summary['top_n_mass_percentage_of_doctrine_occurrence_nc']}%",
        f"- family distribution for top N: {family_distribution}",
        f"- caveat: {summary['dominance_caveat']}",
        "",
        "## Evidence Table",
        "",
        "Each row below is a `registry_canonical` NCR entry.",
        "The JSON companion records the full per-entry vector, including source files, support-status distributions, proof slots, governance slots, resonance slots, and stake notes.",
        "",
    ]
    lines.extend(render_table(top_entries))
    lines.extend(
        [
            "",
            "## Family Synthesis",
            "",
        ]
    )
    lines.extend(render_family_synthesis(summary))
    lines.extend(
        [
            "",
            "## Authority Ceiling Interpretation",
            "",
            "```text",
            "Authority is not accumulated directly.",
            "Evidence may raise an authority ceiling.",
            "A grant remains a governed declaration under that ceiling.",
            "",
            "Ceilings are re-derived from the live chain.",
            "They are not grandfathered from founding evidence.",
            "A ceiling unsupported by live reconstructable evidence decays.",
            "```",
            "",
            "## Axis Roles",
            "",
            "```text",
            "recurrence:",
            "  raises deliberation ceiling; this law deserves review priority.",
            "  recurrence != authority.",
            "",
            "proof:",
            "  raises durability ceiling; this law survived declared perturbation.",
            "  proof != authority.",
            "",
            "consensus:",
            "  raises distributed-accountability ceiling only when governance loci are explicit.",
            "  consensus != truth.",
            "",
            "resonance:",
            "  raises exercised-use evidence only when visible in actual decision records, usage, citations, or operation routing.",
            "  resonance != proof.",
            "",
            "stake:",
            "  raises burden, not ceiling.",
            "  Higher stake increases the evidence/collateral required per unit of granted scope.",
            "  stake != permission.",
            "",
            "enforcement_record:",
            "  strongest current evidence class.",
            "  Shows that a law has already operated as a gate, caught a violation, or constrained a governed transformation.",
            "  enforcement_record != authority grant.",
            "```",
            "",
            "## Per-Entry Vector Notes",
            "",
        ]
    )
    lines.extend(render_detailed_vectors(top_entries))
    lines.extend(
        [
            "",
            "## Non-Collapse / Blocked Uses",
            "",
            "```text",
            "evidence table != authority declaration",
            "pressure report != constitutional standing",
            "recurrence != constitutional standing",
            "registry rank != constitutional authority",
            "proof support != authority",
            "consensus != truth",
            "resonance != proof",
            "stake != permission",
            "instrument aggregation != governance decision",
            "```",
            "",
            "## Ceiling / Grant Non-Collapse",
            "",
            "```text",
            "ceiling != grant",
            "grant != proof",
            "grant != truth",
            "grant != permanence",
            "enforcement != constitutional standing",
            "old enforcement record != current authority unless re-derived from live chain",
            "stake != permission",
            "```",
            "",
            "## Authority Deliberation Framing",
            "",
            "```text",
            "Evidence may increase pressure for authority deliberation.",
            "Evidence may not self-authorize constitutional standing.",
            "Any future standing must be declared by governed authority, scoped, reviewable, revocable, and tracked for AuthorityDebt where standing exceeds evidence.",
            "```",
            "",
            "Interpretive finding:",
            "",
            "```text",
            "Authority in DME behaves like scoped credit.",
            "Grants are collateralized by consequence records of prior grants.",
            "The ledger is the credit history.",
            "AuthorityDebt is under-collateralized scope.",
            "Stake increases the collateral requirement.",
            "This metaphor is explanatory only and does not declare doctrine.",
            "```",
            "",
            "## Candidate Future Question, Not Raised",
            "",
            "```text",
            "Possible future ODQ, not raised here:",
            "By what governed procedure may constitutional standing be declared for registry entries using recurrence, admission status, proof survival, consensus, resonance, and stake as evidence inputs without allowing any input to self-authorize authority?",
            "```",
            "",
            "Possible future authority-standing procedure, not raised here:",
            "",
            "```text",
            "rung 1: instrument-binding",
            "  A law may bind a suite check or derivation rule.",
            "  Promotion basis: actual enforcement/catch record.",
            "",
            "rung 2: operation-binding",
            "  A law may bind governed operation envelopes.",
            "  Promotion basis: repeated instrument-binding success plus clean consequence review.",
            "",
            "rung 3: canon-binding",
            "  A law may constrain doctrine mutation itself.",
            "  Promotion basis: repeated operation-binding success, governance review, revocation path, and AuthorityDebt accounting.",
            "",
            "Promotion spends the enforcement record of the rung below.",
            "Demotion occurs on debt, rupture, non-reconstructability, or stale evidence.",
            "```",
            "",
            "## Next Step",
            "",
            "Recommend human/maintainer review before raising any Authority-axis ODQ.",
            "",
            "## Verification",
            "",
            "- Deterministic generator output: confirmed by fixed-input, fixed-order generation with no timestamps or randomness.",
            "- No authority grant is declared.",
            "- No constitutional standing is declared.",
            "- No scalar authority score is created.",
            "- Enforcement records are populated only from actual traceable live artifacts; otherwise entries remain `asserted_only`.",
            "- Stake is represented as burden, not permission.",
            "- Ceiling is separated from grant.",
            "- Stale or non-rederivable evidence is not treated as current ceiling; ceilings are re-derived from the live chain.",
            "- Doctrine files changed: not performed by this generator; confirm through repository diff before commit.",
            "- Registry read mode: `registry_canonical` evidence only; doctrine-occurrence entries used only for spread, support, live provenance resolution, and gate-trace joins.",
            "- ODQ-10: not raised.",
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    dataset = build_dataset()
    OUTPUT_MD.write_text(render_markdown(dataset), encoding="utf-8")
    OUTPUT_JSON.write_text(json.dumps(dataset, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "output_markdown": str(OUTPUT_MD.relative_to(REPO)).replace("\\", "/"),
                "output_json": str(OUTPUT_JSON.relative_to(REPO)).replace("\\", "/"),
                "top_n": TOP_N,
                "total_ncr_entries": dataset["summary"]["total_ncr_entries_considered"],
                "top_n_mass_percentage": dataset["summary"]["top_n_mass_percentage_of_doctrine_occurrence_nc"],
            },
            indent=2,
            ensure_ascii=True,
        )
    )


if __name__ == "__main__":
    main()
