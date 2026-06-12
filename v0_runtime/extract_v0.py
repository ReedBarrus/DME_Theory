#!/usr/bin/env python3
"""DME v0 claim extractor — implements LanguageAdmissionPrototype spec.
Substrates exercised: Structure (parse), Ledger (record). Nothing else.
extraction_method version: v0.1
"""
import json, re, os, sys
from collections import defaultdict

REPO = "/home/claude/DME_Theory"
TAG = "theory-v2.0-pre-grounding"
EXTRACTOR_VERSION = "v0.1"

# Corpus scope: active doctrine only (declared in run manifest)
INCLUDE_DIRS = ["Core", "Grammar", "Substrates", "Regime_Ecologies",
                "Agentic_Reasoning", "Implementation_Orientation"]
INCLUDE_ROOT_FILES = ["README.md", "MEMORY_INDEX.md"]
EXCLUDE_DIRS = ["Archive", "Meta_Web_Gov_Hub"]  # active!=archive; non-DME material

# Operator vocabulary from Grammar/README.DME.V2.OperatorGrammar.md headings
# + recent patch span operators (Detect/Declare/Classify/Route/Determine)
OPERATOR_VOCAB = {
    "Accept","Archive","Authorize","Bound","Canonize","Compare","Consent",
    "Contest","Differentiate","Echo","Execute","Expose","Integrate","Permit",
    "Project","Prove","Reconcile","Record","Reference","Relate","Release",
    "Repair","Revoke","Select","Simulate","Transform","Translate",
    "Detect","Declare","Classify","Route","Determine","Chart","Ingest",
    "DetectRupture","DeclareRupture",
}

AXES_EVAL = ["Distinction", "Ledger"]
AXES_OMIT = ["Constraint","Identity","Projection","Feedback","Consequence",
             "Proof","Authority","Budget"]

counters = defaultdict(int)
entries = []
stats = defaultdict(int)

def make_entry(ctype, sf, lstart, lend, cstart, cend, verbatim, terms,
               scale, section, fence, pattern_id, notes=""):
    counters[ctype] += 1
    eid = f"CLAIM-{ctype}-{counters[ctype]:04d}"
    entries.append({
        "claim_id": eid,
        "claim_type": ctype,
        "source_file": sf,
        "line_range": [lstart, lend],
        "char_span": [cstart, cend],
        "source_snapshot": TAG,
        "verbatim_span": verbatim.strip()[:400],
        "normalized_terms": terms,
        "scale_band": scale,
        "section_context": section,
        "in_fenced_block": fence,
        "evaluated_axes": AXES_EVAL,
        "omitted_axes": AXES_OMIT,
        "opacity_status": "partially_supported",
        "support_status": "partially_admitted",
        "recurrence_refs": [],
        "extraction_method": f"pattern:{pattern_id};extractor:{EXTRACTOR_VERSION}",
        "notes": notes,
    })
    return eid

def norm_term(t):
    t = t.strip().strip('"\'`*.,;:()[]')
    t = re.sub(r"\s+", " ", t)
    return t.lower().replace(" ", "_")

# ---------- file parsing (RootSymbolChart-lite) ----------

def parse_file(relpath):
    path = os.path.join(REPO, relpath)
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    lines = text.split("\n")
    # char offset of each line start
    offs, pos = [], 0
    for ln in lines:
        offs.append(pos); pos += len(ln) + 1

    heading_chain = []   # (level, title)
    core_law_pending = [False]  # prose 'Core law:' label tags next fence
    in_fence = False
    fence_lines = []     # (lineno, text) accumulated inside current fence
    fence_start = 0
    in_meta = False      # first fence containing 'status:' = metadata block
    seen_first_fence = False

    def section():
        return " > ".join(h[1] for h in heading_chain) or "(root)"

    for i, raw in enumerate(lines):
        line = raw.rstrip()
        ln = i + 1

        if line.lstrip().startswith("```"):
            if not in_fence:
                in_fence = True; fence_lines = []; fence_start = ln
                fence_is_core_law = core_law_pending[0]; core_law_pending[0] = False
            else:
                # fence closed -> process block
                block_is_meta = (not seen_first_fence) and any(
                    re.match(r"\s*(status|schema posture|folder)\s*:", t)
                    for _, t in fence_lines)
                seen_first_fence = True
                process_fenced_block(relpath, fence_lines, section(),
                                     offs, block_is_meta, fence_is_core_law)
                in_fence = False
            continue

        if in_fence:
            fence_lines.append((ln, line))
            continue

        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            lvl = len(m.group(1))
            while heading_chain and heading_chain[-1][0] >= lvl:
                heading_chain.pop()
            heading_chain.append((lvl, m.group(2).strip()))
            continue

        if CORE_LAW.match(line.strip()):
            core_law_pending[0] = True
        process_prose_line(relpath, ln, line, section(), offs)

