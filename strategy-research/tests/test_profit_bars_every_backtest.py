"""
Branch 3 on every backtest -- orchestrator.profit_bars_every_backtest.enabled
(off by default; requires orchestrator.profit_bars_file.enabled). Operator-
approved 2026-09-24; delivery_plan_v26.md target row "8 · profit bars ... one
file, every backtest, stop rule".

Covers:
  1. The flag reader: absent/off, non-bool, the profit_bars_file dependency
     (also enforced at run_loop start, before any stage spends anything).
  2. Flag-off byte-identity: run_loop through protocol_execution never reads
     config/profitability_bars.yaml, never writes profit_bars_evaluation.yaml,
     never sets the flag; the memory keeps null + "not evaluated before regroup".
  3. Every variant evaluated: one result per index.yaml variant (tested ones
     graded, failed / not_tested ones NOT_TESTED), the run_id-keyed single entry
     with the variant loop off.
  4. The stop fires when ANY variant passes every bar and stays off when none
     does; it reuses profit_bars_reached (classified by run_campaign exactly as
     the promote-path stop).
  5. idea_status.yaml / grid_evaluation.yaml / the trial ledger are byte-identical
     across the check (no status change, no trial row).
  6. Campaign memory: per-variant profit_bars when on, null+reason when off,
     loud on a stale / promote-scope / inconsistent evaluation.
  7. Promote-path coexistence: under the new flag the promote path neither
     re-evaluates nor re-pauses; without it the promote path is unchanged.
  8. A malformed bars file fails loud (nothing graded, nothing written; the run
     fails instead of guessing a threshold).

avg_daily_return_min always reads NOT_EVALUABLE today (nothing in the pipeline
computes a mean daily return), so no real input reaches an overall PASS. The
PASS-path tests therefore wrap the REAL _grade_profit_bars and drop only that one
bar -- the other four bars are still graded for real, per variant.
"""
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as rc  # noqa: E402
import campaign_memory as cm  # noqa: E402

from test_e058_s2a_regroup_record import (  # noqa: E402
    ALL_ON, RUN_ID, _seed, _memory, _memory_path, _set_orchestrator, _fake_llm,
    REPORT_CATEGORIES, _minimal_run_at)

PB_FILE_ON = {"profit_bars_file": {"enabled": True}}
PB_ALL_ON = {"profit_bars_file": {"enabled": True},
             "profit_bars_every_backtest": {"enabled": True}}
VARIANT_LOOP_ON = {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True}}

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
_SCHEMA = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" /
                      "campaign_memory.schema.json").read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _write_bars(doc: dict | None = None) -> Path:
    path = rpr.ROOT / "config" / "profitability_bars.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(_VALID_BARS if doc is None else doc), encoding="utf-8")
    return path


def _generous_pr() -> dict:
    """Clears sharpe/drawdown/trade-count bars on every symbol (DSR too, against
    _seed_dsr_ledger's distribution)."""
    return {"verdict": "promote", "results": [
                {"symbol": s, "window": w, "core": {"sharpe": 1.4}}
                for s in ("BTCUSDT", "ETHUSDT") for w in ("w1", "w2")],
            "per_symbol_summary": {
                "BTCUSDT": {"median_sharpe": 1.5, "max_abs_drawdown_pct": 10.0, "min_trade_count": 50},
                "ETHUSDT": {"median_sharpe": 1.3, "max_abs_drawdown_pct": 12.0, "min_trade_count": 60}}}


def _dismal_pr() -> dict:
    return {"verdict": "kill", "results": [
                {"symbol": "BTCUSDT", "window": w, "core": {"sharpe": -1.0}} for w in ("w1", "w2")],
            "per_symbol_summary": {
                "BTCUSDT": {"median_sharpe": -1.0, "max_abs_drawdown_pct": 40.0, "min_trade_count": 3}}}


def _seed_dsr_ledger() -> None:
    """Append 10 real-Sharpe trial rows (other runs) so the DSR is computable:
    trial Sharpes spread around 0, so a candidate at ~1.4 deflates to ~1.0 and one
    at -1.0 to ~0.0. Keeps whatever rows _seed already wrote for RUN_ID."""
    state = rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH) if rpr.CAMPAIGN_STATE_PATH.exists() else {
        "campaign_id": "t", "runs": [], "trial_sharpes": []}
    rows = state.setdefault("trial_sharpes", [])
    rows += [{"trial_id": f"run_{800 + i}", "source": "backtest", "statistic_valid": "sharpe",
              "sharpe": round(-0.25 + 0.05 * i, 2), "forecast_hash": f"fh-ledger-{i}"}
             for i in range(10)]
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)


