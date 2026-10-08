"""E-075 PR-4 (CUL-422, D-088): the analyst's memory view.

What the analyst is told about EARLIER claims: "what is known", not "what looked
good" (engineering/roadmap/E-075/ANALYST_SKILL_REVIEW_1.md P5; plan A1.11 item
7). One row per earlier claim:

    claim_id, source_run, statement, kind, fold_observed, fold_confirmed, status

with status one of `confirmed`, `not_confirmed`, `not_measurable`, `pending`, and
numbers (the confirmed effect and the per-window agreement, with the fold) for
CONFIRMED claims only.

What it deliberately does NOT show -- the thing tools/reader_findings.py's
`reader_findings_summary` shows today (largest effect and "k/6 windows" per
variant, `reader_findings.py` `_largest` and the summary row):
  * no exploratory effect size, no window count, no pending effect;
  * no reason text (the reasons of an unconfirmed claim quote window counts and
    effects: "windows 3 of 6"), only the status;
  * a claim's free-text statement that is not confirmed has its number literals
    masked (explore_confirm.mask_numbers, the same rule E-072 applies to every
    reader copy: run_074's statement quotes "median forecast_return_corr=-0.0057",
    an exploratory number). The claim's mechanical test spec (selector, outcome,
    baseline, statistic, direction -- its parameters, not a result) stays readable
    so the analyst can see what was tried.

Where the claims come from (read only, passed in as dicts; this module never
touches a file but in `load_memory_view`):
  * campaign_record/campaign_memory.yaml `runs.<id>.finding`: the run's own claim.
    It was measured only in the run that inspired it, so it is `pending` (never
    confirmed there); `not_measurable` when it carries no test at all. Its
    `fold_observed` is the run's `fold` (E-077 PR-1) when it has one.
  * campaign_record/confirmations.yaml `findings.<id>`: reader / analyst side
    findings and their confirmation. The status vocabulary is E-077 PR-2's
    (confirmed | not_confirmed | not_measurable | not_comparable) on a row that
    carries its `fold`; `not_comparable` is shown as `not_measurable`. A row of the
    E-072 shape (status `pending`, or measured on an in-run split with
    `confirmation_sign_retained`) was never confirmed on a fold: it is `pending`
    (`not_measurable` if E-072 already marked it so). A ledger row replaces the
    memory claim with the same id.

The view is a plain dict; PR-5 renders it into the analyst's prompt. Pure: no
clock, no model call, no side effect.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import explore_confirm as ec  # noqa: E402  (mask_numbers: the one masking rule)

SCHEMA_VERSION = 1
CONFIRMED = "confirmed"
NOT_CONFIRMED = "not_confirmed"
NOT_MEASURABLE = "not_measurable"
PENDING = "pending"
STATUSES = (CONFIRMED, NOT_CONFIRMED, NOT_MEASURABLE, PENDING)
MEMORY_REL = "campaign_record/campaign_memory.yaml"
LEDGER_REL = ec.LEDGER_REL
STATEMENT_CHARS = 400
TEST_SPEC_KEYS = ("selector", "outcome", "baseline", "statistic", "direction")
NOTE = ("earlier claims and what became of them: numbers only for confirmed claims; "
        "pending, not_confirmed and not_measurable claims carry none (their statement has its "
        "numbers masked)")


def _run_order(run_id: str) -> tuple:
    m = re.fullmatch(r"(.*?)([0-9]+)", run_id)
    return (m.group(1), int(m.group(2))) if m else (run_id, -1)


def _statement(text, keep_numbers: bool):
    if not isinstance(text, str):
        return None
    s = " ".join(text.split())
    if not keep_numbers:
        s = ec.mask_numbers(s)
    return s if len(s) <= STATEMENT_CHARS else s[:STATEMENT_CHARS - 3] + "..."


def _specs(tests) -> list:
    """The mechanical spec of each test (no result): name, spec_hash and the slots."""
    out = []
    for t in tests or []:
        if not isinstance(t, dict):
            continue
        spec = t.get("spec") if isinstance(t.get("spec"), dict) else t
        row = {"name": t.get("name"), "spec_hash": t.get("spec_hash")}
        row.update({k: spec[k] for k in TEST_SPEC_KEYS if k in spec})
        out.append(row)
    return out


def ledger_status(rec: dict) -> str:
    """The view's status of one confirmations-ledger row."""
    st = rec.get("status")
    if st in (CONFIRMED, NOT_CONFIRMED, NOT_MEASURABLE, PENDING):
        return st
    if st in ("not_comparable", "error"):
        return NOT_MEASURABLE
    return PENDING          # an E-072 in-run measurement: never confirmed on a fold


