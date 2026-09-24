"""
E-058 S2a -- the regroup_record stage and campaign_record/campaign_memory.yaml
(orchestrator.regroup_record.enabled, off by default; requires
orchestrator.specialist_readers.enabled). Spec:
engineering/roadmap/E-058/S1_FINDINGS.md §2-§3 + its operator decision.

Covers:
  1. The flag helper: absent/off, non-bool, the specialist_readers dependency
     (also enforced at run_loop start).
  2. Flag-off identity: registry entry without a skill, specialist_readers
     still routes straight through the grid route, no handoff, no memory file.
  3. Flag-on order: specialist_readers -> regroup_record -> the SAME route
     (validated / refuted / inconclusive), memory written before the route.
  4. Memory content: validated / refuted / inconclusive in both grid-column
     shapes (flag-off `run_id` column, variant-loop columns), and a
     component-error run (engineering_fault, no status, no grid numbers).
  5. Replace on re-run; malformed memory file fails loud and is not
     overwritten; atomic write.
  6. No trial rows: campaign_state bytes identical before/after the stage.
  7. Proposals referenced (ids + count), never scores, never a decision input.
  8. No retired field (hypothesis_family, altitude, lineage_routing, ...).

No LLM: readers' proposals are pre-seeded so the readers stage re-validates
them without a model call. Sandbox: tests/conftest.py's autouse fixture
points rpr.ROOT / rpr.CAMPAIGN_STATE_PATH at a per-test tmp dir.
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import campaign_memory as cm  # noqa: E402
import reader_proposals  # noqa: E402
from build_reports import REPORT_CATEGORIES  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e033_slice4b_gate_conformance_promotion import _minimal_run_at  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    _proposal, _fake_llm, _set_orchestrator, _write_menu_pre_registration)

RUN_ID = "run_980"
READERS_ON = {"grid_evaluation": {"enabled": True}, "category_reports": {"enabled": True},
              "specialist_readers": {"enabled": True}}
ALL_ON = {**READERS_ON, "regroup_record": {"enabled": True}}
CRITERIA = ["ic_median", "trade_floor"]


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _memory_path() -> Path:
    return rpr.ROOT / "campaign_record" / "campaign_memory.yaml"


def _grid(variants: list, idea_status: str) -> dict:
    cell = {"result": "PASS", "value": 0.031, "threshold": 0.02, "n_windows": 2, "n_trades": 40}
    grid = {c: {v: dict(cell) for v in variants} for c in CRITERIA}
    if idea_status == "refuted":
        grid["ic_median"][variants[-1]] = {"result": "FAIL", "value": 0.001, "threshold": 0.02,
                                           "n_windows": 2, "n_trades": 40}
        reason = "at least one criterion FAILed with sufficient data on at least one variant"
    elif idea_status == "inconclusive":
        grid["trade_floor"][variants[0]] = {"result": "INCONCLUSIVE", "n_windows": 2, "n_trades": 3,
                                            "reason": "n_trades=3 < floor 20"}
        reason = "no criterion FAILed, but at least one cell lacked sufficient data to judge"
    else:
        reason = "every criterion PASSed on every variant"
    return {"result": "GRID_EVALUATED", "criteria": list(CRITERIA), "variants": list(variants),
            "grid": grid, "idea_status": idea_status, "reason": reason,
            "evaluated_at": "2026-09-23T00:00:00+00:00"}


def _pr(errors_count=None, symbols=("BTCUSDT",)) -> dict:
    results = []
    for sym in symbols:
        for w in ("w1", "w2"):
            entry = {"symbol": sym, "window": w, "core": {"sharpe": 0.1, "trade_count": 20}}
            if errors_count is not None:
                entry["component_errors"] = {"count": errors_count, "samples": []}
            results.append(entry)
    return {"verdict": "kill", "protocol_file": str(rpr.ROOT / "protocols" / "p.json"),
            "results": results}


def _seed(run_id=RUN_ID, idea_status="refuted", errors_count=None, variant_loop=False,
          pending="regroup_record", proposals=1, score=2) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = pending
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-MEM-1", "timeframe": "1h"})
    _write_menu_pre_registration(run_dir)
    rpr.save_yaml(arts / "protocol_result.yaml", _pr(errors_count))
    (arts / "candidate_strategy_config.json").write_text(json.dumps({"a": 1}), encoding="utf-8")
    if variant_loop:
        variants = ["base", "design"]
        index = {}
        for v in variants + ["broken"]:
            cfg = arts / "variants" / v / "strategy_config.json"
            cfg.parent.mkdir(parents=True, exist_ok=True)
            cfg.write_text(json.dumps({"v": v}), encoding="utf-8")
            index[v] = {"status": "validated", "config_path": f"artifacts/variants/{v}/strategy_config.json"}
        index["asset"] = {"status": "not_tested", "reason": "patch application failed: /x"}
        rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
        for v in variants:
            rpr.save_yaml(arts / "variants" / v / "protocol_result.yaml",
                          _pr(errors_count, symbols=("BTCUSDT", "ETHUSDT") if v == "design" else ("BTCUSDT",)))
    else:
        variants = [run_id]
    grid = _grid(variants, idea_status)
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, run_id))
    for c in REPORT_CATEGORIES:
        rpr.save_yaml(arts / "reports" / f"{c}.yaml", {"category": c})
        rpr.save_yaml(arts / "proposals" / f"{c}.yaml",
                      [_proposal(c, run_id, n, score) for n in range(1, proposals + 1)])
    _seed_trials(run_id, variant_loop)
    return run_dir


def _seed_trials(run_id: str, variant_loop: bool) -> None:
    # forecast_hash values are deliberately NOT the hash of any file on disk: the
    # memory must copy them from the ledger, never recompute them.
    rows = [{"trial_id": run_id, "source": "prescreen", "sharpe": 0.1, "forecast_hash": "fh-prescreen"}]
    if variant_loop:
        rows += [{"trial_id": f"{run_id}:base", "source": "backtest", "sharpe": 0.3,
                  "forecast_hash": "fh-base"},
                 {"trial_id": f"{run_id}:design", "source": "backtest", "sharpe": 0.3,
                  "forecast_hash": "fh-design"},
                 {"trial_id": f"{run_id}:broken", "source": "backtest_failed", "sharpe": None,
                  "forecast_hash": "fh-broken"}]
    else:
        rows += [{"trial_id": run_id, "source": "backtest", "sharpe": 0.2, "forecast_hash": "fh-run"}]
    rows += [{"trial_id": "run_001", "source": "backtest", "sharpe": 0.9, "forecast_hash": "x"},
             {"trial_id": f"{run_id}0", "source": "backtest", "sharpe": 0.9,
              "forecast_hash": "x"}]  # prefix trap
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": rows})


def _memory() -> dict:
    return yaml.safe_load(_memory_path().read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Flag helper and dependency
# ---------------------------------------------------------------------------

def test_flag_false_when_absent():
    _set_orchestrator(None)
    assert rpr._regroup_record_enabled() is False
    _set_orchestrator(READERS_ON)
    assert rpr._regroup_record_enabled() is False


def test_flag_true_with_readers_on():
    _set_orchestrator(ALL_ON)
    assert rpr._regroup_record_enabled() is True


@pytest.mark.parametrize("bad", ["true", None, 1])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**READERS_ON, "regroup_record": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._regroup_record_enabled()


def test_flag_on_without_specialist_readers_raises():
    _set_orchestrator({"regroup_record": {"enabled": True}})
    with pytest.raises(ValueError, match="requires orchestrator.specialist_readers.enabled=true"):
        rpr._regroup_record_enabled()


def test_run_loop_fails_at_start_when_readers_off(monkeypatch):
    _set_orchestrator({"grid_evaluation": {"enabled": True}, "category_reports": {"enabled": True},
                       "regroup_record": {"enabled": True}})
    run_dir = _seed(pending="specialist_readers")
    invoked = []
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", lambda *a, **k: invoked.append(a[0]))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=invoked))
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert invoked == []
    assert state["status"] == "failed" and "specialist_readers" in state["last_error"]
    assert state["pending_stage"] == "specialist_readers"
    assert not _memory_path().exists()


# ---------------------------------------------------------------------------
# 2. Registry and flag-off identity
# ---------------------------------------------------------------------------

def test_registered_without_skill_and_existing_entries_unchanged():
    assert rpr.STAGE_CONFIGS["regroup_record"] == {
        "handoff": "specialist_readers_to_regroup_record.yaml", "default_next": "dynamic_routing"}
    assert "regroup_record" not in rpr._SKILL_MAP
    assert rpr.STAGE_CONFIGS["specialist_readers"] == {
        "handoff": "protocol_to_specialist_readers.yaml", "default_next": "dynamic_routing"}
    assert rpr.STAGE_CONFIGS["protocol_execution"]["default_next"] == "verdict_interpreter"


def _loop_from_specialist_readers(monkeypatch, orchestrator, idea_status, errors_count=None,
                                  run_id=RUN_ID, spy=None):
    _set_orchestrator(orchestrator)
    run_dir = _seed(run_id=run_id, idea_status=idea_status, errors_count=errors_count,
                    pending="specialist_readers")
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))
    # A validated route continues into holdout_evaluation; stop there without running it.
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "holdout_evaluation",
                        {**rpr.STAGE_CONFIGS["holdout_evaluation"], "handoff": "missing.yaml"})
    if spy is not None:
        monkeypatch.setattr(rpr, "determine_post_specialist_readers_route", spy)
    if idea_status == "validated" and not errors_count:
        with pytest.raises(FileNotFoundError):
            rpr.run_loop(run_id)
    else:
        rpr.run_loop(run_id)
    assert calls == []  # proposals pre-seeded: no reader re-run, no LLM
    return run_dir, rpr.load_yaml(run_dir / "pipeline_state.yaml")


def _routing_view(state: dict) -> dict:
    return {k: state.get(k) for k in ("status", "flags")} | {
        "pending_terminal": state.get("pending_stage") if state.get("status") != "paused_for_human" else None}


@pytest.mark.parametrize("idea_status,expected", [
    ("validated", "holdout_evaluation"), ("refuted", "completed_rejected"), ("inconclusive", None)])
def test_flag_off_specialist_readers_routes_directly(monkeypatch, idea_status, expected):
    run_dir, state = _loop_from_specialist_readers(monkeypatch, READERS_ON, idea_status)
    assert "regroup_record" not in (state.get("completed_stages") or [])
    if expected:
        assert state["completed_stages"][-1] == "specialist_readers"
        assert state["pending_stage"] == expected
    else:
        assert state["pending_stage"] == "specialist_readers"
        assert state["status"] == "paused_for_human"
    assert not (run_dir / "handoffs" / "specialist_readers_to_regroup_record.yaml").exists()
    assert not _memory_path().exists()
    assert not (rpr.ROOT / "campaign_record").exists() or \
        not any((rpr.ROOT / "campaign_record").iterdir())


# ---------------------------------------------------------------------------
# 3. Flag on: order, same route, memory before the route
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status", ["validated", "refuted", "inconclusive"])
def test_flag_on_same_route_after_regroup_record(monkeypatch, idea_status):
    _, off = _loop_from_specialist_readers(monkeypatch, READERS_ON, idea_status, run_id="run_981")
    seen = []
    real_route = rpr.determine_post_specialist_readers_route

    def _spy(path, run_id, **kw):
        # memory is written BEFORE the route is taken
        seen.append(run_id in (_memory()["runs"] if _memory_path().exists() else {}))
        return real_route(path, run_id, **kw)
    run_dir, on = _loop_from_specialist_readers(monkeypatch, ALL_ON, idea_status, spy=_spy)
    assert seen == [True]
    assert _routing_view(on) == _routing_view(off)
    if idea_status == "inconclusive":
        assert on["completed_stages"][-1] == "specialist_readers"
        assert on["pending_stage"] == "regroup_record"  # pause leaves the stage, like readers flag-off
        assert on["flags"] == {"inconclusive_grid": True}
        assert camp._classify_human_pause(run_dir, on) == "inconclusive_grid"
    else:
        assert on["completed_stages"][-2:] == ["specialist_readers", "regroup_record"]
        assert on["pending_stage"] == off["pending_stage"]
    assert (run_dir / "handoffs" / "specialist_readers_to_regroup_record.yaml").exists()
    assert _memory()["runs"][RUN_ID]["idea_status"] == idea_status


def test_full_loop_from_protocol_execution_stage_order(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _seed(pending="protocol_execution", idea_status="refuted")
    rpr._ensure_protocol_ref_pinned(run_dir, RUN_ID, {"protocol_ref": f"protocols/{RUN_ID}_pinned.json"})
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    for c in REPORT_CATEGORIES:  # let the readers run (mocked) this time
        (run_dir / "artifacts" / "proposals" / f"{c}.yaml").unlink()
    stages = []

    async def _record(stage_name, run_id, retry_context=None):
        stages.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert stages == ["protocol_execution"]  # regroup_record never goes through async_invoke_agent
    assert len(calls) == 5
    assert state["completed_stages"][-3:] == ["protocol_execution", "specialist_readers", "regroup_record"]
    assert state["pending_stage"] == "completed_rejected"
    entry = _memory()["runs"][RUN_ID]
    assert entry["idea_status"] == "refuted"
    assert [p["count"] for p in entry["proposals"]] == [0] * 5


def test_pending_regroup_record_with_flag_off_fails_loud(monkeypatch):
    _set_orchestrator(READERS_ON)
    run_dir = _seed(pending="regroup_record")
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "failed" and "regroup_record" in state["last_error"]
    assert state["pending_stage"] == "regroup_record"
    assert not _memory_path().exists()


def test_regroup_record_survives_the_loop_top_budget_check(monkeypatch):
    """Review fix 1: with the budget already spent by the readers, flag-off
    takes the route in the readers' own iteration; flag-on must not lose the
    memory entry and the route to the loop-top budget check."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted", pending="regroup_record")
    monkeypatch.setattr(rpr, "_load_token_budget", lambda: 1)
    monkeypatch.setattr(rpr, "_compute_weighted_budget_usage", lambda log: (10**9, []))
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert RUN_ID in _memory()["runs"]
    assert state["completed_stages"][-1] == "regroup_record"
    assert state["pending_stage"] == "completed_rejected"
    assert state["status"] == "rejected"