def _variant_run(variant_prs: dict, run_id: str = RUN_ID) -> Path:
    """A variant-loop run: index.yaml with the given tested variants (each with its
    own protocol_result), plus `broken` (validated, no result: its backtest failed)
    and `asset` (not_tested by the data gate)."""
    run_dir = _seed(run_id=run_id, idea_status="refuted", variant_loop=True)
    arts = run_dir / "artifacts"
    index = {}
    for vid in list(variant_prs) + ["broken"]:
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
    index["asset"] = {"status": "not_tested", "reason": "patch application failed: /x"}
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    for vid, pr in variant_prs.items():
        rpr.save_yaml(arts / "variants" / vid / "protocol_result.yaml", pr)
    broken_pr = arts / "variants" / "broken" / "protocol_result.yaml"
    if broken_pr.exists():
        broken_pr.unlink()
    return run_dir


@pytest.fixture
def drop_daily_return_bar(monkeypatch):
    """Wrap the REAL grader; drop only avg_daily_return_min (never evaluable
    today) and recompute the overall from the four real bars."""
    real = rpr._grade_profit_bars

    def _wrapped(bars, **kw):
        results, _overall, _reasons = real(bars, **kw)
        results = [r for r in results if r["name"] != "avg_daily_return_min"]
        overall = "PASS" if {r["result"] for r in results} == {"PASS"} else "FAIL"
        reasons = [f"{r['name']}: {r['result']}" for r in results if r["result"] != "PASS"]
        return results, overall, reasons
    monkeypatch.setattr(rpr, "_grade_profit_bars", _wrapped)


def _state(run_dir: Path) -> dict:
    return rpr.load_yaml(run_dir / "pipeline_state.yaml")


def _pbe(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "artifacts" / "profit_bars_evaluation.yaml")
                          .read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. The flag reader and its dependency
# ---------------------------------------------------------------------------

def test_flag_false_when_absent_or_off():
    _set_orchestrator(None)
    assert rpr._profit_bars_every_backtest_enabled() is False
    _set_orchestrator(PB_FILE_ON)
    assert rpr._profit_bars_every_backtest_enabled() is False
    _set_orchestrator({**PB_FILE_ON, "profit_bars_every_backtest": {"enabled": False}})
    assert rpr._profit_bars_every_backtest_enabled() is False


def test_flag_true_with_profit_bars_file_on():
    _set_orchestrator(PB_ALL_ON)
    assert rpr._profit_bars_every_backtest_enabled() is True


@pytest.mark.parametrize("bad", ["true", None, 1])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**PB_FILE_ON, "profit_bars_every_backtest": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real"):
        rpr._profit_bars_every_backtest_enabled()


def test_flag_on_without_profit_bars_file_raises():
    _set_orchestrator({"profit_bars_every_backtest": {"enabled": True}})
    with pytest.raises(ValueError, match="requires orchestrator.profit_bars_file.enabled=true"):
        rpr._profit_bars_every_backtest_enabled()


def test_run_loop_fails_at_start_when_dependency_missing(monkeypatch):
    _set_orchestrator({"profit_bars_every_backtest": {"enabled": True}})
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    invoked = []

    async def _record(stage_name, run_id, retry_context=None):
        invoked.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert invoked == []  # nothing spent
    assert state["status"] == "failed" and "profit_bars_file" in state["last_error"]
    assert state["pending_stage"] == "protocol_execution"


# ---------------------------------------------------------------------------
# 2. Flag-off byte-identity
# ---------------------------------------------------------------------------

def _loop_from_protocol_execution(monkeypatch, orchestrator: dict, pr: dict | None = None,
                                  dsr_ledger: bool = False):
    """specialist_readers + regroup_record flow from protocol_execution, variant
    loop off, the backtest itself stubbed (its artifacts are pre-seeded)."""
    _set_orchestrator(orchestrator)
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _seed(pending="protocol_execution", idea_status="refuted")
    rpr._ensure_protocol_ref_pinned(run_dir, RUN_ID, {"protocol_ref": f"protocols/{RUN_ID}_pinned.json"})
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    if pr is not None:
        pr = {**pr, "protocol_file": str(rpr.ROOT / "protocols" / "p.json")}
        rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", pr)
    if dsr_ledger:
        _seed_dsr_ledger()
    for c in REPORT_CATEGORIES:
        (run_dir / "artifacts" / "proposals" / f"{c}.yaml").unlink()
    stages, calls = [], []

    async def _record(stage_name, run_id, retry_context=None):
        stages.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))
    rpr.run_loop(RUN_ID)
    return run_dir, stages, calls


