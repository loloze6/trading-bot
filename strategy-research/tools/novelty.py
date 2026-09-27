"""
novelty -- the ONE definition of "this exact thing was already tested"
(E-036 S2a, delivery_plan_v26.md slice 8.1; spec:
engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md and its operator decision of
2026-09-27: "one key, one source").

The exact-match key (card K) is

    (forecast_hash, tuple(sorted(symbols)), timeframe, window_set)

  * forecast_hash -- the canonical-JSON sha256 of the config
    (forecast_hash_of_config: the canonicalisation of
    run_phase1_research._compute_forecast_hash). The trial row carries it;
    campaign_memory.yaml copies it per tested variant.
  * symbols -- the symbols the backtest runs (memory: measured from
    protocol_result.yaml; before a backtest: the protocol file's `symbols`,
    which is what tools/run_protocol.py iterates).
  * timeframe and window_set -- read from the PROTOCOL FILE the engine runs
    (protocol_spec): its `timeframe`, and a content hash of its `windows`.
    Never the raw protocol path: generated protocols are per-run file names
    (protocols/<run_id>_generated.json), so a path would never repeat. When a
    memory entry's protocol file cannot be read (missing, unparseable, no
    `windows` list), its key falls back to the entry's own (card) timeframe
    and "unresolved:<ref>" -- a key that can never equal a resolved one, so
    that entry can never produce a REPEAT (the safe direction); the problem is
    recorded as a warning. A CANDIDATE's own protocol is read strictly
    (protocol_spec(..., strict=True)): it must resolve, or the check fails
    loud.

The only source of truth is campaign_record/campaign_memory.yaml
(tools/campaign_memory.py, written by the regroup_record stage). A run with
no memory entry (every run before that stage, never backfilled), an
engineering-fault entry, and an entry marked `legacy: true` can never
produce a REPEAT. The `legacy: true` skip is the intended change to
tools/decide_next.py's exact-match behaviour in E-036 S2a (slice 8.1: "legacy
entries can never produce REPEAT"); campaign_memory.schema.json makes the
writer emit `legacy: false`, so it only matters for a hand-marked entry. The
one other decide_next difference is the unreadable-protocol degradation
above: an unparseable memory protocol used to raise out of
decide_next.load_inputs; it now keys that entry "unresolved" with a warning.

Extracted from tools/decide_next.py (E-059 S2a), which imports it back;
tools/anti_adjacency_gate.py (the 5a gate) imports the same functions, so
the two call sites can never drift on what "the same idea" means.

No orchestrator import, no file write. protocol_spec reads a protocol file
(and prints a warning line for an unreadable one); nothing else touches disk.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

REPEAT = "REPEAT"
NOVEL = "NOVEL"


class NoveltyError(ValueError):
    """A candidate's own protocol could not be read strictly."""


def forecast_hash_of_config(config) -> str:
    """sha256 of json.dumps(config, sort_keys=True) -- exactly
    run_phase1_research._compute_forecast_hash's canonicalisation, applied
    to an in-memory config (tests pin the two together)."""
    return hashlib.sha256(json.dumps(config, sort_keys=True).encode("utf-8")).hexdigest()


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


def load_protocol(root: Path, protocol_ref) -> dict:
    """The parsed protocol file (JSON, else YAML) at root/protocol_ref.
    Raises NoveltyError when the ref is empty, the file is missing or
    unparseable, or it is not a mapping with a `windows` list."""
    ref = normalize_ref(protocol_ref)
    if ref is None:
        raise NoveltyError(f"protocol ref {protocol_ref!r} is empty")
    path = Path(root) / ref
    if not path.exists():
        raise NoveltyError(f"protocol {ref} does not exist under {root}")
    try:
        text = path.read_text(encoding="utf-8")
        doc = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise NoveltyError(f"protocol {ref} is unreadable: {exc}") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("windows"), list):
        raise NoveltyError(f"protocol {ref} is not a mapping with a `windows` list")
    return doc


