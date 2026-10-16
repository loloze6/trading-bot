"""
D-144: a backtest trial row written by a DIFFERENT protocol run replaces the
earlier row in place and keeps that attempt under `superseded_attempts`; a write
from the SAME protocol run (or with no run id) is still skipped (H3).

Why it exists: a resume at protocol_execution re-runs the backtests (run_096 ran
three times), and the old guard in `_record_backtest_trial` keyed on
(trial_id, source) alone, so the re-run's numbers never reached the ledger.
Row count, and so the DSR N, must not change (D-124: config + fold = one trial).
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))

import deflate_sharpe as ds  # noqa: E402
import run_phase1_research as rpr  # noqa: E402


def _summary(sharpe, protocol_run_id=None):
    s = {
        "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 0.0}},
        "per_symbol_summary": {"BTCUSD": {"median_sharpe": sharpe}},
        "results": [{"core": {"trade_count": 10}}],
    }
    if protocol_run_id is not None:
        s["protocol_run_id"] = protocol_run_id
    return s


def _whole_test(status="ok", reason=None):
    return {"basis": "whole_test_daily_equal_weight_v2", "status": status, "reason": reason,
            "sr_daily": 0.01 if status == "ok" else None}


@pytest.fixture
def env(tmp_path, monkeypatch):
    state_path = tmp_path / "campaign_state.yaml"
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", state_path)
    config_path = tmp_path / "candidate_strategy_config.json"
    config_path.write_text(json.dumps({"strategy": "x"}), encoding="utf-8")
    return state_path, config_path


def _rows(state_path, trial_id):
    state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
    return [t for t in state["trial_sharpes"] if t["trial_id"] == trial_id and t["source"] == "backtest"]


def test_same_run_id_rewrite_is_byte_identical(env):
    state_path, config_path = env
    rpr._record_backtest_trial("run_960", _summary(1.0, "RID_A"), config_path, whole_test=_whole_test())
    first = state_path.read_bytes()
    rpr._record_backtest_trial("run_960", _summary(-3.0, "RID_A"), config_path, whole_test=_whole_test("error", "x"))
    assert state_path.read_bytes() == first
    (row,) = _rows(state_path, "run_960")
    assert row["protocol_run_id"] == "RID_A" and row["sharpe"] == 1.0
    assert "superseded_attempts" not in row


def test_summary_without_run_id_is_skipped_even_over_a_row_with_one(env):
    state_path, config_path = env
    rpr._record_backtest_trial("run_961", _summary(1.0, "RID_A"), config_path)
    first = state_path.read_bytes()
    rpr._record_backtest_trial("run_961", _summary(2.0), config_path)
    assert state_path.read_bytes() == first


def test_summaries_without_run_ids_keep_the_legacy_row_shape(env):
    state_path, config_path = env
    rpr._record_backtest_trial("run_962", _summary(1.0), config_path)
    first = state_path.read_bytes()
    rpr._record_backtest_trial("run_962", _summary(2.0), config_path)
    assert state_path.read_bytes() == first
    (row,) = _rows(state_path, "run_962")
    assert "protocol_run_id" not in row and "superseded_attempts" not in row


def test_different_run_id_replaces_in_place_and_keeps_the_attempt(env):
    state_path, config_path = env
    state_path.write_text(yaml.safe_dump({"trial_sharpes": [
        {"trial_id": "run_963", "source": "prescreen", "statistic_valid": "neither"},
    ]}), encoding="utf-8")
    rpr._record_backtest_trial("run_963", _summary(1.0, "RID_A"), config_path, whole_test=_whole_test("ok"))
    rpr._record_backtest_trial("run_964", _summary(0.2, "RID_Z"), config_path)
    before = yaml.safe_load(state_path.read_text(encoding="utf-8"))["trial_sharpes"]

    rpr._record_backtest_trial("run_963", _summary(-0.5, "RID_B"), config_path,
                               whole_test=_whole_test("error", "PortfolioRuined: x"))

    after = yaml.safe_load(state_path.read_text(encoding="utf-8"))["trial_sharpes"]
    assert len(after) == len(before) == 3                       # trial count unchanged
    assert [(t["trial_id"], t["source"]) for t in after] == [(t["trial_id"], t["source"]) for t in before]
    (row,) = _rows(state_path, "run_963")
    assert row["sharpe"] == -0.5 and row["protocol_run_id"] == "RID_B"
    assert row["whole_test"]["status"] == "error"
    assert row["superseded_attempts"] == [
        {"protocol_run_id": "RID_A", "sharpe": 1.0, "forecast_hash": rpr._compute_forecast_hash(config_path),
         "whole_test_status": "ok", "whole_test_reason": None}]
    assert after[2] == before[2]                              # the neighbour row is untouched
    assert ds.deduplicate_trials(after)[1] == ds.deduplicate_trials(before)[1]   # the DSR collapse is unchanged
    assert len(ds.deduplicate_trials(after)[0]) == len(ds.deduplicate_trials(before)[0])


def test_a_third_attempt_appends_to_superseded_attempts_in_order(env):
    state_path, config_path = env
    for sharpe, rid in ((1.0, "RID_A"), (2.0, "RID_B"), (3.0, "RID_C")):
        rpr._record_backtest_trial("run_965", _summary(sharpe, rid), config_path, whole_test=_whole_test())
    (row,) = _rows(state_path, "run_965")
    assert row["protocol_run_id"] == "RID_C" and row["sharpe"] == 3.0
    assert [(a["protocol_run_id"], a["sharpe"]) for a in row["superseded_attempts"]] == [
        ("RID_A", 1.0), ("RID_B", 2.0)]


def test_a_row_written_before_d144_is_replaced_by_a_write_that_carries_an_id(env):
    state_path, config_path = env
    rpr._record_backtest_trial("run_966", _summary(1.0), config_path)            # no id: legacy shape
    rpr._record_backtest_trial("run_966", _summary(2.0, "RID_B"), config_path)
    (row,) = _rows(state_path, "run_966")
    assert row["sharpe"] == 2.0 and row["protocol_run_id"] == "RID_B"
    assert row["superseded_attempts"] == [
        {"protocol_run_id": None, "sharpe": 1.0, "forecast_hash": rpr._compute_forecast_hash(config_path),
         "whole_test_status": None, "whole_test_reason": None}]


def test_an_invalidated_row_keeps_its_flag_in_the_kept_attempt_and_the_new_row_starts_clean(env):
    state_path, config_path = env
    rpr._record_backtest_trial("run_967", _summary(1.0, "RID_A"), config_path)
    assert rpr._mark_trial_invalidated("run_967", "conformance: wrong window")
    rpr._record_backtest_trial("run_967", _summary(2.0, "RID_B"), config_path)
    (row,) = _rows(state_path, "run_967")
    assert "invalidated_artifact" not in row and "invalidation_reason" not in row
    (kept,) = row["superseded_attempts"]
    assert kept["invalidated_artifact"] is True and kept["invalidation_reason"] == "conformance: wrong window"
    assert rpr._mark_trial_invalidated("run_967", "again")              # the new row can be marked on its own


def test_a_changed_config_is_visible_in_the_kept_attempt(env):
    state_path, config_path = env
    rpr._record_backtest_trial("run_968", _summary(1.0, "RID_A"), config_path)
    first_hash = rpr._compute_forecast_hash(config_path)
    config_path.write_text(json.dumps({"strategy": "y"}), encoding="utf-8")
    rpr._record_backtest_trial("run_968", _summary(2.0, "RID_B"), config_path)
    (row,) = _rows(state_path, "run_968")
    assert row["forecast_hash"] == rpr._compute_forecast_hash(config_path) != first_hash
    assert row["superseded_attempts"][0]["forecast_hash"] == first_hash


def test_symbols_fold_and_windows_fingerprint_come_from_the_new_write(env, monkeypatch):
    state_path, config_path = env
    monkeypatch.setattr(rpr, "_trial_fold_field", lambda run_id: {"fold": "C"})
    rpr._record_backtest_trial("run_969", _summary(1.0, "RID_A"), config_path, symbols=["BTCUSD"])
    rpr._record_backtest_trial("run_969", _summary(2.0, "RID_B"), config_path, symbols=["ETHUSD"],
                               windows_sha256="a" * 64)
    (row,) = _rows(state_path, "run_969")
    assert row["fold"] == "C" and row["symbols"] == ["ETHUSD"] and row["windows_sha256"] == "a" * 64


@pytest.mark.parametrize("bad", ["", None, 7, ["RID"], {"id": "RID"}])
def test_a_malformed_run_id_counts_as_absent(bad):
    assert rpr._summary_protocol_run_id({"protocol_run_id": bad}) is None


# run_096's four first-attempt rows, copied from the operator's ledger
# (campaign_record/campaign_state.yaml, 2026-10-16): no protocol_run_id, XRP ruined.
_RUN_096_FIRST_ATTEMPT = """
- {trial_id: 'run_096:asset_LTCUSDT', source: backtest, sharpe: 0.512, expectancy_bps: 23.8563, n_trades: 581,
   statistic_valid: sharpe, below_floor_pct: 0.0, forecast_hash: d58e86d72b548c8f75765f4237c10d6d55016f47098ac0b4300117f44d96a2dd,
   symbols: [LTCUSD], fold: C,
   whole_test: {basis: whole_test_daily_equal_weight_v2, status: ok, reason: null, sr_daily: 0.0268, n_daily_returns: 729}}