def test_flag_off_run_loop_reads_and_writes_nothing_new(monkeypatch):
    """No bars file exists at all: any read of it would raise and fail the run."""
    run_dir, stages, calls = _loop_from_protocol_execution(monkeypatch, ALL_ON)
    state = _state(run_dir)
    assert state["completed_stages"][-3:] == ["protocol_execution", "specialist_readers", "regroup_record"]
    assert state["pending_stage"] == "completed_rejected"
    assert not (run_dir / "artifacts" / "profit_bars_evaluation.yaml").exists()
    assert "profit_bars_reached" not in (state.get("flags") or {})
    e = _memory()["runs"][RUN_ID]
    assert e["profit_bars"] is None and e["profit_bars_reason"] == "not evaluated before regroup"


def test_flag_off_with_profit_bars_file_on_still_evaluates_nothing_after_backtest(monkeypatch):
    """profit_bars_file alone keeps its promote-path-only behaviour: nothing is
    graded right after protocol_execution."""
    _write_bars()
    run_dir, _stages, _calls = _loop_from_protocol_execution(monkeypatch, {**ALL_ON, **PB_FILE_ON})
    assert _state(run_dir)["pending_stage"] == "completed_rejected"
    assert not (run_dir / "artifacts" / "profit_bars_evaluation.yaml").exists()


def test_extracted_dsr_context_matches_promotion_audit(tmp_path):
    """_promotion_dsr_context was extracted verbatim from _write_promotion_audit:
    the audit still reports exactly the context's numbers for the same candidate."""
    run_dir = _seed(idea_status="refuted")
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", _generous_pr())
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "H-MEM-1"})
    _seed_dsr_ledger()
    rpr._write_promotion_audit(run_dir, RUN_ID)
    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    ctx = rpr._promotion_dsr_context()
    raw, sparse, passes, e_max, dsr = ctx["dsr_candidate"](_generous_pr())
    assert audit["raw_median_sharpe"] == raw and audit["is_sparse_trading"] == sparse
    assert audit["passes_deflated_threshold"] == passes
    assert audit["promotion_threshold_raw"] == e_max
    assert audit["deflated_sharpe_ratio"] == dsr["deflated_sharpe_ratio"]
    assert audit["total_hypotheses_tested"] == ctx["n_dsr_total"]
    assert audit["n_trials_used"] == ctx["n_trials"]
    assert list(audit) == [  # insertion order unchanged (save_yaml keeps it)
        "hypothesis_id", "generated_at", "raw_median_sharpe", "total_hypotheses_tested",
        "total_campaign_runs", "total_variants_tested", "n_trials_used", "is_sparse_trading",
        "passes_deflated_threshold", "promotion_threshold_raw", "promotion_threshold_deflated",
        "excluded_trial_counts", "deflated_sharpe_ratio", "expected_max_sharpe",
        "trial_sharpe_variance", "correction_method"]


# ---------------------------------------------------------------------------
# 3. Every variant evaluated
# ---------------------------------------------------------------------------

def test_every_variant_evaluated_under_the_variant_loop():
    _set_orchestrator({**PB_ALL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"base": _dismal_pr(), "design": _generous_pr()})
    _seed_dsr_ledger()
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    assert ev == _pbe(run_dir)
    assert ev["scope"] == "every_backtest" and ev["run_id"] == RUN_ID
    assert sorted(ev["variants"]) == ["asset", "base", "broken", "design"]
    for vid in ("base", "design"):
        v = ev["variants"][vid]
        assert v["tested"] is True
        assert v["protocol_result_ref"] == f"artifacts/variants/{vid}/protocol_result.yaml"
        assert [b["name"] for b in v["bars"]] == [
            "sharpe_min", "deflated_sharpe_threshold", "max_drawdown_pct_max",
            "trade_count_min", "avg_daily_return_min"]
    for vid in ("asset", "broken"):
        assert ev["variants"][vid]["tested"] is False
        assert ev["variants"][vid]["result"] == "NOT_TESTED" and ev["variants"][vid]["bars"] == []
    # Each variant graded on its OWN numbers, not the base's.
    design = {b["name"]: b for b in ev["variants"]["design"]["bars"]}
    base = {b["name"]: b for b in ev["variants"]["base"]["bars"]}
    assert design["sharpe_min"]["actual"] == 1.4 and design["sharpe_min"]["result"] == "PASS"
    assert design["deflated_sharpe_threshold"]["result"] == "PASS"
    assert design["max_drawdown_pct_max"]["actual"] == 12.0
    assert base["sharpe_min"]["result"] == "FAIL" and base["trade_count_min"]["actual"] == 3
    assert design["avg_daily_return_min"]["result"] == "NOT_EVALUABLE"
    # Real grading today: the always-NOT_EVALUABLE bar blocks every overall PASS.
    assert ev["result"] == "FAIL" and ev["passing"] == [] and ev["stop_raised"] is False
    assert ev["bars_ratified_by"] is None


