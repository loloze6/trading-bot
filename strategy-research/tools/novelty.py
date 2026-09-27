"""
novelty -- the ONE definition of "this exact thing was already tested"
(E-036 S2a, delivery_plan_v26.md slice 8.1; spec:
engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md and its operator decision of
2026-09-27: "one key, one source").

The exact-match key (card K) is

    (forecast_hash, tuple(sorted(symbols)), timeframe, window_set)

  * forecast_hash -- run_phase1_research._compute_forecast_hash: sha256 of the
    config's canonical JSON (json.dumps(..., sort_keys=True)). The trial row
    carries it; campaign_memory.yaml copies it per tested variant.
  * symbols -- the symbols the backtest runs (memory: measured from
    protocol_result.yaml; before a backtest: the protocol file's `symbols`,
    which is what tools/run_protocol.py iterates).
  * timeframe and window_set -- read from the PROTOCOL FILE the engine runs
    (protocol_spec): its `timeframe`, and a content hash of its `windows`.
    Never the raw protocol path: generated protocols are per-run file names
    (protocols/<run_id>_generated.json), so a path would never repeat. Only
    when the protocol file cannot be read does the key fall back to the
    memory entry's own (card) timeframe and "unresolved:<ref>" -- a key that
    can never equal a resolved one.

The only source of truth is campaign_record/campaign_memory.yaml
(tools/campaign_memory.py, written by the regroup_record stage). A run with
no memory entry (every run before that stage, never backfilled) and an entry
marked `legacy: true` can never produce a REPEAT.

Extracted verbatim from tools/decide_next.py (E-059 S2a), which imports it
back; tools/anti_adjacency_gate.py (the 5a gate) imports the same functions,
so the two call sites can never drift on what "the same idea" means.

Pure: no orchestrator import, no write. protocol_spec reads a protocol file;
nothing else touches disk.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

REPEAT = "REPEAT"
NOVEL = "NOVEL"


def _canonical_sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def normalize_timeframe(tf):
    """'1H' / ' 1h ' -> '1h'; anything that is not a non-empty string -> None."""
    return tf.strip().lower() if isinstance(tf, str) and tf.strip() else None


def normalize_ref(ref):
    """Path separators normalised ('\\' -> '/'), leading './' dropped."""
    if not isinstance(ref, str) or not ref.strip():
        return None
    out = ref.strip().replace("\\", "/")
    while out.startswith("./"):
        out = out[2:]
    return out


def protocol_spec(root: Path, protocol_ref) -> dict | None:
    """What a protocol file actually tests, independent of its per-run file
    name (generated protocols are protocols/<run_id>_generated.json, so the
    path never repeats): {timeframe (normalised), windows_sha256 (canonical
    JSON of its `windows` list)}. None when the file cannot be read."""
    ref = normalize_ref(protocol_ref)
    if ref is None:
        return None
    path = Path(root) / ref
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    doc = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    if not isinstance(doc, dict) or not isinstance(doc.get("windows"), list):
        return None
    return {"timeframe": normalize_timeframe(doc.get("timeframe")),
            "windows_sha256": _canonical_sha(doc["windows"])}


def protocol_specs(root: Path, memory: dict, extra_refs=()) -> dict:
    """{normalised protocol_ref: protocol_spec} for every memory entry's
    protocol_ref (the loop decide_next.load_inputs runs), plus `extra_refs`
    (a candidate's own protocol)."""
    specs: dict = {}
    refs = [e.get("protocol_ref") for e in ((memory or {}).get("runs") or {}).values()
            if isinstance(e, dict)]
    for raw in list(refs) + list(extra_refs):
        ref = normalize_ref(raw)
        if ref and ref not in specs:
            specs[ref] = protocol_spec(root, ref)
    return specs


def novelty_key(forecast_hash, symbols, entry: dict, specs: dict) -> tuple:
    """Card K's exact key: (config hash, symbols, timeframe, window set).
    Symbols come from the measured variant (protocol_result), the timeframe
    and window set from the protocol file the engine ran (the memory entry's
    own `timeframe` is copied from the LLM-written card, so it is only the
    fallback when the protocol file cannot be read, normalised)."""
    ref = normalize_ref(entry.get("protocol_ref"))
    spec = specs.get(ref) if ref else None
    if spec:
        timeframe, window_set = spec["timeframe"], f"windows:{spec['windows_sha256']}"
    else:
        timeframe, window_set = normalize_timeframe(entry.get("timeframe")), f"unresolved:{ref}"
    return (forecast_hash, tuple(sorted(symbols or [])), timeframe, window_set)


def _tested_variants(memory: dict):
    """(run_id, variant_id, key-input variant) for every TESTED variant with a
    forecast_hash, in sorted run order. Skipped: engineering-fault entries and
    any entry marked `legacy: true` (slice 8.1: a legacy entry can never
    produce REPEAT; tools/campaign_memory.py writes `legacy: false` on every
    entry, so on writer-produced memory this skips nothing)."""
    runs = (memory or {}).get("runs") or {}
    for run_id in sorted(runs):
        entry = runs[run_id]
        if entry.get("engineering_fault") or entry.get("legacy"):
            continue
        for vid, v in (entry.get("variants") or {}).items():
            if v.get("status") != "tested" or not v.get("forecast_hash"):
                continue
            yield run_id, vid, entry, v


def exact_index(memory: dict, specs: dict) -> dict:
    """{novelty_key: [run_id, ...]} over every TESTED variant in the memory.
    Legacy runs are not in memory, so they can never match (slice 8.1)."""
    index: dict = {}
    for run_id, _vid, entry, v in _tested_variants(memory):
        key = novelty_key(v["forecast_hash"], v.get("symbols"), entry, specs)
        runs = index.setdefault(key, [])
        if run_id not in runs:
            runs.append(run_id)
    return index


def exact_matches(key: tuple, memory: dict, specs: dict, *, exclude_run_id=None) -> list:
    """Every tested memory variant whose key equals `key`, as
    [{run_id, variant_id}] in sorted run order. `exclude_run_id`: the run
    being checked, so a re-run never matches its own earlier entry (memory
    entries are replaced on re-run)."""
    out = []
    for run_id, vid, entry, v in _tested_variants(memory):
        if exclude_run_id is not None and run_id == exclude_run_id:
            continue
        if novelty_key(v["forecast_hash"], v.get("symbols"), entry, specs) == key:
            out.append({"run_id": run_id, "variant_id": vid})
    return out


def lookup(key: tuple, memory: dict, specs: dict, *, exclude_run_id=None) -> str:
    """REPEAT when a tested memory variant has exactly this key, else NOVEL."""
    return REPEAT if exact_matches(key, memory, specs, exclude_run_id=exclude_run_id) else NOVEL