# ---------- pattern passes ----------

NC_INLINE = re.compile(r"^(.{1,80}?)\s*(?:!=|≠)\s*(.{1,80})$")
NC_ISNOT = re.compile(r"\b([A-Z][A-Za-z_/ -]{1,50}?)\s+is not\s+(?:an?\s+|the\s+)?([A-Za-z][A-Za-z_/ -]{1,50}?)(?:[.,;]|$)")
NC_IMPLY = re.compile(r"\b([A-Za-z_/ -]{2,60}?)\s+does not (?:imply|mean|equal|guarantee)\s+([A-Za-z_/ -]{2,60}?)(?:[.,;]|$)")
NC_COLLAPSE = re.compile(r"\b([A-Za-z_/ -]{2,60}?)\s+must not be (?:collapsed|confused) (?:with|into)\s+([A-Za-z_/ -]{2,60}?)(?:[.,;]|$)")

DEF_TERM_EQ = re.compile(r"^([A-Za-z][A-Za-z_/ ()-]{0,60}?)\s*=\s*$")
DEF_INLINE_EQ = re.compile(r"^([A-Za-z][A-Za-z_/ ()-]{0,60}?)\s*=\s*(.{3,})$")
DEF_LABEL = re.compile(r"^Definition\s*:\s*(.*)$", re.I)

BL_MODAL = re.compile(r"\b(may not|must not|must|never|requires?|only when|only if|cannot)\b", re.I)
CORE_LAW = re.compile(r"^Core law", re.I)

ARROW_SPLIT = re.compile(r"\s*(?:→|->)\s*")
DEP_REF = re.compile(r"(?:defined|specified)\s+(?:later\s+)?in\s+([A-Za-z0-9_./]+\.md)", re.I)
DEP_DOWNSTREAM = re.compile(r"\b([A-Za-z_/ -]{2,60}?)\s+is downstream of\s+([A-Za-z_/ -]{2,60}?)(?:[.,;]|$)")
DEP_LIST_ITEM = re.compile(r"^\s*-\s+([A-Za-z0-9_./ ]+\.md)\s*$")

def first_words(s, n=6):
    return norm_term(" ".join(s.split()[:n]))

