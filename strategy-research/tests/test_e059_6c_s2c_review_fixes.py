"""
E-059 S3 / slice 6c S2c -- code-review fixes (orchestrator.verdict_routing_retired).
Each test here fails on df5725c7 (the reviewed commit):
  1. R2 terminates: a parked R2 request counts as EMPTY.
  2. Only a genuinely missing class parks; one shared component_class_status.
  3. The crash window: a parked run found before run_loop is parked, never re-run.
  4. A decide-next failure after a park is retried on the next launch.
  5. Only a fetchable data shortfall parks (SealedDataError, reserved/unknown
     feed, Layer 1, the sealed range, a refine: previous behaviour).
  6. A parked owner keeps its brief R2-eligible.
  7. The locked, idempotent appender for data_requests.yaml.
  9. --unpark refreshes loop_health / schedulability.
 10. The CLI calls _unpark_entry directly; resume_paused_entry has no unpark mode.
No LLM, no backtest, no trial row, no holdout read (the sealed range is taken
from the policy file, never written as a literal here).
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import campaign_review_retired as crr  # noqa: E402
import decide_next as dn  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _entry, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_6c_s2c_parked_states import (  # noqa: E402
    FOO, V12, _gate_doc, _gate_run, _minimal_run, _nt, _ok, _parked_entry, _parking_run_loop,
    _queue, _stage_park_queue, _state, _v12, _v12_line, _write_component, _write_variant_gate,
    tbot,  # noqa: F401  (autouse fixture)
    _stub_tbot_python,  # noqa: F401  (autouse fixture)
)


def _seal() -> tuple:
    return rpr._load_holdout_range()


# ---------------------------------------------------------------------------
# 1. R2 terminates
# ---------------------------------------------------------------------------

def test_a_brief_whose_every_card_parks_stops_r2():
    owner = {"id": "B", "brief_path": "briefs/b.md", "status": "done", "outcome": "refuted",
             "brief_status": dn.BRIEF_OPEN, "priority": 1, "run_ids": ["run_1"]}
    reqs = [{"id": f"B__more_{n}", "brief_path": "briefs/b.md", "origin": dn.ORIGIN_BRIEF,
             "status": "paused:waiting_for_component", "priority": 999, "run_ids": [f"run_{n + 1}"]}
            for n in range(1, dn.BRIEF_MAX_CONSECUTIVE_EMPTY_R2 + 1)]
    entries = [owner, *reqs]
    assert dn.consecutive_empty_r2(owner, entries) == [r["id"] for r in reqs]
    updates = camp._brief_updates({"queue": entries}, reqs[-1])
    assert updates["B"]["brief_status"] == dn.BRIEF_EXHAUSTED
    # an unparked card is outstanding again: it neither counts nor breaks the streak
    reqs[-1]["status"] = "ready"
    assert dn.r2_request_yielded(reqs[-1]) is None


# ---------------------------------------------------------------------------
# 2. Only a genuinely missing class parks
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("line", [
    # an ImportError inside an existing module
    ("VIOLATION V12 strategies.regimes.t.components[0].class: cannot load "
     f"'{FOO}': Cannot load component class '{FOO}': No module named 'numpyy'"),
    _v12_line(module="strategies.strategy_componentz"),        # module typo
    ("VIOLATION V12 strategies.regimes.t.components[0].class: cannot load 'FooComponent': "
     "not enough values to unpack (expected 2, got 1)"),       # dotless path
    _v12_line(cls="ExistingComponent"),                        # defined after all
])
def test_a_v12_that_is_not_a_missing_class_never_parks(line):
    assert rpr._v12_missing_classes(line) == []
    assert rpr._variant_park_kind({"base": _v12(line)}) == (None, [])


def test_a_genuinely_missing_class_parks():
    assert rpr._v12_missing_classes(V12) == [FOO]


def test_one_shared_class_check_with_one_scope(tbot):
    _write_component(tbot, "FooComponent")
    for path in dn.known_component_classes(tbot):
        assert dn.component_class_status(tbot, path) == "defined"
    assert dn.component_class_status(tbot, "strategies.strategy_components.Nope") == "missing"
    assert dn.component_class_status(tbot, "strategies.other_module.FooComponent") == "invalid"
    # --unpark uses the same function (no private copy)
    src = inspect.getsource(camp._unpark_entry)
    assert "dn.component_class_status(" in src
    assert not hasattr(camp, "_parked_class_defined")


def test_5a_import_error_stays_the_pause(monkeypatch):
    run_dir = _minimal_run(rpr.ROOT, "run_960")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": _v12(_v12_line(module="strategies.strategy_componentz"))}})
    rpr.save_yaml(rpr.ROOT / "config" / "campaign_config.yaml",
                  {"orchestrator": {"config_direct_authoring": {"enabled": True}}})
    assert rpr._route_post_config_direct_backtest_specification(run_dir, routing_retired=True) == \
        "human_pause"
    assert rpr.PARKED_KEY not in _state(run_dir)


# ---------------------------------------------------------------------------
# 3. The crash window and 4. the retryable decision
# ---------------------------------------------------------------------------

def _no_run_loop(run_id):
    raise AssertionError(f"run_loop must never run on the parked {run_id}")


def test_a_parked_run_whose_queue_save_was_lost_is_parked_before_run_loop(campaign_root,
                                                                          monkeypatch):
    _stage_park_queue(campaign_root)
    # the run parked, then the process died before the queue was saved
    rpr._park_run(campaign_root["runs_dir"] / "run_062", kind="component",
                  stage="strategy_config_authoring", reason="component_gap: x", request_refs=[],
                  resume_stage="strategy_config_authoring")
    assert next(e for e in _queue(campaign_root) if e["id"] == "PARK_ME")["status"] == "in_progress"
    monkeypatch.setattr(rpr, "run_loop", _no_run_loop)
    assert camp.process_once() is True
    entry = next(e for e in _queue(campaign_root) if e["id"] == "PARK_ME")
    assert entry["status"] == "paused:waiting_for_component"
    state = _state(campaign_root["runs_dir"] / "run_062")
    assert state["status"] == "paused_for_human" and state[rpr.PARKED_KEY]["kind"] == "component"


def test_a_decide_next_failure_after_a_park_is_retried(campaign_root, monkeypatch):
    _stage_park_queue(campaign_root)
    monkeypatch.setattr(rpr, "run_loop", _parking_run_loop(campaign_root))
    real_decide = dn.decide

    def _boom(*a, **k):
        raise RuntimeError("decide-next exploded")
    monkeypatch.setattr(dn, "decide", _boom)
    with pytest.raises(RuntimeError, match="exploded"):
        camp.process_once()
    entry = next(e for e in _queue(campaign_root) if e["id"] == "PARK_ME")
    assert entry["status"] == "in_progress"  # not parked on disk before the decision
    root = campaign_root["root"]
    assert not (root / "runs" / "run_062" / "artifacts" / "parked").exists()

    monkeypatch.setattr(dn, "decide", real_decide)
    monkeypatch.setattr(rpr, "run_loop", _no_run_loop)  # the retry never re-runs the run
    assert camp.process_once() is True
    queue = _queue(campaign_root)
    assert next(e for e in queue if e["id"] == "PARK_ME")["status"] == "paused:waiting_for_component"
    assert (root / "runs" / "run_062" / "artifacts" / "parked" / "park_1" /
            "decision_record.yaml").exists()
    history = _state(root / "runs" / "run_062")["halt_history"]
    assert sum(1 for h in history if "parked" in h) == 1
    log = (root / "campaign_log.md").read_text(encoding="utf-8")
    assert log.count("The campaign continues; unpark with --unpark PARK_ME") == 1
    assert "retrying the decision after this park" in log


def test_runbook_decide_next_row_names_the_park_retry():
    runbook = (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    row = next(ln for ln in runbook.splitlines()
               if ln.startswith("| `decide_next stop: no_eligible_candidate`"))
    assert "the same holds after a park" in row and "BEFORE `run_loop`" in row


# ---------------------------------------------------------------------------
# 5. Only a fetchable data shortfall parks
# ---------------------------------------------------------------------------

def test_a_plain_shortfall_outside_the_seal_is_fetchable():
    assert rpr._gate_shortfall_fetchable(_gate_doc()) is True


def _sealed_window() -> dict:
    start, end = _seal()
    return _gate_doc(start=start, end=end)


@pytest.mark.parametrize("make", [
    lambda: _gate_doc(fetch_error="SealedDataError: request window touches the sealed range"),
    lambda: _gate_doc(fetch_error="ConnectionError: offline"),
    lambda: _gate_doc(layer=1, reason="window end is entirely before BTCUSDT's confirmed earliest "
                                      "OHLCV date -- impossible at the source"),
    _sealed_window,
    lambda: _gate_doc(outcome="refine"),
    lambda: {**_gate_doc(), "windows": [{**_gate_doc()["windows"][0], "outcome": "validate"}],
             "aux_feeds": [{"feed": "whale_x", "label": "w1", "start": "2021-01-01",
                            "end": "2021-03-31", "outcome": "decline", "missing_fraction": 1.0,
                            "reason": "'whale_x' is a RESERVED feed (deny-by-default)"}]},
    lambda: {**_gate_doc(), "windows": [{**_gate_doc()["windows"][0], "outcome": "validate"}],
             "aux_feeds": [{"feed": "nope", "label": "w1", "start": "2021-01-01",
                            "end": "2021-03-31", "outcome": "decline", "missing_fraction": 1.0,
                            "reason": "'nope' is not a known feed (not in FEED_REGISTRY)"}]},
])
def test_an_unfetchable_shortfall_is_not(make):
    assert rpr._gate_shortfall_fetchable(make()) is False


def test_the_gate_tool_still_emits_the_markers_this_reads():
    src = (_SR / "tools" / "data_availability_gate.py").read_text(encoding="utf-8")
    for marker in rpr._UNFETCHABLE_AUX_REASON_MARKERS:
        assert marker in src
    assert '"fetch_error": f"{type(e).__name__}: {e}"' in src and '"layer": 1' in src


def test_single_gate_sealed_decline_keeps_the_terminal_rejection(monkeypatch):
    run_dir = _gate_run(monkeypatch, "run_961", variant_loop=False)
    rpr.save_yaml(run_dir / "artifacts" / "data_availability_gate.yaml",
                  _gate_doc(fetch_error="SealedDataError: sealed"))
    rpr.run_loop("run_961")
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_rejected" and rpr.PARKED_KEY not in state
    assert not (rpr.ROOT / "campaign_record" / "data_requests.yaml").exists()


def test_single_gate_refine_keeps_the_pause(monkeypatch):
    run_dir = _gate_run(monkeypatch, "run_962", variant_loop=False)
    rpr.save_yaml(run_dir / "artifacts" / "data_availability_gate.yaml", _gate_doc("refine"))
    rpr.run_loop("run_962")
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and rpr.PARKED_KEY not in state
    assert state["pending_stage"] == "data_availability_gate"


def test_per_variant_sealed_decline_keeps_the_pause(monkeypatch):
    run_dir = _gate_run(monkeypatch, "run_963", variant_loop=True)
    reason = "data_availability_gate outcome=decline: sealed"
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": _ok(), "a": _nt(reason), "b": _nt(reason)}})
    _write_variant_gate(run_dir, "a", _gate_doc(fetch_error="SealedDataError: sealed"))
    _write_variant_gate(run_dir, "b")
    rpr.run_loop("run_963")
    state = _state(run_dir)
    assert state["flags"]["variant_gate_insufficient"] is True and rpr.PARKED_KEY not in state


def test_no_runbook_text_points_at_the_sealed_store():
    for doc in ("RUNBOOK.md", "HALT_RECOVERY.md"):
        assert "holdout_sealed" not in (_SR / "docs" / doc).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 6. A parked owner keeps its brief eligible
# ---------------------------------------------------------------------------

def test_a_parked_owner_stays_r2_eligible():
    owner = {"id": "B", "brief_status": dn.BRIEF_OPEN, "status": "paused:waiting_for_data"}
    assert dn.r2_eligible_owner(owner) is True
    assert dn.r2_eligible_owner({**owner, "status": "paused:unhandled_exception"}) is False


# ---------------------------------------------------------------------------
# 7. The locked, idempotent appender
# ---------------------------------------------------------------------------

def test_park_unpark_cycles_add_no_duplicate_data_request(monkeypatch):
    for _ in range(2):
        run_dir = _gate_run(monkeypatch, "run_964", variant_loop=False)
        rpr.save_yaml(run_dir / "artifacts" / "data_availability_gate.yaml", _gate_doc())
        rpr.run_loop("run_964")
        assert _state(run_dir)[rpr.PARKED_KEY]["kind"] == "data"
    rows = yaml.safe_load((rpr.ROOT / "campaign_record" / "data_requests.yaml")
                          .read_text(encoding="utf-8"))["requests"]
    assert len(rows) == 1


def test_append_requests_key_dedupes_within_and_across_calls(tmp_path):
    path = tmp_path / "data_requests.yaml"
    row = {"run_id": "r", "stage": "s", "variant_id": None, "reason": "x"}
    assert crr.append_requests(path, [row, dict(row)], key=crr.request_key) == 1
    assert crr.append_requests(path, [row, {**row, "reason": "y"}], key=crr.request_key) == 1
    assert len(yaml.safe_load(path.read_text(encoding="utf-8"))["requests"]) == 2


def test_flag_off_per_variant_writer_is_unchanged(tmp_path):
    rows = [{"variant_id": "a", "outcome": "decline", "reason": "r"}]
    rpr._append_data_requests("run_1", rows)
    rpr._append_data_requests("run_1", rows)  # flag off: appended as before, no dedupe
    doc = yaml.safe_load((rpr.ROOT / "campaign_record" / "data_requests.yaml")
                         .read_text(encoding="utf-8"))
    assert len(doc["requests"]) == 2


# ---------------------------------------------------------------------------
# 9. + 10. --unpark
# ---------------------------------------------------------------------------

def test_unpark_refreshes_loop_health_and_schedulability(campaign_root, monkeypatch, tbot):
    _parked_entry(campaign_root)
    _write_component(tbot)
    health = campaign_root["root"] / "campaign_record" / "loop_health.yaml"
    health.unlink(missing_ok=True)
    wrote = []
    monkeypatch.setattr(camp, "_schedulability_block_enabled", lambda: True)
    monkeypatch.setattr(camp, "_write_schedulability", lambda: wrote.append(1))
    assert camp._unpark_entry("PARK_ME") is True
    assert health.exists() and wrote == [1]


def test_cli_calls_unpark_directly_and_resume_has_no_unpark_mode():
    assert list(inspect.signature(camp.resume_paused_entry).parameters) == ["queue"]
    src = (_SR / "workflow" / "run_campaign.py").read_text(encoding="utf-8")
    assert "sys.exit(0 if _unpark_entry(args.unpark) else 1)" in src