def test_budget_check_unchanged_for_other_stages(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted", pending="specialist_readers")
    monkeypatch.setattr(rpr, "_load_token_budget", lambda: 1)
    monkeypatch.setattr(rpr, "_compute_weighted_budget_usage", lambda log: (10**9, []))
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "rejected_budget_exceeded"
    assert state["pending_stage"] == "specialist_readers"
    assert not _memory_path().exists()


def test_preflight_skips_a_terminal_run():
    """Review fix 8: a finished run is not marked failed by a misconfigured flag."""
    _set_orchestrator({"grid_evaluation": {"enabled": True}, "category_reports": {"enabled": True},
                       "specialist_readers": {"enabled": True}, "regroup_record": {"enabled": "yes"}})
    run_dir = _seed(pending="completed_rejected")
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["status"] = "rejected"
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "rejected" and not state.get("last_error")
    assert state["pending_stage"] == "completed_rejected"


@pytest.mark.parametrize("errors_count", [None, 1])
def test_checks_computed_once_and_flag_resolved_once(monkeypatch, errors_count):
    """Review fix 9: no second flag check in the stage body; component errors and
    idea_status computed once per regroup_record iteration and handed to the route."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted", errors_count=errors_count)
    counts = {"flag": 0, "errors": 0, "idea": 0}

    def _count(name, key):
        real = getattr(rpr, name)

        def _wrapped(*a, **k):
            counts[key] += 1
            return real(*a, **k)
        monkeypatch.setattr(rpr, name, _wrapped)
    _count("_regroup_record_enabled", "flag")
    _count("_protocol_component_errors", "errors")
    _count("_load_idea_status", "idea")
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    if errors_count:
        assert state["status"] == "paused_for_human"
    else:
        assert state["completed_stages"][-1] == "regroup_record"
    assert counts == {"flag": 1, "errors": 1, "idea": 0 if errors_count else 1}


# ---------------------------------------------------------------------------
# 4. Memory entry content
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status", ["validated", "refuted", "inconclusive"])
def test_entry_flag_off_column_shape(idea_status):
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status=idea_status)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    doc = _memory()
    assert doc["schema_version"] == 1
    assert "campaign_knowledge_base.yaml" in doc["legacy_note"]
    e = doc["runs"][RUN_ID]
    assert e["run_id"] == RUN_ID and e["hypothesis_id"] == "H-MEM-1" and e["legacy"] is False
    assert e["idea_status"] == idea_status
    assert e["idea_status_reason"] == rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")["reason"]
    assert e["idea_status_ref"] == f"runs/{RUN_ID}/artifacts/idea_status.yaml"
    assert e["engineering_fault"] is None and e["engineering_fault_detail"] == []
    g = e["grid"]
    assert g["ref"] == f"runs/{RUN_ID}/artifacts/grid_evaluation.yaml"
    assert g["criteria"] == CRITERIA and g["variants"] == [RUN_ID]
    assert g["cells"]["ic_median"][RUN_ID]["threshold"] == 0.02
    expected_counts = {"validated": {"PASS": 2, "FAIL": 0, "INCONCLUSIVE": 0},
                       "refuted": {"PASS": 1, "FAIL": 1, "INCONCLUSIVE": 0},
                       "inconclusive": {"PASS": 1, "FAIL": 0, "INCONCLUSIVE": 1}}[idea_status]
    assert g["counts"] == expected_counts
    assert e["variants"] == {RUN_ID: {
        "status": "tested", "reason": None,
        "config_ref": f"runs/{RUN_ID}/artifacts/candidate_strategy_config.json",
        "forecast_hash": "fh-run",  # copied from the ledger row, not recomputed
        "symbols": ["BTCUSDT"], "n_windows": 2, "trial_id": RUN_ID}}
    assert e["trial_ids"] == [RUN_ID]  # backtest rows only; not the prescreen row, not run_9800
    assert e["protocol_ref"] == "protocols/p.json"
    assert e["timeframe"] == "1h"
    # E-058 S2b: a validated run without block_manifest.yaml registers nothing
    assert e["registry"] == ({"skipped": "no_manifest"} if idea_status == "validated"
                             else {"skipped": "not_validated"})
    assert e["profit_bars"] is None and e["profit_bars_reason"] == "not evaluated before regroup"
    assert e["kb_entry_id"] is None  # no KB file in the sandbox: skipped loudly (S2b)


def test_entry_variant_loop_shape():
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted", variant_loop=True)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    e = _memory()["runs"][RUN_ID]
    assert e["grid"]["variants"] == ["base", "design"]
    assert e["grid"]["cells"]["ic_median"]["design"]["result"] == "FAIL"
    v = e["variants"]
    assert set(v) == {"asset", "base", "broken", "design"}
    assert v["base"]["status"] == "tested" and v["base"]["trial_id"] == f"{RUN_ID}:base"
    assert v["base"]["forecast_hash"] == "fh-base" and v["design"]["forecast_hash"] == "fh-design"
    # review fix 3: 4 result rows (2 symbols x 2 windows) are 2 windows, not 4
    assert v["design"]["symbols"] == ["BTCUSDT", "ETHUSDT"] and v["design"]["n_windows"] == 2
    assert v["broken"]["status"] == "failed" and v["broken"]["trial_id"] == f"{RUN_ID}:broken"
    assert v["broken"]["forecast_hash"] == "fh-broken"
    assert v["asset"] == {"status": "not_tested", "reason": "patch application failed: /x",
                          "config_ref": None, "forecast_hash": None, "symbols": [], "n_windows": 0,
                          "trial_id": None}
    assert v["base"]["config_ref"] == f"runs/{RUN_ID}/artifacts/variants/base/strategy_config.json"
    assert e["trial_ids"] == [f"{RUN_ID}:base", f"{RUN_ID}:design", f"{RUN_ID}:broken"]


def test_config_direct_without_variant_loop_uses_the_single_column():
    """config_direct_authoring writes artifacts/variants/index.yaml, but with the
    variant loop off only the base config is backtested and the grid's one column
    is named after run_id -- the index must not be mistaken for loop columns."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="validated")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": {"status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"},
        "design": {"status": "validated", "config_path": "artifacts/variants/design/strategy_config.json"}}})
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    e = _memory()["runs"][RUN_ID]
    assert list(e["variants"]) == [RUN_ID]
    assert e["variants"][RUN_ID]["status"] == "tested" and e["variants"][RUN_ID]["trial_id"] == RUN_ID
    assert e["trial_ids"] == [RUN_ID]


