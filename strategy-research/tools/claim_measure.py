"""E-068 slice 3 (CUL-393): measure the claim card's tests after the backtests.

Under orchestrator.claim_tests.enabled only (run_phase1_research wires it;
nothing here reads a flag). Design: engineering/roadmap/E-068/DESIGN_PROPOSAL.md
sections 3 and 8. Pure functions plus two writers (the per-run files are
written by the caller; this module writes only the coverage record).

What it does: after a run's backtests, every test of the run's own claim card
(tools/claim_card.py) is measured on each graded variant's saved bars.csv:
the EFFECT SIZE per horizon, per window, per coin and per era, plus the event
counts and a plain description. Nothing more:

  - no p-value, no verdict, no calibration (automatic verdicts are CUL-394);
  - statuses are `measured` or `not_measured` (with a reason), never
    supported / refuted;
  - every measured test is labelled "measured, not proven".

INFORMATION ONLY (operator, 2026-10-04): a measurement never changes
idea_status or the grid, never routes, stops, parks or fails a run. It is not a
grid criterion. Every error is recorded as `not_measured` (reason `error`) by
the caller's safety net, and the run continues.

WHY THIS CANNOT LEAK (no lookahead): it runs only after a completed backtest,
on that run's own bars.csv. claim_tests.effect_sizes uses the slice-1 blocks
unchanged: selectors read bar t only (quantile is trailing); forward outcomes
are matched by TIMESTAMP inside one window, never across windows. No signal is
recomputed and no data cache is read (no warm-up rows). Any window reaching
the holdout start (config/campaign_data_policy.yaml) is refused.

Every signal and timeframe works, regime selectors included: the effect size
needs no signal recompute, so the regime refusal check_spec makes for a
verdict does not apply here (claim_card._check_test drops exactly that one).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import claim_card as cc  # noqa: E402
import claim_tests as ct  # noqa: E402

MEASURED = "measured"
NOT_MEASURED = "not_measured"
# a test whose selector matched no bar at any horizon: looked at (counted for
# best-of-N), but no effect exists -- never "measured"
NO_EVENTS = "no_events"
NO_EVENTS_REASON = "the selector matched no bars"
LABEL = "measured, not proven"
NOTE = ("effect sizes only: no p-value and no verdict (automatic claim verdicts are "
        "parked, CUL-394); information only, it never changes idea_status")
VARIANT_FILE = "claim_test.yaml"          # artifacts/variants/<vid>/claim_test.yaml
RUN_FILE = "claim_status.yaml"            # artifacts/claim_status.yaml
# Why something was not measured: the card's gap (claim_card.GAP_REASONS), or
BARS_MISSING = "bars_missing"
HOLDOUT = "holdout"                       # a bar at or after the holdout start: refused
ERROR = "error"
NO_VARIANTS = "no_graded_variants"
# set by the caller for variants it does not measure (this attempt's set):
# "stale_result" (an earlier attempt's protocol_result.yaml), "invalidated"
_FLOOR_KEY = {"min_events": "n_events", "min_windows": "n_windows_with_events",
              "min_blocks": "n_blocks", "min_eras": "n_eras_with_events"}


class HoldoutOverlap(ValueError):
    """A window reaches the holdout start: never measured."""


# ---------------------------------------------------------------------------
# One test
# ---------------------------------------------------------------------------

def test_spec(test: dict):
    """(TestSpec, spec_hash) of one claim-card test, checked exactly as slice 2
    checked it (claim_card._check_test: regime selectors allowed). Raises
    ValueError on an invalid test."""
    name = test.get("name") if isinstance(test, dict) else None
    errors, h, _possible = cc._check_test(test, f"test {name!r}")
    if errors:
        raise ValueError("; ".join(errors))
    d = {k: test[k] for k in cc.TEST_KEYS - {"name"} if k in test}
    d.setdefault("baseline", None)
    return ct.TestSpec.from_dict(d), h


test_spec.__test__ = False  # not a pytest test


def check_before_holdout(windows: list, holdout_start: str) -> None:
    """Every bar strictly before the holdout start day (00:00 UTC)."""
    import pandas as pd
    bound = int(pd.Timestamp(holdout_start, tz="UTC").timestamp())
    for w in windows:
        if len(w.ts) and int(np.max(w.ts)) >= bound:
            raise HoldoutOverlap(f"{w.label}: a bar reaches the holdout start; not measured")


def _claimed(cells) -> tuple:
    """(windows with the claimed sign, windows with a defined value)."""
    vals = [c["oriented"] for c in cells if c.get("oriented") is not None]
    return sum(1 for v in vals if v > 0), len(vals)


def _num(v):
    return None if v is None or not np.isfinite(v) else float(v)


def _per_coin(per: list, spec, h: int) -> dict:
    """The test's statistic pooled over each coin's windows, with its window
    signs: the same measurement as the variant's, restricted to one coin."""
    stat = ct.STATISTICS[spec.statistic]
    out = {}
    for sym in sorted({p["w"].symbol for p in per}):
        sub = [p for p in per if p["w"].symbol == sym]
        raw, oriented = stat(*ct._pooled(sub, h), spec.direction)
        events = [p["mask"] & np.isfinite(p["ys"][h]) for p in sub]
        if spec.statistic == "rank_ic":
            events = [ev & np.isfinite(p["fc"]) for ev, p in zip(events, sub)]
        cells = []
        for p in sub:
            o = stat(p["ys"][h], p["mask"], p["wref"], p["fc"], spec.direction)[1]
            cells.append({"oriented": _num(o)})
        k, n = _claimed(cells)
        out[sym] = {"value": _num(raw), "oriented": _num(oriented),
                    "n_events": int(sum(int(ev.sum()) for ev in events)),
                    "windows_with_claimed_sign": k, "windows_with_a_value": n,
                    "n_windows": len(sub)}
    return out


