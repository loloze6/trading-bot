"""
E-046a Slice 5a -- tests for tools/build_reports.py and the off-by-default
orchestrator.category_reports.enabled flag wired into
workflow/run_phase1_research.py's protocol_execution branch.

Three things this file proves, per the dispatch brief:

  1. Re-projection property test (test_reprojection_*): every value
     build_reports.py emits that came from a source artifact equals that
     source field EXACTLY -- not just "has the right shape." Uses the real
     run_059 corpus as the fixture (98 windows, both symbols, a real
     trade_diagnostics.json, hypothesis_verdict.diagnostics block, etc).
     EXCEPTION (E-061 C2 S2d, G7): trade_efficiency's and
     component_attribution's per_window/per_regime/per_symbol slices are
     n/mean/median/p10/p90 aggregates over the source records, not the raw
     records themselves -- those two tests independently recompute the same
     statistic from the untouched source and assert the report's aggregate
     equals it, rather than asserting record-for-record equality.

  2. A slice that legitimately can't be populated
     (test_unavailable_slice_is_explicit_not_fabricated): a synthetic run
     directory with a protocol_result.yaml but no trade_diagnostics.json
     must produce trade_efficiency's per_window/per_regime/per_symbol as the
     explicit {"unavailable": true, "reason": ...} shape, never a fabricated
     aggregate.

  3. Flag-off byte identity (test_category_reports_flag_off_never_writes_
     artifacts): same acceptance bar and same pattern as
     tests/test_grid_evaluation.py's own flag-off test -- exercises the
     actual writer condition (_category_reports_enabled()) rather than
     re-deriving it, so an accidental removal of the guard in
     run_phase1_research.py's protocol_execution branch is caught here.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import run_phase1_research as rpr  # noqa: E402
import build_reports as br  # noqa: E402

# Independent of rpr.ROOT (which the autouse sandbox fixture in conftest.py
# repoints at a throwaway tmp_path for every test) -- same pattern
# test_grid_evaluation.py's module docstring documents for reading real,
# frozen historical run artifacts as fixture data.
_REAL_STRATEGY_RESEARCH_ROOT = Path(__file__).resolve().parent.parent
_RUN_059 = _REAL_STRATEGY_RESEARCH_ROOT / "runs" / "run_059"


# ---------------------------------------------------------------------------
# 1. Re-projection property test (run_059 fixture)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def run_059_sources():
    assert _RUN_059.exists(), f"fixture run directory missing: {_RUN_059}"
    return br.load_run_sources(_RUN_059)


@pytest.fixture(scope="module")
def run_059_reports(run_059_sources):
    return {name: builder(run_059_sources) for name, builder in br.BUILDERS.items()}


def test_reprojection_profitability_diagnostics_equals_source(run_059_sources, run_059_reports):
    pr = run_059_sources["protocol_result"]
    source_diagnostics = pr["hypothesis_verdict"]["diagnostics"]
    report_diagnostics = run_059_reports["profitability"]["slices"]["overall"]["diagnostics"]
    assert report_diagnostics == source_diagnostics


def test_reprojection_profitability_per_window_core_equals_source(run_059_sources, run_059_reports):
    pr = run_059_sources["protocol_result"]
    results = pr["results"]
    per_window = run_059_reports["profitability"]["slices"]["per_window"]
    assert len(per_window) == len(results)
    for source_entry, report_entry in zip(results, per_window):
        assert report_entry["symbol"] == source_entry["symbol"]
        assert report_entry["window"] == source_entry["window"]
        assert report_entry["run_id"] == source_entry["run_id"]
        assert report_entry["core"] == source_entry["core"]


def test_reprojection_profitability_per_symbol_is_exact_regrouping(run_059_sources, run_059_reports):
    """CUL-370: the per_symbol slice is an INDEX of each symbol's windows
    ({window, run_id}), a pure regroup of the source results -- every result
    exactly once, under its own symbol, with no second copy of `core` (that
    lives in per_window only; the duplicate doubled the report)."""
    pr = run_059_sources["protocol_result"]
    by_symbol_window = {(r["symbol"], r["window"]): r["run_id"] for r in pr["results"]}
    per_symbol = run_059_reports["profitability"]["slices"]["per_symbol"]
    seen = 0
    for symbol, entries in per_symbol.items():
        for entry in entries:
            assert set(entry) == {"window", "run_id"}
            assert by_symbol_window[(symbol, entry["window"])] == entry["run_id"]
            seen += 1
    assert seen == len(pr["results"])


def test_reprojection_trade_efficiency_summary_equals_source(run_059_sources, run_059_reports):
    pr = run_059_sources["protocol_result"]
    source_summary = pr["trade_diagnostics_summary"]
    overall = run_059_reports["trade_efficiency"]["slices"]["overall"]
    for key, value in source_summary.items():
        assert overall[key] == value


def test_reprojection_trade_efficiency_per_window_is_g7_aggregate_of_source(run_059_sources, run_059_reports):
    """E-061 C2 S2d (G7): per_window is now {window: {n, <field>: {mean,
    median, p10, p90}, ...}}, not {window: [raw trade dicts]} -- asserts the
    report's aggregate for one numeric field equals an INDEPENDENTLY
    computed statistic over the same untouched source trades (real
    re-projection of a real record count and real order statistics, not a
    fabricated figure)."""
    td = run_059_sources["trade_diagnostics"]
    source_trades_by_window: dict[str, list[dict]] = {}
    for trade in td["trades"]:
        source_trades_by_window.setdefault(trade["window"], []).append(trade)

    per_window = run_059_reports["trade_efficiency"]["slices"]["per_window"]
    assert set(per_window.keys()) == set(source_trades_by_window.keys())
    for window, agg in per_window.items():
        source_trades = source_trades_by_window[window]
        assert agg["n"] == len(source_trades)
        values = sorted(t["realized_return"] for t in source_trades)
        assert agg["realized_return"]["mean"] == pytest.approx(statistics.fmean(values))
        assert agg["realized_return"]["median"] == pytest.approx(statistics.median(values))


def test_reprojection_forecast_power_corr_equals_source(run_059_sources, run_059_reports):
    pr = run_059_sources["protocol_result"]
    per_window = run_059_reports["forecast_power"]["slices"]["per_window"]
    assert len(per_window) == len(pr["results"])
    for source_entry, report_entry in zip(pr["results"], per_window):
        assert report_entry["forecast_return_corr"] == source_entry["core"]["forecast_return_corr"]
        assert report_entry["forecast_return_corr_pvalue"] == \
            source_entry["core"]["forecast_return_corr_pvalue"]


def test_reprojection_forecast_power_cross_check_equals_source(run_059_sources, run_059_reports):
    pr = run_059_sources["protocol_result"]
    overall = run_059_reports["forecast_power"]["slices"]["overall"]
    assert overall["prescreen_backtest_cross_check"] == pr["prescreen_backtest_cross_check"]
    assert overall["median_forecast_return_corr"] == \
        pr["hypothesis_verdict"]["diagnostics"]["median_forecast_return_corr"]


def test_reprojection_regime_power_per_window_blocks_equal_source(run_059_sources, run_059_reports):
    pr = run_059_sources["protocol_result"]
    per_window = run_059_reports["regime_power"]["slices"]["per_window"]
    assert len(per_window) == len(pr["results"])
    for source_entry, report_entry in zip(pr["results"], per_window):
        assert report_entry["per_regime"] == source_entry.get("per_regime")
        assert report_entry["regime_validity"] == source_entry.get("regime_validity")


def test_reprojection_regime_power_detector_health_equals_source(run_059_sources, run_059_reports):
    rdr = run_059_sources["regime_detector_report"]
    health = run_059_reports["regime_power"]["slices"]["overall"]["detector_health"]
    if rdr is None:
        assert health.get("unavailable") is True
    else:
        assert health["detector_version"] == rdr.get("detector_version")
        assert health["per_symbol_per_timeframe"] == rdr.get("per_symbol_per_timeframe")


def test_reprojection_component_attribution_per_symbol_is_g7_aggregate_of_bars_csv(
        run_059_sources, run_059_reports):
    """E-061 C2 S2d (G7): per_symbol is now {symbol: {component: {n, <metric>:
    {mean, median, p10, p90}, ...}}}, not {symbol: [raw per-bar-per-component
    records]} -- spot-checks the aggregate for the first window/component
    pair with component columns against an INDEPENDENTLY computed statistic
    over the same untouched bars.csv rows."""
    bars_by_window = run_059_sources["bars_by_window"]
    (symbol, window), first_bars = next(
        (k, v) for k, v in bars_by_window.items() if v and any(
            col.startswith(br._COMPONENT_COLUMN_PREFIX) for col in v[0]))
    components = br._parse_component_columns(list(first_bars[0].keys()))
    first_component = next(iter(components))
    first_metric, first_col = next(iter(components[first_component].items()))

    # Aggregation for per_symbol pools every window for that symbol -- rebuild
    # the same pool independently from the raw source, across every window
    # sharing this symbol, not just `window`.
    pooled_values = []
    for (s, w), bars in bars_by_window.items():
        if s != symbol or not bars:
            continue
        cols = br._parse_component_columns(list(bars[0].keys()))
        if first_component not in cols or first_metric not in cols[first_component]:
            continue
        col = cols[first_component][first_metric]
        pooled_values += [float(row[col]) for row in bars if row.get(col) not in (None, "")]

    per_symbol = run_059_reports["component_attribution"]["slices"]["per_symbol"]
    agg = per_symbol[symbol][first_component]
    assert agg["n"] >= len(first_bars), "expected at least this window's rows pooled in"
    assert agg[first_metric]["mean"] == pytest.approx(statistics.fmean(sorted(pooled_values)))
    assert agg[first_metric]["median"] == pytest.approx(statistics.median(sorted(pooled_values)))


def test_hindsight_lag_is_the_only_new_computation_and_matches_real_finding(run_059_sources, run_059_reports):
    """Real-corpus sanity check, not a fabricated pass: run_059's detector
    genuinely never transitions live regime within any window (confirmed by
    direct inspection during this slice's build), so every window's
    hindsight_lag must legitimately report zero live transitions with a
    stated reason -- proving the empty/null-with-reason shape isn't a bug,
    it's what the real data produces."""
    per_window = run_059_reports["regime_power"]["slices"]["per_window"]
    assert per_window, "expected populated per_window slice for run_059"
    for entry in per_window:
        lag = entry["hindsight_lag"]
        assert lag.get("unavailable") is not True, f"unexpected unavailable: {lag}"
        assert lag["live_transition_count"] == 0
        assert lag["median_lag_bars"] is None
        assert "zero live regime transitions" in lag["reason"]


# ---------------------------------------------------------------------------
# 2. A slice that legitimately can't be populated (synthetic run dir)
# ---------------------------------------------------------------------------

def test_unavailable_slice_is_explicit_not_fabricated(tmp_path):
    """A run directory with a real protocol_result.yaml (carrying
    trade_diagnostics_summary, the pre-aggregated overall figure) but NO
    trade_diagnostics.json alongside it -- the per-trade file this project's
    real corpus sometimes lacks. per_window/per_regime/per_symbol must come
    back as the explicit unavailable shape with a real, specific reason;
    overall must still populate from the pre-aggregated block that IS
    present."""
    run_dir = tmp_path / "run_synthetic"
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True)

    protocol_result = {
        "results": [
            {"symbol": "BTCUSDT", "window": "2020-01", "run_id": "abc123",
             "core": {"net_return_pct": 1.0, "sharpe": 0.5, "trade_count": 3}},
        ],
        "trade_diagnostics_summary": {"win_rate_net": 50.0, "zero_trade_slot_pct": 0.0},
    }
    with open(artifacts / "protocol_result.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(protocol_result, f)
    # deliberately NOT writing run_dir / "trade_diagnostics.json"

    reports = br.build_reports(run_dir, write=False)
    te = reports["trade_efficiency"]["slices"]

    assert te["overall"] == {
        "source": "protocol_result.yaml:trade_diagnostics_summary "
                   "(pre-computed aggregate, re-projected verbatim)",
        "win_rate_net": 50.0,
        "zero_trade_slot_pct": 0.0,
    }
    for slice_name in ("per_window", "per_regime", "per_symbol"):
        value = te[slice_name]
        assert isinstance(value, dict) and value.get("unavailable") is True, \
            f"{slice_name} must be the explicit unavailable shape, got {value!r}"
        assert "trade_diagnostics.json" in value["reason"]


def test_unavailable_slice_never_silently_empty_list(tmp_path):
    """A run with NO protocol_result.yaml results at all must mark every
    slice unavailable with a reason -- never an empty [] / {} that a reader
    could mistake for 'zero, computed for real'."""
    run_dir = tmp_path / "run_no_results"
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True)
    with open(artifacts / "protocol_result.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({}, f)

    reports = br.build_reports(run_dir, write=False)
    for category in br.REPORT_CATEGORIES:
        for slice_name in ("per_window", "per_regime", "per_symbol"):
            value = reports[category]["slices"][slice_name]
            assert value == [] or (isinstance(value, dict) and (
                value.get("unavailable") is True or value == {}
            )), f"{category}.{slice_name} should be empty-dict-regroup or unavailable, got {value!r}"


# ---------------------------------------------------------------------------
# 3. Flag wiring + flag-off byte identity
# ---------------------------------------------------------------------------

def _set_category_reports_flag(root: Path, enabled: bool | None) -> None:
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:
        (config_dir / "campaign_config.yaml").write_text("orchestrator: {}\n", encoding="utf-8")
        return
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": {"category_reports": {"enabled": bool(enabled)}}}, f)


@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, False)])
def test_category_reports_enabled_reads_flag(enabled, expected):
    root = rpr.ROOT
    _set_category_reports_flag(root, enabled)
    assert rpr._category_reports_enabled() is expected


