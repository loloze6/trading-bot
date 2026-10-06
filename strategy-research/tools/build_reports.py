"""
tools/build_reports.py -- E-046a Slice 5a: category reports
(delivery_plan_v26.md, "Slice 5 -- Reports and readers", bullet 5a).

WHAT THIS WRITES
----------------
Given one run directory (e.g. strategy-research/runs/run_059), writes five
files under <run_dir>/artifacts/reports/:

    profitability.yaml
    trade_efficiency.yaml
    forecast_power.yaml
    regime_power.yaml
    component_attribution.yaml

Each file has the shape:

    category: <name>
    source_run_id: <run_dir.name>
    generated_at: <UTC ISO timestamp of this build>
    slices:
      overall:     <dict, or {"unavailable": true, "reason": "..."}>
      per_window:  <list, or {"unavailable": true, "reason": "..."}>
      per_regime:  <dict keyed by regime label, or unavailable>
      per_symbol:  <dict keyed by symbol, or unavailable>

A slice is NEVER a fabricated aggregate when its source data doesn't support
that cut -- it is written as the explicit `{"unavailable": true, "reason":
"..."}` shape above, with a real, specific reason. This is deliberate: 5b's
readers must be able to tell "this cut genuinely has nothing" apart from "the
builder forgot this cut."

PER-VARIANT REPORTS (E-061 C2 S2d, schema_version 2)
-----------------------------------------------------
`build_reports(run_dir, variants={...})` builds the same five files in a
different top-level shape -- see `build_reports`'s own docstring for the
exact fields. Every variant's `slices` are still built by the same functions
below, just pointed (via `_variant_sources`) at that variant's own
`artifacts/variants/<vid>/protocol_result.yaml` /
`variants/<vid>/trade_diagnostics.json` / `variants/<vid>/results/.../bars.csv`
instead of the run-level defaults. `variants=None` (the default) is
byte-identical to this module's pre-S2d behaviour.

SOURCES, AND THE TWO EXCEPTIONS TO "ZERO NEW COMPUTATION"
------------------------------------------------------------
Every value in every report is a direct re-projection (copy, or regrouping-
by-existing-key with no arithmetic) of a field that already exists in one of:

  - <run_dir>/artifacts/protocol_result.yaml
  - <run_dir>/trade_diagnostics.json           (top-level trades list; NOT
    under artifacts/ -- confirmed against the real run_054/057/059 corpus)
  - <run_dir>/results/<window_run_id>/bars.csv  (one per protocol_result.yaml
    results[] entry, keyed by that entry's own `run_id` field)
CUL-381 (2026-10-02): every source is THIS run's own output. The campaign-
level strategy-research/regime_detector_report.yaml is NOT read: it is
written by tools/validate_regime_detector.py on its own fixed coins,
timeframe and period, so on run_065/run_066 it was run_064's file (another
venue, period and, for run_065, timeframe), and the regime reader cited it as
this run's detector failing. The regime_power report no longer carries a
`detector_health` block.

...with exactly TWO exceptions, both scoped and both approved before being
written:

  1. delivery_plan_v26.md's own Slice 5a text: the regime_power report's
     `hindsight_lag` values (see _compute_hindsight_lag below), inherited
     from E-040's decided regime-power checks. E-040 (EPICS.md) actually
     names three checks -- (a) does using the regime label beat ignoring it,
     (b) a hindsight-lag comparison that measures LAG, not correctness, and
     (c) detector health numbers -- but delivery_plan_v26.md's Slice 5a
     bullet narrows THIS slice's inherited scope to only (b) and (c). (a) is
     intentionally NOT computed anywhere in this file; regime_power's
     `overall` slice says so explicitly rather than silently omitting it.
  2. E-061 C2 S2d (G7, C2_S1_FINDINGS.md, operator-accepted 2026-09-28):
     trade_efficiency's and component_attribution's per_window/per_regime/
     per_symbol slices are n/mean/median/p10/p90 AGGREGATES
     (`_aggregate_records` / `_aggregate_by_component`) over the same raw
     trade-diagnostics/bars.csv records the pre-S2d version copied verbatim
     -- a real record count and simple order statistics, never a fabricated
     or curve-fit figure. This applies whether or not `variants` is passed
     (a single-run trade_efficiency/component_attribution report is
     compacted too) -- the one thing `variants=None`'s docstring promise
     does NOT cover byte-for-byte, because these two reports' raw per-record
     lists were themselves the reason S2d exists (see REPORT_CHAR_BUDGET).

THE LOOKAHEAD TRAP, AND WHY THIS IS SAFE
------------------------------------------
_hindsight_labels() deliberately looks at FUTURE bars relative to bar i (that
is the entire point of a hindsight label: "what did price actually do
next"). E-040's own decided-checks note names this as a known trap: "the
hindsight labeller must never reach a signal." The guard here is structural,
not a flag: this module is a standalone, run-after-the-fact reporting tool.
Nothing in strategies/, execution/, or risk/ imports it, calls it, or reads
its output; its only caller in the live pipeline is the protocol_execution
branch of workflow/run_phase1_research.py, AFTER a run's backtest has
already completed and AFTER trade_diagnostics.json/protocol_result.yaml are
already final. The hindsight label is written only into
artifacts/reports/regime_power.yaml and never read back into anything that
makes a trading decision.

CLI
---
    python build_reports.py <run_dir> [--no-write]

`<run_dir>` is a path to a run directory, e.g. strategy-research/runs/run_059
(relative to your current working directory, or absolute). `--no-write`
builds the five report dicts in memory and prints a summary without touching
disk (used by tests).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

REPORT_CATEGORIES = [
    "profitability",
    "trade_efficiency",
    "forecast_power",
    "regime_power",
    "component_attribution",
]

# [NEW COMPUTATION -- see module docstring] tuning constants for the
# hindsight-lag comparison. Forward horizon used to label the hindsight-
# optimal direction at each bar, and the maximum bar-distance within which a
# live regime transition may be matched to a hindsight-label transition.
_HINDSIGHT_HORIZON_BARS = 5
_HINDSIGHT_MATCH_WINDOW_BARS = 20

_COMPONENT_COLUMN_PREFIX = "debug_info.components."


# ---------------------------------------------------------------------------
# Small shared helpers
# ---------------------------------------------------------------------------

def _unavailable(reason: str) -> dict:
    """The explicit empty/null shape a slice takes when its source data
    genuinely doesn't support that cut. Never used to hide a bug -- every
    call site names the specific missing source."""
    return {"unavailable": True, "reason": reason}


def _wrap(category: str, overall: Any, per_window: Any, per_regime: Any, per_symbol: Any) -> dict:
    return {
        "category": category,
        "slices": {
            "overall": overall,
            "per_window": per_window,
            "per_regime": per_regime,
            "per_symbol": per_symbol,
        },
    }


def _group_by(items: list[dict], key_fn: Callable[[dict], Any]) -> dict[Any, list[dict]]:
    """Pure regrouping by an already-existing field -- no arithmetic, so this
    does not count as new computation. Used for every per_window/per_regime/
    per_symbol slice built off a flat list of source records (trades,
    component-attribution rows)."""
    grouped: dict[Any, list[dict]] = defaultdict(list)
    for item in items:
        grouped[key_fn(item)].append(item)
    return dict(grouped)


def _percentile(sorted_values: list[float], pct: float) -> float:
    """Linear-interpolation percentile (numpy's default 'linear' method),
    `sorted_values` must already be sorted and non-empty."""
    n = len(sorted_values)
    if n == 1:
        return sorted_values[0]
    k = (n - 1) * pct
    f = int(k)
    c = min(f + 1, n - 1)
    if f == c:
        return sorted_values[f]
    return sorted_values[f] * (c - k) + sorted_values[c] * (k - f)


def _numeric_or_none(value: Any) -> float | None:
    """Coerces a record value to float for aggregation, or None if it isn't
    numeric. Trade-diagnostics records are already real Python int/float
    (JSON-loaded); bars.csv-derived component-attribution records are raw
    CSV strings (csv.DictReader, never cast upstream -- same as every other
    bars.csv consumer in this file, e.g. _compute_hindsight_lag's own
    `float(row["close"])`), so a numeric-looking string is coerced too.
    Booleans are excluded on purpose (never averaged as 0/1 here -- a rate
    would be a different, not-yet-decided statistic)."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _aggregate_records(records: list[dict]) -> dict:
    """[NEW COMPUTATION -- G7, C2_S1_FINDINGS.md, operator-accepted 2026-09-28]
    Collapses a list of per-record dicts (one per trade, or one per bar-
    component measurement) into {n, <numeric field>: {mean, median, p10,
    p90}}, dropping the individual records. Non-numeric fields (ids,
    timestamps, labels) are summarized only by inclusion in `n` -- their
    per-record values still exist verbatim upstream (trade_diagnostics.json /
    bars.csv), this is a report-scale slice, not the only copy of the data."""
    agg: dict = {"n": len(records)}
    if not records:
        return agg
    fields: dict[str, list[float]] = defaultdict(list)
    for rec in records:
        for key, value in rec.items():
            num = _numeric_or_none(value)
            if num is None:
                continue
            fields[key].append(num)
    for key in sorted(fields):
        values = sorted(fields[key])
        if not values:
            continue
        agg[key] = {
            "mean": statistics.fmean(values),
            "median": statistics.median(values),
            "p10": _percentile(values, 0.10),
            "p90": _percentile(values, 0.90),
        }
    return agg


def _aggregate_by_component(records: list[dict]) -> dict:
    """component_attribution's own compaction (G7): aggregate WITHIN each
    component, never across components -- blending unrelated components'
    values into one set of stats would hide exactly the per-component signal
    this report exists to carry."""
    by_component = _group_by(records, lambda rec: rec["component"])
    return {comp: _aggregate_records(recs) for comp, recs in sorted(by_component.items())}


def _write_yaml_atomic(path: Path, data: Any) -> None:
    """Same temp-file-then-os.replace pattern as
    workflow/run_phase1_research.py::save_yaml, so a crash mid-write can
    never leave a partially-written report on disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _load_yaml(path: Path):
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_json(path: Path):
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_bars_csv(path: Path) -> list[dict] | None:
    if not path.exists():
        return None
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Source loading
# ---------------------------------------------------------------------------

def load_run_sources(run_dir: Path, *, protocol_result_path: Path | None = None,
                      trade_diagnostics_path: Path | None = None,
                      variant_run_dir: Path | None = None) -> dict:
    """Load every source artifact this tool re-projects, from one run
    directory. Missing files are represented as None/{}/[] -- every builder
    function below must handle that explicitly (see each function's
    _unavailable(...) branches) rather than assume presence.

    E-061 C2 S2d: the three keyword overrides let a caller point this at one
    VARIANT's own sources instead of the run-level defaults, without changing
    a single line of any builder function below (they only ever read the
    returned `sources` dict). Every default is exactly today's single-run
    path, so `load_run_sources(run_dir)` is byte-identical to before this
    slice. Callers pass:
      protocol_result_path = RUN_DIR/artifacts/variants/<vid>/protocol_result.yaml
      trade_diagnostics_path = RUN_DIR/variants/<vid>/trade_diagnostics.json
      variant_run_dir = RUN_DIR/variants/<vid>   (bars.csv lives under
        <variant_run_dir>/results/<window_run_id>/bars.csv)
    """
    run_dir = Path(run_dir)
    artifacts = run_dir / "artifacts"
    pr_path = protocol_result_path if protocol_result_path is not None \
        else artifacts / "protocol_result.yaml"
    protocol_result = _load_yaml(pr_path) or {}
    td_path = trade_diagnostics_path if trade_diagnostics_path is not None \
        else run_dir / "trade_diagnostics.json"
    trade_diagnostics = _load_json(td_path)

    bars_root = variant_run_dir if variant_run_dir is not None else run_dir
    bars_by_window: dict[tuple, list[dict] | None] = {}
    for entry in protocol_result.get("results") or []:
        window_run_id = entry.get("run_id")
        if not window_run_id:
            continue
        bars_path = bars_root / "results" / window_run_id / "bars.csv"
        bars_by_window[(entry.get("symbol"), entry.get("window"))] = _load_bars_csv(bars_path)

    return {
        "run_dir": run_dir,
        "protocol_result": protocol_result,
        "trade_diagnostics": trade_diagnostics,
        "bars_by_window": bars_by_window,
    }


# ---------------------------------------------------------------------------
# profitability.yaml
# ---------------------------------------------------------------------------

def build_profitability_report(sources: dict) -> dict:
    pr = sources["protocol_result"]
    results = pr.get("results") or []
    hv = pr.get("hypothesis_verdict") or {}
    diagnostics = hv.get("diagnostics")

    if diagnostics:
        overall = {
            "source": "protocol_result.yaml:hypothesis_verdict.diagnostics "
                       "(pre-computed aggregate, re-projected verbatim)",
            "diagnostics": diagnostics,
            "verdict": hv.get("verdict"),
            "verdict_reason": hv.get("verdict_reason"),
        }
    else:
        overall = _unavailable(
            "protocol_result.yaml has no hypothesis_verdict.diagnostics block for this run.")

    if not results:
        no_results_reason = "protocol_result.yaml has no results entries for this run."
        return _wrap("profitability", overall, _unavailable(no_results_reason),
                      _unavailable(no_results_reason), _unavailable(no_results_reason))

    per_window = [
        {"symbol": r.get("symbol"), "window": r.get("window"), "run_id": r.get("run_id"),
         "core": r.get("core")}
        for r in results
    ]

    per_regime: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        for regime, block in (r.get("per_regime") or {}).items():
            per_regime[regime].append({"symbol": r.get("symbol"), "window": r.get("window"), **block})
    per_regime_out = dict(per_regime) if per_regime else _unavailable(
        "no result entry in protocol_result.yaml carried a per_regime block.")

    # CUL-370: an INDEX of each symbol's windows, not a second copy of `core`.
    # per_window already carries every core block with its symbol; repeating
    # it here doubled the report (716,645 chars on 95 windows x 2 variants,
    # over REPORT_CHAR_BUDGET). Group per_window by `symbol` for a per-symbol
    # view.
    per_symbol: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        per_symbol[r.get("symbol")].append({"window": r.get("window"), "run_id": r.get("run_id")})
    per_symbol_out = dict(per_symbol)

    return _wrap("profitability", overall, per_window, per_regime_out, per_symbol_out)


# C5.8 (C13, D-050): the legacy label fields a profitability report re-projects.
# Under build_reports(legacy_verdict_retired=True) they are dropped, so readers
# score from the numbers, never from a verdict-shaped word. Every numeric field
# stays (post_backtest_cost_check(_real), the correlation fields, the
# diagnostics' median_* figures).
LEGACY_VERDICT_OVERALL_KEYS = ("verdict", "verdict_reason")
LEGACY_ROUTE_DIAGNOSTICS_KEYS = ("post_backtest_route_real", "post_backtest_route_real_tied",
                                 "cost_dominated_real")
LEGACY_ROUTE_CORE_KEYS = ("post_backtest_route", "post_backtest_route_rationale",
                          "post_backtest_route_real", "post_backtest_route_real_rationale")


def _without(d: dict, keys: tuple) -> dict:
    return {k: v for k, v in d.items() if k not in keys}


def _strip_legacy_verdict_slices(slices: dict) -> dict:
    out = dict(slices)
    overall = slices.get("overall")
    if isinstance(overall, dict) and not overall.get("unavailable"):
        overall = _without(overall, LEGACY_VERDICT_OVERALL_KEYS)
        if isinstance(overall.get("diagnostics"), dict):
            overall["diagnostics"] = _without(overall["diagnostics"], LEGACY_ROUTE_DIAGNOSTICS_KEYS)
        out["overall"] = overall
    per_window = slices.get("per_window")
    if isinstance(per_window, list):
        out["per_window"] = [
            {**row, "core": _without(row["core"], LEGACY_ROUTE_CORE_KEYS)}
            if isinstance(row, dict) and isinstance(row.get("core"), dict) else row
            for row in per_window]
    per_symbol = slices.get("per_symbol")
    if isinstance(per_symbol, dict):  # an {unavailable, reason} block has no list values
        out["per_symbol"] = {
            sym: ([_without(r, LEGACY_ROUTE_CORE_KEYS) if isinstance(r, dict) else r for r in rows]
                  if isinstance(rows, list) else rows)
            for sym, rows in per_symbol.items()}
    return out


def _strip_legacy_verdict_fields(report: dict) -> dict:
    """C5.8: a copy of a profitability report, in either shape (single-run
    `slices`, or schema 2 `variants.<vid>.slices`), without the legacy label:
    `verdict`/`verdict_reason` in `overall`, the three route keys in
    `overall.diagnostics`, and the four route/rationale keys in every
    `per_window[].core` and `per_symbol[<sym>][]` row. Nothing else changes.
    Pure: the input is never mutated."""
    out = dict(report)
    if isinstance(report.get("slices"), dict):
        out["slices"] = _strip_legacy_verdict_slices(report["slices"])
    if isinstance(report.get("variants"), dict):
        out["variants"] = {
            vid: ({**block, "slices": _strip_legacy_verdict_slices(block["slices"])}
                  if isinstance(block, dict) and isinstance(block.get("slices"), dict) else block)
            for vid, block in report["variants"].items()}
    return out


# ---------------------------------------------------------------------------
# trade_efficiency.yaml
# ---------------------------------------------------------------------------

def build_trade_efficiency_report(sources: dict) -> dict:
    pr = sources["protocol_result"]
    summary = pr.get("trade_diagnostics_summary")
    if summary:
        overall = {
            "source": "protocol_result.yaml:trade_diagnostics_summary "
                       "(pre-computed aggregate, re-projected verbatim)",
            **summary,
        }
    else:
        overall = _unavailable("protocol_result.yaml has no trade_diagnostics_summary block.")

    td = sources["trade_diagnostics"]
    trades = (td or {}).get("trades") if td else None
    if trades:
        # G7 compaction: each grouping is {key: aggregate}, not {key: [raw
        # trade dicts]} -- see _aggregate_records' docstring.
        per_window = {k: _aggregate_records(v)
                      for k, v in _group_by(trades, lambda t: t.get("window")).items()}
        per_symbol = {k: _aggregate_records(v)
                      for k, v in _group_by(trades, lambda t: t.get("symbol")).items()}
        per_regime = {k: _aggregate_records(v)
                      for k, v in _group_by(trades, lambda t: t.get("regime_at_entry")).items()}
    else:
        reason = (
            "no trade_diagnostics.json found alongside this run (or it has an "
            "empty trades list); only the pre-aggregated trade_diagnostics_summary "
            "in protocol_result.yaml is available -- see the overall slice."
        )
        per_window = _unavailable(reason)
        per_symbol = _unavailable(reason)
        per_regime = _unavailable(reason)

    return _wrap("trade_efficiency", overall, per_window, per_regime, per_symbol)


# ---------------------------------------------------------------------------
# forecast_power.yaml
# ---------------------------------------------------------------------------

def build_forecast_power_report(sources: dict) -> dict:
    pr = sources["protocol_result"]
    results = pr.get("results") or []
    hv_diag = (pr.get("hypothesis_verdict") or {}).get("diagnostics") or {}
    cross_check = pr.get("prescreen_backtest_cross_check")

    overall: dict = {}
    if "median_forecast_return_corr" in hv_diag:
        overall["median_forecast_return_corr"] = hv_diag["median_forecast_return_corr"]
        overall["median_forecast_return_corr_source"] = \
            "protocol_result.yaml:hypothesis_verdict.diagnostics.median_forecast_return_corr"
    if cross_check is not None:
        overall["prescreen_backtest_cross_check"] = cross_check
    overall_out = overall if overall else _unavailable(
        "protocol_result.yaml has neither hypothesis_verdict.diagnostics."
        "median_forecast_return_corr nor a prescreen_backtest_cross_check block.")

    if not results:
        reason = "protocol_result.yaml has no results entries for this run."
        return _wrap("forecast_power", overall_out, _unavailable(reason),
                      _unavailable(reason), _unavailable(reason))

    per_window = []
    for r in results:
        core = r.get("core") or {}
        per_window.append({
            "symbol": r.get("symbol"), "window": r.get("window"), "run_id": r.get("run_id"),
            "forecast_return_corr": core.get("forecast_return_corr"),
            "forecast_return_corr_pvalue": core.get("forecast_return_corr_pvalue"),
        })

    per_regime: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        for regime, block in (r.get("regime_validity") or {}).items():
            per_regime[regime].append({"symbol": r.get("symbol"), "window": r.get("window"), **block})
    per_regime_out = dict(per_regime) if per_regime else _unavailable(
        "no result entry in protocol_result.yaml carried a regime_validity block.")

    per_symbol: dict[str, list[dict]] = defaultdict(list)
    for entry in per_window:
        per_symbol[entry["symbol"]].append({
            "window": entry["window"],
            "forecast_return_corr": entry["forecast_return_corr"],
            "forecast_return_corr_pvalue": entry["forecast_return_corr_pvalue"],
        })
    per_symbol_out = dict(per_symbol)

    return _wrap("forecast_power", overall_out, per_window, per_regime_out, per_symbol_out)


# ---------------------------------------------------------------------------
# regime_power.yaml -- health (pure re-projection) + hindsight-lag (NEW COMPUTATION)
# ---------------------------------------------------------------------------

def _hindsight_labels(closes: list[float], horizon: int) -> list[str | None]:
    """[NEW COMPUTATION -- see module docstring's "ONE exception"]. For each
    bar i, label 'up'/'down'/'flat' by the sign of the close price `horizon`
    bars in the future relative to bar i. The last `horizon` bars of any
    series get label None (not enough future data to compute).

    This deliberately looks ahead -- see module docstring's "THE LOOKAHEAD
    TRAP" section for why writing this only into a report is safe."""
    n = len(closes)
    labels: list[str | None] = [None] * n
    for i in range(n - horizon):
        now, future = closes[i], closes[i + horizon]
        if future > now:
            labels[i] = "up"
        elif future < now:
            labels[i] = "down"
        else:
            labels[i] = "flat"
    return labels


def _transition_indices(labels: list) -> list[int]:
    """Bar indices where label[i] != label[i-1]. Skips None (hindsight label
    not yet computable), '' (the observed trailing-partial-bar data quirk:
    every window's bars.csv in the real corpus, e.g. run_059/run_054, writes
    an empty `regime` value on its final row -- the not-yet-classified
    boundary bar, not a real regime change), and 'unknown' (MarketRegime.UNKNOWN
    -- the detector's own not-yet-classified/gate-closed label, emitted both
    during warmup and on every gate-fail bar in threshold_rules/score_product
    mode, per trading-bot/strategies/regime_engine.py) on either side of a
    comparison, so none of the three is mistaken for a genuine regime
    detection.

    CODE-REVIEW FIX (2026-09-21): 'unknown' was not excluded originally --
    the bar where a window's detector first finishes warmup (label flips
    from 'unknown' to a real regime) was counted as a live transition,
    contaminating _compute_hindsight_lag's lag statistic with a 'time to
    finish warmup' figure indistinguishable from a genuine regime-change
    lag. Excluding 'unknown' here means a transition INTO or OUT OF a real
    regime (from/to unknown) is not counted either -- this is deliberate:
    the gate opening/closing is a different event from the regime the gate
    then reveals, and this metric measures lag on regime CHANGES, not on
    gate state changes."""
    idx = []
    prev = None
    for i, label in enumerate(labels):
        if label in (None, "", "unknown"):
            continue
        if prev is not None and label != prev:
            idx.append(i)
        prev = label
    return idx


def _compute_hindsight_lag(bars: list[dict]) -> dict:
    """[NEW COMPUTATION]. Returns the lag, in bars, between each live regime
    transition and the nearest hindsight-label transition within
    _HINDSIGHT_MATCH_WINDOW_BARS. A positive lag means the live label changed
    AFTER the hindsight-optimal direction did (expected for a causal
    detector); this measures LAG, not correctness -- it says nothing about
    whether the live label was the right one, only how quickly it moved
    relative to what hindsight says price actually did next."""
    if not bars:
        return _unavailable("no bars.csv rows for this window.")
    try:
        closes = [float(row["close"]) for row in bars]
    except (KeyError, ValueError) as exc:
        return _unavailable(f"bars.csv missing/non-numeric close column ({exc}).")

    live_labels = [row.get("regime") for row in bars]
    live_transitions = _transition_indices(live_labels)
    hindsight_labels = _hindsight_labels(closes, _HINDSIGHT_HORIZON_BARS)
    hindsight_transitions = _transition_indices(hindsight_labels)

    if not live_transitions:
        return {
            "live_transition_count": 0,
            "hindsight_transition_count": len(hindsight_transitions),
            "lags_bars": [],
            "median_lag_bars": None,
            "reason": (
                "detector emitted zero live regime transitions in this window "
                "(excluding the trailing blank-regime row and 'unknown' "
                "warmup/gate-closed bars -- see _transition_indices' "
                "docstring) -- a constant single-label window."
            ),
        }

    lags = []
    for live_idx in live_transitions:
        candidates = [h for h in hindsight_transitions
                      if abs(h - live_idx) <= _HINDSIGHT_MATCH_WINDOW_BARS]
        if candidates:
            nearest = min(candidates, key=lambda h: abs(h - live_idx))
            lags.append(live_idx - nearest)

    return {
        "live_transition_count": len(live_transitions),
        "hindsight_transition_count": len(hindsight_transitions),
        "lags_bars": lags,
        "median_lag_bars": statistics.median(lags) if lags else None,
        "reason": None if lags else (
            f"{len(live_transitions)} live transition(s) found but none had a "
            f"hindsight-label transition within {_HINDSIGHT_MATCH_WINDOW_BARS} bars."
        ),
    }


def build_regime_power_report(sources: dict) -> dict:
    pr = sources["protocol_result"]
    results = pr.get("results") or []
    bars_by_window = sources["bars_by_window"]

    overall = {
        "note": (
            "E-040's decided regime-power checks (EPICS.md) rank three items: "
            "(a) does using the regime label beat ignoring it, (b) a "
            "hindsight-lag comparison measuring LAG not correctness, (c) "
            "detector health numbers. delivery_plan_v26.md's Slice 5a text "
            "names only (b) and (c) as this slice's inherited scope -- (a) is "
            "intentionally NOT computed or claimed anywhere in this report. "
            "(c) is not in this report either (CUL-381): no detector health "
            "is produced from this run's own backtest, and the campaign-level "
            "file belonged to another run."
        ),
    }

    if not results:
        reason = "protocol_result.yaml has no results entries for this run."
        return _wrap("regime_power", overall, _unavailable(reason),
                      _unavailable(reason), _unavailable(reason))

    per_window = []
    for r in results:
        key = (r.get("symbol"), r.get("window"))
        bars = bars_by_window.get(key)
        if bars is None:
            hindsight_lag = _unavailable(
                f"no bars.csv found for {key[0]} {key[1]} "
                f"(results/{r.get('run_id')}/bars.csv missing).")
        else:
            hindsight_lag = _compute_hindsight_lag(bars)
        per_window.append({
            "symbol": r.get("symbol"), "window": r.get("window"), "run_id": r.get("run_id"),
            "per_regime": r.get("per_regime"),
            "regime_validity": r.get("regime_validity"),
            "hindsight_lag": hindsight_lag,
        })

    per_regime: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        for regime, block in (r.get("per_regime") or {}).items():
            per_regime[regime].append({
                "symbol": r.get("symbol"), "window": r.get("window"),
                "per_regime": block,
                "regime_validity": (r.get("regime_validity") or {}).get(regime),
            })
    per_regime_out = dict(per_regime) if per_regime else _unavailable(
        "no result entry in protocol_result.yaml carried a per_regime block.")

    per_symbol: dict[str, list[dict]] = defaultdict(list)
    for entry in per_window:
        per_symbol[entry["symbol"]].append(entry)
    per_symbol_out = dict(per_symbol)

    return _wrap("regime_power", overall, per_window, per_regime_out, per_symbol_out)


# ---------------------------------------------------------------------------
# component_attribution.yaml
# ---------------------------------------------------------------------------

def _parse_component_columns(fieldnames: list[str]) -> dict[str, dict[str, str]]:
    """Map component_name -> {metric_name: column_name} for every
    debug_info.components.<name>.<metric> column in a bars.csv header."""
    components: dict[str, dict[str, str]] = defaultdict(dict)
    for col in fieldnames:
        if not col.startswith(_COMPONENT_COLUMN_PREFIX):
            continue
        rest = col[len(_COMPONENT_COLUMN_PREFIX):]
        if "." not in rest:
            continue
        name, metric = rest.split(".", 1)
        components[name][metric] = col
    return dict(components)


def _component_records(bars: list[dict], symbol: str, window: str) -> list[dict]:
    if not bars:
        return []
    components = _parse_component_columns(list(bars[0].keys()))
    records = []
    for row in bars:
        for name, metric_cols in components.items():
            records.append({
                "symbol": symbol,
                "window": window,
                "timestamp": row.get("timestamp"),
                "regime": row.get("regime"),
                "component": name,
                **{metric: row.get(col) for metric, col in metric_cols.items()},
            })
    return records


def build_component_attribution_report(sources: dict) -> dict:
    pr = sources["protocol_result"]
    results = pr.get("results") or []
    bars_by_window = sources["bars_by_window"]

    all_records: list[dict] = []
    discovered: set[str] = set()
    for r in results:
        key = (r.get("symbol"), r.get("window"))
        bars = bars_by_window.get(key)
        if not bars:
            continue
        recs = _component_records(bars, r.get("symbol"), r.get("window"))
        all_records.extend(recs)
        discovered.update(rec["component"] for rec in recs)

    if discovered:
        overall = {
            "components_discovered": sorted(discovered),
            "note": "inventory only (component names parsed from bars.csv "
                    "debug_info.components.* column headers); per_window/per_regime/"
                    "per_symbol below are G7-compacted per-component aggregates "
                    "(n, mean, median, p10, p90), not raw per-bar rows.",
        }
    else:
        overall = _unavailable(
            "no debug_info.components.*.* columns found in any window's bars.csv "
            "for this run.")

    if all_records:
        # G7 compaction: aggregate WITHIN each component (_aggregate_by_component),
        # per window/regime/symbol -- {key: {component: aggregate}}, not
        # {key: [raw per-bar-per-component records]}.
        per_window = {k: _aggregate_by_component(v)
                      for k, v in _group_by(all_records, lambda rec: rec["window"]).items()}
        # CODE-REVIEW FIX (2026-09-21): every window's bars.csv ends with one
        # trailing boundary row whose `regime` value is the empty string (the
        # not-yet-classified final bar -- same data quirk _transition_indices
        # above documents and excludes). Grouping on the raw `regime` field
        # unfiltered put that row's component records under an undocumented
        # "" key here, unlike regime_power's handling of the same quirk.
        # Excluded from per_regime specifically; per_window/per_symbol are
        # unaffected since they don't key on regime.
        _regime_records = [rec for rec in all_records if rec["regime"] != ""]
        per_regime = {k: _aggregate_by_component(v)
                      for k, v in _group_by(_regime_records, lambda rec: rec["regime"]).items()}
        per_symbol = {k: _aggregate_by_component(v)
                      for k, v in _group_by(all_records, lambda rec: rec["symbol"]).items()}
    else:
        reason = "no component records extracted (see overall slice's reason)."
        per_window = _unavailable(reason)
        per_regime = _unavailable(reason)
        per_symbol = _unavailable(reason)

    return _wrap("component_attribution", overall, per_window, per_regime, per_symbol)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

BUILDERS: dict[str, Callable[[dict], dict]] = {
    "profitability": build_profitability_report,
    "trade_efficiency": build_trade_efficiency_report,
    "forecast_power": build_forecast_power_report,
    "regime_power": build_regime_power_report,
    "component_attribution": build_component_attribution_report,
}

# E-061 C2 S2d (G7): a report this size, YAML-serialized, is a real bug (an
# unbounded grouping key -- e.g. one component/window/regime pair per bar
# that G7's aggregation should have collapsed), never something to silently
# truncate. Generous over any real report measured so far (C2_S1_FINDINGS.md's
# own table showed up to ~440K chars for an UNCOMPACTED trade_efficiency
# report and ~1.7M for UNCOMPACTED component_attribution; G7's aggregation
# brings both down by orders of magnitude). CORRECTED 2026-10-02 (CUL-370):
# profitability/forecast_power/regime_power list one row per window, so they
# grow linearly with windows x variants and do NOT always stay under this:
# run_064's profitability.yaml was 716,645 chars on 95 monthly windows x 2
# variants, ~40% of it a duplicate of each `core` block in per_symbol (now an
# index). Measured on run_064's two variants (190 window-variants): the slices
# went from 647,950 to 386,366 chars, ~2.0K per window-variant -- so run_064
# itself (slices + ~69K of the rest of the report) would still be ~455K, over
# budget. Long protocols are bounded by choosing fewer, longer windows
# (RUNBOOK); the per-window layout itself is for the report review epic.
REPORT_CHAR_BUDGET = 400_000


def _check_report_budget(category: str, report: dict) -> None:
    """Fail loud (G7) rather than silently write, or silently truncate, an
    oversized report -- see REPORT_CHAR_BUDGET's own comment."""
    size = len(yaml.safe_dump(report, sort_keys=False, allow_unicode=True))
    if size > REPORT_CHAR_BUDGET:
        raise ValueError(
            f"{category}.yaml would be {size} chars, over REPORT_CHAR_BUDGET="
            f"{REPORT_CHAR_BUDGET} -- refusing to write an oversized report. This means "
            f"a grouping key has unbounded cardinality (e.g. too many distinct windows/"
            f"components/variants) -- fix the aggregation, never raise this budget to "
            f"make the symptom disappear."
        )


def _variant_sources(run_dir: Path, variant_id: str) -> dict:
    """load_run_sources pointed at one variant's own artifacts (E-061 C2 S2b's
    per-variant layout, S1_FINDINGS.md C2.2 proposed change #2):
      artifacts/variants/<vid>/protocol_result.yaml
      variants/<vid>/trade_diagnostics.json
      variants/<vid>/results/<window_run_id>/bars.csv"""
    variant_artifacts_dir = run_dir / "artifacts" / "variants" / variant_id
    variant_run_dir = run_dir / "variants" / variant_id
    return load_run_sources(
        run_dir,
        protocol_result_path=variant_artifacts_dir / "protocol_result.yaml",
        trade_diagnostics_path=variant_run_dir / "trade_diagnostics.json",
        variant_run_dir=variant_run_dir,
    )


# CUL-413 (D-077): what forecast_power's correlations are, written next to them
# only when build_reports(label_statistics=True) -- the orchestrator passes it
# under orchestrator.reader_findings only (v3 readers), because v2 readers read
# this same report and their prompts must not change. Source:
# trading-bot/reporting/run_artifact.py (pearson_correlation of forecast vs
# close[t+1]/close[t]-1 on bars with forecast != 0) and tools/run_protocol.py
# (the median of those per-window values).
FORECAST_POWER_STATISTIC_LABELS = {
    "forecast_return_corr": ("Pearson correlation of the forecast with the next bar's return, "
                             "on active bars (forecast != 0), one value per window"),
    "forecast_return_corr_pvalue": "t-test p-value of that Pearson correlation",
    "median_forecast_return_corr": ("median over windows of forecast_return_corr (Pearson, "
                                    "active bars, next-bar return)"),
    # review: present only when the run had a prescreen (tools/run_protocol.py)
    "prescreen_backtest_cross_check.prescreen_pooled_ic": (
        "the prescreen's pooled information coefficient (computed by the prescreen, not by "
        "the claim test); that block compares its SIGN with the backtest's mean "
        "forecast_return_corr (Pearson, active bars)"),
}


def build_reports(run_dir: Path | str, write: bool = True, *,
                   variants: dict[str, dict] | None = None,
                   failed_variants: dict[str, str] | None = None,
                   untested_variants: dict[str, str] | None = None,
                   legacy_verdict_retired: bool = False,
                   label_statistics: bool = False) -> dict[str, dict]:
    """Build all five category reports for one run directory.

    `variants=None` (the default): today's single-run behaviour -- reads the
    run-level artifacts/protocol_result.yaml, trade_diagnostics.json and
    results/<w>/bars.csv, and every report keeps its original
    `{category, source_run_id, generated_at, slices}` shape. profitability/
    forecast_power/regime_power are byte-identical to before E-061 C2 S2d;
    trade_efficiency/component_attribution's per_window/per_regime/per_symbol
    slices are G7-compacted aggregates rather than raw record lists even here
    -- see the module docstring's "two exceptions" section (exception 2).

    `variants={<vid>: {kind, symbol, status, ...}}` (E-061 C2 S2d, G7/G8,
    C2_S1_FINDINGS.md's C2.2): builds each of the five reports from every
    named variant's OWN sources (`_variant_sources`) instead of the run-level
    ones, and wraps them as `schema_version: 2`:

        category: <name>
        source_run_id: <run_dir.name>
        generated_at: <UTC ISO timestamp>
        schema_version: 2
        variants:
          <vid>: {kind: <str|None>, symbol: <str|None>, status: <str>,
                  coverage: <str>,  # only present when the caller's vinfo carries one
                  slices: {overall, per_window, per_regime, per_symbol}}
          ...
        failed_variants: {<vid>: <reason>}       # only when failed_variants given
        untested_variants: {<vid>: <reason>}     # only when untested_variants given

    `kind`/`symbol` are read from each `variants[vid]` entry when present and
    left `None` otherwise (E-061 C2 S2b adds those fields to
    artifacts/variants/index.yaml; this function never invents them). `status`
    defaults to `"graded"` when the caller's vinfo doesn't carry one --
    meaning only "this variant was backtested and graded," never a verdict
    (readers must not read it as "this variant passed"). `coverage` is a
    plain passthrough, present only when `vinfo` carries one (E-061 C2 S2b's
    D-042 partial-coverage marker, e.g. `"partial, windows run 2 of 4"`) --
    this function never computes it. There is no separate top-level `slices`
    for a "base" variant -- G8's own token-saving call -- every variant,
    including base, lives under `variants.<vid>.slices`. `failed_variants`/
    `untested_variants` are never columns: they carry only the reason string
    a reader can cite, exactly mirroring `verdict_criteria_evaluator.evaluate_grid`'s
    own top-level keys of the same name, so a reader that already understands
    grid_evaluation.yaml reads these the same way.

    Every built report is checked against REPORT_CHAR_BUDGET before being
    returned or written (both branches) -- see that constant's own comment.

    `legacy_verdict_retired=True` (C5.8, C13/D-050; passed by the orchestrator's
    variant loop only under config_direct_authoring AND verdict_routing_retired):
    the profitability report, in either shape, goes through
    `_strip_legacy_verdict_fields` -- no `verdict`/`verdict_reason`, no
    post_backtest_route* / cost_dominated_real label keys; every number stays.
    The other four reports are unchanged. False (the default): the output is
    exactly the pre-C5.8 output.

    `label_statistics=True` (CUL-413, D-077; passed by the orchestrator only
    under orchestrator.reader_findings): the forecast_power report gains one
    top-level key, `statistic_labels` (FORECAST_POWER_STATISTIC_LABELS: which
    correlation each field is). False (the default): unchanged output.

    When `write` is True (the default, and what
    workflow/run_phase1_research.py's protocol_execution branch uses), writes
    each report to <run_dir>/artifacts/reports/<category>.yaml via the same
    atomic temp-file-then-replace pattern as save_yaml. Returns the built
    dicts either way, so tests can inspect content without touching disk
    (write=False)."""
    run_dir = Path(run_dir)
    generated_at = datetime.now(timezone.utc).isoformat()
    source_run_id = run_dir.name

    reports: dict[str, dict] = {}
    if variants is None:
        sources = load_run_sources(run_dir)
        for name, builder in BUILDERS.items():
            report = builder(sources)
            report["source_run_id"] = source_run_id
            report["generated_at"] = generated_at
            _check_report_budget(name, report)
            reports[name] = report
    else:
        if not isinstance(variants, dict) or not variants:
            raise ValueError(
                "variants must be a non-empty {variant_id: {...}} dict when given -- pass "
                "None (the default) for single-run behaviour, never an empty dict.")
        per_variant_sources = {vid: _variant_sources(run_dir, vid) for vid in variants}
        for name, builder in BUILDERS.items():
            variant_blocks = {}
            for vid, vinfo in variants.items():
                built = builder(per_variant_sources[vid])
                variant_blocks[vid] = {
                    "kind": (vinfo or {}).get("kind"),
                    "symbol": (vinfo or {}).get("symbol"),
                    "status": (vinfo or {}).get("status", "graded"),
                    **({"coverage": vinfo["coverage"]}
                       if isinstance(vinfo, dict) and vinfo.get("coverage") else {}),
                    "slices": built["slices"],
                }
            report = {
                "category": name,
                "source_run_id": source_run_id,
                "generated_at": generated_at,
                "schema_version": 2,
                "variants": variant_blocks,
            }
            if failed_variants:
                report["failed_variants"] = dict(failed_variants)
            if untested_variants:
                report["untested_variants"] = dict(untested_variants)
            _check_report_budget(name, report)
            reports[name] = report

    if legacy_verdict_retired:  # C5.8: only drops keys, so the budget check above still holds
        reports["profitability"] = _strip_legacy_verdict_fields(reports["profitability"])

    if label_statistics:  # CUL-413 (D-077): v3 readers only; adds one small key
        reports["forecast_power"] = {**reports["forecast_power"],
                                     "statistic_labels": dict(FORECAST_POWER_STATISTIC_LABELS)}

    if write:
        out_dir = run_dir / "artifacts" / "reports"
        for name, report in reports.items():
            _write_yaml_atomic(out_dir / f"{name}.yaml", report)

    return reports


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", help="Path to a run directory, e.g. strategy-research/runs/run_059")
    parser.add_argument("--no-write", action="store_true",
                         help="Build reports in memory only; do not write artifacts/reports/*.yaml.")
    args = parser.parse_args()

    reports = build_reports(Path(args.run_dir), write=not args.no_write)
    for name in REPORT_CATEGORIES:
        report = reports[name]
        slice_summary = {
            slice_name: ("unavailable" if isinstance(v, dict) and v.get("unavailable") else "populated")
            for slice_name, v in report["slices"].items()
        }
        print(f"{name}: {slice_summary}")


if __name__ == "__main__":
    main()
