"""
The grid-based KB writer (E-058 S2b, delivery_plan_v26.md slice 6a; spec:
engineering/roadmap/E-058/S1_FINDINGS.md guess 2 and the operator decision
of 2026-09-23).

Adds ONE entry per run to campaign_record/campaign_knowledge_base.yaml:

    id: grid_<run_id>
    hypothesis_id: <from the memory entry>
    evidence_runs: [<run_id>]
    evidence_count: 1
    outcome: <idea_status>                       # validated | refuted | inconclusive
    legacy_schema: false
    verdict_status: gated                        # validated / refuted only
    pass_rule_evaluation_ref: runs/<run_id>/artifacts/idea_status.yaml   # validated / refuted only
    outcome_reason: <idea_status.yaml reason>

Why a new writer and not run_phase1_research._write_kb_findings_entry: under
the readers flag that writer never runs (it needs verdict_interpretation.yaml
and is called only on the retired refine/pivot/escalate routes), and its
outcome map has no grid words, so it would record `refuted` as
`inconclusive`.

Rules:
  * The outcome is the grid's idea_status, copied from the memory entry --
    nothing here decides. `idea_status.yaml` carries `result: PASS|FAIL` for
    validated/refuted, so it is cited as the pass_rule_evaluation_ref and
    verdict_criteria_evaluator.validate_verdict_provenance resolves it (exists,
    under this entry's own run, binding result). An inconclusive outcome is
    not verdict-bearing and cites nothing (its idea_status.yaml carries
    result: INCONCLUSIVE, which is not a resolved verdict).
  * It NEVER merges into, updates or closes another entry -- in particular
    not a legacy entry with the same hypothesis_id -- so the F09 reactivation
    closure in the legacy writer is never touched. Its own entry (same id,
    `legacy_schema: false`, `evidence_runs == [run_id]`) is replaced on a
    re-run of the same run; any other entry holding that id raises.
  * Engineering-fault runs get no entry (the caller does not call it).
  * Every finding in the file is re-validated (closed schema + provenance)
    before the write, like the legacy writer. A malformed KB raises and is
    never overwritten.
  * The KB file absent -> skipped with a loud line and None returned (the
    legacy writer's own precedent: it never creates the KB).

Importable without the orchestrator: paths and the derived-view recompute
are passed in by the caller.
"""
from __future__ import annotations

from pathlib import Path

import yaml

import campaign_memory as _cm  # tools/ sibling: atomic write + lock primitive
import verdict_criteria_evaluator as _vce

KB_LOCK_FILENAME = ".campaign_knowledge_base.lock"
KB_ENTRY_ID_PREFIX = "grid_"
_GATED_STATUSES = ("validated", "refuted")


class GridKBError(ValueError):
    """The KB file or the entry is malformed, or the entry's id is held by a
    record this writer does not own. Never caught here."""


def kb_entry_id(run_id: str) -> str:
    return f"{KB_ENTRY_ID_PREFIX}{run_id}"


def build_kb_entry(memory_entry: dict) -> dict:
    """The KB entry for one full (non-fault) memory entry."""
    if memory_entry.get("engineering_fault") is not None:
        raise GridKBError(f"{memory_entry.get('run_id')}: engineering-fault runs get no KB entry")
    run_id = memory_entry.get("run_id")
    hyp_id = memory_entry.get("hypothesis_id")
    status = memory_entry.get("idea_status")
    if not isinstance(run_id, str) or not run_id or not isinstance(hyp_id, str) or not hyp_id:
        raise GridKBError(f"memory entry lacks run_id/hypothesis_id: {run_id!r}/{hyp_id!r}")
    if status not in ("validated", "refuted", "inconclusive"):
        raise GridKBError(f"{run_id}: idea_status={status!r} is not a grid status")
    entry = {
        "id": kb_entry_id(run_id),
        "hypothesis_id": hyp_id,
        "evidence_runs": [run_id],
        "evidence_count": 1,
        "outcome": status,
        "legacy_schema": False,
    }
    if status in _GATED_STATUSES:
        entry["verdict_status"] = "gated"
        entry["pass_rule_evaluation_ref"] = memory_entry["idea_status_ref"]
    entry["outcome_reason"] = memory_entry.get("idea_status_reason")
    return entry