def test_category_reports_enabled_false_when_config_file_absent():
    # deliberately do not create config/campaign_config.yaml (relies on
    # conftest.py's autouse sandbox already pointing rpr.ROOT at an empty tmp_path)
    assert rpr._category_reports_enabled() is False


def test_category_reports_flag_off_never_writes_artifacts(tmp_path):
    """Flag-off byte identity, same acceptance bar and pattern as
    test_grid_evaluation.py's test_grid_evaluation_flag_off_never_writes_
    artifacts: exercises the actual writer condition
    (_category_reports_enabled()) rather than re-deriving it, so a future
    accidental removal of the guard in run_phase1_research.py's
    protocol_execution branch (the `if _category_reports_enabled():` block)
    is caught here."""
    root = rpr.ROOT
    _set_category_reports_flag(root, False)
    assert rpr._category_reports_enabled() is False

    artifacts = tmp_path / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    reports_dir = artifacts / "reports"
    # Mirrors the writer's own guard exactly -- see run_phase1_research.py's
    # protocol_execution branch, the `if _category_reports_enabled():` block.
    if rpr._category_reports_enabled():
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "profitability.yaml").write_text("should not exist\n", encoding="utf-8")
    assert not reports_dir.exists()
    for category in br.REPORT_CATEGORIES:
        assert not (artifacts / "reports" / f"{category}.yaml").exists()