def process_fenced_block(sf, flines, section, offs, is_meta, is_core_law=False):
    if not flines:
        return
    pending_core_law = False
    # DEP from metadata blocks
    if is_meta:
        in_rel = False
        for ln, t in flines:
            if re.match(r"\s*(related|depends_on)\s*:", t):
                in_rel = True; continue
            if in_rel:
                m = DEP_LIST_ITEM.match(t)
                if m:
                    make_entry("DEP", sf, ln, ln, offs[ln-1], offs[ln-1]+len(t),
                               t, [norm_term(os.path.basename(sf)),
                                   norm_term(os.path.basename(m.group(1))),
                                   "depends_on"],
                               "document", section, True, "DEP-meta")
                elif t.strip() and not t.startswith("  "):
                    in_rel = False
        return

    i = 0
    n = len(flines)
    while i < n:
        ln, t = flines[i]
        ts = t.strip()
        if not ts:
            i += 1; continue

        # NC inline (!= / ≠) — highest precedence in fenced doctrine
        m = NC_INLINE.match(ts)
        if m and not ts.startswith("="):
            l, r = m.group(1), m.group(2)
            if l.strip() and r.strip():
                make_entry("NC", sf, ln, ln, offs[ln-1], offs[ln-1]+len(t), ts,
                           [norm_term(l), norm_term(r), "non_equivalence"],
                           "sentence/doctrine_law", section, True, "NC-symbol")
                stats["nc_fenced"] += 1
                i += 1; continue

        # DEF: "Term =" then body lines until blank
        m = DEF_TERM_EQ.match(ts)
        if m:
            term = m.group(1)
            body, j, endln = [], i+1, ln
            while j < n and flines[j][1].strip():
                body.append(flines[j][1].strip()); endln = flines[j][0]; j += 1
            if body:
                verb = ts + " " + " ".join(body)
                make_entry("DEF", sf, ln, endln, offs[ln-1],
                           offs[endln-1]+len(flines[j-1][1]), verb,
                           [norm_term(term), "defined_as", first_words(" ".join(body))],
                           "sentence", section, True, "DEF-block")
                i = j; continue

        # OP: arrow chain — single line or multi-line block
        if ("→" in ts or "->" in ts) or ts.startswith(("→","->")):
            # assemble multi-line chain: current + following lines starting with arrow
            chain_text = [ts]; endln = ln; j = i+1
            while j < n and flines[j][1].strip().startswith(("→","->")):
                chain_text.append(flines[j][1].strip()); endln = flines[j][0]; j += 1
            full = " ".join(chain_text)
            elems = [e.strip() for e in ARROW_SPLIT.split(full) if e.strip()]
            ops = [e for e in elems
                   if e.split()[0].strip("():,") in OPERATOR_VOCAB
                   or e.split("(")[0].strip() in OPERATOR_VOCAB]
            if len(elems) >= 2 and len(ops) >= 2:
                make_entry("OP", sf, ln, endln, offs[ln-1],
                           offs[endln-1]+len(flines[j-1][1] if j-1 < n else t),
                           full, [norm_term(o.split("(")[0]) for o in ops],
                           "span", section, True, "OP-chain",
                           notes=f"{len(ops)}/{len(elems)} elements in operator vocab")
                stats["op_admitted"] += 1
                i = j; continue
            elif len(elems) >= 2:
                stats["op_chains_nonvocab"] += 1
                i = j; continue

        # BL inside fenced blocks: Core law label or modal patterns
        if CORE_LAW.match(ts):
            pending_core_law = True
            i += 1; continue
        if (BL_MODAL.search(ts) or is_core_law) and len(ts) <= 220 and not ts.endswith('?'):
            pid = "BL-corelaw" if (pending_core_law or is_core_law) else "BL-modal"
            make_entry("BL", sf, ln, ln, offs[ln-1], offs[ln-1]+len(t), ts,
                       [first_words(ts, 8)],
                       "sentence/doctrine_law", section, True, pid)
            pending_core_law = False
            i += 1; continue

        # NC textual forms inside fences
        for rx, pid in ((NC_ISNOT,"NC-isnot"),(NC_IMPLY,"NC-imply"),
                        (NC_COLLAPSE,"NC-collapse")):
            m = rx.search(ts)
            if m:
                make_entry("NC", sf, ln, ln, offs[ln-1], offs[ln-1]+len(t), ts,
                           [norm_term(m.group(1)), norm_term(m.group(2)),
                            "non_equivalence"],
                           "sentence/doctrine_law", section, True, pid)
                break
        i += 1

def process_prose_line(sf, ln, line, section, offs):
    ts = line.strip()
    if not ts or ts.startswith(("|","<",">","-")) and not DEP_LIST_ITEM.match(ts):
        # still allow DEP refs in prose below
        pass
    if not ts:
        return
    base = offs[ln-1]

    # DEP forward references in prose
    for m in DEP_REF.finditer(ts):
        make_entry("DEP", sf, ln, ln, base, base+len(line), ts,
                   [norm_term(os.path.basename(sf)),
                    norm_term(os.path.basename(m.group(1))), "forward_ref"],
                   "document", section, False, "DEP-ref")
    m = DEP_DOWNSTREAM.search(ts)
    if m:
        make_entry("DEP", sf, ln, ln, base, base+len(line), ts,
                   [norm_term(m.group(1)), norm_term(m.group(2)), "downstream_of"],
                   "document", section, False, "DEP-downstream")

    # NC textual in prose
    for rx, pid in ((NC_IMPLY,"NC-imply"),(NC_COLLAPSE,"NC-collapse")):
        m = rx.search(ts)
        if m:
            make_entry("NC", sf, ln, ln, base, base+len(line), ts,
                       [norm_term(m.group(1)), norm_term(m.group(2)),
                        "non_equivalence"],
                       "sentence/doctrine_law", section, False, pid)
            return
    # NC symbol in prose
    if ("!=" in ts or "≠" in ts):
        m = NC_INLINE.match(ts)
        if m:
            make_entry("NC", sf, ln, ln, base, base+len(line), ts,
                       [norm_term(m.group(1)), norm_term(m.group(2)),
                        "non_equivalence"],
                       "sentence/doctrine_law", section, False, "NC-symbol")
            return
    # DEF label in prose
    m = DEF_LABEL.match(ts)
    if m:
        make_entry("DEF", sf, ln, ln, base, base+len(line), ts,
                   [first_words(m.group(1) or "following", 6), "definition_label"],
                   "sentence", section, False, "DEF-label")

