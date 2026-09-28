"""
E-061 C1.4 + C1.5 (delivery_plan_v26_continuation.md C1; DELIVERY_REVIEW.md A4, A6,
A8) -- unit tests for workflow/run_campaign.py's stage-exception pause and launch
pre-flight, and for the strict flag readers of run_phase1_research.py.

The joined-up proof is tests/test_e061_end_to_end_wiring.py (A4, A6, A8[*]); these
pin each piece on its own: the pause record, KeyboardInterrupt/SystemExit
passthrough, every strict reader, every dependency the pre-flight moves forward,
the D-3 protocol check, and --resume after a flag refusal. Hermetic: the conftest
sandbox is ROOT, run_loop is stubbed, no LLM, no subprocess.
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402

RUN = "run_001"
ENTRY = "TEST_ENTRY"


# ---------------------------------------------------------------------------
# Fixtures (the conftest sandbox is camp.ROOT == rpr.ROOT)
# ---------------------------------------------------------------------------

def _root() -> Path:
    return camp.ROOT


def _write_config(orchestrator: dict | None) -> None:
    path = _root() / "config" / "campaign_config.yaml"
    if orchestrator is None:
        if path.exists():
            path.unlink()
        return
    path.write_text(yaml.safe_dump({"orchestrator": orchestrator}, sort_keys=False),
                    encoding="utf-8")


def _scaffold(run_id: str = RUN, *, constraints: dict | None = None, **state) -> Path:
    run_dir = _root() / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "handoffs").mkdir(parents=True, exist_ok=True)
    doc = {"run_id": run_id, "status": "active", "current_stage": None,
           "pending_stage": "hypothesis_generation", "completed_stages": [],
           "counters": {}, "flags": {}, "audit_log": {}}
    doc.update(state)
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump(doc, sort_keys=False),
                                                encoding="utf-8")
    if constraints is not None:
        (run_dir / "artifacts" / "pre_registration.yaml").write_text(
            yaml.safe_dump({"machine_constraints": constraints}), encoding="utf-8")
    return run_dir


def _queue(entries: list) -> None:
    camp.QUEUE_PATH.write_text(yaml.safe_dump({"queue": entries}, sort_keys=False),
                               encoding="utf-8")


def _entry(status="in_progress", run_ids=(RUN,)) -> dict:
    return {"id": ENTRY, "brief_path": "briefs/irrelevant.md", "status": status,
            "priority": 1, "run_ids": list(run_ids), "outcome": None}


def _entries() -> list:
    return yaml.safe_load(camp.QUEUE_PATH.read_text(encoding="utf-8"))["queue"]


def _state(run_id: str = RUN) -> dict:
    return yaml.safe_load((_root() / "runs" / run_id / "pipeline_state.yaml")
                          .read_text(encoding="utf-8"))


def _log_text() -> str:
    return camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8") \
        if camp.CAMPAIGN_LOG_PATH.exists() else ""


def _protocol(name: str, promotion, provenance=None) -> Path:
    (_root() / "protocols").mkdir(exist_ok=True)
    doc = {"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": [], "promotion": promotion}
    if provenance is not None:
        doc["promotion_provenance"] = provenance
    path = _root() / "protocols" / name
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


_NON_GENERIC = {"median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 25,
                "min_trade_count_gte": 15, "kill_median_sharpe_lt": -1}


@pytest.fixture
def run_loop_calls(monkeypatch):
    calls = []
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: calls.append(run_id))
    return calls


# ---------------------------------------------------------------------------
# C1.4: an exception escaping run_loop is a classified pause
# ---------------------------------------------------------------------------

def test_stage_exception_is_a_classified_pause_and_a_restart_does_not_recrash(monkeypatch):
    _scaffold()
    _queue([_entry()])
    calls = []

    def _boom(run_id):
        calls.append(run_id)
        raise RuntimeError("C1.4 injected failure")
    monkeypatch.setattr(rpr, "run_loop", _boom)

    assert camp.process_once() is False
    assert _entries()[0]["status"] == "paused:stage_exception"
    st = _state()
    assert st["status"] == "paused_for_human"
    assert st["last_error"] == "RuntimeError: C1.4 injected failure"
    assert st["flags"]["stage_exception"] is True
    assert st["halt_history"][-1]["reason"] == "stage_exception"
    assert st["halt_history"][-1]["last_error"] == st["last_error"]
    assert "HALT — stage_exception: RuntimeError: C1.4 injected failure" in _log_text()
    assert camp._hard_pause_reason(_root() / "runs" / RUN, st) == ("stage_exception", "")

    # the restart: the entry is paused, so nothing is selected and nothing re-runs
    assert camp.process_once() is False
    assert calls == [RUN]
    assert "Queue exhausted" in _log_text()
    # --resume refuses until the operator resets the run (RUNBOOK §4)
    assert camp.resume_paused_entry(camp._load_queue()) is False
    rpr.update_state(path=_root() / "runs" / RUN, status="active", last_error=None,
                     flags={"stage_exception": False})
    assert camp.resume_paused_entry(camp._load_queue()) is True
    assert _entries()[0]["status"] == "in_progress"


@pytest.mark.parametrize("exc_type", [KeyboardInterrupt, SystemExit])
def test_keyboard_interrupt_and_system_exit_pass_through(monkeypatch, exc_type):
    _scaffold()
    _queue([_entry()])

    def _stop(run_id):
        raise exc_type()
    monkeypatch.setattr(rpr, "run_loop", _stop)
    with pytest.raises(exc_type):
        camp.process_once()
    assert _entries()[0]["status"] == "in_progress"
    st = _state()
    assert st["status"] == "active" and "halt_history" not in st
    assert "HALT" not in _log_text()


def test_unwritable_run_state_still_pauses_the_entry(monkeypatch):
    run_dir = _scaffold()
    _queue([_entry()])

    def _corrupt_then_raise(run_id):
        (run_dir / "pipeline_state.yaml").write_text("", encoding="utf-8")
        raise ValueError("state went away")
    monkeypatch.setattr(rpr, "run_loop", _corrupt_then_raise)
    assert camp.process_once() is False
    assert _entries()[0]["status"] == "paused:stage_exception"
    log = _log_text()
    assert "ValueError: state went away" in log
    assert f"{RUN}: pipeline_state.yaml could not be updated" in log


# ---------------------------------------------------------------------------
# C1.5 (b): strict boolean readers
# ---------------------------------------------------------------------------

_ONCE_PLAIN_BOOL_READERS = {
    "grid_evaluation": rpr._grid_evaluation_enabled,
    "category_reports": rpr._category_reports_enabled,
    "profit_bars_file": rpr._profit_bars_file_enabled,
    "exclusion_digest_input": rpr._exclusion_digest_input_enabled,
    "stale_input_path_fix": rpr._stale_input_path_fix_enabled,
    "variant_selection_record": rpr._variant_selection_record_enabled,
    "variant_anti_adjacency_gate": rpr._variant_anti_adjacency_gate_enabled,
    "schedulability_block": camp._schedulability_block_enabled,
}


@pytest.mark.parametrize("name", sorted(_ONCE_PLAIN_BOOL_READERS))
@pytest.mark.parametrize("value", ["false", "true", None, 0, 1])
def test_once_plain_bool_readers_refuse_a_non_bool(name, value):
    _write_config({name: {"enabled": value}})
    with pytest.raises(ValueError, match=rf"orchestrator\.{name}\.enabled=.* is not a real boolean"):
        _ONCE_PLAIN_BOOL_READERS[name]()
    refusal = camp._flag_preflight_refusal()
    assert refusal and f"orchestrator.{name}.enabled={value!r}" in refusal


@pytest.mark.parametrize("name", sorted(_ONCE_PLAIN_BOOL_READERS))
def test_once_plain_bool_readers_unchanged_for_real_booleans_and_absence(name):
    reader = _ONCE_PLAIN_BOOL_READERS[name]
    _write_config(None)
    assert reader() is False
    _write_config({})
    assert reader() is False
    _write_config({name: {}})
    assert reader() is False
    _write_config({name: {"enabled": False}})
    assert reader() is False
    if name != "variant_anti_adjacency_gate":  # its True needs no dependency to read
        _write_config({name: {"enabled": True}})
        assert reader() is True


def test_preflight_names_every_non_bool_at_once_including_quarantine():
    _write_config({"grid_evaluation": {"enabled": "false"},
                   "decide_next": {"enabled": None},
                   "halt_policy": {"quarantine_enabled": "false"}})
    refusal = camp._flag_preflight_refusal()
    for needle in ("orchestrator.grid_evaluation.enabled='false'",
                   "orchestrator.decide_next.enabled=None",
                   "orchestrator.halt_policy.quarantine_enabled='false'"):
        assert needle in refusal


def test_preflight_passes_on_the_real_campaign_config():
    """The committed config/campaign_config.yaml carries no quoted booleans and a
    consistent flag set (copied into the sandbox; the real file is only read)."""
    real = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    orch_cfg = real["orchestrator"]
    enabled = {k: v["enabled"] for k, v in orch_cfg.items()
               if isinstance(v, dict) and "enabled" in v}
    assert enabled and all(isinstance(v, bool) for v in enabled.values()), enabled
    assert isinstance(orch_cfg["halt_policy"]["quarantine_enabled"], bool)
    _write_config(orch_cfg)
    assert camp._flag_preflight_refusal() is None


def test_preflight_passes_with_no_config_at_all():
    _write_config(None)
    assert camp._flag_preflight_refusal() is None


# ---------------------------------------------------------------------------
# C1.5 (a): dependencies once enforced lazily, after spend
# ---------------------------------------------------------------------------

_CHAIN = {"grid_evaluation", "category_reports", "specialist_readers", "regroup_record",
          "profit_bars_file", "profit_bars_every_backtest", "config_direct_authoring",
          "decide_next", "verdict_routing_retired", "variant_loop", "composition_runs"}


def _flags(on: set) -> dict:
    return {name: {"enabled": True} for name in on}


def test_variant_loop_without_config_direct_is_refused():
    _write_config(_flags({"variant_loop"}))
    assert "orchestrator.config_direct_authoring.enabled=true" in camp._flag_preflight_refusal()


@pytest.mark.parametrize("missing", ["decide_next", "variant_loop",
                                     "profit_bars_every_backtest", "verdict_routing_retired"])
def test_composition_runs_without_a_prerequisite_is_refused(missing):
    on = set(_CHAIN) - {missing}
    if missing == "decide_next":
        on -= {"verdict_routing_retired"}  # vrr requires decide_next itself
    if missing == "profit_bars_every_backtest":
        on -= {"verdict_routing_retired"}
    _write_config(_flags(on))
    refusal = camp._flag_preflight_refusal()
    assert refusal and f"orchestrator.{missing}.enabled=true" in refusal
    assert "composition_runs" in refusal


def test_the_full_target_chain_passes():
    _write_config(_flags(_CHAIN | {"variant_anti_adjacency_gate"}))
    assert camp._flag_preflight_refusal() is None


def test_anti_adjacency_without_regroup_record_and_no_memory_is_refused():
    _write_config(_flags({"variant_anti_adjacency_gate", "config_direct_authoring"}))
    refusal = camp._flag_preflight_refusal()
    assert "orchestrator.regroup_record.enabled=true" in refusal
    # the same condition as the 5a check: an existing memory lifts it
    (_root() / "campaign_record").mkdir(exist_ok=True)
    (_root() / rpr._CAMPAIGN_MEMORY_REL).write_text("runs: {}\n", encoding="utf-8")
    assert camp._flag_preflight_refusal() is None


def test_anti_adjacency_on_the_legacy_path_needs_variant_selection_record():
    (_root() / "campaign_record").mkdir(exist_ok=True)
    (_root() / rpr._CAMPAIGN_MEMORY_REL).write_text("runs: {}\n", encoding="utf-8")
    _write_config(_flags({"variant_anti_adjacency_gate"}))
    assert "orchestrator.variant_selection_record.enabled=true" in camp._flag_preflight_refusal()
    _write_config(_flags({"variant_anti_adjacency_gate", "variant_selection_record"}))
    assert camp._flag_preflight_refusal() is None


# ---------------------------------------------------------------------------
# C1.5: the flag refusal in process_once, and --resume
# ---------------------------------------------------------------------------

def test_flag_refusal_pauses_a_fresh_entry_before_setup_run(monkeypatch, run_loop_calls):
    _write_config({"grid_evaluation": {"enabled": "false"}})
    _queue([_entry(status="ready", run_ids=())])
    monkeypatch.setattr(camp, "setup_run", lambda run_id: pytest.fail("setup_run called"))
    assert camp.process_once() is False
    assert _entries()[0]["status"] == "paused:flag_misconfiguration"
    assert not (_root() / "runs").exists() or not list((_root() / "runs").iterdir())
    assert "HALT — flag_misconfiguration: orchestrator.grid_evaluation.enabled='false' is not " \
           "a real boolean" in _log_text()
    assert run_loop_calls == []

    # --resume re-checks the config: refused while it is still wrong ...
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert _entries()[0]["status"] == "paused:flag_misconfiguration"
    # ... and, fixed, puts the run-less entry back to ready
    _write_config({"grid_evaluation": {"enabled": False}})
    assert camp.resume_paused_entry(camp._load_queue()) is True
    assert _entries()[0]["status"] == "ready"


def test_flag_refusal_records_on_an_in_progress_run(run_loop_calls):
    _scaffold()
    _queue([_entry()])
    _write_config(_flags({"variant_loop"}))
    assert camp.process_once() is False
    assert _entries()[0]["status"] == "paused:flag_misconfiguration"
    st = _state()
    assert st["status"] == "active"  # config-level: the run's own status is untouched
    assert st["halt_history"][-1]["reason"] == "flag_misconfiguration"
    assert "config_direct_authoring" in st["halt_history"][-1]["detail"]
    assert run_loop_calls == []
    _write_config(None)
    assert camp.resume_paused_entry(camp._load_queue()) is True
    assert _entries()[0]["status"] == "in_progress"


def test_flag_refusal_with_nothing_to_pause_logs_a_halt(run_loop_calls):
    _queue([])
    _write_config({"decide_next": {"enabled": "true"}})
    assert camp.process_once() is False
    assert "HALT — flag_misconfiguration" in _log_text()
    assert "decide_next" in _log_text()


# ---------------------------------------------------------------------------
# C1.5 (c): the pre-registered protocol passes D-3 before run_loop
# ---------------------------------------------------------------------------

def test_pinned_unratified_generic_protocol_is_refused_before_run_loop(run_loop_calls):
    _protocol("generic.json", dict(rpr._GENERIC_PROMOTION))
    _scaffold(constraints={"protocol_ref": "protocols/generic.json"})
    _queue([_entry()])
    assert camp.process_once() is False
    assert run_loop_calls == []
    assert _entries()[0]["status"] == "paused:protocol_promotion_unratified"
    st = _state()
    assert st["status"] == "paused_for_human"
    assert st["flags"]["protocol_promotion_unratified"] is True
    for needle in ("generic.json", "promotion", "ratified_by"):
        assert needle in st["last_error"]
    assert st["halt_history"][-1]["reason"] == "protocol_promotion_unratified"
    assert "HALT — protocol_promotion_unratified" in _log_text()


@pytest.mark.parametrize("promotion,provenance", [
    (_NON_GENERIC, None),
    (dict(rpr._GENERIC_PROMOTION), {"ratified_by": "operator", "ratified_at": "2025-01-01"}),
])
def test_ratified_or_non_generic_pinned_protocol_passes(monkeypatch, promotion, provenance):
    class _Reached(BaseException):  # passes through the C1.4 handler, like KeyboardInterrupt
        pass

    def _reach(run_id):
        raise _Reached(run_id)
    monkeypatch.setattr(rpr, "run_loop", _reach)
    _protocol("ok.json", promotion, provenance)
    _scaffold(constraints={"protocol_ref": "protocols/ok.json"})
    _queue([_entry()])
    with pytest.raises(_Reached):
        camp.process_once()
    assert _entries()[0]["status"] == "in_progress"


def test_generated_protocol_with_a_generic_promotion_is_refused_before_generation():
    run_dir = _scaffold(constraints={"protocol": {"symbols": ["BTCUSDT"], "start": "2022-01-01",
                                                  "end": "2022-03-01",
                                                  "promotion": dict(rpr._GENERIC_PROMOTION)}})
    refusal = camp._protocol_preflight_refusal(run_dir, RUN)
    assert refusal and "G7/D-3" in refusal and f"{RUN}_generated.json" in refusal
    run_dir2 = _scaffold("run_002", constraints={"protocol": {"promotion": _NON_GENERIC}})
    assert camp._protocol_preflight_refusal(run_dir2, "run_002") is None


def test_protocol_check_skips_runs_past_their_backtest_and_unpinned_runs():
    _protocol("generic.json", dict(rpr._GENERIC_PROMOTION))
    pin = {"protocol_ref": "protocols/generic.json"}
    past = _scaffold("run_010", constraints=pin, completed_stages=["protocol_execution"],
                     pending_stage="specialist_readers")
    assert camp._protocol_preflight_refusal(past, "run_010") is None
    done = _scaffold("run_011", constraints=pin, pending_stage="completed_refuted")
    assert camp._protocol_preflight_refusal(done, "run_011") is None
    unpinned = _scaffold("run_012")
    assert camp._protocol_preflight_refusal(unpinned, "run_012") is None
    missing = _scaffold("run_013", constraints={"protocol_ref": "protocols/nope.json"})
    assert camp._protocol_preflight_refusal(missing, "run_013") is None  # the pin raises later


def test_register_reads_decide_next_itself_not_its_prerequisites(monkeypatch):
    """A misconfigured prerequisite no longer crashes `register`; the launch
    pre-flight refuses it instead. A non-bool decide_next still raises there."""
    seen = []
    monkeypatch.setattr(camp, "register_hypothesis",
                        lambda brief, priority, notes, **k: seen.append(k) or 0)
    _write_config(_flags({"decide_next"}))  # regroup_record etc. missing
    assert camp._register_from_cli(Path("b.md"), 1, "n") == 0
    assert seen == [{"extra": {"brief_status": "open"}}]
    _write_config({"decide_next": {"enabled": "true"}})
    with pytest.raises(ValueError, match="not a real boolean"):
        camp._register_from_cli(Path("b.md"), 1, "n")


# ===========================================================================
# Code-review fixes (the second commit)
# ===========================================================================

# ---- fix 1: stale halt flags ----------------------------------------------

def test_resume_clears_the_stale_run_halt_flags():
    run_dir = _scaffold(status="active",
                        flags={"stage_exception": True, "protocol_promotion_unratified": True,
                               "launch_exception": True, "profit_bars_reached": True})
    _queue([_entry(status="paused:stage_exception")])
    assert camp.resume_paused_entry(camp._load_queue()) is True
    flags = _state()["flags"]
    assert flags["stage_exception"] is False
    assert flags["protocol_promotion_unratified"] is False
    assert flags["launch_exception"] is False
    assert flags["profit_bars_reached"] is True  # not ours: untouched
    assert run_dir.exists()


@pytest.mark.parametrize("flag", ["stage_exception", "protocol_promotion_unratified",
                                  "launch_exception"])
def test_a_stale_halt_flag_never_masks_the_holdout_step(flag):
    """The reviewer's scenario: the operator reset only `status` after a
    stage_exception (flag left true), the run later reaches the promote path."""
    run_dir = _scaffold(status="paused_for_human", flags={flag: True})
    (run_dir / "artifacts" / "promotion_audit.yaml").write_text("x: 1\n", encoding="utf-8")
    assert camp._classify_human_pause(run_dir, _state()) == "provisional_promote_awaiting_holdout"
    (run_dir / "artifacts" / "holdout_result.yaml").write_text("status: pending\n",
                                                              encoding="utf-8")
    assert camp._classify_human_pause(run_dir, _state()) == \
        "provisional_promote_holdout_inconclusive"
    # and alone, it still reads as itself
    other = _scaffold("run_002", status="paused_for_human", flags={flag: True})
    assert camp._classify_human_pause(other, _state("run_002")) == flag


# ---- fix 2: bookkeeping after an exception ---------------------------------

def test_a_split_recorded_before_the_exception_still_gets_its_queue_entry(monkeypatch):
    _scaffold()
    _scaffold("run_002")  # the sibling run_loop scaffolded before raising
    _queue([_entry()])

    def _split_then_raise(run_id):
        state = rpr.load_campaign_state()
        state["hypothesis_splits"] = [{"parent_run": RUN, "children": ["run_002"]}]
        rpr._save_campaign_state(state)
        raise RuntimeError("after the split")
    monkeypatch.setattr(rpr, "run_loop", _split_then_raise)
    assert camp.process_once() is False
    entries = {e["id"]: e for e in _entries()}
    assert entries[ENTRY]["status"] == "paused:stage_exception"
    sibling = entries[f"{ENTRY}__split_run_002"]
    assert sibling["run_ids"] == ["run_002"] and sibling["status"] == "in_progress"
    assert "SPLIT" in _log_text()


# ---- fix 3: run_context / claimed-escalation protocols ---------------------

def test_a_claimed_escalation_protocol_is_refused_before_run_loop(run_loop_calls):
    """Flag-off legacy: an escalation child resolves its protocol from
    campaign_state.last_escalation -- refused before 1a, with no state write by
    the resolver (on_stale_escalation=None)."""
    proto = _protocol("escalation_generic.json", dict(rpr._GENERIC_PROMOTION))
    state = rpr.load_campaign_state()
    state["last_escalation"] = {"protocol_path": str(proto), "claimed_by_run": RUN}
    rpr._save_campaign_state(state)
    _scaffold()  # no machine_constraints, no run_context: the B10 fallback
    _queue([_entry()])
    assert camp.process_once() is False
    assert run_loop_calls == []
    assert _entries()[0]["status"] == "paused:protocol_promotion_unratified"
    st = _state()
    assert "campaign_state.last_escalation" in st["last_error"]
    assert "escalation_generic.json" in st["last_error"] and "ratified_by" in st["last_error"]
    assert "stale_escalation_unclaimed" not in (st.get("flags") or {})


def test_an_unclaimed_escalation_is_left_to_run_loop(run_loop_calls):
    proto = _protocol("escalation_generic.json", dict(rpr._GENERIC_PROMOTION))
    state = rpr.load_campaign_state()
    state["last_escalation"] = {"protocol_path": str(proto), "claimed_by_run": "run_999"}
    rpr._save_campaign_state(state)
    run_dir = _scaffold()
    assert camp._protocol_preflight_refusal(run_dir, RUN) is None


def test_a_run_context_protocol_is_refused_before_run_loop():
    _protocol("forced_generic.json", dict(rpr._GENERIC_PROMOTION))
    run_dir = _scaffold()
    (run_dir / "artifacts" / "run_context.yaml").write_text(
        yaml.safe_dump({"run_type": "forced_diagnostic", "protocol": "forced_generic.json"}),
        encoding="utf-8")
    refusal = camp._protocol_preflight_refusal(run_dir, RUN)
    assert refusal and "run_context.yaml" in refusal and "forced_generic.json" in refusal


# ---- fix 4: the data_block_hitl --resume path ------------------------------

def _stage_hitl():
    run_dir = _scaffold(status="paused_for_human", pending_stage="human_pause")
    (run_dir / "artifacts" / "human_resolution.yaml").write_text(
        "status: resolved_proceed\n", encoding="utf-8")
    _queue([_entry(status="paused:data_block_hitl")])
    return run_dir


def test_hitl_resume_refuses_a_flag_misconfiguration_before_resume_pipeline(monkeypatch):
    _stage_hitl()
    monkeypatch.setattr(rpr, "resume_pipeline", lambda run_id: pytest.fail("resumed"))
    _write_config({"grid_evaluation": {"enabled": "false"}})
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert _entries()[0]["status"] == "paused:data_block_hitl"
    assert "RESUME REFUSED" in _log_text() and "grid_evaluation" in _log_text()


def test_hitl_resume_refuses_an_unratified_protocol_before_resume_pipeline(monkeypatch):
    run_dir = _stage_hitl()
    _protocol("generic.json", dict(rpr._GENERIC_PROMOTION))
    (run_dir / "artifacts" / "pre_registration.yaml").write_text(
        yaml.safe_dump({"machine_constraints": {"protocol_ref": "protocols/generic.json"}}),
        encoding="utf-8")
    monkeypatch.setattr(rpr, "resume_pipeline", lambda run_id: pytest.fail("resumed"))
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert _entries()[0]["status"] == "paused:data_block_hitl"
    assert "protocol_promotion_unratified" in _log_text()


def test_hitl_resume_exception_is_a_classified_pause(monkeypatch):
    _stage_hitl()

    def _boom(run_id):
        raise RuntimeError("resume_pipeline blew up")
    monkeypatch.setattr(rpr, "resume_pipeline", _boom)
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert _entries()[0]["status"] == "paused:stage_exception"
    st = _state()
    assert st["flags"]["stage_exception"] is True
    assert st["last_error"] == "RuntimeError: resume_pipeline blew up"
    assert "HALT — stage_exception" in _log_text()


# ---- fix 5: a stale generated protocol is regenerated ----------------------

def _generated_constraints(promotion):
    return {"protocol": {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2022-01-01",
                         "end": "2022-03-01", "promotion": promotion}}


def test_fixing_pre_registration_regenerates_the_generated_protocol(monkeypatch):
    generic = dict(rpr._GENERIC_PROMOTION)
    run_dir = _scaffold(constraints=_generated_constraints(generic))
    # the file generated earlier from the generic block, before the fix
    gen_path = _protocol(f"{RUN}_generated.json", generic)
    _queue([_entry()])
    calls = []
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: calls.append(run_id))
    assert camp.process_once() is False
    assert calls == []
    assert _entries()[0]["status"] == "paused:protocol_promotion_unratified"

    # the RUNBOOK fix: real thresholds in pre_registration, reset, --resume
    (run_dir / "artifacts" / "pre_registration.yaml").write_text(
        yaml.safe_dump({"machine_constraints": _generated_constraints(_NON_GENERIC)}),
        encoding="utf-8")
    rpr.update_state(path=run_dir, status="active", last_error=None)
    assert camp.resume_paused_entry(camp._load_queue()) is True
    assert _state()["flags"]["protocol_promotion_unratified"] is False

    class _Reached(BaseException):
        pass

    def _reach(run_id):
        raise _Reached(run_id)
    monkeypatch.setattr(rpr, "run_loop", _reach)
    with pytest.raises(_Reached):
        camp.process_once()
    assert json.loads(gen_path.read_text(encoding="utf-8"))["promotion"] == _NON_GENERIC
    assert "regenerated" in _log_text()


# ---- fix 6: an exception while launching -----------------------------------

def _write_brief(name="brief_c14.md") -> str:
    front = {"strategy_domain": "crypto_directional", "market_universe": "BTCUSDT",
             "timeframe": "1h", "research_goal": "wiring", "venue": "binance",
             "product": "perp",
             "machine_constraints": {"protocol_ref": "protocols/ok.json"}}
    (_root() / "briefs").mkdir(exist_ok=True)
    (_root() / "briefs" / name).write_text(
        "---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n\nbrief\n", encoding="utf-8")
    return f"briefs/{name}"


def test_a_b11_lint_failure_at_launch_is_a_classified_pause_without_orphans(monkeypatch,
                                                                         run_loop_calls):
    entry = _entry(status="ready", run_ids=())
    entry["brief_path"] = _write_brief()
    _queue([entry])
    monkeypatch.setattr(rpr, "_lint_pass_rule_total_mapping",
                        lambda pre_registration: (["injected B11 violation"], []))
    assert camp.process_once() is False
    runs = sorted(p.name for p in (_root() / "runs").iterdir())
    assert runs == [RUN]
    e = _entries()[0]
    assert e["status"] == "paused:launch_exception" and e["run_ids"] == [RUN]
    st = _state()
    assert st["status"] == "paused_for_human" and st["flags"]["launch_exception"] is True
    assert "B11" in st["last_error"] and st["halt_history"][-1]["reason"] == "launch_exception"
    assert "HALT — launch_exception: ValueError" in _log_text()
    assert run_loop_calls == []

    # a restart allocates nothing and runs nothing; --resume refuses in place
    assert camp.process_once() is False
    assert sorted(p.name for p in (_root() / "runs").iterdir()) == [RUN]
    assert camp.resume_paused_entry(camp._load_queue()) is False


# ---- fix 7: the protocol refusal's state write is guarded ------------------

def test_protocol_refusal_with_an_unwritable_state_still_halts(run_loop_calls):
    _protocol("generic.json", dict(rpr._GENERIC_PROMOTION))
    run_dir = _scaffold(constraints={"protocol_ref": "protocols/generic.json"})
    (run_dir / "pipeline_state.yaml").write_text("", encoding="utf-8")
    _queue([_entry()])
    assert camp.process_once() is False
    assert _entries()[0]["status"] == "paused:protocol_promotion_unratified"
    log = _log_text()
    assert "HALT — protocol_promotion_unratified" in log
    assert f"{RUN}: pipeline_state.yaml could not be updated" in log
    assert run_loop_calls == []


# ---- fix 8: one strict check ----------------------------------------------

def test_the_duplicate_strict_helper_is_gone():
    assert not hasattr(rpr, "_strict_flag_value")
    _write_config({"grid_evaluation": {"enabled": "false"}})
    with pytest.raises(ValueError) as a:
        rpr._grid_evaluation_enabled()
    with pytest.raises(ValueError) as b:
        rpr._strict_orchestrator_flag("grid_evaluation")
    assert str(a.value) == str(b.value)


# ---- fix 9: in-memory rules == readers ------------------------------------

def test_the_rule_table_and_the_readers_name_the_same_flags():
    assert [n for n, _, _ in camp._FLAG_RULES] == list(camp._flag_readers())


def _readers_verdict():
    values = {}
    for name, reader in camp._flag_readers().items():
        try:
            values[name] = reader()
        except (ValueError, AttributeError):
            return None
    return values


def test_in_memory_rules_agree_with_the_readers_on_every_flag():
    import random
    names = [n for n, _, _ in camp._FLAG_RULES]
    choices = ("absent", True, False, "false", None)
    rng = random.Random(1561)
    configs = [{}]
    for name in names:  # each flag alone, every value
        for v in choices[1:]:
            configs.append({name: v})
    for name in names:  # each flag on with everything else on
        configs.append({n: (n != name) for n in names})
    for _ in range(400):  # random mixes, weighted to real booleans
        configs.append({n: rng.choice((True, True, False, False, "absent", "false", None))
                        for n in names})
    for assignment in configs:
        orch_cfg = {n: {"enabled": v} for n, v in assignment.items() if v != "absent"}
        _write_config(orch_cfg)
        by_readers = _readers_verdict()
        values, refusal = camp._flag_rules_check({"orchestrator": orch_cfg})
        assert (refusal is None) == (by_readers is not None), (assignment, refusal)
        if by_readers is not None:
            assert {n: values[n] for n in names} == by_readers, assignment


# ---- fix 10: schedulability still written ---------------------------------

def test_schedulability_is_written_while_another_flag_is_refused(run_loop_calls):
    _queue([_entry(status="ready", run_ids=())])
    _write_config({"schedulability_block": {"enabled": True},
                   "grid_evaluation": {"enabled": "false"}})
    path = _root() / "campaign_record" / "schedulability.yaml"
    assert not path.exists()
    assert camp.process_once() is False
    assert path.exists()
    assert _entries()[0]["status"] == "paused:flag_misconfiguration"
    # its own value invalid: not written
    path.unlink()
    _queue([_entry(status="ready", run_ids=())])
    _write_config({"schedulability_block": {"enabled": "true"}})
    assert camp.process_once() is False
    assert not path.exists()
