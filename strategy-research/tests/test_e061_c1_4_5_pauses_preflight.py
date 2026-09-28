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
    run_dir2 = _scaffold("run_002", constraints=_generated_constraints(_NON_GENERIC))
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
# Code-review fixes (the second and third commits)
# ===========================================================================

class _Reached(BaseException):
    """Passes through the C1.4 handler (like KeyboardInterrupt): run_loop reached."""


def _reach_run_loop(monkeypatch):
    def _reach(run_id):
        raise _Reached(run_id)
    monkeypatch.setattr(rpr, "run_loop", _reach)


# ---- stale / fresh halt flags (review fix 1, third-round fix 8) ----------

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
def test_a_fresh_halt_flag_wins_over_an_old_artifact(flag):
    """A flag set by THIS halt is the reason, even next to an old
    refinement_notes.yaml (an earlier data block) or an old promotion_audit."""
    run_dir = _scaffold(status="paused_for_human", flags={flag: True})
    (run_dir / "artifacts" / "refinement_notes.yaml").write_text(
        yaml.safe_dump({"decision": {"implementation_allowed": False}}), encoding="utf-8")
    assert camp._classify_human_pause(run_dir, _state()) == flag
    (run_dir / "artifacts" / "promotion_audit.yaml").write_text("x: 1\n", encoding="utf-8")
    assert camp._classify_human_pause(run_dir, _state()) == flag


def _unpause(path, run_dir, flag):
    """Un-pause the run through one of the three real un-pause paths."""
    if path == "resume":
        _queue([_entry(status="paused:stage_exception")])
        assert camp.resume_paused_entry(camp._load_queue()) is True
    elif path == "unpark":
        rpr.update_state(path=run_dir, status="paused_for_human",
                         **{rpr.PARKED_KEY: {"kind": "data", "resume_stage": "backtest_specification"}})
        _queue([_entry(status="paused:waiting_for_data")])
        assert camp._unpark_entry(ENTRY) is True
    else:  # resume_pipeline (the data_block_hitl resolution)
        rpr.update_state(path=run_dir, status="paused_for_human")
        (run_dir / "artifacts" / "human_resolution.yaml").write_text(
            "status: resolved_proceed\n", encoding="utf-8")
        rpr.resume_pipeline(RUN)


@pytest.mark.parametrize("path", ["resume", "unpark", "resume_pipeline"])
@pytest.mark.parametrize("flag", ["stage_exception", "protocol_promotion_unratified",
                                  "launch_exception"])