# ---------- run ----------

corpus = []
for d in INCLUDE_DIRS:
    for root, _, files in os.walk(os.path.join(REPO, d)):
        for fn in sorted(files):
            if fn.endswith(".md"):
                corpus.append(os.path.relpath(os.path.join(root, fn), REPO))
for fn in INCLUDE_ROOT_FILES:
    if os.path.exists(os.path.join(REPO, fn)):
        corpus.append(fn)
corpus.sort()

for rel in corpus:
    parse_file(rel)

# ---------- RecurrencePass (computed, not pre-declared) ----------
term_map = defaultdict(list)
for e in entries:
    for t in e["normalized_terms"]:
        if t and t not in ("non_equivalence","defined_as","depends_on",
                           "forward_ref","downstream_of","definition_label"):
            term_map[t].append(e["claim_id"])

id2entry = {e["claim_id"]: e for e in entries}
for t, ids in term_map.items():
    if len(ids) > 1:
        for cid in ids:
            refs = [x for x in ids if x != cid]
            id2entry[cid]["recurrence_refs"] = sorted(
                set(id2entry[cid]["recurrence_refs"]) | set(refs))[:50]

# cross-document recurrence
xdoc = {}
for t, ids in term_map.items():
    files = {id2entry[i]["source_file"] for i in ids}
    if len(ids) > 1:
        xdoc[t] = {"count": len(ids), "files": sorted(files),
                   "n_files": len(files), "claim_ids": sorted(ids)}

# duplicate verbatim NC laws (compression signal)
verb_map = defaultdict(list)
for e in entries:
    if e["claim_type"] == "NC":
        key = re.sub(r"\s+"," ", e["verbatim_span"].replace("≠","!=")).lower()
        verb_map[key].append(e["claim_id"])
dupes = {k: v for k, v in verb_map.items() if len(v) > 1}

# ---------- outputs ----------
OUT = "/home/claude/out_v0"
os.makedirs(OUT, exist_ok=True)
with open(f"{OUT}/claim_inventory.jsonl","w") as f:
    for e in entries:
        f.write(json.dumps(e, ensure_ascii=False)+"\n")
with open(f"{OUT}/recurrence_map.json","w") as f:
    json.dump({"terms": dict(sorted(xdoc.items(),
              key=lambda kv:-kv[1]["count"])),
              "duplicate_nc_laws": dupes}, f, indent=1, ensure_ascii=False)
manifest = {
    "source_snapshot": TAG, "extractor_version": EXTRACTOR_VERSION,
    "corpus_scope": {"included_dirs": INCLUDE_DIRS,
                     "included_root_files": INCLUDE_ROOT_FILES,
                     "excluded_dirs": EXCLUDE_DIRS,
                     "n_files": len(corpus)},
    "counts_by_type": dict(counters),
    "total_entries": len(entries),
    "op_chains_rejected_nonvocab": stats["op_chains_nonvocab"],
    "status_ceiling": "partially_admitted (per spec section 7)",
}
with open(f"{OUT}/run_manifest.json","w") as f:
    json.dump(manifest, f, indent=1)
print(json.dumps(manifest, indent=1))
print(f"\nrecurrent terms (cross-entry): {len(xdoc)}")
print(f"duplicate verbatim NC laws: {len(dupes)}")
top = sorted(xdoc.items(), key=lambda kv: -kv[1]["count"])[:15]
for t, info in top:
    print(f"  {t:45s} {info['count']:3d} entries across {info['n_files']:2d} files")