def entry_id_for_run(kb_path: Path, run_id: str) -> str | None:
    """The id of this writer's entry for `run_id` if the KB holds one (read
    only; None when the KB file is absent). A malformed KB raises."""
    kb_path = Path(kb_path)
    if not kb_path.exists():
        return None
    try:
        kb = yaml.safe_load(kb_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise GridKBError(f"{kb_path}: unparseable YAML ({exc})") from exc
    findings = kb.get("findings") if isinstance(kb, dict) else None
    if not isinstance(findings, list):
        raise GridKBError(f"{kb_path}: findings is not a list")
    want = kb_entry_id(run_id)
    for f in findings:
        if isinstance(f, dict) and f.get("id") == want and f.get("legacy_schema") is False:
            return want
    return None


def _owned_by(existing: dict, entry: dict) -> bool:
    return (existing.get("legacy_schema") is False
            and existing.get("evidence_runs") == entry["evidence_runs"])


def write_kb_entry(kb_path: Path, entry: dict, *, root: Path, recompute_views=None) -> str | None:
    """Append (or replace this writer's own entry for the same run) under a
    lock, atomically. Returns the entry id, or None when the KB file does not
    exist. `recompute_views(kb)` refreshes the derived coverage views
    (run_phase1_research._recompute_kb_views), as the legacy writer does."""
    kb_path = Path(kb_path)
    if not kb_path.exists():
        print(f"WARNING [E-058] KB: {kb_path} not found -- the grid KB entry for "
              f"{entry['evidence_runs'][0]} is NOT written (the legacy writer skips the same way). "
              f"Memory records kb_entry_id: null.")
        return None
    with _cm._file_lock(kb_path.parent / KB_LOCK_FILENAME, "the campaign knowledge base",
                        error_cls=GridKBError):
        try:
            kb = yaml.safe_load(kb_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise GridKBError(f"{kb_path}: unparseable YAML ({exc})") from exc
        if not isinstance(kb, dict):
            raise GridKBError(f"{kb_path}: expected a mapping, got {type(kb).__name__}")
        findings = kb.setdefault("findings", [])
        if not isinstance(findings, list) or not all(isinstance(f, dict) for f in findings):
            raise GridKBError(f"{kb_path}: findings is not a list of mappings")
        idx = [i for i, f in enumerate(findings) if f.get("id") == entry["id"]]
        if len(idx) > 1:
            raise GridKBError(f"{kb_path}: id {entry['id']!r} appears {len(idx)} times")
        if idx and not _owned_by(findings[idx[0]], entry):
            raise GridKBError(
                f"{kb_path}: id {entry['id']!r} is held by an entry this writer did not write "
                f"(legacy_schema is not false or evidence_runs differ) -- not overwriting it")
        # Closed schema + provenance, for the new entry and every existing one
        # (a hand-edited entry must not slip in behind this write) -- except
        # this writer's own entry being replaced: its citation points at the
        # run's idea_status.yaml, which the re-run has already rewritten.
        _vce.validate_verdict_provenance(entry, entry_ref=f"KB finding {entry['id']!r}", root=root)
        for i, f in enumerate(findings):
            if idx and i == idx[0]:
                continue
            _vce.validate_verdict_provenance(f, entry_ref=f"KB finding {f.get('id')!r}", root=root)
        if idx:
            findings[idx[0]] = entry
        else:
            findings.append(entry)
        if recompute_views is not None:
            recompute_views(kb)
        _cm._atomic_write(kb_path, kb)
    print(f"[E-058] KB: wrote {entry['id']} (outcome={entry['outcome']}, legacy_schema=false) -> {kb_path}")
    return entry["id"]
