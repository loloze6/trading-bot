"""
E-059 S3 / slice 6c S2c -- parked states under
orchestrator.verdict_routing_retired.enabled (off by default). Spec:
engineering/roadmap/E-059/S1_FINDINGS_6C.md §2, §6, §8 (S2c) and guesses 7, 8,
9, 12, 13 (operator decision 2026-09-25: guesses 2-13 on the S1 defaults).

All synthetic: no LLM, no backtest, no trial row, no holdout.
  1. What is parkable (guess 7): the V12 / data-gated classifier.
  2. The orchestrator sites set the marker (flag on) and stay the same pause
     (flag off): 1b component_gap, 5a V12, the per-variant and single data
     gate; a parked run restarted by hand refuses to start.
  3. process_once: a parked run marks its entry paused:waiting_for_<kind>,
     logs PARKED, writes a halt_history record, and decide-next runs; the loop
     is never blocked; flag off a pause stays a pause.
  4. --resume skips parked entries; --unpark refuses / restores.
  5. Quarantine interplay (guess 9).
  6. Drift: status, pause and outcome lists; decide-next's R2 view; the
     decision record schema; the RUNBOOK / HALT_RECOVERY rows.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import campaign_lock  # noqa: E402
import decide_next as dn  # noqa: E402
import record_schema as rs  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _save_queue_entries, _write_campaign_state, _write_fresh_scaffold, _entry,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_s2a_decide_next import _patch, _stage_flag_on_source  # noqa: E402
from test_e059_6c_s2a_route_retirement import FLAT_ON, RETIRED_ON  # noqa: E402
from test_e033_slice4a_variant_loop import _set_flag  # noqa: E402
from test_e033_slice4b_gate_conformance_promotion import (  # noqa: E402
    _minimal_run_at, _noop_invoke, _write_handoff)
from test_k3_protocol_pinning import _minimal_run  # noqa: E402

def _v12_line(cls="FooComponent", loc="strategies.regimes.trend.components[0]",
              module="strategies.strategy_components"):
    """validate_config.py's V12 line, with strategies/registry._load_class's own
    message for a class the module does not define."""
    path = f"{module}.{cls}"
    return (f"VIOLATION V12 {loc}.class: cannot load '{path}': Cannot load component class "
            f"'{path}': module '{module}' has no attribute '{cls}'")


V12 = _v12_line()
V12_B = _v12_line("BarComponent", "regime_detector.components[1]")
V12_NO_KEY = "VIOLATION V12 regime_detector.components[0]: missing required 'class' key"
V3 = "VIOLATION V3 strategies.regimes.trend: bad transform"
DATA = "data_availability_gate outcome=decline: no funding feed before 2021"
DATA_REFINE = "data_availability_gate outcome=refine: window 3 partially available"
FOO = "strategies.strategy_components.FooComponent"


def _write_component(tbot: Path, *names):
    """strategies/strategy_components.py defining ExistingComponent plus `names`
    (FooComponent when none is given)."""
    names = names or ("FooComponent",)
    path = tbot / "strategies" / "strategy_components.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(f"class {n}:\n    pass\n\n" for n in ("ExistingComponent", *names))
    path.write_text(body, encoding="utf-8")


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


@pytest.fixture(autouse=True)
def tbot(tmp_path, monkeypatch):
    """A trading-bot checkout whose component module defines only
    ExistingComponent (FooComponent / BarComponent are genuinely missing)."""
    root = tmp_path / "tbot_root"
    _write_component(root, "ExistingComponent")
    monkeypatch.setattr(rpr, "_TRADING_BOT_ROOT", root, raising=False)
    monkeypatch.setattr(camp, "_TRADING_BOT_ROOT", root)
    return root


def _gate_doc(outcome="decline", start="2021-01-01", end="2021-03-31", **window) -> dict:
    """A data_availability_gate.yaml whose one price window came back short
    from a real (Layer 2) fetch, no fetch error, outside the sealed range."""
    w = {"label": "w1", "symbol": "BTCUSDT", "start": start, "end": end, "layer": 2,
         "outcome": outcome, "missing_fraction": 0.4, "reason": "40.0% of expected bars missing",
         **window}
    return {"outcome": outcome, "reasons": [f"BTCUSDT w1: {w['reason']}"], "windows": [w],
            "aux_feeds": []}


def _write_variant_gate(run_dir: Path, vid: str, doc=None):
    rpr.save_yaml(run_dir / "artifacts" / "variants" / vid / "data_availability_gate.yaml",
                  doc or _gate_doc())


def _nt(reason, report=None):
    v = {"status": "not_tested", "reason": reason}
    if report is not None:
        v["report"] = report
    return v


def _v12(report=V12):
    return _nt("validate_config.py violations", report)


def _ok():
    return {"status": "validated", "config_path": "variants/x/strategy_config.json"}


def _state(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))


def _write_cfg(root: Path, flat: dict | None, quarantine=None):
    orch = {name: {"enabled": v} for name, v in (flat or {}).items()}
    if quarantine is not None:
        orch["halt_policy"] = {"quarantine_enabled": quarantine}
    (root / "config").mkdir(exist_ok=True)
    (root / "config" / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": orch}), encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. What is parkable (guess 7)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variants,expected", [
    ({"a": _v12(), "b": _v12(V12_B)}, ("component", [FOO, "strategies.strategy_components.BarComponent"])),
    ({"a": _ok(), "b": _nt(DATA), "c": _nt(DATA)}, ("data", [])),
    ({"a": _ok(), "b": _nt(DATA), "c": _nt(DATA_REFINE)}, (None, [])),  # a refine never parks
    ({"a": _nt(DATA), "b": _v12()}, ("component", [FOO])),  # a mix parks as component
    ({"a": _v12(V12 + "\n" + V3)}, (None, [])),               # another V-code: design error
    ({"a": _v12(V12_NO_KEY)}, (None, [])),                     # missing 'class' key: design error
    ({"a": _v12("Traceback (most recent call last):\nboom")}, (None, [])),
    ({"a": _v12(), "b": _nt("patch application failed: bad pointer")}, (None, [])),
    ({"a": _nt(DATA), "b": _nt("manifest paths unresolved: ['/x']")}, (None, [])),
    ({"a": _nt(DATA), "b": _nt("data_availability_gate.py crashed (exit 1): x")}, (None, [])),
    ({"a": _nt(DATA), "b": _nt("data_availability_gate outcome=unknown: ")}, (None, [])),
    ({"a": _ok(), "b": _ok()}, (None, [])),                    # nothing waits
    ({}, (None, [])),
])
def test_variant_park_kind(variants, expected):
    run_dir = _minimal_run(rpr.ROOT, "run_949")
    for vid in variants:
        _write_variant_gate(run_dir, vid)
    kind, classes = rpr._variant_park_kind(variants, run_dir / "artifacts")
    assert (kind, sorted(classes)) == (expected[0], sorted(expected[1]))


def test_v12_missing_classes_needs_every_line_to_be_a_cannot_load():
    assert rpr._v12_missing_classes(V12 + "\n\n" + V12) == [FOO]
    assert rpr._v12_missing_classes(V12 + "\n" + V3) == []
    assert rpr._v12_missing_classes("") == [] and rpr._v12_missing_classes(None) == []


# ---------------------------------------------------------------------------
# 2. The orchestrator sites
# ---------------------------------------------------------------------------

def _gap_run(run_id="run_950") -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", {
        "hypothesis_id": "H-1", "stage": "strategy_config_authoring", "status": "component_gap",
        "rationale": "needs FooComponent, which does not exist",
        "blocking_issues": ["engine lacks FooComponent"]})
    return run_dir


def test_1b_component_gap_parks_under_the_flag():
    run_dir = _gap_run()
    assert rpr.determine_post_strategy_config_authoring_route(run_dir, routing_retired=True) == \
        "human_pause"
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and state["flags"] == {}  # no sticky flag
    marker = state[rpr.PARKED_KEY]
    assert marker["kind"] == "component" and marker["stage"] == "strategy_config_authoring"
    assert marker["resume_stage"] == "strategy_config_authoring" and marker["classes"] == []
    assert marker["request_refs"] == ["runs/run_950/artifacts/decision.yaml",
                                      "campaign_record/component_requests.yaml"]
    reqs = yaml.safe_load((rpr.ROOT / "campaign_record" / "component_requests.yaml")
                          .read_text(encoding="utf-8"))["requests"]
    assert reqs == [{"run_id": "run_950", "stage": "strategy_config_authoring", "variant_id": None,
                     "reason": "needs FooComponent, which does not exist",
                     "blocking_issues": ["engine lacks FooComponent"]}]
    # the same gap on the same run again (after an unpark) is not appended twice
    rpr.determine_post_strategy_config_authoring_route(run_dir, routing_retired=True)
    assert len(yaml.safe_load((rpr.ROOT / "campaign_record" / "component_requests.yaml")
                              .read_text(encoding="utf-8"))["requests"]) == 1


def test_1b_component_gap_flag_off_is_the_same_pause():
    run_dir = _gap_run()
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and rpr.PARKED_KEY not in state
    assert not (rpr.ROOT / "campaign_record" / "component_requests.yaml").exists()


def _index_run(variants: dict, run_id="run_951") -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": variants})
    return run_dir


@pytest.mark.parametrize("variant_loop,variants", [
    (True, {"base": _v12(), "design_v2": _v12(V12_B)}),
    # variant loop off: only `base` blocks; a sibling's patch failure is irrelevant
    (False, {"base": _v12(), "design_v2": _nt("patch application failed: x")}),
])
def test_5a_v12_only_parks_as_component(variant_loop, variants):
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True},
                         "variant_loop": {"enabled": variant_loop}})
    run_dir = _index_run(variants)
    assert rpr._route_post_config_direct_backtest_specification(run_dir, routing_retired=True) == \
        "human_pause"
    marker = _state(run_dir)[rpr.PARKED_KEY]
    assert marker["kind"] == "component" and marker["stage"] == "backtest_specification"
    assert marker["resume_stage"] == "backtest_specification" and FOO in marker["classes"]
    assert "campaign_record/component_requests.yaml" in marker["request_refs"]


@pytest.mark.parametrize("routing_retired,variants", [
    (True, {"base": _v12(), "design_v2": _nt("patch application failed: x")}),  # design error
    (True, {"base": _v12(V12 + "\n" + V3), "design_v2": _v12()}),
    (False, {"base": _v12(), "design_v2": _v12()}),                                 # flag off
])
def test_5a_other_failures_stay_the_pause(routing_retired, variants):
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True},
                         "variant_loop": {"enabled": True}})
    run_dir = _index_run(variants)
    kw = {"routing_retired": True} if routing_retired else {}
    assert rpr._route_post_config_direct_backtest_specification(run_dir, **kw) == "human_pause"
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and rpr.PARKED_KEY not in state


def test_5a_with_a_validated_variant_is_not_parked():
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True},
                         "variant_loop": {"enabled": True}})
    run_dir = _index_run({"base": _ok(), "design_v2": _v12()})
    assert rpr._route_post_config_direct_backtest_specification(run_dir, routing_retired=True) != \
        "human_pause"
    assert rpr.PARKED_KEY not in _state(run_dir)


def _gate_run(monkeypatch, run_id, variant_loop: bool, retired=True) -> Path:
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    monkeypatch.setattr(rpr, "_check_specialist_readers_preflight", lambda run_dir: None)
    cfg = {**(RETIRED_ON if retired else {}), "config_direct_authoring": {"enabled": True},
           "variant_loop": {"enabled": variant_loop}}
    if not retired:
        cfg = {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": variant_loop}}
    _set_flag(rpr.ROOT, cfg)
    run_dir = _minimal_run_at(rpr.ROOT, run_id, "data_availability_gate")
    _write_handoff(run_dir, "backtest_spec_to_data_availability_gate.yaml")
    return run_dir


def test_variant_data_gate_shortfall_parks_as_data(monkeypatch):
    run_dir = _gate_run(monkeypatch, "run_952", variant_loop=True)
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": _ok(), "design_v2": _nt(DATA), "asset_v2": _nt(DATA)}})
    _write_variant_gate(run_dir, "design_v2")
    _write_variant_gate(run_dir, "asset_v2")
    rpr.run_loop("run_952")
    state = _state(run_dir)
    assert state["status"] == "paused_for_human"
    assert state["pending_stage"] == "data_availability_gate"
    assert "variant_gate_insufficient" not in (state.get("flags") or {})
    marker = state[rpr.PARKED_KEY]
    assert marker["kind"] == "data" and marker["resume_stage"] == "backtest_specification"
    assert marker["request_refs"] == ["campaign_record/data_requests.yaml",
                                      "runs/run_952/artifacts/variants/index.yaml"]


def test_variant_data_gate_mix_with_v12_parks_as_component(monkeypatch):
    run_dir = _gate_run(monkeypatch, "run_953", variant_loop=True)
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": _ok(), "design_v2": _nt(DATA), "asset_v2": _v12()}})
    _write_variant_gate(run_dir, "design_v2")
    rpr.run_loop("run_953")
    marker = _state(run_dir)[rpr.PARKED_KEY]
    assert marker["kind"] == "component" and marker["classes"] == [FOO]
    assert marker["request_refs"][0] == "campaign_record/component_requests.yaml"


@pytest.mark.parametrize("retired", [True, False])
def test_variant_data_gate_crash_or_flag_off_stays_the_pause(monkeypatch, retired):
    run_dir = _gate_run(monkeypatch, "run_954", variant_loop=True, retired=retired)
    bad = (_nt("data_availability_gate.py crashed (exit 1): boom") if retired else _nt(DATA))
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": _ok(), "design_v2": _nt(DATA), "asset_v2": bad}})
    _write_variant_gate(run_dir, "design_v2")
    _write_variant_gate(run_dir, "asset_v2")
    rpr.run_loop("run_954")
    state = _state(run_dir)
    assert state["status"] == "paused_for_human"
    assert state["flags"]["variant_gate_insufficient"] is True
    assert rpr.PARKED_KEY not in state


@pytest.mark.parametrize("outcome", ["decline"])
def test_single_data_gate_fetchable_decline_parks(monkeypatch, outcome):
    run_dir = _gate_run(monkeypatch, "run_955", variant_loop=False)
    doc = _gate_doc(outcome)
    doc["reasons"] = ["no funding feed before 2021"]
    rpr.save_yaml(run_dir / "artifacts" / "data_availability_gate.yaml", doc)
    rpr.run_loop("run_955")
    state = _state(run_dir)
    assert state["status"] == "paused_for_human"
    assert state["pending_stage"] == "data_availability_gate"  # never completed_rejected
    marker = state[rpr.PARKED_KEY]
    assert marker["kind"] == "data" and marker["resume_stage"] == "data_availability_gate"
    reqs = yaml.safe_load((rpr.ROOT / "campaign_record" / "data_requests.yaml")
                          .read_text(encoding="utf-8"))["requests"]
    assert reqs == [{"run_id": "run_955", "stage": "data_availability_gate", "variant_id": None,
                     "outcome": outcome,
                     "reason": f"data_availability_gate outcome={outcome}: no funding feed before 2021",
                     "reasons": ["no funding feed before 2021"]}]


@pytest.mark.parametrize("outcome,pending", [("decline", "completed_rejected"),
                                             ("refine", "data_availability_gate")])
def test_single_data_gate_flag_off_is_unchanged(monkeypatch, outcome, pending):
    run_dir = _gate_run(monkeypatch, "run_956", variant_loop=False, retired=False)
    rpr.save_yaml(run_dir / "artifacts" / "data_availability_gate.yaml",
                  {"outcome": outcome, "reasons": ["x"]})
    rpr.run_loop("run_956")
    state = _state(run_dir)
    assert state["pending_stage"] == pending and rpr.PARKED_KEY not in state
    assert not (rpr.ROOT / "campaign_record" / "data_requests.yaml").exists()


def test_a_parked_run_restarted_by_hand_refuses_to_start(monkeypatch):
    run_dir = _gate_run(monkeypatch, "run_957", variant_loop=False)
    rpr.save_yaml(run_dir / "artifacts" / "data_availability_gate.yaml",
                  {"outcome": "validate", "reasons": []})
    rpr.update_state(path=run_dir, status="active",
                     **{rpr.PARKED_KEY: {"kind": "data", "stage": "data_availability_gate"}})
    ran = []
    monkeypatch.setattr(rpr, "async_invoke_agent", lambda *a, **k: ran.append(a))
    rpr.run_loop("run_957")
    state = _state(run_dir)
    assert ran == []
    assert state["status"] == "failed" and "--unpark" in state["last_error"]
    assert state["pending_stage"] == "data_availability_gate"


# ---------------------------------------------------------------------------
# 3. process_once
# ---------------------------------------------------------------------------

def _stage_park_queue(campaign_root, *, extra=(), cfg=FLAT_ON, quarantine=None):
    """run_061: a finished refuted run with one reader proposal (decide-next's
    source). PARK_ME (run_062) is in progress at step 1b."""
    root = campaign_root["root"]
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    _write_cfg(root, cfg, quarantine)
    done = {**_entry("run_061"), "status": "done", "outcome": "refuted",
            "pass_rule_evaluation_ref": "runs/run_061/artifacts/idea_status.yaml"}
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_062", status="active",
                          pending_stage="strategy_config_authoring")
    park_me = {**_entry("run_062", "PARK_ME"), "priority": 5}
    _save_queue_entries(campaign_root["queue_path"], [done, park_me, *extra])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_061"], trial_sharpes=[])


def _parking_run_loop(campaign_root, kind="component", ran=None):
    def _run_loop(run_id):
        if ran is not None:
            ran.append(run_id)
        run_dir = campaign_root["runs_dir"] / run_id
        rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", {
            "hypothesis_id": "H-1", "stage": "strategy_config_authoring",
            "status": "component_gap", "rationale": "needs FooComponent"})
        if kind == "component":
            rpr.determine_post_strategy_config_authoring_route(run_dir, routing_retired=True)
        else:
            rpr._park_run(run_dir, kind="data", stage="data_availability_gate",
                          reason="data_availability_gate outcome=decline: x",
                          request_refs=["campaign_record/data_requests.yaml"],
                          resume_stage="data_availability_gate")
    return _run_loop


def _queue(campaign_root) -> list:
    return yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]


def test_park_marks_the_entry_logs_and_calls_decide_next(campaign_root, monkeypatch):
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")  # the decision record's schema
    _stage_park_queue(campaign_root)
    monkeypatch.setattr(rpr, "run_loop", _parking_run_loop(campaign_root))
    root = campaign_root["root"]

    assert camp.process_once() is True  # the park never stops the loop

    queue = _queue(campaign_root)
    parked = next(e for e in queue if e["id"] == "PARK_ME")
    assert parked["status"] == "paused:waiting_for_component"
    assert parked["parked_reason"].startswith(
        "waiting_for_component at strategy_config_authoring: component_gap: needs FooComponent")
    assert parked.get("outcome") is None and parked["priority"] == 5
    # decide-next ran after the park and minted the source run's proposal
    new = next(e for e in queue if e["id"] == "profitability-run_061-1")
    assert new["status"] == "ready"
    ref = "runs/run_062/artifacts/parked/park_1/decision_record.yaml"
    assert new["decision_ref"] == ref
    record = yaml.safe_load((root / ref).read_text(encoding="utf-8"))
    assert record["trigger"] == {"after_run": "run_062", "after_entry": "PARK_ME",
                                 "idea_status": None, "parked": "component"}
    assert record["picked"]["candidate_id"] == "profitability-run_061-1"
    assert not (root / "runs" / "run_062" / "artifacts" / "decision_record.yaml").exists()
    state = _state(root / "runs" / "run_062")
    assert state["halt_history"][-1]["reason"] == "waiting_for_component"
    assert state["halt_history"][-1]["parked"]["kind"] == "component"
    log = (root / "campaign_log.md").read_text(encoding="utf-8")
    assert "PARKED PARK_ME / run_062: component at strategy_config_authoring" in log
    assert "--unpark PARK_ME" in log and "HALT" not in log
    assert log.index("PARKED PARK_ME") < log.index("DECIDE after PARK_ME (run_062)")
    summary = (root / "campaign_summary.md").read_text(encoding="utf-8")
    assert "## Parked" in summary and "campaign_record/component_requests.yaml" in summary
    health = yaml.safe_load((root / "campaign_record" / "loop_health.yaml").read_text(encoding="utf-8"))
    assert health["outcomes"]["parked"] == 1 and health["outcomes"]["escalated"] == 0
    assert health["halts"]["total"] == 0
    # no trial row, no child run
    assert yaml.safe_load(campaign_root["campaign_state_path"].read_text(encoding="utf-8"))[
        "trial_sharpes"] == []
    assert "continuation_child" not in state
    # the parked entry is never selected again by the scheduler
    assert camp._select_entry(queue)["id"] == "profitability-run_061-1"


def test_a_parked_run_never_blocks_the_next_one(campaign_root, monkeypatch):
    other = {**_entry("run_063", "OTHER"), "status": "ready", "priority": 7}
    _stage_park_queue(campaign_root, extra=[other])
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_063", status="active",
                          pending_stage="hypothesis_generation")
    ran = []
    monkeypatch.setattr(rpr, "run_loop", _parking_run_loop(campaign_root, kind="data", ran=ran))
    assert camp.process_once() is True
    queue = _queue(campaign_root)
    assert next(e for e in queue if e["id"] == "PARK_ME")["status"] == "paused:waiting_for_data"
    # decide-next saw OTHER scheduled next (nothing minted)
    record = yaml.safe_load((campaign_root["root"] / "runs" / "run_062" / "artifacts" / "parked" /
                             "park_1" / "decision_record.yaml").read_text(encoding="utf-8"))
    picked = record["picked"]
    assert (picked.get("operator_entry") or picked.get("queue_entry_id")) == "OTHER"
    assert "candidate_id" not in picked
    assert [e["id"] for e in queue] == ["TEST_ENTRY", "PARK_ME", "OTHER"]

    class _Stop(Exception):
        pass

    def _record(run_id):
        ran.append(run_id)
        raise _Stop
    monkeypatch.setattr(rpr, "run_loop", _record)
    with pytest.raises(_Stop):
        camp.process_once()
    assert ran == ["run_062", "run_063"]  # the next step runs OTHER, not the parked run


def test_stop_lines_name_the_parked_entries(campaign_root, monkeypatch):
    _stage_park_queue(campaign_root)
    queue = _queue(campaign_root)
    queue[1]["status"] = "paused:waiting_for_data"
    _save_queue_entries(campaign_root["queue_path"], queue)
    assert camp.process_once() is False
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert ("Queue exhausted — no ready or in_progress entries remain. Parked, waiting for a "
            "component or data: ['PARK_ME']") in log
    assert "queue_exhausted_with_open_briefs" in log


def test_flag_off_a_pause_stays_a_pause(campaign_root, monkeypatch):
    """Flag off: the same 1b component_gap is the classic HALT, byte for byte --
    also when a parked marker is left on the run (flag switched off since)."""
    results = []
    for marker in (None, {"kind": "component", "stage": "strategy_config_authoring"}):
        for p in campaign_root["runs_dir"].iterdir():
            import shutil
            shutil.rmtree(p)
        _write_cfg(campaign_root["root"], {})
        run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_062", status="active",
                                        pending_stage="strategy_config_authoring")
        _save_queue_entries(campaign_root["queue_path"], [_entry("run_062", "PARK_ME")])
        _write_campaign_state(campaign_root["campaign_state_path"], runs=[], trial_sharpes=[])
        (campaign_root["root"] / "campaign_log.md").unlink(missing_ok=True)

        def _pause(run_id, marker=marker):
            rd = campaign_root["runs_dir"] / run_id
            rpr.save_yaml(rd / "artifacts" / "decision.yaml",
                          {"hypothesis_id": "H-1", "stage": "strategy_config_authoring",
                           "status": "component_gap", "rationale": "needs FooComponent"})
            assert rpr.determine_post_strategy_config_authoring_route(rd) == "human_pause"
            if marker:
                rpr.update_state(path=rd, **{rpr.PARKED_KEY: marker})
        monkeypatch.setattr(rpr, "run_loop", _pause)
        assert camp.process_once() is False
        entry = _queue(campaign_root)[0]
        log = re.sub(r"^- \S+Z ", "- ", (campaign_root["root"] / "campaign_log.md")
                     .read_text(encoding="utf-8"), flags=re.M)
        results.append((entry, log))
        assert entry["status"] == "paused:component_gap" and "parked_reason" not in entry
        assert "HALT — component_gap" in log and "PARKED" not in log
        assert "parked" not in _state(run_dir)["halt_history"][-1]
    assert results[0] == results[1]


# ---------------------------------------------------------------------------
# 4. --resume and --unpark
# ---------------------------------------------------------------------------

def _parked_entry(campaign_root, classes=(FOO,), kind="component"):
    """PARK_ME parked the way process_once leaves it."""
    _stage_park_queue(campaign_root)

    def _run_loop(run_id):
        rpr._park_run(campaign_root["runs_dir"] / run_id, kind=kind, stage="backtest_specification",
                      reason="no variant passed validation", request_refs=[],
                      resume_stage="backtest_specification", classes=list(classes))
    import unittest.mock as um
    with um.patch.object(rpr, "run_loop", _run_loop):
        assert camp.process_once() is True
    return campaign_root["runs_dir"] / "run_062"


def test_resume_skips_parked_entries(campaign_root):
    _parked_entry(campaign_root)
    queue = _queue(campaign_root)
    # a real pause listed AFTER the parked entry, already resolved on disk
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_064", status="active",
                          pending_stage="protocol_execution")
    queue.append({**_entry("run_064", "REAL"), "status": "paused:component_execution_error"})
    _save_queue_entries(campaign_root["queue_path"], queue)
    assert camp.resume_paused_entry(camp._load_queue()) is True
    queue = _queue(campaign_root)
    assert next(e for e in queue if e["id"] == "REAL")["status"] == "in_progress"
    assert next(e for e in queue if e["id"] == "PARK_ME")["status"] == "paused:waiting_for_component"


def test_resume_with_only_parked_entries_resumes_nothing(campaign_root, capsys):
    _parked_entry(campaign_root)
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert "--unpark" in capsys.readouterr().out
    assert next(e for e in _queue(campaign_root) if e["id"] == "PARK_ME")["status"] == \
        "paused:waiting_for_component"


def test_unpark_restores_the_entry_and_the_same_run_continues(campaign_root, monkeypatch, tbot):
    run_dir = _parked_entry(campaign_root)
    # the class is still missing: refused, nothing changes
    before = campaign_root["queue_path"].read_text(encoding="utf-8")
    assert camp._unpark_entry("PARK_ME") is False
    assert campaign_root["queue_path"].read_text(encoding="utf-8") == before
    assert _state(run_dir)[rpr.PARKED_KEY]["kind"] == "component"

    _write_component(tbot)
    assert camp._unpark_entry("PARK_ME") is True
    entry = next(e for e in _queue(campaign_root) if e["id"] == "PARK_ME")
    assert entry["status"] == "ready" and entry["priority"] == 5
    assert "parked_reason" not in entry and entry["run_ids"] == ["run_062"]
    state = _state(run_dir)
    assert state[rpr.PARKED_KEY] is None
    assert state["status"] == "active" and state["pending_stage"] == "backtest_specification"
    assert "UNPARK PARK_ME / run_062" in (campaign_root["root"] / "campaign_log.md").read_text(
        encoding="utf-8")
    assert not campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH).exists()  # released

    # the next step continues the SAME run from its parking stage (the minted
    # candidate is set aside so the scheduler reaches PARK_ME)
    queue = _queue(campaign_root)
    for e in queue:
        if e["id"] == "profitability-run_061-1":
            e["status"] = "superseded"
    _save_queue_entries(campaign_root["queue_path"], queue)
    seen = []
    monkeypatch.setattr(rpr, "run_loop",
                        lambda run_id: seen.append((run_id, _state(run_dir)["pending_stage"])))
    camp.process_once()
    assert seen == [("run_062", "backtest_specification")]


def test_unpark_data_park_needs_no_class_check(campaign_root):
    run_dir = _parked_entry(campaign_root, classes=(), kind="data")
    assert camp._unpark_entry("PARK_ME") is True
    assert _state(run_dir)["status"] == "active"


@pytest.mark.parametrize("damage", ["not_parked", "unknown_id", "marker_missing", "kind_mismatch",
                                    "run_not_paused"])
def test_unpark_refusals(campaign_root, tbot, damage):
    run_dir = _parked_entry(campaign_root)
    _write_component(tbot)
    queue = _queue(campaign_root)
    entry_id = "PARK_ME"
    if damage == "not_parked":
        queue[1]["status"] = "paused:component_execution_error"
    elif damage == "unknown_id":
        entry_id = "NOPE"
    elif damage == "marker_missing":
        rpr.update_state(path=run_dir, **{rpr.PARKED_KEY: None})
    elif damage == "kind_mismatch":
        queue[1]["status"] = "paused:waiting_for_data"
    else:
        rpr.update_state(path=run_dir, status="active")
    _save_queue_entries(campaign_root["queue_path"], queue)
    before = campaign_root["queue_path"].read_text(encoding="utf-8")
    assert camp._unpark_entry(entry_id) is False
    assert campaign_root["queue_path"].read_text(encoding="utf-8") == before


def test_unpark_refused_while_the_campaign_lock_is_held(campaign_root, tbot):
    run_dir = _parked_entry(campaign_root)
    _write_component(tbot)
    lock = campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH)
    campaign_lock.acquire(lock)
    try:
        assert camp._unpark_entry("PARK_ME") is False
        assert lock.exists()  # never released on someone else's behalf
    finally:
        campaign_lock.release(lock)
    assert _state(run_dir)[rpr.PARKED_KEY]["kind"] == "component"
    assert next(e for e in _queue(campaign_root) if e["id"] == "PARK_ME")["status"] == \
        "paused:waiting_for_component"


def test_component_class_status_reads_source_without_importing(tmp_path):
    _write_component(tmp_path)
    assert dn.component_class_status(tmp_path, FOO) == "defined"
    assert dn.component_class_status(tmp_path, "strategies.strategy_components.Missing") == "missing"
    assert dn.component_class_status(tmp_path, "strategies.nowhere.FooComponent") == "invalid"
    assert dn.component_class_status(tmp_path, "FooComponent") == "invalid"
    assert dn.component_class_status(tmp_path / "absent", FOO) == "invalid"


def test_cli_exposes_unpark():
    src = (_SR / "workflow" / "run_campaign.py").read_text(encoding="utf-8")
    assert 'parser.add_argument("--unpark"' in src
    assert "_unpark_entry(args.unpark)" in src and "unpark=" not in src


# ---------------------------------------------------------------------------
# 5. Quarantine interplay (guess 9)
# ---------------------------------------------------------------------------

def test_park_supersedes_quarantine_under_the_flag(campaign_root, monkeypatch):
    _stage_park_queue(campaign_root, quarantine=True)
    monkeypatch.setattr(rpr, "run_loop", _parking_run_loop(campaign_root))
    assert camp.process_once() is True
    entry = next(e for e in _queue(campaign_root) if e["id"] == "PARK_ME")
    assert entry["status"] == "paused:waiting_for_component"  # not blocked_on_component
    state = _state(campaign_root["runs_dir"] / "run_062")
    assert "quarantine" not in state["halt_history"][-1]
    assert "QUARANTINE" not in (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")


def test_flag_off_quarantine_is_unchanged(campaign_root, monkeypatch):
    _write_cfg(campaign_root["root"], {}, quarantine=True)
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_062", status="active",
                          pending_stage="strategy_config_authoring")
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_062", "PARK_ME")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[], trial_sharpes=[])

    def _pause(run_id):
        rd = campaign_root["runs_dir"] / run_id
        rpr.save_yaml(rd / "artifacts" / "decision.yaml",
                      {"hypothesis_id": "H-1", "stage": "strategy_config_authoring",
                           "status": "component_gap", "rationale": "needs FooComponent"})
        rpr.determine_post_strategy_config_authoring_route(rd)
    monkeypatch.setattr(rpr, "run_loop", _pause)
    assert camp.process_once() is True
    assert _queue(campaign_root)[0]["status"] == "blocked_on_component:FooComponent"


# ---------------------------------------------------------------------------
# 6. Drift: status, pause and outcome lists; docs
# ---------------------------------------------------------------------------

def test_parked_statuses_are_valid_queue_statuses():
    assert rpr.PARK_KINDS == ("component", "data")
    assert camp.PARKED_STATUSES == ("paused:waiting_for_component", "paused:waiting_for_data")
    for status in camp.PARKED_STATUSES:
        assert rs._QUEUE_STATUS_RE.match(status)
        rs.validate_queue_entry({"id": "x", "status": status,
                                 "parked_reason": "waiting_for_data at data_availability_gate: y"})
        assert status.startswith(camp.PARKED_STATUS_PREFIX)
        assert camp._blocker_of(status) == status[len("paused:"):]
        assert camp._select_entry([{"id": "x", "status": status}]) is None


def test_parking_is_not_a_pause_reason_nor_an_outcome():
    reasons = {f"waiting_for_{k}" for k in rpr.PARK_KINDS}
    assert not reasons & {r for _, r in camp._PAUSE_FLAG_TO_REASON}
    assert not reasons & set(camp._QUARANTINE_SAFE_REASONS)
    assert not reasons & set(vce._NON_VERDICT_OUTCOMES)
    # the classifier never reads the marker (no sticky flag, no pause row)
    state = {"flags": {}, rpr.PARKED_KEY: {"kind": "data"}}
    assert camp._classify_human_pause(Path("nonexistent"), state) == "human_pause_unclassified"
    # a parked entry carries no outcome and clears the provenance gate
    vce.validate_verdict_provenance({"id": "x", "status": "paused:waiting_for_data",
                                     "parked_reason": "waiting_for_data at g: r"},
                                    schema=rs.QUEUE_ENTRY_SCHEMA)


def test_decide_next_treats_a_parked_request_as_empty_and_a_parked_owner_as_eligible():
    assert dn.PARKED_STATUS_PREFIX == camp.PARKED_STATUS_PREFIX
    assert dn.r2_request_yielded({"status": "paused:waiting_for_component"}) is False
    assert dn.r2_request_yielded({"status": "paused:waiting_for_data"}) is False
    assert dn.r2_request_yielded({"status": "paused:component_execution_error"}) is False
    assert dn.r2_eligible_owner({"brief_status": dn.BRIEF_OPEN,
                                 "status": "paused:waiting_for_data"})
    assert not dn.r2_eligible_owner({"brief_status": dn.BRIEF_OPEN,
                                     "status": "paused:component_execution_error"})


def test_decision_record_schema_admits_exactly_the_park_kinds():
    import json
    schema = json.loads((_SR / "workflow_artifacts" / "schemas" / "decision_record.schema.json")
                        .read_text(encoding="utf-8"))
    trigger = schema["properties"]["trigger"]
    assert trigger["additionalProperties"] is False
    assert tuple(trigger["properties"]["parked"]["enum"]) == rpr.PARK_KINDS
    assert "parked" not in trigger["required"]


def test_runbook_rows_and_procedure_exist():
    runbook = (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert "| `paused:waiting_for_component` / `paused:waiting_for_data`" in runbook
    assert f"| `{camp.QUEUE_EXHAUSTED_WITH_OPEN_BRIEFS}` (not a pause)" in runbook
    assert "### Parked entries — `--unpark` (slice 6c S2c)" in runbook
    assert "workflow/run_campaign.py --unpark <entry_id>" in runbook
    # guess 13: the row names decide-next's stop reason verbatim
    reason = re.search(r'stop = \{"reason": "(\w+)"',
                       (_SR / "tools" / "decide_next.py").read_text(encoding="utf-8")).group(1)
    row = next(ln for ln in runbook.splitlines()
               if ln.startswith(f"| `{camp.QUEUE_EXHAUSTED_WITH_OPEN_BRIEFS}`"))
    assert reason == "no_eligible_candidate" and reason in row
    assert "Queue exhausted — no ready or in_progress entries remain." in row
    halt = (_SR / "docs" / "HALT_RECOVERY.md").read_text(encoding="utf-8")
    assert "## 4b. Parked runs (E-059 slice 6c S2c)" in halt and "--unpark" in halt