def _fmt(v) -> str:
    return "undefined" if v is None else f"{v:+.4g}"


def describe(name: str, spec, horizons: dict, floor_not_met: list) -> list:
    """Plain lines a person reads next to the numbers."""
    base = (spec.baseline or {}).get("kind") or "no baseline (a rank correlation)"
    lines = [f"{name}: {LABEL}. {spec.statistic} of {spec.outcome['kind']} on the selected "
             f"bars against {base}; the claim says {spec.direction}."]
    for h, r in horizons.items():
        lines.append(f"h={h}: effect {_fmt(r['value'])}; claimed sign in "
                     f"{r['windows_with_claimed_sign']} of {r['windows_with_a_value']} windows; "
                     f"{r['n_events']} events")
        for sym, c in r["per_coin"].items():
            lines.append(f"  {sym}: effect {_fmt(c['value'])}; claimed sign in "
                         f"{c['windows_with_claimed_sign']} of {c['windows_with_a_value']} "
                         f"windows; {c['n_events']} events")
    if floor_not_met:
        lines.append("Below the card's floor: " + "; ".join(floor_not_met))
    lines.append("No p-value and no verdict: a measurement, not proof.")
    return lines


def measure_test(windows: list, test: dict, eras: list | None) -> dict:
    """One claim-card test on one variant's windows: effect sizes only."""
    spec, h_spec = test_spec(test)
    per, out_h, horizons, _rng = ct.effect_sizes(windows, spec, eras)
    rows, floor_not_met = {}, []
    for h in horizons:
        r = out_h[h]
        k, n = _claimed(r["per_window"].values())
        rows[h] = {"value": r["value"], "oriented": r["oriented"],
                   "n_events": r["n_events"], "n_windows_with_events": r["n_windows_with_events"],
                   "n_blocks": r["n_blocks"], "n_eras_with_events": r["n_eras_with_events"],
                   "windows_with_claimed_sign": k, "windows_with_a_value": n,
                   "n_windows": len(per),
                   "per_coin": _per_coin(per, spec, h),
                   "per_window": r["per_window"], "per_era": r["per_era"]}
        for unit, need in spec.floor.items():
            have = r[_FLOOR_KEY[unit]] or 0
            if have < need:
                floor_not_met.append(f"{unit}={need} at h={h} (have {have})")
    out = {"name": test["name"], "status": MEASURED, "label": LABEL, "spec_hash": h_spec,
           "statistic": spec.statistic, "direction": spec.direction,
           "outcome": spec.outcome["kind"], "horizons": rows,
           "floor": dict(spec.floor), "floor_not_met": floor_not_met}
    if spec.statistic == "decay_curve":
        vals = {h: rows[h]["oriented"] for h in horizons if rows[h]["oriented"] is not None}
        out["peak_horizon"] = max(vals, key=vals.get) if vals else None
    out["description"] = describe(test["name"], spec, rows, floor_not_met)
    if all(rows[h]["n_events"] == 0 for h in horizons):
        # nothing was measured: a look taken (counted for best-of-N), never an effect
        reason = NO_EVENTS_REASON
        if spec.selector.get("kind") in ct.NOT_RECOMPUTABLE_SELECTORS:
            labels = sorted({str(r) for w in windows for r in w.regime if r})
            reason += f"; regime labels present in the bars: {labels if labels else 'none'}"
        out.update(status=NO_EVENTS, reason=reason)
        out["description"] = [f"{test['name']}: no events -- {reason}. Nothing was measured."]
    return out