def protocol_spec(root: Path, protocol_ref, *, strict: bool = False, warnings=None) -> dict | None:
    """What a protocol file actually tests, independent of its per-run file
    name (generated protocols are protocols/<run_id>_generated.json, so the
    path never repeats): {timeframe (normalised), windows_sha256 (canonical
    JSON of its `windows` list)}.

    strict=False (a MEMORY entry's protocol): an empty ref gives None
    silently; a missing, unparseable or malformed file gives None, prints a
    WARNING line and appends {protocol_ref, reason} to `warnings` (when a
    list is passed) -- the entry is then keyed "unresolved" and can never
    match.
    strict=True (a CANDIDATE's own protocol): raises NoveltyError instead."""
    ref = normalize_ref(protocol_ref)
    if ref is None and not strict:
        return None
    try:
        doc = load_protocol(root, protocol_ref)
    except NoveltyError as exc:
        if strict:
            raise
        print(f"WARNING [novelty] {exc} -- entries on this protocol are keyed "
              f"'unresolved' and can never match")
        if warnings is not None:
            warnings.append({"protocol_ref": ref, "reason": str(exc)})
        return None
    return {"timeframe": normalize_timeframe(doc.get("timeframe")),
            "windows_sha256": _canonical_sha(doc["windows"])}


def protocol_specs(root: Path, memory: dict, extra_refs=(), warnings=None) -> dict:
    """{normalised protocol_ref: protocol_spec (non-strict)} for every memory
    entry's protocol_ref, in memory order, plus `extra_refs`. THE one loop:
    decide_next.load_inputs, campaign_memory.tried_ideas and the 5a gate all
    use it. Unreadable files are None and listed in `warnings`."""
    specs: dict = {}
    refs = [e.get("protocol_ref") for e in ((memory or {}).get("runs") or {}).values()
            if isinstance(e, dict)]
    for raw in list(refs) + list(extra_refs):
        ref = normalize_ref(raw)
        if ref and ref not in specs:
            specs[ref] = protocol_spec(root, ref, warnings=warnings)
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
    """(run_id, variant_id, entry, variant) for every TESTED variant with a
    forecast_hash, in sorted run order. Skipped: engineering-fault entries and
    entries marked `legacy: true` (see the module docstring)."""
    runs = (memory or {}).get("runs") or {}
    for run_id in sorted(runs):
        entry = runs[run_id]
        if entry.get("engineering_fault") or entry.get("legacy"):
            continue
        for vid, v in (entry.get("variants") or {}).items():
            if v.get("status") != "tested" or not v.get("forecast_hash"):
                continue
            yield run_id, vid, entry, v


def match_index(memory: dict, specs: dict, *, exclude_run_id=None) -> dict:
    """{novelty_key: [{run_id, variant_id}, ...]} over every TESTED memory
    variant, built once per run and looked up per candidate.
    `exclude_run_id`: the run being checked, so a re-run never matches its
    own earlier entry (memory entries are replaced on re-run)."""
    index: dict = {}
    for run_id, vid, entry, v in _tested_variants(memory):
        if exclude_run_id is not None and run_id == exclude_run_id:
            continue
        key = novelty_key(v["forecast_hash"], v.get("symbols"), entry, specs)
        index.setdefault(key, []).append({"run_id": run_id, "variant_id": vid})
    return index


def exact_index(memory: dict, specs: dict) -> dict:
    """{novelty_key: [run_id, ...]} (each run once, first-seen order) --
    decide_next's view of match_index."""
    out: dict = {}
    for key, matches in match_index(memory, specs).items():
        runs = out.setdefault(key, [])
        for m in matches:
            if m["run_id"] not in runs:
                runs.append(m["run_id"])
    return out


def exact_matches(key: tuple, memory: dict, specs: dict, *, exclude_run_id=None) -> list:
    """Every tested memory variant whose key equals `key`, as
    [{run_id, variant_id}] in sorted run order."""
    return list(match_index(memory, specs, exclude_run_id=exclude_run_id).get(key) or [])


def lookup(key: tuple, memory: dict, specs: dict, *, exclude_run_id=None) -> str:
    """REPEAT when a tested memory variant has exactly this key, else NOVEL."""
    return REPEAT if exact_matches(key, memory, specs, exclude_run_id=exclude_run_id) else NOVEL