@pytest.mark.parametrize("variant_loop", [False, True])
def test_component_error_run_recorded_as_engineering_fault(variant_loop):
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="validated", errors_count=2, variant_loop=variant_loop)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    e = _memory()["runs"][RUN_ID]
    # review fix 6: the minimal fault-only form, nothing else
    assert set(e) == {"run_id", "hypothesis_id", "legacy", "recorded_at", "engineering_fault",
                      "engineering_fault_detail"}
    assert e["run_id"] == RUN_ID and e["hypothesis_id"] == "H-MEM-1" and e["legacy"] is False
    assert e["engineering_fault"] == "component_execution_error"
    assert e["engineering_fault_detail"] and "component_errors.count=2" in e["engineering_fault_detail"][0]


def test_fault_entry_parses_no_grid_variant_or_proposal_artifact():
    """Review fix 6: broken grid / index / proposals / hypothesis card on a faulted
    run still record the fault (hypothesis_id null) and never parse those files."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="validated", errors_count=1, variant_loop=True)
    arts = run_dir / "artifacts"
    for rel in ("grid_evaluation.yaml", "idea_status.yaml", "variants/index.yaml",
                f"proposals/{REPORT_CATEGORIES[0]}.yaml", "hypothesis_card.yaml"):
        (arts / rel).write_text("{broken: [\n", encoding="utf-8")
    checks = rpr._run_regroup_record_stage(RUN_ID, run_dir)
    e = _memory()["runs"][RUN_ID]
    assert e["hypothesis_id"] is None and e["engineering_fault"] == "component_execution_error"
    assert checks["entry"] == e and checks["idea"] is None and checks["component_errors"]


def test_fault_entry_write_failure_still_pauses(monkeypatch):
    """Review fix 6: a memory write that fails on a faulted run is logged, and the
    component_execution_error pause still fires (no unhandled exception)."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="validated", errors_count=1)
    _memory_path().parent.mkdir(parents=True, exist_ok=True)
    _memory_path().write_text("runs: [unclosed\n", encoding="utf-8")  # malformed memory file
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert state["flags"] == {"component_execution_error_flagged": True}
    assert camp._classify_human_pause(run_dir, state) == "component_execution_error"
    assert _memory_path().read_text(encoding="utf-8") == "runs: [unclosed\n"