def test_single_backtest_keyed_by_run_id_with_variant_loop_off():
    _set_orchestrator(PB_ALL_ON)
    _write_bars()
    run_dir = _seed(idea_status="refuted")
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", _generous_pr())
    # config-direct authoring writes an index even with the loop off: not variants.
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"}}})
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    assert list(ev["variants"]) == [RUN_ID]
    assert ev["variants"][RUN_ID]["protocol_result_ref"] == "artifacts/protocol_result.yaml"


def test_no_graded_backtest_at_all_fails_loud():
    _set_orchestrator({**PB_ALL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({})
    with pytest.raises(ValueError, match="no candidate"):
        rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)


# ---------------------------------------------------------------------------
# 4. The stop: fires on any passing variant, stays off otherwise
# ---------------------------------------------------------------------------

def test_stop_fires_when_any_variant_passes(drop_daily_return_bar):
    _set_orchestrator({**PB_ALL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"base": _dismal_pr(), "design": _generous_pr()})
    _seed_dsr_ledger()
    nxt = rpr._run_profit_bars_every_backtest(run_dir, RUN_ID, "specialist_readers")
    assert nxt == "human_pause"
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and state["flags"]["profit_bars_reached"] is True
    ev = _pbe(run_dir)
    assert ev["result"] == "PASS" and ev["passing"] == ["design"] and ev["stop_raised"] is True
    assert ev["variants"]["base"]["result"] == "FAIL"
    # The existing pause reason, reused -- no promotion_audit.yaml exists yet here.
    assert not (run_dir / "artifacts" / "promotion_audit.yaml").exists()
    assert rc._classify_human_pause(run_dir, state) == "profit_bars_reached"


def test_stop_stays_off_when_no_variant_passes(drop_daily_return_bar):
    _set_orchestrator({**PB_ALL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"base": _dismal_pr(), "design": _dismal_pr()})
    _seed_dsr_ledger()
    before = _state(run_dir)
    assert rpr._run_profit_bars_every_backtest(run_dir, RUN_ID, "specialist_readers") == "specialist_readers"
    after = _state(run_dir)
    assert after == before  # no flag, no status change
    ev = _pbe(run_dir)
    assert ev["result"] == "FAIL" and ev["passing"] == [] and ev["stop_raised"] is False


def test_conformance_pause_on_the_same_pass_wins(drop_daily_return_bar):
    """A pause already raised on this protocol_execution pass (conformance) is not
    doubled: the result is recorded, the stop is not raised."""
    _set_orchestrator({**PB_ALL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"design": _generous_pr()})
    _seed_dsr_ledger()
    assert rpr._run_profit_bars_every_backtest(run_dir, RUN_ID, "human_pause") == "human_pause"
    assert "profit_bars_reached" not in (_state(run_dir).get("flags") or {})
    ev = _pbe(run_dir)
    assert ev["passing"] == ["design"] and ev["stop_raised"] is False
    assert ev["stop_suppressed_by"]


def test_run_loop_pauses_right_after_protocol_execution_on_a_pass(monkeypatch, drop_daily_return_bar):
    _write_bars()
    run_dir, stages, calls = _loop_from_protocol_execution(
        monkeypatch, {**ALL_ON, **PB_ALL_ON}, pr=_generous_pr(), dsr_ledger=True)
    state = _state(run_dir)
    assert stages == ["protocol_execution"] and calls == []  # readers never ran
    assert state["status"] == "paused_for_human"  # not overwritten by step 6
    assert state["flags"]["profit_bars_reached"] is True
    assert _pbe(run_dir)["passing"] == [RUN_ID]


# ---------------------------------------------------------------------------
# 5. idea_status and the trial ledger are untouched
# ---------------------------------------------------------------------------

def test_idea_status_grid_and_ledger_byte_identical(drop_daily_return_bar):
    _set_orchestrator({**PB_ALL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"base": _dismal_pr(), "design": _generous_pr()})
    _seed_dsr_ledger()
    arts = run_dir / "artifacts"
    watched = [arts / "idea_status.yaml", arts / "grid_evaluation.yaml", rpr.CAMPAIGN_STATE_PATH,
               arts / "variants" / "index.yaml"]
    before = {p: p.read_bytes() for p in watched}
    assert rpr._run_profit_bars_every_backtest(run_dir, RUN_ID, "specialist_readers") == "human_pause"
    assert {p: p.read_bytes() for p in watched} == before
    assert rpr.load_yaml(arts / "idea_status.yaml")["idea_status"] == "refuted"  # a pass, not validated


# ---------------------------------------------------------------------------
# 6. Campaign memory
# ---------------------------------------------------------------------------

def test_memory_filled_per_variant_when_on():
    _set_orchestrator({**ALL_ON, **PB_ALL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"base": _dismal_pr(), "design": _generous_pr()})
    _seed_dsr_ledger()
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    doc = _memory()
    e = doc["runs"][RUN_ID]
    assert e["profit_bars_reason"] is None
    pb = e["profit_bars"]
    assert pb["scope"] == "every_backtest" and pb["result"] == "FAIL" and pb["passing"] == []
    assert pb["ref"] == f"runs/{RUN_ID}/artifacts/profit_bars_evaluation.yaml"
    assert set(pb["variants"]) == set(e["variants"]) == {"asset", "base", "broken", "design"}
    assert pb["variants"]["asset"] == {"result": "NOT_TESTED", "bars": {}}
    assert pb["variants"]["design"]["bars"]["sharpe_min"] == {"result": "PASS", "actual": 1.4,
                                                               "threshold": 0.5}
    assert e["idea_status"] == "refuted"  # copied from the grid, never from profit bars
    jsonschema.Draft202012Validator(_SCHEMA).validate(doc)


def test_memory_null_and_reason_when_off():
    _set_orchestrator({**ALL_ON, **PB_FILE_ON})
    run_dir = _seed(idea_status="refuted")
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    doc = _memory()
    e = doc["runs"][RUN_ID]
    assert e["profit_bars"] is None and e["profit_bars_reason"] == cm.PROFIT_BARS_NOT_EVALUATED
    jsonschema.Draft202012Validator(_SCHEMA).validate(doc)


def test_schema_rejects_filled_profit_bars_with_a_reason():
    _set_orchestrator({**ALL_ON, **PB_ALL_ON})
    _write_bars()
    run_dir = _seed(idea_status="refuted")
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    doc = _memory()
    jsonschema.Draft202012Validator(_SCHEMA).validate(doc)
    doc["runs"][RUN_ID]["profit_bars_reason"] = cm.PROFIT_BARS_NOT_EVALUATED
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(_SCHEMA).validate(doc)


def test_memory_refuses_missing_evaluation_when_on():
    _set_orchestrator({**ALL_ON, **PB_ALL_ON})
    run_dir = _seed(idea_status="refuted")
    with pytest.raises(cm.CampaignMemoryError, match="profit_bars_evaluation.yaml is missing"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not _memory_path().exists()


def test_memory_refuses_promote_path_evaluation():
    """The promote-path file has one candidate and no scope -- never read as
    per-variant results."""
    _set_orchestrator({**ALL_ON, **PB_ALL_ON})
    run_dir = _seed(idea_status="refuted")
    rpr.save_yaml(run_dir / "artifacts" / "profit_bars_evaluation.yaml",
                  {"run_id": RUN_ID, "generated_at": "x", "bars": [], "result": "FAIL", "reasons": []})
    with pytest.raises(cm.CampaignMemoryError, match="scope"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)


def test_memory_refuses_a_graded_variant_whose_backtest_failed():
    """A stale protocol_result graded for a variant the grid shows as failed on
    this pass: the memory stops loudly instead of recording it as tested."""
    _set_orchestrator({**ALL_ON, **PB_ALL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"base": _dismal_pr(), "design": _generous_pr()})
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "broken" / "protocol_result.yaml", _dismal_pr())
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    with pytest.raises(cm.CampaignMemoryError, match="'broken' is 'failed'"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)


def test_memory_refuses_inconsistent_overall_result():
    _set_orchestrator({**ALL_ON, **PB_ALL_ON})
    _write_bars()
    run_dir = _seed(idea_status="refuted")
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    path = run_dir / "artifacts" / "profit_bars_evaluation.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    doc["result"] = "PASS"
    rpr.save_yaml(path, doc)
    with pytest.raises(cm.CampaignMemoryError, match="disagree"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)


def test_full_loop_flag_on_no_pass_records_memory(monkeypatch):
    _write_bars()
    run_dir, stages, calls = _loop_from_protocol_execution(monkeypatch, {**ALL_ON, **PB_ALL_ON})
    state = _state(run_dir)
    assert state["completed_stages"][-3:] == ["protocol_execution", "specialist_readers", "regroup_record"]
    assert state["pending_stage"] == "completed_rejected"  # the grid's route, unchanged
    assert "profit_bars_reached" not in (state.get("flags") or {})
    e = _memory()["runs"][RUN_ID]
    assert e["profit_bars"]["result"] == "FAIL" and list(e["profit_bars"]["variants"]) == [RUN_ID]


# ---------------------------------------------------------------------------
# 7. Promote-path coexistence
# ---------------------------------------------------------------------------

def _promote(run_dir: Path) -> str:
    return rpr._dispatch_verdict_route(run_dir, RUN_ID, {"hypothesis_verdict": "promote"},
                                       {"runs": [], "trial_sharpes": []}, "promote", None)


def test_promote_path_skipped_under_the_new_flag(monkeypatch, drop_daily_return_bar):
    """Per-backtest check already graded every variant (and paused if one passed);
    the promote path must neither overwrite its artifact nor pause again -- even
    if its own evaluator would say PASS."""
    _set_orchestrator(PB_ALL_ON)
    _write_bars()
    run_dir = _seed(idea_status="refuted")
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "H-MEM-1"})
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    before = (run_dir / "artifacts" / "profit_bars_evaluation.yaml").read_bytes()
    called = []
    monkeypatch.setattr(rpr, "_evaluate_profit_bars",
                        lambda d, r: called.append(r) or {"result": "PASS", "bars": [], "reasons": []})
    assert _promote(run_dir) == "holdout_evaluation"
    assert called == []
    assert (run_dir / "artifacts" / "profit_bars_evaluation.yaml").read_bytes() == before
    assert (run_dir / "artifacts" / "promotion_audit.yaml").exists()
    assert "profit_bars_reached" not in (_state(run_dir).get("flags") or {})


