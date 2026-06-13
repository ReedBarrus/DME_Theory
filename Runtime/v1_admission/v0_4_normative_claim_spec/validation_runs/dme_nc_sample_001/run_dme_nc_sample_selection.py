import json
import random
from pathlib import Path


RUN_ID = "dme_nc_sample_001"
SEED = 20260613
SAMPLE_SIZE = 50


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def resolve_inventory(root: Path) -> Path:
    candidates = [
        root / "Grounding" / "v2_2_1" / "claim_inventory.jsonl",
        root / "Grounding" / "v2_2_1" / "claim_inventory.jsonl".replace("/", "\\"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Unable to locate Grounding/v2_2_1/claim_inventory.jsonl")


def normalized_claim_content(entry: dict) -> str:
    normalized_terms = entry.get("normalized_terms") or []
    if normalized_terms:
        return " || ".join(str(term) for term in normalized_terms)
    return str(entry.get("verbatim_span", "")).strip().lower()


def select_unique_nc_population(inventory_path: Path) -> tuple[list[dict], str]:
    unique = {}
    with inventory_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            entry = json.loads(line)
            if entry.get("claim_type") != "NC":
                continue
            if entry.get("basis") != "doctrine_occurrence":
                continue
            normalized_text = normalized_claim_content(entry)
            if not normalized_text:
                continue
            if normalized_text in unique:
                continue
            unique[normalized_text] = {
                "source_claim_id": entry.get("claim_id", ""),
                "source_file": entry.get("source_file", ""),
                "line_range": entry.get("line_range", []),
                "raw_text": entry.get("verbatim_span", ""),
                "normalized_text": normalized_text,
                "basis": "doctrine_occurrence",
                "claim_type": "NC",
            }
    ordered = sorted(
        unique.values(),
        key=lambda entry: (
            entry["normalized_text"],
            entry["source_claim_id"],
            entry["source_file"],
            entry["line_range"],
        ),
    )
    return ordered, str(inventory_path.relative_to(repo_root())).replace("\\", "/")


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")


def main() -> None:
    root = repo_root()
    run_dir = Path(__file__).resolve().parent
    blind_dir = run_dir / "blind_regrade_packet"
    blind_dir.mkdir(parents=True, exist_ok=True)

    inventory_path = resolve_inventory(root)
    population, resolved_path = select_unique_nc_population(inventory_path)
    if len(population) < SAMPLE_SIZE:
        raise ValueError(f"Population too small for sample_size {SAMPLE_SIZE}: {len(population)}")

    sampler = random.Random(SEED)
    selected = sampler.sample(population, SAMPLE_SIZE)
    selected = sorted(selected, key=lambda entry: entry["normalized_text"])

    sampled_rows = []
    regrade_template_rows = []
    for index, entry in enumerate(selected):
        sampled_row = {"sample_index": index, **entry}
        sampled_rows.append(sampled_row)
        regrade_template_rows.append(
            {
                "sample_index": index,
                "source_claim_id": entry["source_claim_id"],
                "source_text": entry["raw_text"],
                "projection_status": "",
                "actor": None,
                "polarity": "",
                "action": "",
                "object": "",
                "comparison_or_target": "",
                "scope": None,
                "rationale": None,
                "omitted_fields": [],
                "invented_fields": [],
                "judge_notes": "",
                "confidence": "",
            }
        )

    manifest = {
        "run_id": RUN_ID,
        "spec_path": "Runtime/v1_admission/v0_4_normative_claim_spec/",
        "source_population": resolved_path,
        "population_filter": {
            "claim_type": "NC",
            "basis": "doctrine_occurrence",
            "exclude_basis": ["registry_canonical"],
            "unique_by": "normalized_claim_content",
        },
        "sample_size": SAMPLE_SIZE,
        "seed": SEED,
        "doctrine_mutation_allowed": False,
        "authority_grant_allowed": False,
        "full_projection_allowed": False,
        "purpose": "test H3 bridge hypothesis under predeclared falsification criteria",
        "preliminary_judge_status": "primed_non_independent",
        "independent_regrade_required": True,
    }

    write_json(run_dir / "sample_manifest.json", manifest)
    write_jsonl(run_dir / "sampled_nc_claims.jsonl", sampled_rows)
    write_jsonl(blind_dir / "sampled_nc_claims.jsonl", sampled_rows)
    write_jsonl(blind_dir / "regrade_template.jsonl", regrade_template_rows)


if __name__ == "__main__":
    main()