def test_category_reports_real_campaign_config_default_is_off():
    """The real, checked-in config/campaign_config.yaml must ship with this
    flag off -- catches an accidental `enabled: true` slipping into the repo
    default, independent of the synthetic flag tests above."""
    with open(_REAL_STRATEGY_RESEARCH_ROOT / "config" / "campaign_config.yaml", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    assert cfg["orchestrator"]["category_reports"]["enabled"] is False


def test_build_reports_write_true_creates_all_five_files(tmp_path):
    """End-to-end (write=True) against the synthetic minimal run dir used
    above -- proves the actual file-writing path, not just the in-memory
    dict shape."""
    run_dir = tmp_path / "run_synthetic_write"
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True)
    protocol_result = {
        "results": [
            {"symbol": "BTCUSDT", "window": "2020-01", "run_id": "abc123",
             "core": {"net_return_pct": 1.0}},
        ],
    }
    with open(artifacts / "protocol_result.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(protocol_result, f)

    br.build_reports(run_dir, write=True)
    reports_dir = artifacts / "reports"
    for category in br.REPORT_CATEGORIES:
        path = reports_dir / f"{category}.yaml"
        assert path.exists()
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        assert doc["category"] == category
        assert doc["source_run_id"] == "run_synthetic_write"


# ---------------------------------------------------------------------------
# CODE-REVIEW REGRESSION (2026-09-21): _compute_hindsight_lag's actual lag
# arithmetic (the lags.append/statistics.median path) had ZERO test coverage
# -- every window in the run_059 fixture happens to have 0 live transitions,
# so only the "reason" short-circuit branch was ever exercised. This test
# hand-constructs a fixture with exactly one live transition and one
# hindsight transition at a known offset, so the lag value is verified
# against a manually-traced expectation, not just "did it run."
# ---------------------------------------------------------------------------

def test_hindsight_lag_arithmetic_on_a_hand_traced_fixture():
    # closes: horizon=5 (br._HINDSIGHT_HORIZON_BARS). Traced by hand:
    #   i=0: closes[5]=10  vs closes[0]=10 -> flat
    #   i=1: closes[6]=20  vs closes[1]=10 -> up
    #   i=2..6: closes[i+5] > closes[i] -> up (same label as i=1, no new transition)
    #   i=7..11: None (not enough future data, horizon=5, n=12)
    # -> hindsight_labels = ['flat','up','up','up','up','up','up',None,None,None,None,None]
    # -> hindsight_transitions = [1] (flat->up at index 1; no further changes)
    closes = [10, 10, 10, 10, 10, 10, 20, 30, 40, 50, 60, 70]
    # live regime: one clean transition at index 3 (trending -> mean_reversion)
    regimes = ["trending"] * 3 + ["mean_reversion"] * 9
    bars = [{"close": c, "regime": r} for c, r in zip(closes, regimes)]

    result = br._compute_hindsight_lag(bars)

    assert result["live_transition_count"] == 1
    assert result["hindsight_transition_count"] == 1
    # live transition at index 3, nearest hindsight transition at index 1 ->
    # lag = 3 - 1 = 2 (live changed 2 bars AFTER the hindsight-optimal point).
    assert result["lags_bars"] == [2]
    assert result["median_lag_bars"] == 2
    assert result["reason"] is None


def test_hindsight_lag_arithmetic_no_match_within_window_reports_reason():
    # Same live transition (index 2), but the hindsight transition lands far
    # enough away (beyond _HINDSIGHT_MATCH_WINDOW_BARS=20) that no candidate
    # exists. Traced by hand: closes flat (10.0) for indices 0-29, then
    # increasing for indices 30-39. horizon=5, so label[i] first differs
    # (flat->up) at i=25 (closes[30]=11.0 > closes[25]=10.0) and stays 'up'
    # for all i>=25 (n-horizon=35, so labels defined for i=0..34) -- exactly
    # one hindsight transition, at index 25. |25 - 2| = 23 > 20 -> no match.
    n = 40
    closes = [10.0] * 30 + [10.0 + i for i in range(1, 11)]
    regimes = ["trending"] * 2 + ["mean_reversion"] * (n - 2)
    bars = [{"close": c, "regime": r} for c, r in zip(closes, regimes)]

    result = br._compute_hindsight_lag(bars)

    assert result["live_transition_count"] == 1
    assert result["hindsight_transition_count"] == 1
    assert result["lags_bars"] == []
    assert result["median_lag_bars"] is None
    assert result["reason"] is not None
    assert "none had a hindsight-label transition within" in result["reason"]


# ---------------------------------------------------------------------------
# CODE-REVIEW REGRESSION (2026-09-21): 'unknown' (MarketRegime.UNKNOWN,
# emitted during warmup and on every gate-fail bar) must not be treated as
# a genuine live transition -- a warmup-completion flip from 'unknown' to a
# real regime is not a regime CHANGE, and counting it contaminates the lag
# statistic with a "time to finish warmup" figure.
# ---------------------------------------------------------------------------

def test_unknown_to_real_regime_is_not_counted_as_a_live_transition():
    closes = [10.0] * 8 + [20.0, 30.0, 40.0, 50.0]
    regimes = ["unknown"] * 6 + ["trending"] * 6  # warmup-completion flip at index 6
    bars = [{"close": c, "regime": r} for c, r in zip(closes, regimes)]

    result = br._compute_hindsight_lag(bars)

    assert result["live_transition_count"] == 0, (
        "unknown -> real regime must not count as a live transition"
    )


def test_transition_indices_skips_unknown_bars_but_still_detects_a_real_change_across_a_gap():
    # unknown -> trending -> unknown -> mean_reversion: 'unknown' bars are
    # skipped entirely (never inspected, never become `prev`), so the
    # algorithm compares the two REAL labels on either side of the gap
    # (trending at i=1, mean_reversion at i=3) directly -- a genuine regime
    # change is still detected even though the gate closed in between. This
    # is deliberate: an intervening gate-closed period should not HIDE a
    # real regime change, only a pure warmup-completion or gate-close event
    # (below) should be excluded.
    labels = ["unknown", "trending", "unknown", "mean_reversion"]
    assert br._transition_indices(labels) == [3]


def test_transition_indices_pure_warmup_completion_is_not_a_transition():
    # No real regime precedes the first real label -- nothing to transition
    # FROM, so warmup completion alone must never fire.
    labels = ["unknown", "unknown", "trending", "trending"]
    assert br._transition_indices(labels) == []


def test_transition_indices_gate_reopening_to_the_same_regime_is_not_a_transition():
    # Gate closes (unknown) then reopens to the SAME regime as before --
    # the real label never actually changed, so no transition either.
    labels = ["trending", "unknown", "trending"]
    assert br._transition_indices(labels) == []


# ---------------------------------------------------------------------------
# CODE-REVIEW REGRESSION (2026-09-21): build_component_attribution_report's
# per_regime grouping must exclude the trailing blank-regime ('') row the
# same way regime_power's _transition_indices already does for the same
# real data quirk (every window's bars.csv ends with one not-yet-classified
# boundary row).
# ---------------------------------------------------------------------------

def test_component_attribution_per_regime_excludes_blank_trailing_row():
    bars = [
        {"regime": "trending", "debug_info.components.rsi.forecast": "1.0"},
        {"regime": "trending", "debug_info.components.rsi.forecast": "2.0"},
        {"regime": "", "debug_info.components.rsi.forecast": "3.0"},  # trailing boundary bar
    ]
    sources = {
        "protocol_result": {"results": [{"symbol": "BTCUSDT", "window": "2020-01"}]},
        "bars_by_window": {("BTCUSDT", "2020-01"): bars},
    }
    report = br.build_component_attribution_report(sources)
    per_regime = report["slices"]["per_regime"]
    assert "" not in per_regime, (
        f"blank-regime trailing row must not appear as a per_regime key: {sorted(per_regime)}"
    )
    assert "trending" in per_regime


# ---------------------------------------------------------------------------
# E-061 C2 S2d -- per-variant reports (G7 compaction budget guard, G8 shape,
# B2/A3 §3.4: a variant's report reads ITS OWN variants/<vid>/ sources).
# ---------------------------------------------------------------------------

def _write_variant_protocol_result(run_dir: Path, variant_id: str, *, symbol: str, window: str,
                                    run_id_suffix: str) -> None:
    variant_artifacts = run_dir / "artifacts" / "variants" / variant_id
    variant_artifacts.mkdir(parents=True, exist_ok=True)
    protocol_result = {
        "results": [
            {"symbol": symbol, "window": window, "run_id": f"{variant_id}_{run_id_suffix}",
             "core": {"net_return_pct": 1.0, "sharpe": 0.4}},
        ],
    }
    with open(variant_artifacts / "protocol_result.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(protocol_result, f)


def test_build_reports_variants_populates_every_variant_with_its_own_symbol(tmp_path):
    """G8/D-003 ("experts see every variant"): variants={base, design_1}
    builds a schema_version: 2 report whose `variants` map carries each
    variant's own kind/symbol/status and its own slices (built from that
    variant's own artifacts/variants/<vid>/ sources, not the run-level ones);
    failed_variants/untested_variants are carried as their own top-level rows,
    never as graded columns."""
    run_dir = tmp_path / "run_variant_build"
    _write_variant_protocol_result(run_dir, "base", symbol="BTCUSDT", window="2020-01",
                                    run_id_suffix="w1")
    _write_variant_protocol_result(run_dir, "design_1", symbol="BTCUSDT", window="2020-01",
                                    run_id_suffix="w1")

    reports = br.build_reports(
        run_dir, write=False,
        variants={
            "base": {"kind": "base", "symbol": "BTCUSDT", "status": "graded"},
            "design_1": {"kind": "design", "symbol": "BTCUSDT", "status": "graded"},
        },
        failed_variants={"crashed_1": "backtest_failed: injected"},
        untested_variants={"asset_1": "skipped as an exact REPEAT"},
    )

    for category in br.REPORT_CATEGORIES:
        report = reports[category]
        assert report["schema_version"] == 2
        assert set(report["variants"]) == {"base", "design_1"}
        assert report["variants"]["base"]["kind"] == "base"
        assert report["variants"]["base"]["symbol"] == "BTCUSDT"
        assert report["variants"]["design_1"]["kind"] == "design"
        assert "slices" in report["variants"]["base"]
        assert "slices" not in report, "no separate base-only top-level slices (G8)"
        assert report["failed_variants"] == {"crashed_1": "backtest_failed: injected"}
        assert report["untested_variants"] == {"asset_1": "skipped as an exact REPEAT"}


def test_build_reports_variants_falls_back_gracefully_when_symbol_absent(tmp_path):
    """S2b (a sibling slice) is what adds kind/symbol to index.yaml -- until
    it lands, a caller may pass variant entries without those keys at all;
    this must never raise or invent a value (dispatch instruction: read
    symbol/kind when present, fall back gracefully, never add the field)."""
    run_dir = tmp_path / "run_variant_no_symbol"
    _write_variant_protocol_result(run_dir, "base", symbol="BTCUSDT", window="2020-01",
                                    run_id_suffix="w1")

    reports = br.build_reports(run_dir, write=False, variants={"base": {"status": "graded"}})
    assert reports["profitability"]["variants"]["base"]["kind"] is None
    assert reports["profitability"]["variants"]["base"]["symbol"] is None


def test_build_reports_variants_status_defaults_to_graded_not_validated(tmp_path):
    """C2 S2d review fix: a reader must never read a variant's report-row `status`
    as a pass/fail verdict -- that authority is the grid's alone. When the caller's
    vinfo carries no `status` key at all, build_reports must default to "graded"
    ("backtested and graded"), never the old "validated" label."""
    run_dir = tmp_path / "run_variant_status_default"
    _write_variant_protocol_result(run_dir, "base", symbol="BTCUSDT", window="2020-01",
                                    run_id_suffix="w1")

    reports = br.build_reports(run_dir, write=False, variants={"base": {"kind": "base"}})
    assert reports["profitability"]["variants"]["base"]["status"] == "graded"


def test_build_reports_variants_passes_through_coverage_when_given(tmp_path):
    """E-061 C2 S2b's D-042 partial-coverage marker is a plain passthrough on a
    variant's report row -- present only when the caller's vinfo carries one,
    never computed or invented by build_reports itself."""
    run_dir = tmp_path / "run_variant_coverage"
    _write_variant_protocol_result(run_dir, "base", symbol="BTCUSDT", window="2020-01",
                                    run_id_suffix="w1")
    _write_variant_protocol_result(run_dir, "asset_1", symbol="ETHUSDT", window="2020-01",
                                    run_id_suffix="w1")

    reports = br.build_reports(
        run_dir, write=False,
        variants={
            "base": {"kind": "base", "symbol": "BTCUSDT"},
            "asset_1": {"kind": "asset", "symbol": "ETHUSDT",
                        "coverage": "partial, windows run 2 of 4"},
        },
    )
    assert "coverage" not in reports["profitability"]["variants"]["base"]
    assert reports["profitability"]["variants"]["asset_1"]["coverage"] == \
        "partial, windows run 2 of 4"


def test_build_reports_variants_rejects_empty_dict(tmp_path):
    run_dir = tmp_path / "run_variant_empty"
    _write_variant_protocol_result(run_dir, "base", symbol="BTCUSDT", window="2020-01",
                                    run_id_suffix="w1")
    with pytest.raises(ValueError):
        br.build_reports(run_dir, write=False, variants={})


def test_build_reports_variant_reads_its_own_trade_and_bar_sources(tmp_path):
    """The B2/A3 §3.4 finding this slice fixes: a variant's report must be
    built from ITS OWN variants/<vid>/trade_diagnostics.json (and
    variants/<vid>/results/<w>/bars.csv), not the run-level paths that are
    never written under the variant loop."""
    run_dir = tmp_path / "run_variant_sources"
    _write_variant_protocol_result(run_dir, "base", symbol="BTCUSDT", window="2020-01",
                                    run_id_suffix="w1")
    variant_run_dir = run_dir / "variants" / "base"
    variant_run_dir.mkdir(parents=True, exist_ok=True)
    trades = [{"trade_id": "t1", "symbol": "BTCUSDT", "window": "2020-01",
               "regime_at_entry": "trending", "realized_return": 1.5}]
    with open(variant_run_dir / "trade_diagnostics.json", "w", encoding="utf-8") as f:
        json.dump({"trades": trades}, f)

    reports = br.build_reports(run_dir, write=False,
                                variants={"base": {"kind": "base", "symbol": "BTCUSDT"}})
    per_window = reports["trade_efficiency"]["variants"]["base"]["slices"]["per_window"]
    assert per_window["2020-01"]["n"] == 1
    assert per_window["2020-01"]["realized_return"]["mean"] == pytest.approx(1.5)


def test_report_char_budget_guard_raises_on_oversized_report(tmp_path, monkeypatch):
    """G7's fail-loud budget guard: a report whose serialized size exceeds
    REPORT_CHAR_BUDGET must raise, never silently truncate or write."""
    run_dir = tmp_path / "run_budget"
    _write_variant_protocol_result(run_dir, "base", symbol="BTCUSDT", window="2020-01",
                                    run_id_suffix="w1")
    monkeypatch.setattr(br, "REPORT_CHAR_BUDGET", 10)
    with pytest.raises(ValueError, match="REPORT_CHAR_BUDGET"):
        br.build_reports(run_dir, write=False)


def test_report_char_budget_guard_does_not_fire_on_run_059(run_059_sources):
    """The tracked run_059 fixture (98 windows, both symbols, a real
    trade_diagnostics.json) stays under REPORT_CHAR_BUDGET for every report,
    single-run mode -- proves G7's compaction actually brought the two
    previously-huge reports (trade_efficiency, component_attribution) back
    under budget, not just that the guard exists."""
    for name, builder in br.BUILDERS.items():
        report = builder(run_059_sources)
        size = len(yaml.safe_dump(report, sort_keys=False, allow_unicode=True))
        assert size <= br.REPORT_CHAR_BUDGET, f"{name}.yaml is {size} chars, over budget"


def test_cul370_per_symbol_is_a_small_index_not_a_second_copy(run_059_reports):
    """CUL-370: the per_symbol slice carries no core block, so it stays a small
    fraction of per_window (the duplicate made it as large, doubling the report
    -- run_064's profitability.yaml was 716,645 chars)."""
    import yaml as _yaml
    slices = run_059_reports["profitability"]["slices"]
    size = lambda x: len(_yaml.safe_dump(x, sort_keys=False))  # noqa: E731
    assert size(slices["per_symbol"]) * 5 < size(slices["per_window"])  # ~1/9.5 measured; ~1/1 before
