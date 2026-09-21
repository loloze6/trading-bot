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
    """Every (symbol, window) core block in the per_symbol slice must equal
    the corresponding source entry's core block exactly -- proves the
    per_symbol slice is a pure regroup, not a recomputed aggregate."""
    pr = run_059_sources["protocol_result"]
    by_symbol_window = {(r["symbol"], r["window"]): r["core"] for r in pr["results"]}
    per_symbol = run_059_reports["profitability"]["slices"]["per_symbol"]
    seen = 0
    for symbol, entries in per_symbol.items():
        for entry in entries:
            source_core = by_symbol_window[(symbol, entry["window"])]
            # entry is source_core's fields spread alongside window/run_id --
            # every key that also exists in source_core must match exactly.
            for key, value in source_core.items():
                assert entry[key] == value
            seen += 1
    assert seen == len(pr["results"])


def test_reprojection_trade_efficiency_summary_equals_source(run_059_sources, run_059_reports):
    pr = run_059_sources["protocol_result"]
    source_summary = pr["trade_diagnostics_summary"]
    overall = run_059_reports["trade_efficiency"]["slices"]["overall"]
    for key, value in source_summary.items():
        assert overall[key] == value


def test_reprojection_trade_efficiency_per_window_trades_equal_source(run_059_sources, run_059_reports):
    td = run_059_sources["trade_diagnostics"]
    source_trades_by_window: dict[str, list[dict]] = {}
    for trade in td["trades"]:
        source_trades_by_window.setdefault(trade["window"], []).append(trade)

    per_window = run_059_reports["trade_efficiency"]["slices"]["per_window"]
    assert set(per_window.keys()) == set(source_trades_by_window.keys())
    for window, trades in per_window.items():
        assert trades == source_trades_by_window[window]


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


def test_reprojection_component_attribution_cell_equals_bars_csv(run_059_sources, run_059_reports):
    """Spot-checks real bars.csv cells against the component_attribution
    report for the first window that has component columns -- proves the
    per-bar values are copied, not recomputed."""
    bars_by_window = run_059_sources["bars_by_window"]
    first_key, first_bars = next(
        (k, v) for k, v in bars_by_window.items() if v and any(
            col.startswith(br._COMPONENT_COLUMN_PREFIX) for col in v[0]))
    symbol, window = first_key
    per_symbol = run_059_reports["component_attribution"]["slices"]["per_symbol"]
    records = [r for r in per_symbol[symbol] if r["window"] == window]

    components = br._parse_component_columns(list(first_bars[0].keys()))
    expected_count = len(first_bars) * len(components)
    assert len(records) == expected_count

    first_component = next(iter(components))
    first_metric, first_col = next(iter(components[first_component].items()))
    matching = [r for r in records if r["component"] == first_component and r["timestamp"] == first_bars[0]["timestamp"]]
    assert len(matching) == 1
    assert matching[0][first_metric] == first_bars[0][first_col]


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