def test_component_error_run_pauses_after_recording(monkeypatch):
    run_dir, state = _loop_from_specialist_readers(monkeypatch, ALL_ON, "validated", errors_count=1)
    assert state["status"] == "paused_for_human"
    assert state["flags"] == {"component_execution_error_flagged": True}
    assert state["pending_stage"] == "regroup_record"
    assert camp._classify_human_pause(run_dir, state) == "component_execution_error"
    assert _memory()["runs"][RUN_ID]["engineering_fault"] == "component_execution_error"
    assert not (run_dir / "artifacts" / "promotion_audit.yaml").exists()


def test_missing_hypothesis_id_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed()
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", {"title": "no id"})
    with pytest.raises(cm.CampaignMemoryError, match="hypothesis_id"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not _memory_path().exists()


def test_grid_disagreeing_with_idea_status_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted")
    grid = rpr.load_yaml(run_dir / "artifacts" / "grid_evaluation.yaml")
    grid["idea_status"] = "validated"
    rpr.save_yaml(run_dir / "artifacts" / "grid_evaluation.yaml", grid)
    with pytest.raises(cm.CampaignMemoryError, match="disagrees"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)


def test_malformed_idea_status_fails_before_writing():
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted")
    doc = rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")
    doc["run_id"] = "run_001"
    rpr.save_yaml(run_dir / "artifacts" / "idea_status.yaml", doc)
    with pytest.raises(ValueError, match="stale"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not _memory_path().exists()


# ---------------------------------------------------------------------------
# 5. Replace on re-run; malformed file; atomic write
# ---------------------------------------------------------------------------

def test_rerun_replaces_entry_and_keeps_others():
    _set_orchestrator(ALL_ON)
    other = _seed(run_id="run_979", idea_status="validated")
    rpr._run_regroup_record_stage("run_979", other)
    run_dir = _seed(idea_status="refuted")
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    grid = _grid([RUN_ID], "inconclusive")
    rpr.save_yaml(run_dir / "artifacts" / "grid_evaluation.yaml", grid)
    rpr.save_yaml(run_dir / "artifacts" / "idea_status.yaml", rpr._build_idea_status_artifact(grid, RUN_ID))
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    doc = _memory()
    assert list(doc["runs"]) == ["run_979", RUN_ID]
    assert doc["runs"][RUN_ID]["idea_status"] == "inconclusive"
    assert doc["runs"]["run_979"]["idea_status"] == "validated"
    assert _memory_path().read_text(encoding="utf-8").count(f"run_id: {RUN_ID}") == 1


@pytest.mark.parametrize("content,match", [
    ("runs: [unclosed\n", "unparseable"),
    ("- a\n- b\n", "expected a mapping"),
    ("schema_version: 2\nruns: {}\n", "schema_version"),
    ("schema_version: 1\nruns: []\n", "runs is not a mapping"),
    ("schema_version: 1\nruns:\n  run_1: {run_id: run_2}\n", "keyed by its own run_id"),
])
def test_malformed_memory_file_fails_loud_and_is_not_overwritten(content, match):
    _set_orchestrator(ALL_ON)
    run_dir = _seed()
    _memory_path().parent.mkdir(parents=True, exist_ok=True)
    _memory_path().write_text(content, encoding="utf-8")
    with pytest.raises(cm.CampaignMemoryError, match=match):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert _memory_path().read_text(encoding="utf-8") == content


def test_atomic_write_leaves_previous_file_on_failure(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    before = _memory_path().read_bytes()

    def _boom(*a, **k):
        raise OSError("disk full")
    monkeypatch.setattr(cm.os, "replace", _boom)
    with pytest.raises(OSError, match="disk full"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert _memory_path().read_bytes() == before
    assert [p.name for p in _memory_path().parent.iterdir()] == ["campaign_memory.yaml"]


# ---------------------------------------------------------------------------
# 6. No trial rows
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variant_loop", [False, True])
@pytest.mark.parametrize("errors_count", [None, 1])
def test_trial_ledger_byte_identical_across_the_stage(variant_loop, errors_count):
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="validated", variant_loop=variant_loop, errors_count=errors_count)
    before = rpr.CAMPAIGN_STATE_PATH.read_bytes()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)  # a re-run too
    assert rpr.CAMPAIGN_STATE_PATH.read_bytes() == before


def test_absent_ledger_fails_loud_and_is_not_created():
    """A tested run with no ledger at all breaks the ledger invariant: fail
    loud, and never create (write) the ledger."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed()
    rpr.CAMPAIGN_STATE_PATH.unlink()
    with pytest.raises(cm.CampaignMemoryError, match="no 'backtest' row"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not rpr.CAMPAIGN_STATE_PATH.exists()
    assert not _memory_path().exists()


# ---------------------------------------------------------------------------
# 7. Proposals: referenced, never scored, never a decision input
# ---------------------------------------------------------------------------

def _all_keys(obj) -> set:
    if isinstance(obj, dict):
        return set(obj) | set().union(*(_all_keys(v) for v in obj.values()))
    if isinstance(obj, list):
        return set().union(*(_all_keys(v) for v in obj)) if obj else set()
    return set()


def test_proposals_referenced_by_id_and_count_only():
    _set_orchestrator(ALL_ON)
    run_dir = _seed(proposals=2)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    e = _memory()["runs"][RUN_ID]
    assert [p["category"] for p in e["proposals"]] == list(REPORT_CATEGORIES)
    first = e["proposals"][0]
    cat = REPORT_CATEGORIES[0]
    assert first == {"category": cat, "ref": f"runs/{RUN_ID}/artifacts/proposals/{cat}.yaml",
                     "proposal_ids": [f"{cat}-{RUN_ID}-1", f"{cat}-{RUN_ID}-2"], "count": 2}
    keys = _all_keys(e)
    assert not keys & {"scores", "confidence_real", "distance_to_profitable",
                       "mechanism_plausibility", "patch", "evidence"}


@pytest.mark.parametrize("idea_status", ["validated", "refuted", "inconclusive"])
def test_proposal_scores_change_nothing_but_the_reference(idea_status):
    _set_orchestrator(ALL_ON)
    entries = []
    for i, (n, score) in enumerate([(0, 0), (3, 0), (3, 3)]):
        run_id = f"run_97{i}"
        run_dir = _seed(run_id=run_id, idea_status=idea_status, proposals=n, score=score)
        reader_proposals.load_proposals(run_dir / "artifacts" / "proposals", REPORT_CATEGORIES)
        entries.append(rpr._run_regroup_record_stage(run_id, run_dir)["entry"])
    decided = [{k: e[k] for k in ("idea_status", "registry", "engineering_fault")} for e in entries]
    assert decided == [decided[0]] * 3
    assert decided[0]["idea_status"] == idea_status


def test_malformed_proposal_file_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed()
    (run_dir / "artifacts" / "proposals" / f"{REPORT_CATEGORIES[0]}.yaml").write_text(
        "{a: 1}\n", encoding="utf-8")
    with pytest.raises(reader_proposals.ProposalError):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not _memory_path().exists()


# ---------------------------------------------------------------------------
# 8. Retired machinery
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variant_loop", [False, True])
def test_entry_has_no_retired_field(variant_loop):
    _set_orchestrator(ALL_ON)
    run_dir = _seed(variant_loop=variant_loop)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    keys = _all_keys(_memory())
    assert not keys & {"hypothesis_family", "altitude", "altitude_history", "lineage_routing",
                       "hypothesis_verdict", "continuation_child", "failed_families"}


def test_upsert_refuses_a_retired_field():
    entry = {"run_id": "run_1", "grid": {"lineage_routing": "pivot"}}
    with pytest.raises(cm.CampaignMemoryError, match="retired"):
        cm.upsert_memory(_memory_path(), entry)
    assert not _memory_path().exists()


def test_stage_touches_no_retired_campaign_state_writer(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted")

    def _boom(*a, **k):
        raise AssertionError("retired / trial writer called from regroup_record")
    for name in ("update_campaign_state_after_run", "record_pivot", "record_escalation",
                 "_record_backtest_trial", "_record_failed_backtest_trial", "_save_campaign_state",
                 "_write_kb_findings_entry", "_auto_generate_findings_carryover",
                 "_apply_circuit_breaker", "determine_post_specialist_readers_route"):
        monkeypatch.setattr(rpr, name, _boom)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert RUN_ID in _memory()["runs"]


# ---------------------------------------------------------------------------
# 9. The written file matches workflow_artifacts/schemas/campaign_memory.schema.json
# ---------------------------------------------------------------------------

def test_written_file_matches_schema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" / "campaign_memory.schema.json")
                        .read_text(encoding="utf-8"))
    _set_orchestrator(ALL_ON)
    for i, (status, vl, err) in enumerate([("validated", False, None), ("refuted", True, None),
                                           ("inconclusive", False, None), ("validated", True, 1)]):
        run_id = f"run_96{i}"
        rpr._run_regroup_record_stage(run_id, _seed(run_id=run_id, idea_status=status,
                                                    variant_loop=vl, errors_count=err))
    doc = _memory()
    assert len(doc["runs"]) == 4
    jsonschema.validate(doc, schema)
    assert "idea_status" not in doc["runs"]["run_963"]  # the fault-only form
    bad = json.loads(json.dumps(doc))
    bad["runs"]["run_960"]["hypothesis_family"] = "x"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schema)
    bad = json.loads(json.dumps(doc))
    bad["runs"]["run_963"]["grid"] = None  # a fault entry may not grow full-entry fields
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schema)


def test_schema_is_applied_on_write(monkeypatch):
    """Review fix 10: the schema's $comment says validate_workflow_artifact applies
    it at write time -- prove it (raise mode blocks a schema-violating document)."""
    pytest.importorskip("jsonschema")
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    bad = {"run_id": "run_1", "hypothesis_id": "H", "legacy": True, "recorded_at": "t",
           "engineering_fault": "component_execution_error", "engineering_fault_detail": ["x"]}
    with pytest.raises(Exception, match="legacy|False|const"):
        cm.upsert_memory(_memory_path(), bad)
    assert not _memory_path().exists()
    good = dict(bad, legacy=False)
    cm.upsert_memory(_memory_path(), good)
    assert _memory()["runs"]["run_1"] == good


def test_non_string_timeframe_fails_loud():
    """Review fix 10: the writer type-checks timeframe like the schema does."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed()
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", {"hypothesis_id": "H-MEM-1", "timeframe": 60})
    with pytest.raises(cm.CampaignMemoryError, match="timeframe"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not _memory_path().exists()


# ---------------------------------------------------------------------------
# 10. Code-review fixes: ledger invariant, unknown variant states, lock, outcomes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variant_loop,missing", [(False, None), (True, "base")])
def test_tested_variant_without_trial_row_fails_loud(variant_loop, missing):
    """Review fix 4: a tested variant must have its 'backtest' ledger row."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted", variant_loop=variant_loop)
    tid = RUN_ID if missing is None else f"{RUN_ID}:{missing}"
    state = rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH)
    state["trial_sharpes"] = [r for r in state["trial_sharpes"]
                              if not (r["trial_id"] == tid and r["source"] == "backtest")]
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    with pytest.raises(cm.CampaignMemoryError, match="no 'backtest' row"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not _memory_path().exists()


def test_tested_variant_row_without_forecast_hash_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted")
    state = rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH)
    for r in state["trial_sharpes"]:
        if r["trial_id"] == RUN_ID and r["source"] == "backtest":
            r["forecast_hash"] = None
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    with pytest.raises(cm.CampaignMemoryError, match="forecast_hash"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)


@pytest.mark.parametrize("variant,entry,match", [
    ("asset", {"status": "declined"}, "status='declined'"),
    ("asset", "not_tested", "not a mapping"),
    ("asset", {"status": "not_tested", "surprise": 1}, "unknown key"),
    ("asset", {"status": "validated"}, "no config_path"),
    ("base", {"status": "not_tested", "reason": "x",
              "config_path": "artifacts/variants/base/strategy_config.json"}, "grid column 'base'"),
])
def test_unknown_variant_state_fails_loud(variant, entry, match):
    """Review fix 5: no silent defaults for an index status or entry shape."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed(idea_status="refuted", variant_loop=True)
    index_path = run_dir / "artifacts" / "variants" / "index.yaml"
    index = rpr.load_yaml(index_path)
    index["variants"][variant] = entry
    rpr.save_yaml(index_path, index)
    with pytest.raises(cm.CampaignMemoryError, match=match):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)


def test_two_interleaved_writers_lose_nothing(monkeypatch):
    """Review fix 7: writer B starts its read-modify-write while A is between its
    read and its write. With the lock, B waits and both entries survive."""
    import threading
    a_read, b_read = threading.Event(), threading.Event()
    real_load = cm.load_memory

    def _load(path):
        doc = real_load(path)
        if threading.current_thread().name == "A":
            a_read.set()
            b_read.wait(timeout=1.0)  # without a lock, B reads the same stale doc here
        else:
            b_read.set()
        return doc
    monkeypatch.setattr(cm, "load_memory", _load)
    errors = []

    def _writer(run_id):
        try:
            cm.upsert_memory(_memory_path(), {"run_id": run_id, "hypothesis_id": None, "legacy": False,
                                              "recorded_at": "t", "engineering_fault":
                                              "component_execution_error",
                                              "engineering_fault_detail": ["x"]})
        except Exception as exc:  # pragma: no cover - surfaced below
            errors.append(exc)
    a = threading.Thread(target=_writer, args=("run_a",), name="A")
    b = threading.Thread(target=_writer, args=("run_b",), name="B")
    a.start()
    assert a_read.wait(timeout=5)
    b.start()
    a.join(10)
    b.join(10)
    assert errors == []
    assert set(_memory()["runs"]) == {"run_a", "run_b"}
    assert not (_memory_path().parent / cm.MEMORY_LOCK_FILENAME).exists()


def test_lock_held_past_the_wait_fails_loud(monkeypatch):
    import campaign_lock
    monkeypatch.setattr(cm, "MEMORY_LOCK_WAIT_SECONDS", 0.2)
    lock = _memory_path().parent / cm.MEMORY_LOCK_FILENAME
    campaign_lock.acquire(lock)  # held by this (live) process
    try:
        with pytest.raises(cm.CampaignMemoryError, match="still held"):
            cm.upsert_memory(_memory_path(), {"run_id": "run_1", "hypothesis_id": None, "legacy": False,
                                              "recorded_at": "t",
                                              "engineering_fault": "component_execution_error",
                                              "engineering_fault_detail": ["x"]})
    finally:
        campaign_lock.release(lock)
    assert not _memory_path().exists()


def test_every_stage_name_is_a_non_verdict_outcome():
    """Review fix 2: a queue entry's outcome can be its run's pending stage; every
    STAGE_CONFIGS key must be admissible as a non-verdict outcome."""
    import verdict_criteria_evaluator as vce
    missing = sorted(set(rpr.STAGE_CONFIGS) - vce._NON_VERDICT_OUTCOMES)
    assert missing == []
    assert not vce.outcome_is_verdict_bearing("regroup_record")
    assert not vce.outcome_is_verdict_bearing("specialist_readers")
