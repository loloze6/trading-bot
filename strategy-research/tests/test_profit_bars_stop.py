"""
delivery_plan_v26.md 0.2 (item 2) -- config/profitability_bars.yaml and the
branch-3 stop, gated by orchestrator.profit_bars_file.enabled (off by default).

Covers:
  * _load_profitability_bars's schema validation (loud on missing/wrong-typed
    fields, never a silent default).
  * _evaluate_profit_bars's bar-by-bar grading on synthetic
    promotion_audit.yaml/protocol_result.yaml-shaped fixtures -- a clear PASS
    bar, a clear FAIL bar, and a genuinely NOT_EVALUABLE bar (avg_daily_return_min,
    which nothing in this pipeline computes today, and a missing per_symbol_summary
    for the drawdown/trade-count bars).
  * The flag-off byte-identity of _dispatch_verdict_route's promote branch --
    config/profitability_bars.yaml is never read, profit_bars_evaluation.yaml is
    never written, and the route stays "holdout_evaluation" unconditionally,
    exactly as before this feature existed.
  * The flag-on PASS path: profit_bars_reached is set, status becomes
    paused_for_human, and the route becomes "human_pause".
  * run_campaign._classify_human_pause's new profit_bars_reached branch, and
    that it correctly outranks the pre-existing provisional_promote_awaiting_holdout
    check for the exact reason research_only_unverified does (promotion_audit.yaml
    is written on the SAME promote branch, before this flag, so it always exists
    by the time profit_bars_reached could be set).

Every test relies on tests/conftest.py's autouse `_sandbox_by_default` fixture,
which redirects run_phase1_research.ROOT (and run_campaign.ROOT) into a
per-test tmp_path sandbox -- config/profitability_bars.yaml and
config/campaign_config.yaml are written into THAT sandboxed config/ dir, never
the real repo files.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_campaign as rc  # noqa: E402
import run_phase1_research as rpr  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_BARS = {
    "sharpe_min": 0.5,
    "max_drawdown_pct_max": 25.0,
    "avg_daily_return_min": 0.0005,
    "trade_count_min": 30,
    "deflated_sharpe_threshold": 0.95,
    "target_instrument_set": ["BTCUSDT", "ETHUSDT"],
    "ratified_by": None,
    "ratified_at": None,
}


def _write_bars_file(root: Path, overrides: dict | None = None, doc: dict | None = None) -> Path:
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    body = dict(_VALID_BARS) if doc is None else doc
    if overrides:
        body.update(overrides)
    path = config_dir / "profitability_bars.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(body, f)
    return path


def _set_profit_bars_flag(root: Path, enabled) -> None:
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    cfg_path = config_dir / "campaign_config.yaml"
    existing = {}
    if cfg_path.exists():
        existing = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    orchestrator = existing.get("orchestrator") or {}
    if enabled is None:
        orchestrator.pop("profit_bars_file", None)
    else:
        orchestrator["profit_bars_file"] = {"enabled": bool(enabled)}
    existing["orchestrator"] = orchestrator
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(existing, f)


_VALID_AUDIT = {
    "hypothesis_id": "run_test",
    "generated_at": "2026-09-20T00:00:00+00:00",
    "raw_median_sharpe": 1.2,
    "total_hypotheses_tested": 10,
    "total_campaign_runs": 10,
    "total_variants_tested": 10,
    "n_trials_used": 10,
    "is_sparse_trading": False,
    "passes_deflated_threshold": True,
    "promotion_threshold_raw": 0.1,
    "promotion_threshold_deflated": 0.95,
    "excluded_trial_counts": {
        "statistic_expectancy": 0, "statistic_neither": 0, "no_sharpe_value": 0,
        "non_finite_sharpe": 0, "dedup_removed": 0, "invalidated_artifact": 0,
    },
    "deflated_sharpe_ratio": 0.97,
    "expected_max_sharpe": -0.3,
    "trial_sharpe_variance": 0.05,
    "correction_method": "bailey_lopezdeprado_2014",
}


def _make_run_dir(tmp_path: Path, audit: dict | None, protocol_result: dict | None,
                   pipeline_state: dict | None = None) -> Path:
    run_dir = tmp_path / "run_test"
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    # _write_promotion_audit reads verdict_interpretation.yaml unconditionally
    # (for hypothesis_id) -- every real run reaching the promote branch has one
    # (verdict_interpreter always runs before _dispatch_verdict_route).
    with open(artifacts / "verdict_interpretation.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"hypothesis_id": "run_test"}, f)
    if audit is not None:
        with open(artifacts / "promotion_audit.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(audit, f)
    if protocol_result is not None:
        with open(artifacts / "protocol_result.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(protocol_result, f)
    state = pipeline_state if pipeline_state is not None else {
        "status": "active", "flags": {}, "audit_log": {}, "current_stage": "verdict_interpreter",
    }
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f)
    return run_dir


def _generous_protocol_result() -> dict:
    """Every bar should PASS against this + _VALID_AUDIT (except
    avg_daily_return_min, which is always NOT_EVALUABLE -- nothing computes it)."""
    return {
        "per_symbol_summary": {
            "BTCUSDT": {"median_sharpe": 1.5, "max_abs_drawdown_pct": 10.0, "min_trade_count": 50},
            "ETHUSDT": {"median_sharpe": 1.1, "max_abs_drawdown_pct": 12.0, "min_trade_count": 60},
        },
    }


def _dismal_protocol_result() -> dict:
    """Worst-symbol drawdown/trade-count both clearly fail their bars."""
    return {
        "per_symbol_summary": {
            "BTCUSDT": {"median_sharpe": -2.0, "max_abs_drawdown_pct": 40.0, "min_trade_count": 3},
            "ETHUSDT": {"median_sharpe": -1.0, "max_abs_drawdown_pct": 12.0, "min_trade_count": 60},
        },
    }


# ---------------------------------------------------------------------------
# Loader / schema validation
# ---------------------------------------------------------------------------

def test_load_profitability_bars_valid_file():
    _write_bars_file(rpr.ROOT)
    bars = rpr._load_profitability_bars()
    assert bars["sharpe_min"] == 0.5
    assert bars["target_instrument_set"] == ["BTCUSDT", "ETHUSDT"]
    assert bars["ratified_by"] is None


def test_load_profitability_bars_missing_file_raises():
    with pytest.raises(rpr.ProfitabilityBarsSchemaError):
        rpr._load_profitability_bars()


@pytest.mark.parametrize("missing_key", sorted(_VALID_BARS.keys()))
def test_load_profitability_bars_missing_field_raises_loudly(missing_key):
    doc = dict(_VALID_BARS)
    del doc[missing_key]
    _write_bars_file(rpr.ROOT, doc=doc)
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match=missing_key):
        rpr._load_profitability_bars()


def test_load_profitability_bars_wrong_type_raises_loudly():
    _write_bars_file(rpr.ROOT, overrides={"trade_count_min": "thirty"})
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="trade_count_min"):
        rpr._load_profitability_bars()


def test_load_profitability_bars_bool_rejected_for_numeric_field():
    """bool is a subclass of int in Python -- sharpe_min: true must not silently
    pass as 1."""
    _write_bars_file(rpr.ROOT, overrides={"sharpe_min": True})
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="sharpe_min"):
        rpr._load_profitability_bars()


def test_load_profitability_bars_empty_instrument_set_rejected():
    _write_bars_file(rpr.ROOT, overrides={"target_instrument_set": []})
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="target_instrument_set"):
        rpr._load_profitability_bars()


def test_load_profitability_bars_non_mapping_file_rejected():
    config_dir = rpr.ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "profitability_bars.yaml").write_text("- just\n- a\n- list\n", encoding="utf-8")
    with pytest.raises(rpr.ProfitabilityBarsSchemaError):
        rpr._load_profitability_bars()


# ---------------------------------------------------------------------------
# _profit_bars_file_enabled flag reading
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, False)])
def test_profit_bars_file_enabled_reads_flag(enabled, expected):
    _set_profit_bars_flag(rpr.ROOT, enabled)
    assert rpr._profit_bars_file_enabled() is expected


def test_profit_bars_file_enabled_false_when_config_absent():
    assert rpr._profit_bars_file_enabled() is False


# ---------------------------------------------------------------------------
# _evaluate_profit_bars: bar-by-bar grading
# ---------------------------------------------------------------------------

def test_evaluate_profit_bars_all_evaluable_bars_pass(tmp_path):
    """A bar that clearly passes: generous numbers against _VALID_BARS's
    thresholds. avg_daily_return_min is NOT_EVALUABLE regardless (no source
    anywhere in this pipeline today), so overall result is FAIL even though
    every OTHER bar passes -- 'every bar must pass' means NOT_EVALUABLE does
    not count as a pass."""
    _write_bars_file(rpr.ROOT)
    run_dir = _make_run_dir(tmp_path, _VALID_AUDIT, _generous_protocol_result())

    result = rpr._evaluate_profit_bars(run_dir, "run_test")

    by_name = {b["name"]: b for b in result["bars"]}
    assert by_name["sharpe_min"]["result"] == "PASS"
    assert by_name["deflated_sharpe_threshold"]["result"] == "PASS"
    assert by_name["max_drawdown_pct_max"]["result"] == "PASS"
    assert by_name["trade_count_min"]["result"] == "PASS"
    assert by_name["avg_daily_return_min"]["result"] == "NOT_EVALUABLE"
    assert result["result"] == "FAIL"  # NOT_EVALUABLE blocks overall PASS
    assert (run_dir / "artifacts" / "profit_bars_evaluation.yaml").exists()


def test_evaluate_profit_bars_clear_fail_bar(tmp_path):
    """A bar that clearly fails: dismal drawdown/trade-count numbers."""
    _write_bars_file(rpr.ROOT)
    run_dir = _make_run_dir(tmp_path, _VALID_AUDIT, _dismal_protocol_result())

    result = rpr._evaluate_profit_bars(run_dir, "run_test")

    by_name = {b["name"]: b for b in result["bars"]}
    assert by_name["max_drawdown_pct_max"]["result"] == "FAIL"
    assert by_name["max_drawdown_pct_max"]["actual"] == 40.0  # worst symbol, not best
    assert by_name["trade_count_min"]["result"] == "FAIL"
    assert by_name["trade_count_min"]["actual"] == 3  # worst symbol, not best
    assert result["result"] == "FAIL"
    assert any("max_drawdown_pct_max" in r for r in result["reasons"])
    assert any("trade_count_min" in r for r in result["reasons"])


def test_evaluate_profit_bars_not_evaluable_when_data_absent(tmp_path):
    """No promotion_audit.yaml and no protocol_result.yaml at all -- every bar
    sourced from either file reads NOT_EVALUABLE, never a crash or a silent PASS."""
    _write_bars_file(rpr.ROOT)
    run_dir = _make_run_dir(tmp_path, audit=None, protocol_result=None)

    result = rpr._evaluate_profit_bars(run_dir, "run_test")

    for bar in result["bars"]:
        assert bar["result"] == "NOT_EVALUABLE", bar
    assert result["result"] == "FAIL"


def test_evaluate_profit_bars_deflated_sharpe_not_evaluable_on_sparse_path(tmp_path):
    """promotion_audit.yaml's sparse-trading branch never computes
    deflated_sharpe_ratio (it stays None) -- must read NOT_EVALUABLE, not FAIL
    (a None comparison is not a measured failure)."""
    _write_bars_file(rpr.ROOT)
    sparse_audit = dict(_VALID_AUDIT)
    sparse_audit["is_sparse_trading"] = True
    sparse_audit["deflated_sharpe_ratio"] = None
    run_dir = _make_run_dir(tmp_path, sparse_audit, _generous_protocol_result())

    result = rpr._evaluate_profit_bars(run_dir, "run_test")

    by_name = {b["name"]: b for b in result["bars"]}
    assert by_name["deflated_sharpe_threshold"]["result"] == "NOT_EVALUABLE"


# ---------------------------------------------------------------------------
# Flag-off byte identity of _dispatch_verdict_route's promote branch
# ---------------------------------------------------------------------------

def _promote_interp() -> dict:
    return {"hypothesis_verdict": "promote", "lineage_routing": None}


def test_flag_off_promote_branch_never_reads_or_writes_profit_bars(tmp_path):
    _set_profit_bars_flag(rpr.ROOT, False)
    assert rpr._profit_bars_file_enabled() is False
    # Deliberately do NOT write config/profitability_bars.yaml -- if the flag-off
    # path ever tried to read it, this test would fail with
    # ProfitabilityBarsSchemaError instead of silently passing.

    run_dir = _make_run_dir(tmp_path, audit=None, protocol_result={"per_symbol_summary": {}})
    campaign = {"runs": [], "trial_sharpes": []}

    route = rpr._dispatch_verdict_route(
        run_dir, "run_test", _promote_interp(), campaign, "promote", None,
    )

    assert route == "holdout_evaluation"
    assert (run_dir / "artifacts" / "promotion_audit.yaml").exists()
    assert not (run_dir / "artifacts" / "profit_bars_evaluation.yaml").exists()
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["status"] == "active"
    assert "profit_bars_reached" not in state.get("flags", {})


def test_flag_on_but_bars_fail_still_routes_to_holdout_evaluation(tmp_path, monkeypatch):
    _set_profit_bars_flag(rpr.ROOT, True)
    _write_bars_file(rpr.ROOT)
    # Force a FAIL: no protocol_result.yaml means every per-symbol bar reads
    # NOT_EVALUABLE, and no promotion_audit numbers beyond what
    # _write_promotion_audit itself derives (n_dsr_total < 2 in an empty sandbox
    # campaign -> passes_deflated False, dsr None) -- overall result is FAIL either way.
    run_dir = _make_run_dir(tmp_path, audit=None, protocol_result=None)
    campaign = {"runs": [], "trial_sharpes": []}

    route = rpr._dispatch_verdict_route(
        run_dir, "run_test", _promote_interp(), campaign, "promote", None,
    )

    assert route == "holdout_evaluation"
    pbe = yaml.safe_load((run_dir / "artifacts" / "profit_bars_evaluation.yaml").read_text(encoding="utf-8"))
    assert pbe["result"] == "FAIL"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["status"] == "active"
    assert "profit_bars_reached" not in state.get("flags", {})


def test_flag_on_and_bars_pass_pauses_for_human(tmp_path, monkeypatch):
    _set_profit_bars_flag(rpr.ROOT, True)
    _write_bars_file(rpr.ROOT)
    # Stub _evaluate_profit_bars directly: avg_daily_return_min's permanent
    # NOT_EVALUABLE status means no REAL input can produce an overall PASS today
    # (see its own comment in run_phase1_research.py) -- this is the one place
    # that must be verified as pure routing logic, not bar arithmetic (already
    # covered by test_evaluate_profit_bars_* above).
    monkeypatch.setattr(
        rpr, "_evaluate_profit_bars",
        lambda run_dir, run_id: {"result": "PASS", "bars": [], "reasons": []},
    )
    run_dir = _make_run_dir(tmp_path, audit=None, protocol_result={"per_symbol_summary": {}})
    campaign = {"runs": [], "trial_sharpes": []}

    route = rpr._dispatch_verdict_route(
        run_dir, "run_test", _promote_interp(), campaign, "promote", None,
    )

    assert route == "human_pause"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["status"] == "paused_for_human"
    assert state["flags"]["profit_bars_reached"] is True
    # promotion_audit.yaml is still written -- the stop happens AFTER it, not instead of it.
    assert (run_dir / "artifacts" / "promotion_audit.yaml").exists()


def test_flag_on_evaluation_exception_falls_back_to_holdout_evaluation(tmp_path, monkeypatch):
    """A bug in profit-bars evaluation must never turn an already-successful
    _write_promotion_audit call into a misclassified failure -- same isolation
    posture as the E-046b grid-evaluation block it was modeled on."""
    _set_profit_bars_flag(rpr.ROOT, True)
    # Deliberately do NOT write config/profitability_bars.yaml -- _evaluate_profit_bars
    # will raise ProfitabilityBarsSchemaError when it calls _load_profitability_bars.
    run_dir = _make_run_dir(tmp_path, audit=None, protocol_result={"per_symbol_summary": {}})
    campaign = {"runs": [], "trial_sharpes": []}

    route = rpr._dispatch_verdict_route(
        run_dir, "run_test", _promote_interp(), campaign, "promote", None,
    )

    assert route == "holdout_evaluation"
    assert not (run_dir / "artifacts" / "profit_bars_evaluation.yaml").exists()
    assert (run_dir / "artifacts" / "promotion_audit.yaml").exists()
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["status"] == "active"


# ---------------------------------------------------------------------------
# run_campaign._classify_human_pause: the new branch and its required ordering
# ---------------------------------------------------------------------------

def test_classify_human_pause_returns_profit_bars_reached_when_flagged(tmp_path):
    run_dir = tmp_path / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    state = {"flags": {"profit_bars_reached": True}}
    assert rc._classify_human_pause(run_dir, state) == "profit_bars_reached"


def test_classify_human_pause_falls_through_unchanged_when_flag_unset(tmp_path):
    """Same run_dir/state shape, flag NOT set -- must fall through to the
    pre-existing provisional_promote_awaiting_holdout classification exactly
    as before this slice, since promotion_audit.yaml exists and
    holdout_result.yaml does not."""
    run_dir = tmp_path / "run_test"
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True)
    with open(artifacts / "promotion_audit.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"hypothesis_id": "run_test"}, f)
    state = {"flags": {}}
    assert rc._classify_human_pause(run_dir, state) == "provisional_promote_awaiting_holdout"


def test_classify_human_pause_profit_bars_reached_outranks_promotion_audit_block(tmp_path):
    """Both promotion_audit.yaml (real, on disk -- _write_promotion_audit ran
    before the flag was ever set, same promote branch) AND the flag are present
    simultaneously in the real flow. The new check must win -- exactly the
    research_only_unverified precedent this branch's own comment cites."""
    run_dir = tmp_path / "run_test"
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True)
    with open(artifacts / "promotion_audit.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"hypothesis_id": "run_test"}, f)
    state = {"flags": {"profit_bars_reached": True}}
    assert rc._classify_human_pause(run_dir, state) == "profit_bars_reached"


# ---------------------------------------------------------------------------
# run_loop's own dispatch: the verdict_interpreter branch must not silently
# un-pause a run the profit-bars stop just paused (CODE-REVIEW REGRESSION,
# 2026-09-21).
# ---------------------------------------------------------------------------

def test_run_loop_verdict_interpreter_human_pause_is_not_overwritten(tmp_path, monkeypatch):
    """CODE-REVIEW REGRESSION: unlike every sibling branch that can return
    "human_pause" (backtest_specification, data_availability_gate,
    holdout_evaluation), the verdict_interpreter branch had no
    `if next_stage == "human_pause": break` guard -- step 6's unconditional
    update_state(status="active", ...) ran immediately after and silently
    un-paused a run the profit-bars stop (or any future human_pause route
    through this branch) had just paused. resume_pipeline's own hard check
    (`if status != "paused_for_human": ... return`) would then refuse to
    resume a genuinely halted run. Isolates the run_loop dispatch bug itself
    by monkeypatching determine_post_verdict_route directly -- does not need
    the full profit-bars machinery wired to prove this."""
    root = rpr.ROOT
    run_id = "run_950"
    run_dir = root / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "handoffs").mkdir(parents=True)
    with open(run_dir / "artifacts" / "verdict_interpretation.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"hypothesis_id": run_id}, f)
    with open(run_dir / "handoffs" / "protocol_to_verdict_interpreter.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"required_inputs": [], "deliverables": []}, f)
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({
            "run_id": run_id, "status": "active", "pending_stage": "verdict_interpreter",
            "completed_stages": [], "flags": {}, "audit_log": {},
            "counters": {"refinements_used": 0, "reruns_used": 0},
        }, f, sort_keys=False)

    monkeypatch.setattr(rpr, "determine_post_verdict_route", lambda path, rid: "human_pause")
    monkeypatch.setattr(rpr, "_auto_generate_findings_carryover", lambda path, interp, lineage_routing=None: None)

    rpr.run_loop(run_id)

    final = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert final["status"] == "paused_for_human", (
        f"run_loop's verdict_interpreter branch overwrote a human_pause back to "
        f"{final['status']!r} -- the missing break regression")