- {trial_id: 'run_096:asset_XRPUSDT', source: backtest, sharpe: -0.967, expectancy_bps: -116.6943, n_trades: 587,
   statistic_valid: sharpe, below_floor_pct: 0.0, forecast_hash: d58e86d72b548c8f75765f4237c10d6d55016f47098ac0b4300117f44d96a2dd,
   symbols: [XRPUSD], fold: C,
   whole_test: {basis: whole_test_daily_equal_weight_v2, status: error,
     reason: "PortfolioRuined: equal-weight portfolio: portfolio_states.csv has equity -589.66 at '2018-09-21'",
     sr_daily: null, n_daily_returns: null}}
- {trial_id: 'run_096:base', source: backtest, sharpe: 1.0735, expectancy_bps: 28.7722, n_trades: 584,
   statistic_valid: sharpe, below_floor_pct: 0.0, forecast_hash: d58e86d72b548c8f75765f4237c10d6d55016f47098ac0b4300117f44d96a2dd,
   symbols: [BTCUSD], fold: C,
   whole_test: {basis: whole_test_daily_equal_weight_v2, status: ok, reason: null, sr_daily: 0.0295, n_daily_returns: 731}}
- {trial_id: 'run_096:design_scaling_factor_10', source: backtest, sharpe: 1.066, expectancy_bps: 14.984, n_trades: 653,
   statistic_valid: sharpe, below_floor_pct: 0.0, forecast_hash: 59de571e20c4560c735ce8543dc11812c4d1ee6d3b08f67f3b0a2d15a267be78,
   symbols: [BTCUSD], fold: C,
   whole_test: {basis: whole_test_daily_equal_weight_v2, status: ok, reason: null, sr_daily: 0.0217, n_daily_returns: 731}}