def test_promote_path_unchanged_without_the_new_flag(monkeypatch):
    _set_orchestrator(PB_FILE_ON)
    _write_bars()
    run_dir = _seed(idea_status="refuted")
    rpr.save_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml", {"hypothesis_id": "H-MEM-1"})
    called = []
    monkeypatch.setattr(rpr, "_evaluate_profit_bars",
                        lambda d, r: called.append(r) or {"result": "PASS", "bars": [], "reasons": []})
    assert _promote(run_dir) == "human_pause"
    assert called == [RUN_ID]
    assert _state(run_dir)["flags"]["profit_bars_reached"] is True


# ---------------------------------------------------------------------------
# 8. Malformed bars file fails loud
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("doc", [
    {k: v for k, v in _VALID_BARS.items() if k != "sharpe_min"},
    {**_VALID_BARS, "trade_count_min": "thirty"},
    {**_VALID_BARS, "deflated_sharpe_threshold": True},
])
def test_malformed_bars_file_fails_loud_and_writes_nothing(doc):
    _set_orchestrator(PB_ALL_ON)
    _write_bars(doc)
    run_dir = _seed(idea_status="refuted")
    with pytest.raises(rpr.ProfitabilityBarsSchemaError):
        rpr._run_profit_bars_every_backtest(run_dir, RUN_ID, "specialist_readers")
    assert not (run_dir / "artifacts" / "profit_bars_evaluation.yaml").exists()
    assert "profit_bars_reached" not in (_state(run_dir).get("flags") or {})


def test_missing_bars_file_fails_the_run_loudly(monkeypatch):
    run_dir, stages, calls = _loop_from_protocol_execution(monkeypatch, {**ALL_ON, **PB_ALL_ON})
    state = _state(run_dir)
    assert state["status"] == "failed" and "profitability_bars.yaml" in state["last_error"]
    assert calls == []  # readers never ran on an ungraded backtest
    assert not (run_dir / "artifacts" / "profit_bars_evaluation.yaml").exists()