def test_a_stale_halt_flag_never_masks_the_holdout_step(monkeypatch, path, flag):
    """Restored guard (fourth-round fix 2): whatever un-pause path the operator
    takes, the halt flag is cleared, so the later promote pause reads as
    itself; a FRESH flag (set by the halt itself) still wins (see
    test_a_fresh_halt_flag_wins_over_an_old_artifact)."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir = _scaffold(status="active", flags={flag: True})
    _unpause(path, run_dir, flag)
    assert not _state()["flags"].get(flag), path
    rpr.update_state(path=run_dir, status="paused_for_human")
    (run_dir / "artifacts" / "promotion_audit.yaml").write_text("x: 1\n", encoding="utf-8")
    assert camp._classify_human_pause(run_dir, _state()) == "provisional_promote_awaiting_holdout"
    # the same state with the flag set again (a fresh halt) reads as the flag
    rpr.update_state(path=run_dir, flags={flag: True})
    assert camp._classify_human_pause(run_dir, _state()) == flag


def test_the_run_halt_flag_names_have_one_source():
    assert camp._RUN_FLAG_HALTS == rpr.RUN_HALT_FLAGS == (
        camp.STAGE_EXCEPTION_HALT, camp.PROTOCOL_PREFLIGHT_HALT, camp.LAUNCH_EXCEPTION_HALT)


# ---- bookkeeping after an exception (review fix 2, third-round fix 7) ------

def _split_then_raise(run_id):
    state = rpr.load_campaign_state()
    state["hypothesis_splits"] = [{"parent_run": RUN, "children": ["run_002"]}]
    rpr._save_campaign_state(state)
    raise RuntimeError("after the split")


def test_a_split_recorded_before_the_exception_still_gets_its_queue_entry(monkeypatch):
    _scaffold()
    _scaffold("run_002")  # the sibling run_loop scaffolded before raising
    _queue([_entry()])
    monkeypatch.setattr(rpr, "run_loop", _split_then_raise)
    assert camp.process_once() is False
    entries = {e["id"]: e for e in _entries()}
    assert entries[ENTRY]["status"] == "paused:stage_exception"
    sibling = entries[f"{ENTRY}__split_run_002"]
    assert sibling["run_ids"] == ["run_002"] and sibling["status"] == "in_progress"
    assert "SPLIT" in _log_text()


def test_failed_bookkeeping_never_overwrites_what_it_registered(monkeypatch):
    _scaffold()
    _scaffold("run_002")
    _queue([_entry()])
    monkeypatch.setattr(rpr, "run_loop", _split_then_raise)
    real_add, calls = camp._add_queue_entry_for_split_child, []

    def _register_then_fail_once(queue, parent_entry, parent_run_id, child_id):
        calls.append(child_id)
        if len(calls) == 1:
            disk = camp._load_queue()
            disk["queue"].append({"id": "REGISTERED_CARD", "brief_path": "briefs/x.md",
                                  "status": "queued", "priority": 999, "run_ids": [],
                                  "outcome": None})
            camp._save_queue(disk)
            raise OSError("bookkeeping failed after registering")
        return real_add(queue, parent_entry, parent_run_id, child_id)
    monkeypatch.setattr(camp, "_add_queue_entry_for_split_child", _register_then_fail_once)
    assert camp.process_once() is False
    entries = {e["id"]: e for e in _entries()}
    assert "REGISTERED_CARD" in entries                      # never overwritten
    assert entries[f"{ENTRY}__split_run_002"]["run_ids"] == ["run_002"]  # re-applied
    assert entries[ENTRY]["status"] == "paused:stage_exception"
    assert "bookkeeping after it also failed" in _state()["last_error"]
    assert "sibling run_002 re-applied" in _log_text()


def test_an_entry_gone_after_the_reload_is_never_saved_back(monkeypatch):
    _scaffold()
    _scaffold("run_002")
    _queue([_entry()])
    monkeypatch.setattr(rpr, "run_loop", _split_then_raise)

    def _drop_entry_then_fail(queue, parent_entry, parent_run_id, child_id):
        disk = camp._load_queue()
        disk["queue"] = [e for e in disk["queue"] if e.get("id") != ENTRY]
        disk["queue"].append({"id": "OTHER", "brief_path": "briefs/x.md", "status": "ready",
                              "priority": 5, "run_ids": [], "outcome": None})
        camp._save_queue(disk)
        written.append(camp.QUEUE_PATH.read_bytes())
        raise OSError("bookkeeping failed")
    written = []
    monkeypatch.setattr(camp, "_add_queue_entry_for_split_child", _drop_entry_then_fail)
    assert camp.process_once() is False
    assert camp.QUEUE_PATH.read_bytes() == written[0]  # left exactly as re-read
    assert [e["id"] for e in _entries()] == ["OTHER"]
    st = _state()
    assert st["status"] == "paused_for_human" and st["flags"]["stage_exception"] is True
    assert "IS NOT IN config/campaign_queue.yaml" in _log_text()


# ---- run_context / claimed-escalation protocols (review fix 3) -------------

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


def test_an_unclaimed_escalation_is_left_to_run_loop():
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


# ---- the data_block_hitl --resume path (review fix 4; third-round 3-4) -----

def _stage_hitl(resolution="resolved_proceed", constraints=None):
    run_dir = _scaffold(status="paused_for_human", pending_stage="human_pause",
                        constraints=constraints)
    (run_dir / "artifacts" / "human_resolution.yaml").write_text(
        f"status: {resolution}\n", encoding="utf-8")
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
    _protocol("generic.json", dict(rpr._GENERIC_PROMOTION))
    _stage_hitl(constraints={"protocol_ref": "protocols/generic.json"})
    monkeypatch.setattr(rpr, "resume_pipeline", lambda run_id: pytest.fail("resumed"))
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert _entries()[0]["status"] == "paused:data_block_hitl"
    assert "protocol_promotion_unratified" in _log_text()


def test_hitl_resume_preflight_exception_keeps_the_hitl_pause(monkeypatch):
    _stage_hitl()
    monkeypatch.setattr(rpr, "resume_pipeline", lambda run_id: pytest.fail("resumed"))

    def _boom(*a, **k):
        raise OSError("pre-flight could not read the protocol")
    monkeypatch.setattr(camp, "_protocol_preflight", _boom)
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert _entries()[0]["status"] == "paused:data_block_hitl"
    st = _state()
    assert st["status"] == "paused_for_human"
    assert "OSError: pre-flight could not read the protocol" in st["last_error"]
    assert "stage_exception" not in (st.get("flags") or {})
    assert st["halt_history"][-1]["reason"] == "data_block_hitl"
    assert "HALT — data_block_hitl" in _log_text()


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


def test_an_unresolvable_resolution_closes_the_run_despite_any_preflight_problem():
    _protocol("generic.json", dict(rpr._GENERIC_PROMOTION))
    _stage_hitl(resolution="unresolvable", constraints={"protocol_ref": "protocols/generic.json"})
    _write_config({"grid_evaluation": {"enabled": "false"}})
    assert camp.resume_paused_entry(camp._load_queue()) is True  # the real resume_pipeline
    st = _state()
    assert st["status"] == "rejected" and st["pending_stage"] == "completed_rejected"
    assert "RESUME REFUSED" not in _log_text()


# ---- generated protocols: spend, staleness, atomicity (third-round 1-2) ----

def _generated_constraints(promotion, **over):
    proto = {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2022-01-01",
             "end": "2022-03-01", "promotion": promotion}
    proto.update(over)
    return {"protocol": proto}


def _set_pre_registration(run_dir, constraints):
    (run_dir / "artifacts" / "pre_registration.yaml").write_text(
        yaml.safe_dump({"machine_constraints": constraints}), encoding="utf-8")


_OTHER = {**_NON_GENERIC, "min_trade_count_gte": 30}


def test_the_expected_protocol_is_exactly_what_generation_writes():
    constraints = _generated_constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    written = json.loads(path.read_text(encoding="utf-8"))
    assert camp._expected_generated_protocol(constraints["protocol"], RUN) == written


def test_a_promotion_only_fix_before_any_spend_is_regenerated_atomically(monkeypatch):
    generic = dict(rpr._GENERIC_PROMOTION)
    run_dir = _scaffold(constraints=_generated_constraints(generic))
    gen_path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _generated_constraints(generic))
    _queue([_entry()])
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: pytest.fail("run_loop reached"))
    assert camp.process_once() is False
    assert _entries()[0]["status"] == "paused:protocol_promotion_unratified"

    # the RUNBOOK fix: real thresholds in pre_registration, reset, --resume
    _set_pre_registration(run_dir, _generated_constraints(_NON_GENERIC))
    rpr.update_state(path=run_dir, status="active", last_error=None)
    assert camp.resume_paused_entry(camp._load_queue()) is True
    assert _state()["flags"]["protocol_promotion_unratified"] is False
    _reach_run_loop(monkeypatch)
    with pytest.raises(_Reached):
        camp.process_once()
    doc = json.loads(gen_path.read_text(encoding="utf-8"))
    assert doc == camp._expected_generated_protocol(_generated_constraints(_NON_GENERIC)["protocol"], RUN)
    assert "regenerated before any spend -- field(s) ['promotion']" in _log_text()
    assert not list(gen_path.parent.glob(f".{gen_path.name}.*"))


@pytest.mark.parametrize("evidence", ["trial_row", "variant_trial_row", "protocol_result",
                                      "variant_protocol_result", "stage_attempts"])
def test_after_spend_the_generated_file_is_never_rebuilt_or_regenerated(monkeypatch, evidence):
    """Fourth-round fix 1: spend is checked first; after it only the EXISTING
    file gets the D-3 check -- an edited pre_registration (even one that could
    not generate at all) changes nothing and refuses nothing."""
    constraints = _generated_constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    gen_path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    before_bytes = gen_path.read_bytes()
    campaign = rpr.load_campaign_state()
    if evidence in ("trial_row", "variant_trial_row"):
        tid = RUN if evidence == "trial_row" else f"{RUN}:base"
        campaign["trial_sharpes"] = [{"trial_id": tid, "sharpe": 0.1}]
    rpr._save_campaign_state(campaign)
    if evidence == "protocol_result":
        (run_dir / "artifacts" / "protocol_result.yaml").write_text("x: 1\n", encoding="utf-8")
    if evidence == "variant_protocol_result":
        (run_dir / "artifacts" / "variants" / "base").mkdir(parents=True)
        (run_dir / "artifacts" / "variants" / "base" / "protocol_result.yaml").write_text(
            "x: 1\n", encoding="utf-8")
    if evidence == "stage_attempts":
        rpr.update_state(path=run_dir, stage_attempts={"protocol_execution": 1})
    rows_before = len(rpr.load_campaign_state().get("trial_sharpes") or [])
    for edited in (_generated_constraints(_OTHER),                     # the rules changed
                   {"protocol": {"promotion": _OTHER}}):               # cannot even generate
        _set_pre_registration(run_dir, edited)
        assert camp._protocol_preflight(run_dir, RUN) == (None, None)
    _queue([_entry()])
    _reach_run_loop(monkeypatch)
    with pytest.raises(_Reached):
        camp.process_once()
    assert gen_path.read_bytes() == before_bytes
    assert len(rpr.load_campaign_state().get("trial_sharpes") or []) == rows_before
    assert "regenerated" not in _log_text()


def test_after_spend_an_unratified_generated_file_is_still_refused_by_d3():
    constraints = _generated_constraints(dict(rpr._GENERIC_PROMOTION))
    run_dir = _scaffold(constraints=constraints)
    rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    (run_dir / "artifacts" / "protocol_result.yaml").write_text("x: 1\n", encoding="utf-8")
    refusal, regeneration = camp._protocol_preflight(run_dir, RUN)
    assert regeneration is None and "[G7/D-3]" in refusal and "ratified_by" in refusal
    assert "fix it before" not in refusal


def test_after_spend_a_missing_generated_file_is_refused():
    constraints = _generated_constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    (run_dir / "artifacts" / "protocol_result.yaml").write_text("x: 1\n", encoding="utf-8")
    refusal, _ = camp._protocol_preflight(run_dir, RUN)
    assert refusal and "file is missing although data may already have been spent" in refusal


@pytest.mark.real_repo_readonly
@pytest.mark.parametrize("run_id", ["run_048", "run_050", "run_053"])
def test_real_generated_run_shapes_under_the_hitl_resume(tmp_path, monkeypatch, run_id):
    """Copies of the committed run_048 / run_050 / run_053 shapes (pre-G7 briefs:
    machine_constraints.protocol has NO promotion block; each has a
    protocol_result.yaml) checked as the data_block_hitl resume checks them
    (ignore_pending=True): no rebuild refusal -- only the D-3 check of the
    existing generated file."""
    import shutil
    sandbox = tmp_path / "sr"
    for sub in ("config", "protocols", f"runs/{run_id}/artifacts"):
        (sandbox / sub).mkdir(parents=True)
    shutil.copyfile(_SR / "config" / "campaign_data_policy.yaml",
                    sandbox / "config" / "campaign_data_policy.yaml")
    src = _SR / "runs" / run_id
    shutil.copyfile(src / "pipeline_state.yaml", sandbox / "runs" / run_id / "pipeline_state.yaml")
    for name in ("pre_registration.yaml", "protocol_result.yaml"):
        shutil.copyfile(src / "artifacts" / name, sandbox / "runs" / run_id / "artifacts" / name)
    shutil.copyfile(_SR / "protocols" / f"{run_id}_generated.json",
                    sandbox / "protocols" / f"{run_id}_generated.json")
    monkeypatch.setattr(rpr, "ROOT", sandbox)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", sandbox / "campaign_state.yaml")
    monkeypatch.setattr(camp, "ROOT", sandbox)
    run_dir = sandbox / "runs" / run_id
    assert not rpr._load_machine_constraints(run_dir)["protocol"].get("promotion")
    refusal, regeneration = camp._protocol_preflight(run_dir, run_id, ignore_pending=True)
    assert regeneration is None
    assert refusal is None or ("fix it before" not in refusal and "[G7/D-3]" in refusal), refusal
    before = (sandbox / "protocols" / f"{run_id}_generated.json").read_bytes()
    assert (_SR / "protocols" / f"{run_id}_generated.json").read_bytes() == before


@pytest.mark.parametrize("change,field", [({"end": "2022-04-01"}, "windows"),
                                          ({"symbols": ["ETHUSDT"]}, "symbols"),
                                          ({"timeframe": "4h"}, "timeframe")])
def test_a_non_promotion_change_before_spend_is_refused(monkeypatch, change, field):
    constraints = _generated_constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    gen_path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    before_bytes = gen_path.read_bytes()
    _set_pre_registration(run_dir, _generated_constraints(_OTHER, **change))
    refusal, regeneration = camp._protocol_preflight(run_dir, RUN)
    assert regeneration is None and refusal and field in refusal
    assert "only a promotion-block change is regenerated" in refusal
    assert gen_path.read_bytes() == before_bytes


def test_inputs_that_cannot_generate_are_refused_and_keep_the_file():
    constraints = _generated_constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    gen_path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    before_bytes = gen_path.read_bytes()
    for broken in ({"protocol": {**constraints["protocol"], "promotion": None}},
                   {"protocol": {k: v for k, v in constraints["protocol"].items()
                                 if k != "symbols"}}):
        _set_pre_registration(run_dir, broken)
        refusal, regeneration = camp._protocol_preflight(run_dir, RUN)
        assert regeneration is None and "cannot generate a protocol" in refusal, broken
        assert gen_path.read_bytes() == before_bytes


def test_windows_reaching_the_holdout_are_refused_before_generation():
    hs, _he = rpr._load_holdout_range()  # read at runtime, never a literal
    constraints = _generated_constraints(_NON_GENERIC, end=str(hs))
    constraints["protocol"]["start"] = "2025-10-01"
    run_dir = _scaffold(constraints=constraints)
    # an end AFTER the seal starts: generation would raise HoldoutBoundaryBreach
    import datetime as _dt
    constraints["protocol"]["end"] = (_dt.date.fromisoformat(str(hs))
                                      + _dt.timedelta(days=40)).isoformat()
    _set_pre_registration(run_dir, constraints)
    refusal, regeneration = camp._protocol_preflight(run_dir, RUN)
    assert regeneration is None and refusal and "cannot generate a protocol" in refusal


def test_a_failed_regeneration_write_keeps_the_original(monkeypatch):
    run_dir = _scaffold(constraints=_generated_constraints(_NON_GENERIC))
    gen_path = rpr._ensure_protocol_from_constraints(
        run_dir, RUN, _generated_constraints(_NON_GENERIC))
    before_bytes = gen_path.read_bytes()
    _set_pre_registration(run_dir, _generated_constraints(_OTHER))
    _queue([_entry()])

    real_replace = camp.os.replace

    def _fail_replace(src, dst):
        if Path(dst).name == gen_path.name:
            raise OSError("disk full")
        return real_replace(src, dst)
    monkeypatch.setattr(camp.os, "replace", _fail_replace)
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: pytest.fail("run_loop reached"))
    assert camp.process_once() is False
    assert _entries()[0]["status"] == "paused:stage_exception"
    assert gen_path.read_bytes() == before_bytes
    assert not list(gen_path.parent.glob(f".{gen_path.name}.*"))


# ---- launch exceptions (review fix 6; third-round 5-6) ---------------------

def _write_brief(name="brief_c14.md") -> str:
    front = {"strategy_domain": "crypto_directional", "market_universe": "BTCUSDT",
             "timeframe": "1h", "research_goal": "wiring", "venue": "binance",
             "product": "perp",
             "machine_constraints": {"protocol_ref": "protocols/ok.json"}}
    (_root() / "briefs").mkdir(exist_ok=True)
    (_root() / "briefs" / name).write_text(
        "---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n\nbrief\n", encoding="utf-8")
    return f"briefs/{name}"


def test_a_b11_lint_failure_at_launch_is_recorded_and_abandoned(monkeypatch, run_loop_calls):
    entry = _entry(status="ready", run_ids=())
    entry["brief_path"] = _write_brief()
    _queue([entry])
    monkeypatch.setattr(rpr, "_lint_pass_rule_total_mapping",
                        lambda pre_registration: (["injected B11 violation"], []))
    assert camp.process_once() is False
    assert sorted(p.name for p in (_root() / "runs").iterdir()) == [RUN]
    e = _entries()[0]
    assert e["status"] == "paused:launch_exception" and e["run_ids"] == []
    assert e["launch_failed_run_id"] == RUN and "B11" in e["launch_exception_detail"]
    st = _state()
    assert st["status"] == "abandoned_launch" and "B11" in st["last_error"]
    assert st["abandoned_note"] and st["halt_history"][-1]["reason"] == "launch_exception"
    assert "HALT — launch_exception: ValueError" in _log_text()
    assert run_loop_calls == []

    # a restart allocates nothing, runs nothing, and the abandoned dir is no orphan
    assert camp.process_once() is False
    assert sorted(p.name for p in (_root() / "runs").iterdir()) == [RUN]
    assert camp.reconcile_orphans() == [RUN]
    assert "0 unexpected" in _log_text().splitlines()[-2] + _log_text().splitlines()[-1]
    assert "unreferenced run dir(s)" not in _log_text()
    # --resume relaunches the run-less entry (fix the cause first)
    assert camp.resume_paused_entry(camp._load_queue()) is True
    e = _entries()[0]
    assert e["status"] == "ready"
    assert "launch_failed_run_id" not in e and "launch_exception_detail" not in e


def test_a_launch_failure_before_a_run_id_is_allocated(monkeypatch, run_loop_calls):
    _queue([_entry(status="ready", run_ids=())])

    def _bad_brief(path):
        raise ValueError("frontmatter missing required field 'venue'")
    monkeypatch.setattr(camp, "_parse_brief_frontmatter", _bad_brief)
    assert camp.process_once() is False
    e = _entries()[0]
    assert e["status"] == "paused:launch_exception" and e["run_ids"] == []
    assert e["launch_failed_run_id"] is None
    assert not (_root() / "runs").exists() or not list((_root() / "runs").iterdir())
    assert camp.resume_paused_entry(camp._load_queue()) is True
    assert _entries()[0]["status"] == "ready"


def test_a_refinement_launch_failure_keeps_the_parent(monkeypatch, run_loop_calls):
    parent = "run_000"
    _scaffold(parent, status="completed", pending_stage="completed_refined")
    entry = _entry(status="in_progress", run_ids=(parent,))
    entry["refinement_brief_path"] = "briefs/refine.yaml"
    _queue([entry])
    monkeypatch.setattr(camp, "_parse_refinement_brief_yaml", lambda path: {})

    def _bad_materialize(child_id, brief, brief_path):
        raise ValueError("refinement brief failed the B11 lint")
    monkeypatch.setattr(camp, "_materialize_refinement_run", _bad_materialize)
    assert camp.process_once() is False
    e = _entries()[0]
    assert e["status"] == "paused:launch_exception"
    assert e["run_ids"] == [parent]  # the parent stays the last run
    assert "refinement_brief_consumed_for" not in e
    child = e["launch_failed_run_id"]
    assert child and child != parent
    assert _state(child)["status"] == "abandoned_launch"
    assert _state(parent)["status"] == "completed"  # untouched
    assert camp.resume_paused_entry(camp._load_queue()) is True
    e = _entries()[0]
    assert e["status"] == "in_progress" and e["run_ids"] == [parent]


# ---- the protocol refusal's state write is guarded (review fix 7) ----------

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


# ---- one strict check (review fix 8) --------------------------------------

def test_the_duplicate_strict_helper_is_gone():
    assert not hasattr(rpr, "_strict_flag_value")
    assert not hasattr(camp, "_FLAG_RULES") and not hasattr(camp, "_flag_rules_check")
    _write_config({"grid_evaluation": {"enabled": "false"}})
    with pytest.raises(ValueError) as a:
        rpr._grid_evaluation_enabled()
    with pytest.raises(ValueError) as b:
        rpr._strict_orchestrator_flag("grid_evaluation")
    assert str(a.value) == str(b.value)


# ---- process_once uses the pre-flight's values (third-round fix 9) ---------

def test_process_once_reads_its_flags_from_the_single_parse(monkeypatch):
    _write_config(_flags(set(_CHAIN) - {"composition_runs"}) | {"schedulability_block":
                                                                {"enabled": True}})
    for module, name in ((rpr, "_decide_next_enabled"), (rpr, "_verdict_routing_retired_enabled"),
                         (camp, "_schedulability_block_enabled")):
        real = getattr(module, name)

        def _only_with_cfg(cfg=None, _real=real, _name=name):
            assert cfg is not None, f"{_name} re-read the config outside the pre-flight"
            return _real(cfg)
        monkeypatch.setattr(module, name, _only_with_cfg)
    _scaffold()
    _queue([_entry()])
    _reach_run_loop(monkeypatch)
    with pytest.raises(_Reached):
        camp.process_once()
    assert (_root() / "campaign_record" / "schedulability.yaml").exists()


# ---- the readers are the single source (third-round fix 10) ---------------

def test_every_config_flag_has_a_reader():
    real = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    flags = {n for n, s in real["orchestrator"].items() if isinstance(s, dict) and "enabled" in s}
    assert flags == set(camp._flag_readers())


def test_the_preflight_calls_every_real_reader_on_one_parse(monkeypatch):
    _write_config(_flags(_CHAIN))
    seen = {}
    for name, reader in camp._flag_readers().items():
        module = camp if name == "schedulability_block" else rpr

        def _spy(cfg=None, _name=name, _reader=reader):
            seen.setdefault(_name, set()).add(id(cfg) if cfg is not None else None)
            return _reader(cfg)
        monkeypatch.setattr(module, reader.__name__, _spy)
    values, refusal = camp._flag_preflight()
    assert refusal is None
    assert set(seen) == set(camp._flag_readers())
    ids = set().union(*seen.values())
    assert None not in ids and len(ids) == 1  # every call, the one parsed config


def _file_readers_verdict():
    values = {}
    for name, reader in camp._flag_readers().items():
        try:
            values[name] = reader()
        except (ValueError, AttributeError):
            return None
    return values


def test_the_preflight_agrees_with_the_readers_reading_the_file():
    """Readers handed the parsed config == readers reading the file themselves,
    over single flags, all-on-but-one and seeded random mixes."""
    import random
    names = list(camp._flag_readers())
    choices = (True, False, "false", None)
    rng = random.Random(1561)
    configs = [{}]
    configs += [{name: v} for name in names for v in choices]
    configs += [{n: (n != name) for n in names} for name in names]
    configs += [{n: rng.choice((True, True, False, False, "absent", "false", None)) for n in names}
                for _ in range(300)]
    for assignment in configs:
        orch_cfg = {n: {"enabled": v} for n, v in assignment.items() if v != "absent"}
        _write_config(orch_cfg)
        by_file = _file_readers_verdict()
        values, refusal = camp._flag_preflight()
        anti = bool(values.get("variant_anti_adjacency_gate"))  # its extra checks are file-free
        if by_file is None:
            assert refusal is not None, assignment
        elif not anti:
            assert refusal is None, (assignment, refusal)
            assert values == by_file, assignment


# ---- schedulability still written (review fix 10) -------------------------

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


# ===========================================================================
# Fourth-round review fixes
# ===========================================================================

def _outcome(fn):
    try:
        return ("ok", fn())
    except Exception as e:  # the parity is on the exact exception
        return (type(e).__name__, str(e))


def test_expected_protocol_raises_exactly_where_generation_raises():
    """Fourth-round fix 5: over well-formed and malformed inputs,
    _expected_generated_protocol and _ensure_protocol_from_constraints either
    both succeed with the same protocol or both raise the same exception."""
    hs, _he = rpr._load_holdout_range()
    import datetime as _dt
    past_seal = (_dt.date.fromisoformat(str(hs)) + _dt.timedelta(days=40)).isoformat()
    good = _generated_constraints(_NON_GENERIC)["protocol"]
    cases = [good, {**good, "symbols": []},
             {k: v for k, v in good.items() if k != "symbols"},
             {k: v for k, v in good.items() if k != "start"},
             {k: v for k, v in good.items() if k != "end"},
             {k: v for k, v in good.items() if k != "promotion"},
             {**good, "promotion": None}, {**good, "promotion": {}},
             {**good, "per_symbol_start": {"BTCUSDT": "2022-02-01"}},
             {**good, "per_symbol_start": {}},
             {**good, "end": past_seal},
             {**good, "timeframe": "4h", "holdout": {"start": "x", "end": "y"}}]
    for n, gen in enumerate(cases):
        run_id = f"run_{300 + n:03d}"
        run_dir = _scaffold(run_id)
        expected = _outcome(lambda: camp._expected_generated_protocol(gen, run_id))

        def _generate():
            path = rpr._ensure_protocol_from_constraints(run_dir, run_id, {"protocol": gen})
            return json.loads(path.read_text(encoding="utf-8"))
        assert _outcome(_generate) == expected, (n, gen)


@pytest.mark.parametrize("section", [False, True, "false", 0, ["enabled"]])
def test_a_flag_section_that_is_not_a_mapping_is_refused(section):
    _write_config({"data_availability_gate": section})
    refusal = camp._flag_preflight_refusal()
    assert refusal and "orchestrator.data_availability_gate is not a mapping" in refusal
    _write_config({"halt_policy": "off"})
    assert "orchestrator.halt_policy is not a mapping" in camp._flag_preflight_refusal()


def test_launch_exception_resume_restores_the_prior_status(monkeypatch, run_loop_calls):
    """Fourth-round fix 4: a refinement entry that was `ready` (another lineage
    in progress) goes back to `ready`, never a second in_progress lineage."""
    parent = "run_000"
    _scaffold(parent, status="completed", pending_stage="completed_refined")
    refine = _entry(status="ready", run_ids=(parent,))
    refine["refinement_brief_path"] = "briefs/refine.yaml"
    _queue([refine])
    monkeypatch.setattr(camp, "_parse_refinement_brief_yaml", lambda path: {})
    monkeypatch.setattr(camp, "_materialize_refinement_run",
                        lambda *a: (_ for _ in ()).throw(ValueError("B11 lint")))
    assert camp.process_once() is False
    e = _entries()[0]
    assert e["status"] == "paused:launch_exception" and e["launch_prior_status"] == "ready"
    q = camp._load_queue()
    q["queue"].append({"id": "LIVE", "brief_path": "briefs/x.md", "status": "in_progress",
                       "priority": 1, "run_ids": ["run_777"], "outcome": None})
    camp._save_queue(q)
    assert camp.resume_paused_entry(camp._load_queue()) is True
    statuses = {x["id"]: x["status"] for x in _entries()}
    assert statuses == {ENTRY: "ready", "LIVE": "in_progress"}
    assert "launch_prior_status" not in _entries()[0]


def test_hitl_non_proceed_resume_still_writes_schedulability(monkeypatch):
    """Fourth-round fix 7: the flag values are read for every resolution."""
    _stage_hitl(resolution="unresolvable")
    _write_config({"schedulability_block": {"enabled": True}})
    monkeypatch.setattr(rpr, "resume_pipeline",
                        lambda run_id: (_ for _ in ()).throw(RuntimeError("closing failed")))
    path = _root() / "campaign_record" / "schedulability.yaml"
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert _entries()[0]["status"] == "paused:stage_exception"
    assert path.exists()


@pytest.mark.parametrize("content", ["- not\n- a mapping\n", "just a string\n"])
def test_a_malformed_resolution_is_a_classified_refusal(monkeypatch, content):
    """Fourth-round fix 8: parsed inside the classified handling."""
    run_dir = _stage_hitl()
    (run_dir / "artifacts" / "human_resolution.yaml").write_text(content, encoding="utf-8")
    monkeypatch.setattr(rpr, "resume_pipeline", lambda run_id: pytest.fail("resumed"))
    assert camp.resume_paused_entry(camp._load_queue()) is False
    assert _entries()[0]["status"] == "paused:data_block_hitl"
    log = _log_text()
    assert "RESUME REFUSED" in log and "HALT — data_block_hitl" in log
    st = _state()
    assert st["halt_history"][-1]["reason"] == "data_block_hitl"
    assert "human_resolution.yaml is not a mapping" in st["last_error"]


def _card_run(run_id, *, abandoned=False):
    run_dir = _scaffold(run_id, status="abandoned_launch" if abandoned else "active")
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(yaml.safe_dump({
        "hypothesis_id": "H-DUP", "target_market": "BTCUSDT", "timeframe": "1h",
        "thesis": "Oversold RSI pullbacks revert."}), encoding="utf-8")
    return run_dir


def test_scanners_skip_an_abandoned_launch():
    """Fourth-round fix 9: the exclusion digest (tried-ideas input), the near-miss
    scoreboard and the replay repeat gate never count an abandoned launch's
    card; reconcile_orphans treats it as known."""
    sys.path.insert(0, str(_SR / "tools"))
    import build_exclusion_digest as bed
    import near_miss_scoreboard as nms
    import replay_repeat_gate as rrg
    import abandoned_launch as al
    _card_run("run_001")
    _card_run("run_002", abandoned=True)
    runs = _root() / "runs"
    assert al.is_abandoned_launch(runs / "run_002") and not al.is_abandoned_launch(runs / "run_001")
    digest = bed.scan_run_triples(runs)
    assert digest["runs_scanned"] == 1
    run_ids = [rid for fam in digest["families"].values() for t in fam["triples"]
               for rid in t["run_ids"]]
    assert run_ids == ["run_001"]
    assert [r.get("run_id") for r in nms.build_scoreboard(runs)] == ["run_001"]
    assert [p.name for p in rrg.run_dirs_in_order(runs)] == ["run_001"]
    assert camp.ABANDONED_LAUNCH_STATUS == al.ABANDONED_LAUNCH_STATUS