"""


def test_replay_of_run_096_first_attempt_rows(env, monkeypatch):
    state_path, config_path = env
    monkeypatch.setattr(rpr, "_trial_fold_field", lambda run_id: {"fold": "C"})   # run_096 is a fold-C run
    first = yaml.safe_load(_RUN_096_FIRST_ATTEMPT)
    state_path.write_text(yaml.safe_dump({"trial_sharpes": first}), encoding="utf-8")

    resumed = {  # the re-run's numbers: (variant, symbol, sharpe, whole-test status)
        "asset_LTCUSDT": ("LTCUSD", 0.4, "ok"),
        "asset_XRPUSDT": ("XRPUSD", -0.3, "ok"),
        "base": ("BTCUSD", 0.9, "ok"),
        "design_scaling_factor_10": ("BTCUSD", 0.8, "ok"),
    }
    for variant, (symbol, sharpe, status) in resumed.items():
        rpr._record_backtest_trial("run_096", _summary(sharpe, "RESUME_RID"), config_path,
                                   trial_id=f"run_096:{variant}", symbols=[symbol],
                                   whole_test=_whole_test(status))

    after = yaml.safe_load(state_path.read_text(encoding="utf-8"))["trial_sharpes"]
    assert [t["trial_id"] for t in after] == [t["trial_id"] for t in first]      # same four rows, same order
    by_id = {t["trial_id"]: t for t in after}
    assert all(t["protocol_run_id"] == "RESUME_RID" and t["fold"] == "C" for t in after)
    assert by_id["run_096:asset_XRPUSDT"]["sharpe"] == -0.3
    assert by_id["run_096:asset_XRPUSDT"]["whole_test"]["status"] == "ok"
    (kept,) = by_id["run_096:asset_XRPUSDT"]["superseded_attempts"]              # the ruined try stays visible
    assert kept["protocol_run_id"] is None and kept["sharpe"] == -0.967
    assert kept["whole_test_status"] == "error" and kept["whole_test_reason"].startswith("PortfolioRuined")
    for variant in ("asset_LTCUSDT", "base", "design_scaling_factor_10"):
        (kept,) = by_id[f"run_096:{variant}"]["superseded_attempts"]
        assert kept["whole_test_status"] == "ok"
    assert by_id["run_096:base"]["sharpe"] == 0.9

    again = state_path.read_bytes()                                              # a second pass of the same run is a no-op
    for variant, (symbol, sharpe, status) in resumed.items():
        rpr._record_backtest_trial("run_096", _summary(sharpe, "RESUME_RID"), config_path,
                                   trial_id=f"run_096:{variant}", symbols=[symbol], whole_test=_whole_test(status))
    assert state_path.read_bytes() == again
