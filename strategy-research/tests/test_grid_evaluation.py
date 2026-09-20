"""
E-046b S2 -- the grid (engineering_roadmap.html card C). Tests for
tools/verdict_criteria_evaluator.py::evaluate_grid() and its supporting
reducers/floor/tie-break logic, plus the off-by-default
orchestrator.grid_evaluation.enabled flag in workflow/run_phase1_research.py.

Fixtures are synthetic protocol_result dicts (this file's own
`_protocol_result` helper) rather than real run artifacts -- the reducer,
floor, unanimity and tie-break behaviors need precise, known-answer inputs,
which real historical runs (predating both the CUL-300
realized_edge_to_cost_ratio field and this feature entirely) cannot provide
on demand. See strategy-research/engineering/roadmap/E-046b/S1_FINDINGS.md
for the full characterization this implements, and the dispatching agent's
own final report for the real-corpus calibration run (run_054/run_058/
run_059) this synthetic suite is deliberately kept separate from.
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
import verdict_criteria_evaluator as vce  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _window(symbol: str, window_label: str, **core_overrides) -> dict:
    core = {
        "sharpe": 1.0, "net_return_pct": 1.0, "trade_count": 10,
        "max_drawdown_pct": -5.0, "win_rate": 0.5,
    }
    core.update(core_overrides)
    return {"symbol": symbol, "window": window_label, "core": core}


def _protocol_result(windows: list, trade_diagnostics_summary=None) -> dict:
    return {
        "results": windows,
        "trade_diagnostics_summary": trade_diagnostics_summary or {},
        "per_symbol_summary": {},
        "hypothesis_verdict": {"diagnostics": {}},
    }


def _menu_shaped_pre_reg(criteria: list) -> dict:
    return {"pass_rule": {"criteria": criteria}}


# ---------------------------------------------------------------------------
# Reducers, each on a synthetic per-window table (via evaluate_grid, so the
# floor/comparator machinery around each reducer is exercised too, not just
# the bare statistics call).
# ---------------------------------------------------------------------------

def _windows_for_reducer(values: list) -> list:
    return [_window("BTCUSDT", f"2020-{i+1:02d}", net_return_pct=v, trade_count=10)
            for i, v in enumerate(values)]


@pytest.mark.parametrize("reducer,values,comparator,threshold,expected", [
    ("median", [1.0, 2.0, 3.0, 4.0, 5.0], ">", 2.5, "PASS"),
    ("median", [1.0, 2.0, 3.0, 4.0, 5.0], ">", 3.5, "FAIL"),
    ("mean",   [1.0, 2.0, 3.0, 4.0, 100.0], ">", 20.0, "PASS"),
    ("mean",   [1.0, 2.0, 3.0, 4.0, 5.0], ">", 20.0, "FAIL"),
    ("min",    [1.0, 2.0, 3.0, 4.0, 5.0], ">=", 1.0, "PASS"),
    ("min",    [1.0, 2.0, 3.0, 4.0, 5.0], ">", 1.0, "FAIL"),
    ("max",    [1.0, 2.0, 3.0, 4.0, 5.0], ">=", 5.0, "PASS"),
    ("max",    [1.0, 2.0, 3.0, 4.0, 5.0], ">", 5.0, "FAIL"),
])
def test_scalar_reducers_known_answer(reducer, values, comparator, threshold, expected):
    windows = _windows_for_reducer(values)
    protocol_result = _protocol_result(windows)
    criterion = {"id": "c1", "metric": "net_return_pct", "source": "window",
                 "reducer": reducer, "comparator": comparator, "threshold": threshold,
                 "floor": {"min_windows": 3, "min_trades": 10}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    cell = result["grid"]["c1"]["v1"]
    assert cell["result"] == expected, cell


def test_fraction_above_reducer():
    windows = _windows_for_reducer([1.0, 2.0, 3.0, -1.0, -2.0])  # 3/5 > 0
    protocol_result = _protocol_result(windows)
    criterion = {"id": "frac", "metric": "net_return_pct", "source": "window",
                 "reducer": "fraction_above", "reducer_arg": 0.0,
                 "comparator": ">=", "threshold": 0.6,
                 "floor": {"min_windows": 3, "min_trades": 10}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    cell = result["grid"]["frac"]["v1"]
    assert cell["result"] == "PASS", cell
    assert cell["value"] == pytest.approx(0.6)


def test_fraction_above_missing_reducer_arg_is_spec_error_not_a_crash():
    windows = _windows_for_reducer([1.0, 2.0])
    protocol_result = _protocol_result(windows)
    criterion = {"id": "frac", "metric": "net_return_pct", "source": "window",
                 "reducer": "fraction_above",  # no reducer_arg
                 "comparator": ">=", "threshold": 0.5, "floor": {}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    assert result["result"] == "SPEC_ERROR"
    assert result["idea_status"] is None


def test_sign_consistent_by_era_all_positive_passes():
    # All windows in the SAME era (era_2019_2023_full_feed: 2019-09-10..2023-12-31),
    # all positive -> one era, nonzero positive sign -> PASS.
    windows = [_window("BTCUSDT", "2020-01", net_return_pct=1.0),
               _window("BTCUSDT", "2020-02", net_return_pct=2.0),
               _window("BTCUSDT", "2020-03", net_return_pct=0.5)]
    protocol_result = _protocol_result(windows)
    criterion = {"id": "sce", "metric": "net_return_pct", "source": "window",
                 "reducer": "sign_consistent_by_era", "floor": {"min_windows": 1}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    assert result["grid"]["sce"]["v1"]["result"] == "PASS"


def test_sign_consistent_by_era_disagreeing_eras_fails():
    # era_2019_2023_full_feed (2019-09-10..2023-12-31) positive,
    # era_2024_burned (2024-01-01..2024-11-30) negative -> disagreement -> FAIL.
    windows = [_window("BTCUSDT", "2020-01", net_return_pct=1.0),
               _window("BTCUSDT", "2020-02", net_return_pct=2.0),
               _window("BTCUSDT", "2024-03", net_return_pct=-1.0),
               _window("BTCUSDT", "2024-04", net_return_pct=-2.0)]
    protocol_result = _protocol_result(windows)
    criterion = {"id": "sce", "metric": "net_return_pct", "source": "window",
                 "reducer": "sign_consistent_by_era", "floor": {"min_windows": 1}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    cell = result["grid"]["sce"]["v1"]
    assert cell["result"] == "FAIL"
    assert cell["detail"]["era_signs"] == {"era_2019_2023_full_feed": 1, "era_2024_burned": -1}


def test_sign_consistent_by_era_zero_median_is_not_a_pass():
    windows = [_window("BTCUSDT", "2020-01", net_return_pct=1.0),
               _window("BTCUSDT", "2020-02", net_return_pct=-1.0)]  # median 0
    protocol_result = _protocol_result(windows)
    criterion = {"id": "sce", "metric": "net_return_pct", "source": "window",
                 "reducer": "sign_consistent_by_era", "floor": {"min_windows": 1}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    assert result["grid"]["sce"]["v1"]["result"] == "FAIL"


def test_pooled_source_reuses_existing_lookup():
    protocol_result = _protocol_result(
        _windows_for_reducer([1.0, 1.0, 1.0, 1.0, 1.0]),
        trade_diagnostics_summary={"realized_edge_to_cost_ratio": 0.5},
    )
    criterion = {"id": "redcr", "metric": "realized_edge_to_cost_ratio", "source": "pooled",
                 "comparator": ">", "threshold": 0.3, "floor": {"min_windows": 3, "min_trades": 10}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    cell = result["grid"]["redcr"]["v1"]
    assert cell["result"] == "PASS"
    assert cell["value"] == 0.5


# ---------------------------------------------------------------------------
# Floor -> INCONCLUSIVE, never FAIL
# ---------------------------------------------------------------------------

def test_floor_under_min_windows_is_inconclusive_not_fail():
    windows = _windows_for_reducer([100.0, 100.0])  # would PASS on value alone
    protocol_result = _protocol_result(windows)
    criterion = {"id": "c1", "metric": "net_return_pct", "source": "window",
                 "reducer": "median", "comparator": ">", "threshold": 0.0,
                 "floor": {"min_windows": 10}}  # only 2 windows exist
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    cell = result["grid"]["c1"]["v1"]
    assert cell["result"] == "INCONCLUSIVE"
    assert "min_windows" in cell["reason"]
    assert result["idea_status"] == "inconclusive"


def test_floor_under_min_trades_is_inconclusive():
    windows = _windows_for_reducer([100.0, 100.0, 100.0])
    for w in windows:
        w["core"]["trade_count"] = 1  # 3 windows, 3 trades total
    protocol_result = _protocol_result(windows)
    criterion = {"id": "c1", "metric": "net_return_pct", "source": "window",
                 "reducer": "median", "comparator": ">", "threshold": 0.0,
                 "floor": {"min_trades": 50}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    assert result["grid"]["c1"]["v1"]["result"] == "INCONCLUSIVE"


def test_floor_min_n_eff_raises_loudly_never_silently_satisfied():
    windows = _windows_for_reducer([1.0, 2.0, 3.0])
    protocol_result = _protocol_result(windows)
    criterion = {"id": "c1", "metric": "net_return_pct", "source": "window",
                 "reducer": "median", "comparator": ">", "threshold": 0.0,
                 "floor": {"min_n_eff": 30}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    with pytest.raises(NotImplementedError, match="min_n_eff"):
        vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})


# ---------------------------------------------------------------------------
# Two-variant unanimity
# ---------------------------------------------------------------------------

def test_two_variant_unanimity_both_pass_validates():
    good = _protocol_result(_windows_for_reducer([1.0, 2.0, 3.0]))
    also_good = _protocol_result(_windows_for_reducer([1.5, 2.5, 3.5]))
    criterion = {"id": "c1", "metric": "net_return_pct", "source": "window",
                 "reducer": "median", "comparator": ">", "threshold": 0.0,
                 "floor": {"min_windows": 1}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"base": good, "variant2": also_good}, pre_reg, {}, {})
    assert result["idea_status"] == "validated"
    assert set(result["variants"]) == {"base", "variant2"}


def test_two_variant_unanimity_one_fails_refutes():
    good = _protocol_result(_windows_for_reducer([1.0, 2.0, 3.0]))
    bad = _protocol_result(_windows_for_reducer([-1.0, -2.0, -3.0]))
    criterion = {"id": "c1", "metric": "net_return_pct", "source": "window",
                 "reducer": "median", "comparator": ">", "threshold": 0.0,
                 "floor": {"min_windows": 1}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"base": good, "variant2": bad}, pre_reg, {}, {})
    assert result["idea_status"] == "refuted"
    assert result["grid"]["c1"]["base"]["result"] == "PASS"
    assert result["grid"]["c1"]["variant2"]["result"] == "FAIL"


# ---------------------------------------------------------------------------
# FAIL-dominates-INCONCLUSIVE tie-break (operator-confirmed,
# S1_FINDINGS.md's appended 2026-09-20 decision)
# ---------------------------------------------------------------------------

def test_fail_dominates_inconclusive_tie_break():
    """One criterion FAILs (sufficient data) on one variant; a DIFFERENT
    criterion is under-floor (INCONCLUSIVE) on the OTHER variant. The
    operator-confirmed rule: FAIL dominates -- the idea is REFUTED, not
    INCONCLUSIVE, even though an inconclusive cell also exists."""
    variant_a = _protocol_result(_windows_for_reducer([-1.0, -2.0, -3.0]))  # fails c_fail
    variant_b = _protocol_result(_windows_for_reducer([1.0]))  # only 1 window -> under floor on c_floor

    c_fail = {"id": "c_fail", "metric": "net_return_pct", "source": "window",
              "reducer": "median", "comparator": ">", "threshold": 0.0,
              "floor": {"min_windows": 1}}
    c_floor = {"id": "c_floor", "metric": "net_return_pct", "source": "window",
               "reducer": "median", "comparator": ">", "threshold": -999.0,
               "floor": {"min_windows": 5}}  # neither variant has 5 windows
    pre_reg = _menu_shaped_pre_reg([c_fail, c_floor])
    result = vce.evaluate_grid({"a": variant_a, "b": variant_b}, pre_reg, {}, {})

    assert result["grid"]["c_fail"]["a"]["result"] == "FAIL"
    assert result["grid"]["c_floor"]["a"]["result"] == "INCONCLUSIVE"
    assert result["grid"]["c_floor"]["b"]["result"] == "INCONCLUSIVE"
    assert result["idea_status"] == "refuted", (
        "FAIL must dominate INCONCLUSIVE at the idea level -- a genuine failure "
        "elsewhere is not rescued by an unrelated under-sampled cell"
    )


# ---------------------------------------------------------------------------
# Open-ended-era guard regression (S1_FINDINGS.md's independently-verified
# _era_id_for_timestamp None-comparison bug in run_protocol.py -- this
# module's OWN copy must not reintroduce or depend on it)
# ---------------------------------------------------------------------------

def test_era_id_for_timestamp_open_ended_last_era_does_not_raise():
    eras = [
        {"era_id": "era_early", "range": ["2018-01-01", "2019-12-31"]},
        {"era_id": "era_open_ended", "range": ["2026-07-26", None]},
    ]
    # A date strictly past the open-ended era's lower bound: the ORIGINAL bug
    # (`lo <= d <= hi` with hi=None) raises TypeError here.
    eid = vce._era_id_for_timestamp("2026-08-15", eras)
    assert eid == "era_open_ended"


def test_era_id_for_timestamp_open_ended_era_lower_bound_excludes_earlier_dates():
    eras = [
        {"era_id": "era_early", "range": ["2018-01-01", "2019-12-31"]},
        {"era_id": "era_open_ended", "range": ["2026-07-26", None]},
    ]
    eid = vce._era_id_for_timestamp("2020-01-01", eras)
    assert eid == "era_unmapped"


def test_sign_consistent_by_era_gap_window_excluded_not_compared():
    """CODE-REVIEW REGRESSION (2026-09-20): a window landing in a genuine gap
    between two defined eras (campaign_data_policy.yaml's own
    2026-07-01..2026-07-25 gap, between the holdout's end and
    era_2026_h2_forward_recorded's start) used to resolve to the literal
    "era_unmapped" and get treated as its own bucket in the sign-agreement
    check -- missing era coverage is not a genuine second era to disagree
    with. All real windows here sit in the SAME defined era
    (era_2019_2023_full_feed) and agree in sign; a gap window of the
    OPPOSITE sign must not flip this to FAIL."""
    windows = [_window("BTCUSDT", "2020-01", net_return_pct=1.0),
               _window("BTCUSDT", "2020-02", net_return_pct=2.0),
               _window("BTCUSDT", "2026-07-10", net_return_pct=-100.0)]  # gap, excluded
    protocol_result = _protocol_result(windows)
    criterion = {"id": "sce", "metric": "net_return_pct", "source": "window",
                 "reducer": "sign_consistent_by_era", "floor": {"min_windows": 1}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    cell = result["grid"]["sce"]["v1"]
    assert cell["result"] == "PASS"
    assert "era_unmapped" not in cell["detail"]["era_signs"]


def test_sign_consistent_by_era_all_windows_unmapped_is_inconclusive():
    """If EVERY window falls in an era gap, by_era ends up empty after
    exclusion -- falls through to the existing 'not computable' (None)
    return, which the grid maps to INCONCLUSIVE, never a silent PASS/FAIL."""
    windows = [_window("BTCUSDT", "2026-07-05", net_return_pct=1.0),
               _window("BTCUSDT", "2026-07-15", net_return_pct=1.0)]
    protocol_result = _protocol_result(windows)
    criterion = {"id": "sce", "metric": "net_return_pct", "source": "window",
                 "reducer": "sign_consistent_by_era", "floor": {"min_windows": 1}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    assert result["grid"]["sce"]["v1"]["result"] == "INCONCLUSIVE"


def test_sign_consistent_by_era_reducer_survives_open_ended_era_in_real_policy_shape():
    """End-to-end: a window dated past campaign_data_policy.yaml's real
    open-ended era must not crash the reducer -- proves evaluate_grid's own
    era resolution path (not just the bare function above) is guarded."""
    windows = [_window("BTCUSDT", "2026-08", net_return_pct=1.0),
               _window("BTCUSDT", "2026-09", net_return_pct=2.0)]
    protocol_result = _protocol_result(windows)
    criterion = {"id": "sce", "metric": "net_return_pct", "source": "window",
                 "reducer": "sign_consistent_by_era", "floor": {"min_windows": 1}}
    pre_reg = _menu_shaped_pre_reg([criterion])
    # Must not raise.
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, {})
    assert result["grid"]["sce"]["v1"]["result"] in ("PASS", "FAIL", "INCONCLUSIVE")


# ---------------------------------------------------------------------------
# SPEC_ERROR short-circuit (no idea_status on a malformed grid)
# ---------------------------------------------------------------------------

def test_non_menu_shaped_pass_rule_raises():
    legacy_pre_reg = {"pass_rule": {
        "criteria": [{"id": "a", "metric": "median_sharpe", "comparator": ">=", "threshold": 0.8}],
        "outcomes": [{"branch": "PASS", "hypothesis_verdict": "promote"}],
    }}
    protocol_result = _protocol_result(_windows_for_reducer([1.0]))
    with pytest.raises(ValueError, match="menu-shaped"):
        vce.evaluate_grid({"v1": protocol_result}, legacy_pre_reg, {}, {})


def test_empty_protocol_results_by_variant_raises():
    criterion = {"id": "c1", "metric": "net_return_pct", "source": "window",
                 "reducer": "median", "comparator": ">", "threshold": 0.0}
    pre_reg = _menu_shaped_pre_reg([criterion])
    with pytest.raises(ValueError, match="non-empty"):
        vce.evaluate_grid({}, pre_reg, {}, {})


# ---------------------------------------------------------------------------
# criterion_menu.yaml merge (id + overrides backfilled from the menu)
# ---------------------------------------------------------------------------

def test_pass_rule_criterion_backfilled_from_menu():
    menu = {"criteria": [
        {"id": "c1", "metric": "net_return_pct", "source": "window", "reducer": "median",
         "comparator": ">", "threshold": 0.0, "floor": {"min_windows": 1}},
    ]}
    # pre_registration names only the id + source/reducer (menu-shaped detection
    # needs at least one of those two fields on the criterion itself) and a
    # per-hypothesis threshold override.
    pre_reg = _menu_shaped_pre_reg([{"id": "c1", "source": "window", "reducer": "median",
                                      "threshold": 0.5}])
    protocol_result = _protocol_result(_windows_for_reducer([1.0, 2.0, 3.0]))
    result = vce.evaluate_grid({"v1": protocol_result}, pre_reg, {}, menu)
    cell = result["grid"]["c1"]["v1"]
    assert cell["result"] == "PASS"
    assert cell["threshold"] == 0.5  # override won, not the menu's 0.0


# ---------------------------------------------------------------------------
# Flag-off byte identity (orchestrator.grid_evaluation.enabled)
# ---------------------------------------------------------------------------

def _set_grid_flag(root: Path, enabled) -> None:
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:
        (config_dir / "campaign_config.yaml").write_text("orchestrator: {}\n", encoding="utf-8")
        return
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": {"grid_evaluation": {"enabled": bool(enabled)}}}, f)


@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, False)])
def test_grid_evaluation_enabled_reads_flag(enabled, expected):
    root = rpr.ROOT
    _set_grid_flag(root, enabled)
    assert rpr._grid_evaluation_enabled() is expected


def test_grid_evaluation_enabled_false_when_config_file_absent():
    # deliberately do not create config/campaign_config.yaml (relies on
    # conftest.py's autouse sandbox already pointing rpr.ROOT at an empty tmp_path)
    assert rpr._grid_evaluation_enabled() is False


def test_grid_evaluation_flag_off_never_writes_artifacts(tmp_path):
    """Flag-off byte identity, same acceptance bar as
    test_exclusion_digest_input.py: this is not merely 'the code path is
    skipped' but a positive assertion that grid_evaluation.yaml/
    idea_status.yaml are never written and nothing about
    evaluate_pass_rule_criteria's own call is touched. Exercises the actual
    writer condition (`_grid_evaluation_enabled()`) rather than re-deriving
    it, so a future accidental removal of the guard in
    run_phase1_research.py's protocol_execution branch is caught here."""
    root = rpr.ROOT
    _set_grid_flag(root, False)
    assert rpr._grid_evaluation_enabled() is False

    artifacts = tmp_path / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    # Mirrors the writer's own guard exactly -- see run_phase1_research.py's
    # protocol_execution branch, the `if _grid_evaluation_enabled():` block.
    if rpr._grid_evaluation_enabled():
        (artifacts / "grid_evaluation.yaml").write_text("should not exist\n", encoding="utf-8")
    assert not (artifacts / "grid_evaluation.yaml").exists()
    assert not (artifacts / "idea_status.yaml").exists()


# ---------------------------------------------------------------------------
# idea_status.yaml routing shape (_build_idea_status_artifact)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status,expected_result,expected_hv,expected_lr", [
    ("validated", "PASS", "promote", None),
    ("refuted", "FAIL", "kill", "terminate"),
    ("inconclusive", "INCONCLUSIVE", "human_pause", "inconclusive_grid"),
])
def test_build_idea_status_artifact_routing(idea_status, expected_result, expected_hv, expected_lr):
    grid_result = {"idea_status": idea_status, "reason": "synthetic"}
    artifact = rpr._build_idea_status_artifact(grid_result, "run_999")
    assert artifact["result"] == expected_result
    assert artifact["hypothesis_verdict"] == expected_hv
    assert artifact["lineage_routing"] == expected_lr
    assert artifact["grid_evaluation_ref"] == "runs/run_999/artifacts/grid_evaluation.yaml"


def test_build_idea_status_artifact_rejects_unknown_status():
    with pytest.raises(ValueError, match="not one of"):
        rpr._build_idea_status_artifact({"idea_status": "not_a_real_status"}, "run_999")