def _confirmed_numbers(rec: dict) -> dict:
    """The numbers of a CONFIRMED row, nothing else: fold, effect and agreement per
    test and horizon. Taken from the row's `effect` / `agreement` (E-077 PR-2), else
    from its per-test horizons."""
    effect = rec.get("effect") if isinstance(rec.get("effect"), dict) else None
    agreement = rec.get("agreement") if isinstance(rec.get("agreement"), dict) else None
    if effect is None or agreement is None:
        effect, agreement = {}, {}
        for name, t in sorted((rec.get("tests") or {}).items()):
            hz = (t or {}).get("horizons") or {}
            effect[name] = {str(h): x.get("effect") for h, x in hz.items()}
            agreement[name] = {str(h): f"{x.get('windows_claimed_sign')} of "
                                       f"{x.get('windows_with_value')}" for h, x in hz.items()}
    return {"fold": rec.get("fold"), "effect": effect, "agreement": agreement}


def _memory_claims(memory: dict) -> list:
    out = []
    runs = (memory or {}).get("runs") or {}
    for rid in sorted(runs, key=lambda r: _run_order(str(r))):
        entry = runs[rid]
        f = entry.get("finding") if isinstance(entry, dict) else None
        if not isinstance(f, dict):
            continue
        tests = f.get("tests") or []
        out.append({
            "claim_id": f.get("finding_id") or f"F-{rid}-1", "source_run": str(rid),
            "statement": _statement(f.get("statement"), keep_numbers=False),
            "kind": f.get("kind"),
            "fold_observed": entry.get("fold"), "fold_confirmed": None,
            "status": PENDING if tests else NOT_MEASURABLE,
            "tests": _specs(tests)})
    return out


def _ledger_claims(ledger: dict, memory: dict | None = None) -> list:
    out = []
    runs = (memory or {}).get("runs") or {}
    findings = (ledger or {}).get("findings") or {}
    for fid in sorted(findings):
        rec = findings[fid]
        if not isinstance(rec, dict):
            continue
        status = ledger_status(rec)
        confirmed = status == CONFIRMED
        row = {
            "claim_id": str(rec.get("finding_id") or fid),
            "source_run": rec.get("source_run"),
            "statement": _statement(rec.get("statement"), keep_numbers=confirmed),
            "kind": rec.get("kind"),
            "fold_observed": rec.get("fold_observed") or (
                (runs.get(rec.get("source_run")) or {}).get("fold")
                if isinstance(runs.get(rec.get("source_run")), dict) else None),
            "fold_confirmed": rec.get("fold") if confirmed else None,
            "status": status,
            "tests": [{"spec_hash": h} for h in (rec.get("spec_hashes")
                                                 or rec.get("finding_spec_hashes") or [])]}
        if confirmed:
            row["confirmed"] = _confirmed_numbers(rec)
        out.append(row)
    return out


def build_memory_view(memory: dict, ledger: dict | None = None) -> dict:
    """The analyst's memory view from the campaign memory and the confirmations
    ledger (both already loaded; either may be empty)."""
    by_id = {c["claim_id"]: c for c in _memory_claims(memory)}
    for c in _ledger_claims(ledger or {}, memory):
        by_id[c["claim_id"]] = c                       # the ledger knows what became of it
    claims = list(by_id.values())
    counts = {s: sum(1 for c in claims if c["status"] == s) for s in STATUSES}
    return {"schema_version": SCHEMA_VERSION, "note": NOTE, "n_claims": len(claims),
            "by_status": counts, "claims": claims}


def load_memory_view(root) -> dict:
    """build_memory_view over `<root>/campaign_record/campaign_memory.yaml` and
    `confirmations.yaml` (either may be absent)."""
    def load(rel):
        p = Path(root) / rel
        if not p.exists():
            return {}
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        return doc if isinstance(doc, dict) else {}
    return build_memory_view(load(MEMORY_REL), load(LEDGER_REL))