# ---------------------------------------------------------------------------
# One variant, one run
# ---------------------------------------------------------------------------

def _error(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"


def measure_variant(run_dir: Path, vid: str, tests: list, eras, holdout_start: str) -> dict:
    """Every test on one graded variant's saved bars. Never raises: a variant
    whose bars cannot be read, or a test that errors, is recorded."""
    doc = {"variant": vid, "label": LABEL, "note": NOTE}
    try:
        windows = ct.load_variant_bars(Path(run_dir), vid)
        check_before_holdout(windows, holdout_start)
    except Exception as exc:  # noqa: BLE001 -- information only: recorded, never raised
        reason = (BARS_MISSING if isinstance(exc, FileNotFoundError)
                  else HOLDOUT if isinstance(exc, HoldoutOverlap) else ERROR)
        return {**doc, "status": NOT_MEASURED, "reason": reason, "detail": _error(exc),
                "tests": unmeasured_tests(tests, reason)}
    root = Path(run_dir).resolve()
    doc.update({"symbols": sorted({w.symbol for w in windows}),
                "windows": [w.label for w in windows],
                "bars": [{"window": w.label, "bars": int(len(w.ts)), "sha256": w.sha256,
                          "path": _rel(w.source, root)} for w in windows]})
    results = {}
    for t in tests:
        name = t.get("name") if isinstance(t, dict) else None
        try:
            results[str(name)] = measure_test(windows, t, eras)
        except Exception as exc:  # noqa: BLE001 -- information only
            results[str(name)] = {"name": name, "status": NOT_MEASURED, "reason": ERROR,
                                  "detail": _error(exc)}
    measured = any(r["status"] == MEASURED for r in results.values())
    all_empty = bool(results) and all(r["status"] == NO_EVENTS for r in results.values())
    detail = None if measured else "no test could be measured: " + "; ".join(
        f"{n}: {r.get('detail') or r.get('reason')}" for n, r in results.items())
    doc.update({"status": MEASURED if measured else NOT_MEASURED,
                "reason": None if measured else NO_EVENTS if all_empty else ERROR,
                "detail": detail, "tests": results})
    return doc


def unmeasured_tests(tests: list, reason: str) -> dict:
    """Every test of a variant that could not be measured, so it is still
    listed and counted."""
    out = {}
    for t in tests:
        name = str(t.get("name") if isinstance(t, dict) else None)
        spec_hash = None
        try:
            spec_hash = test_spec(t)[1]
        except Exception:  # noqa: BLE001 -- an invalid test keeps spec_hash None
            pass
        out[name] = {"name": name, "status": NOT_MEASURED, "reason": reason,
                     "spec_hash": spec_hash}
    return out


def _rel(path: str, root: Path) -> str:
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except ValueError:
        return str(path)


def run_doc(run_id: str, card_status: dict, variants: dict, skipped: dict | None = None) -> dict:
    """artifacts/claim_status.yaml: the run's measurement status, next to (never
    inside) idea_status.yaml. `card_status`: claim_card.status_of of the run's
    own card. `variants`: {vid: measure_variant(...)}. `skipped`: {vid: reason}
    for variants this attempt does not measure (listed, never counted as
    measured)."""
    skipped = dict(skipped or {})
    counted = [{"variant": vid, "test": name, "spec_hash": r.get("spec_hash"),
                "status": r["status"]}
               for vid, v in variants.items() for name, r in (v.get("tests") or {}).items()]
    n_measured = sum(1 for c in counted if c["status"] == MEASURED)
    doc = {"run_id": run_id, "label": LABEL, "note": NOTE, "information_only": True}
    if not card_status.get("usable"):
        status, reason, detail = NOT_MEASURED, card_status.get("reason"), card_status.get("detail")
    elif not variants:
        status, reason = NOT_MEASURED, NO_VARIANTS
        detail = ("no variant was backtested in this attempt"
                  + (f" (skipped: {skipped})" if skipped else
                     " (none under artifacts/variants/: the variant loop is off or every "
                     "backtest failed)"))
    elif n_measured:
        status, reason, detail = MEASURED, None, None
    else:
        reasons = {v.get("reason") for v in variants.values()}
        status = NOT_MEASURED
        reason = reasons.pop() if len(reasons) == 1 else ERROR
        detail = "; ".join(f"{vid}: {v.get('detail')}" for vid, v in variants.items())
    rows = {vid: {"status": v["status"], "reason": v.get("reason"),
                  "file": f"variants/{vid}/{VARIANT_FILE}"} for vid, v in variants.items()}
    rows.update({vid: {"status": NOT_MEASURED, "reason": r, "file": None}
                 for vid, r in skipped.items()})
    n_no_events = sum(1 for c in counted if c["status"] == NO_EVENTS)
    doc.update({"claim_status": status, "reason": reason, "detail": detail,
                "n_tests_measured": n_measured,
                "n_tests_no_events": n_no_events,
                "n_tests_not_measured": len(counted) - n_measured - n_no_events,
                "variants": rows, "tests": counted})
    return doc


def error_doc(run_id: str, exc: BaseException) -> dict:
    """The safety net's claim_status.yaml: grading itself failed."""
    return {"run_id": run_id, "label": LABEL, "note": NOTE, "information_only": True,
            "claim_status": NOT_MEASURED, "reason": ERROR, "detail": _error(exc),
            "n_tests_measured": 0, "n_tests_not_measured": 0, "variants": {}, "tests": []}


# ---------------------------------------------------------------------------
# Counting (every measured test), next to slice 2's coverage row
# ---------------------------------------------------------------------------

def record_measured(root: Path, run_id: str, doc: dict) -> None:
    """campaign_record/claim_test_coverage.yaml runs[run_id].measured: this
    run's latest measurement (status, count, every test with its spec_hash),
    so "best of N" can be counted later. The rest of the row (slice 2's) is
    kept. Locked, atomic."""
    import campaign_memory as cm
    import campaign_review_retired as crr
    path = Path(root) / cc.COVERAGE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with crr._lock(path, path.name):
        cov = crr._load_mapping(path, {})
        runs = cov.get("runs") if isinstance(cov.get("runs"), dict) else {}
        row = runs.get(run_id) if isinstance(runs.get(run_id), dict) else {}
        prev = row.get("measured") if isinstance(row.get("measured"), dict) else {}
        # every (variant, test, spec_hash) ever measured in this run: a look taken
        # in an earlier attempt stays counted even if a later attempt does not
        # measure that variant again (best-of-N counts looks, not survivors)
        # A no_events test is a look too (it was tried), kept with its status
        # so the summary shows it apart from the measured ones; the latest
        # attempt's status wins for the same (variant, test, spec_hash).
        looks = {(lk.get("variant"), lk.get("test"), lk.get("spec_hash")):
                 lk.get("status", MEASURED)
                 for lk in prev.get("looks") or [] if isinstance(lk, dict)}
        looks.update({(t.get("variant"), t.get("test"), t.get("spec_hash")): t["status"]
                      for t in doc.get("tests") or []
                      if t.get("status") in (MEASURED, NO_EVENTS)})
        statuses = list(looks.values())
        row["measured"] = {"claim_status": doc.get("claim_status"), "reason": doc.get("reason"),
                           "n_tests_measured": int(doc.get("n_tests_measured") or 0),
                           "n_tests_no_events": int(doc.get("n_tests_no_events") or 0),
                           "tests": list(doc.get("tests") or []),
                           "looks": [{"variant": v, "test": t, "spec_hash": h, "status": s}
                                     for (v, t, h), s in sorted(
                                         looks.items(), key=lambda x: tuple(map(str, x[0])))],
                           "n_looks": len(looks),
                           "n_looks_measured": statuses.count(MEASURED),
                           "n_looks_no_events": statuses.count(NO_EVENTS)}
        runs[run_id] = row
        cm._atomic_write(path, {**cov, "runs": runs})
