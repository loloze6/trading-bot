"""
D-138 (branch independence PR 1, card M): step 1a's extra hypothesis cards are
enqueued as soon as 1a is recorded completed, whatever fails later in the run.
Behind orchestrator.extra_cards_at_1a.enabled (off by default).

Found on run_094 (2026-10-14): 1a completed, protocol_execution then raised, the
run ended `failed`, and the enqueue after run_loop logged "NOT enqueued -- step 1a
did not complete cleanly (status='failed')". The card reached the queue only when
the operator resumed the run and it completed.

All synthetic: no LLM, no backtest, no trial row, no holdout.
  * flag off: byte-identical (run_loop called with the run id only; a failed run
    still enqueues nothing);
  * flag on: the cards are in the queue before the later stages run, and stay
    there after a failure, a pause or an exception; one queue entry per card;
    the same entries as flag off on a run that did not fail; a 1a that did not
    complete enqueues nothing;
  * the real run_loop calls the hook once, right after 1a is recorded completed.
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

from test_halt_quarantine_policy import (  # noqa: E402
    _save_queue_entries, _write_campaign_state, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_s2a_decide_next import _ALL_ON, _write_flags  # noqa: E402
from test_e059_s2b_briefs import _brief, _owner, _protocol, _stage_cards  # noqa: E402

_CARD_IDS = ["OWNER__h2", "OWNER__h3"]
_NOT_ENQUEUED = "NOT enqueued -- step 1a did not complete cleanly"


def _queue(campaign_root) -> list:
    return yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]


def _ids(campaign_root) -> list:
    return [e["id"] for e in _queue(campaign_root)]


def _log(root: Path) -> str:
    path = root / "campaign_log.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    return re.sub(r"^- \S+Z ", "- ", text, flags=re.M)


def _setup(campaign_root, **flags):
    root = campaign_root["root"]
    _write_flags(root, **flags)
    _brief(root)
    _protocol(root)
    _save_queue_entries(campaign_root["queue_path"], [_owner(status="ready")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[])
    return root


def _do_1a(root: Path, run_id: str) -> Path:
    """What a completed step 1a leaves: the real flag-on split (three cards, two
    extra), then 1a recorded in completed_stages as run_loop's step 6 does."""
    run_dir = root / "runs" / run_id
    _stage_cards(run_dir, n=3, context=False)  # process_once wrote the context
    assert rpr._handle_hypothesis_generation_multi_card_split(run_id, run_dir)
    rpr.update_state(path=run_dir, status="active", current_stage="hypothesis_generation",
                     pending_stage="strategy_config_authoring",
                     completed_stages=["hypothesis_generation"])
    return run_dir


def _fail(run_dir):
    rpr.update_state(path=run_dir, status="failed", current_stage="protocol_execution",
                     pending_stage="protocol_execution",
                     last_error="grid evaluation raised CompositeError (synthetic)")


def _pause(run_dir):
    rpr.update_state(path=run_dir, status="paused_for_human", pending_stage="human_pause")


def _raise(run_dir):
    raise RuntimeError("synthetic exception after 1a")


_LATER = {"failed": _fail, "paused": _pause, "raises": _raise}


def _on_run_loop(campaign_root, later, seen):
    """Fake run_loop honouring the real contract: after_1a right after 1a is
    recorded completed, then the later stages (here: one outcome)."""
    root = campaign_root["root"]

    def fake_run_loop(run_id, *, after_1a=None):
        run_dir = _do_1a(root, run_id)
        seen["after_1a_given"] = after_1a is not None
        if after_1a is not None:
            after_1a()
        seen["queue_when_later_stages_start"] = _ids(campaign_root)
        later(run_dir)
    return fake_run_loop


def _off_run_loop(campaign_root, later):
    """The flag-off call is run_loop(run_id) -- a keyword would raise TypeError here."""
    root = campaign_root["root"]

    def fake_run_loop(run_id):
        later(_do_1a(root, run_id))
    return fake_run_loop


def _assert_cards_queued_once(campaign_root):
    queue = _queue(campaign_root)
    ids = [e["id"] for e in queue]
    assert ids.count("OWNER__h2") == 1 and ids.count("OWNER__h3") == 1
    for e in queue[1:]:
        assert e["status"] == "queued" and e["origin"] == "brief" and e["priority"] == 999
    q = yaml.safe_load((campaign_root["root"] / "runs" / "run_001" / "artifacts" /
                        "queued_hypotheses.yaml").read_text(encoding="utf-8"))
    assert q["enqueued"] is True


# ---------------------------------------------------------------------------
# The flag
# ---------------------------------------------------------------------------

def test_flag_reader(campaign_root):
    root = campaign_root["root"]
    _write_flags(root)
    assert rpr._extra_cards_at_1a_enabled() is False
    _write_flags(root, extra_cards_at_1a="true")
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._extra_cards_at_1a_enabled()
    _write_flags(root, extra_cards_at_1a=True)  # no dependency
    assert rpr._extra_cards_at_1a_enabled() is True
    assert camp._flag_readers()["extra_cards_at_1a"] is rpr._extra_cards_at_1a_enabled


def test_flag_is_off_in_the_real_config_and_registered():
    cfg = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["extra_cards_at_1a"]["enabled"] is False
    reg = yaml.safe_load((_SR / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    entry = next(f for f in reg["flags"] if f["name"] == "extra_cards_at_1a")
    assert entry["state"] == "off_incomplete"
    assert entry["reader"] == "run_phase1_research._extra_cards_at_1a_enabled"


# ---------------------------------------------------------------------------
# Flag off: byte-identical
# ---------------------------------------------------------------------------

def _off_step(campaign_root, monkeypatch, flags, later):
    root = _setup(campaign_root, **flags)
    monkeypatch.setattr(rpr, "run_loop", _off_run_loop(campaign_root, later))
    camp.process_once()
    return (campaign_root["queue_path"].read_bytes(), _log(root))


@pytest.mark.parametrize("later", ["failed", "paused"])
def test_flag_off_is_byte_identical(campaign_root, monkeypatch, later):
    """Key absent and `false` give the same queue file and log, and that is
    master's behaviour: a failed run enqueues nothing ("NOT enqueued"), a paused
    one enqueues after run_loop."""
    root = campaign_root["root"]
    absent = _off_step(campaign_root, monkeypatch, _ALL_ON, _LATER[later])
    # reset the sandbox, then the same step with the key written false
    import shutil
    shutil.rmtree(root / "runs")
    (root / "runs").mkdir()
    shutil.rmtree(root / "campaign_record", ignore_errors=True)
    (root / "campaign_log.md").unlink()
    off = _off_step(campaign_root, monkeypatch, {**_ALL_ON, "extra_cards_at_1a": False},
                    _LATER[later])
    assert off == absent
    if later == "failed":
        assert _ids(campaign_root) == ["OWNER"]
        assert _NOT_ENQUEUED in off[1]
    else:
        assert _ids(campaign_root) == ["OWNER"] + _CARD_IDS
        assert _NOT_ENQUEUED not in off[1]


def test_flag_on_without_decide_next_calls_run_loop_as_before(campaign_root, monkeypatch):
    """No decide_next: no extra cards exist, and run_loop gets no hook."""
    _setup(campaign_root, extra_cards_at_1a=True)
    called = []
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: called.append(run_id))
    camp.process_once()
    assert called == ["run_001"]


# ---------------------------------------------------------------------------
# Flag on: queued at 1a, kept whatever fails later
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("later", ["failed", "paused", "raises"])
def test_flag_on_cards_queued_at_1a_and_kept_after_a_later_failure(campaign_root, monkeypatch,
                                                                   later):
    root = _setup(campaign_root, **_ALL_ON, extra_cards_at_1a=True)
    seen = {}
    monkeypatch.setattr(rpr, "run_loop", _on_run_loop(campaign_root, _LATER[later], seen))
    camp.process_once()
    assert seen["after_1a_given"] is True
    # in the queue before any later stage ran
    assert seen["queue_when_later_stages_start"] == ["OWNER"] + _CARD_IDS
    # and still there, once each, after the failure / pause / exception and the
    # halt that saved the queue
    _assert_cards_queued_once(campaign_root)
    assert _NOT_ENQUEUED not in _log(root)
    assert _log(root).count("2 extra hypothesis card(s) in the queue") == 1


def test_flag_on_a_1a_that_did_not_complete_enqueues_nothing(campaign_root, monkeypatch):
    """The split wrote queued_hypotheses.yaml, then a later 1a check raised: 1a
    is never recorded completed, so the hook never fires and the enqueue after
    run_loop refuses, as before."""
    root = _setup(campaign_root, **_ALL_ON, extra_cards_at_1a=True)

    def fake_run_loop(run_id, *, after_1a=None):
        run_dir = root / "runs" / run_id
        _stage_cards(run_dir, n=3, context=False)
        assert rpr._handle_hypothesis_generation_multi_card_split(run_id, run_dir)
        rpr.update_state(path=run_dir, status="failed", last_error="a later 1a check raised")
    monkeypatch.setattr(rpr, "run_loop", fake_run_loop)
    camp.process_once()
    assert _ids(campaign_root) == ["OWNER"]
    assert _NOT_ENQUEUED in _log(root)
    q = yaml.safe_load((root / "runs" / "run_001" / "artifacts" / "queued_hypotheses.yaml")
                       .read_text(encoding="utf-8"))
    assert q["enqueued"] is False


def test_flag_on_paused_run_gives_the_same_queue_as_flag_off(campaign_root, monkeypatch):
    """A run that does not fail after 1a: the same queue file, byte for byte,
    flag on (enqueued at 1a) and flag off (enqueued after run_loop)."""
    import shutil
    root = campaign_root["root"]
    off = _off_step(campaign_root, monkeypatch, _ALL_ON, _pause)[0]
    shutil.rmtree(root / "runs")
    (root / "runs").mkdir()
    shutil.rmtree(root / "campaign_record", ignore_errors=True)
    (root / "campaign_log.md").unlink()
    _setup(campaign_root, **_ALL_ON, extra_cards_at_1a=True)
    monkeypatch.setattr(rpr, "run_loop", _on_run_loop(campaign_root, _pause, {}))
    camp.process_once()
    assert campaign_root["queue_path"].read_bytes() == off


def _record_children_after(campaign_root, flag_on: bool, status: str) -> bytes:
    """_record_run_loop_children on a run whose 1a completed and which then
    ended `status`; under the flag the hook ran at 1a first."""
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _brief(root)
    owner = _owner(status="in_progress")
    _save_queue_entries(campaign_root["queue_path"], [owner])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_001"])
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    (root / "runs" / "run_001" / "artifacts" / "brief_hypotheses_context.yaml").write_text(
        "already_produced: []\n", encoding="utf-8")
    run_dir = _do_1a(root, "run_001")
    queue = camp._load_queue()
    entry = queue["queue"][0]
    kw = {}
    if flag_on:
        holder = {"wrote": False}
        camp._extra_cards_at_1a_hook(entry, "run_001", holder)()
        assert holder["wrote"] is True
        kw = {"cards_at_1a": holder}
    rpr.update_state(path=run_dir, status=status)
    queue, entry, _ = camp._record_run_loop_children(queue, entry, "run_001", [], True, **kw)
    camp._save_queue(queue)  # what process_once does with the in-memory queue next
    return campaign_root["queue_path"].read_bytes()


@pytest.mark.parametrize("status", ["completed", "active"])
def test_normal_completion_same_entries_as_flag_off(campaign_root, status):
    off = _record_children_after(campaign_root, False, status)
    import shutil
    shutil.rmtree(campaign_root["root"] / "runs" / "run_001")
    shutil.rmtree(campaign_root["root"] / "campaign_record")
    on = _record_children_after(campaign_root, True, status)
    assert on == off
    assert _ids(campaign_root) == ["OWNER"] + _CARD_IDS


def test_later_enqueue_is_a_no_op_after_the_hook(campaign_root):
    _record_children_after(campaign_root, True, "failed")
    before = campaign_root["queue_path"].read_bytes()
    entry = _queue(campaign_root)[0]
    assert camp._enqueue_queued_hypotheses(entry, "run_001", whatever_fails_later=True) is False
    assert camp._enqueue_queued_hypotheses(entry, "run_001") is False
    assert campaign_root["queue_path"].read_bytes() == before
    _assert_cards_queued_once(campaign_root)


@pytest.mark.parametrize("fail_at", ["first_register", "marking_enqueued"])
def test_a_failing_hook_is_logged_and_the_cards_are_enqueued_after_the_run(campaign_root,
                                                                         monkeypatch, fail_at):
    """`marking_enqueued`: every card is registered, then the hook fails -- the
    enqueue after the run registers nothing new, so only the hook's holder makes
    process_once re-read the queue before saving it."""
    root = _setup(campaign_root, **_ALL_ON, extra_cards_at_1a=True)
    if fail_at == "first_register":
        real_register, calls = camp.register_hypothesis, []

        def flaky(*a, **k):
            calls.append(k.get("entry_id"))
            if len(calls) == 1:
                raise OSError("synthetic: queue file locked")
            return real_register(*a, **k)
        monkeypatch.setattr(camp, "register_hypothesis", flaky)
    else:
        real_save, failed = rpr.save_yaml, []

        def flaky_save(path, data, *a, **k):
            if (Path(path).name == "queued_hypotheses.yaml" and data.get("enqueued")
                    and not failed):
                failed.append(path)
                raise OSError("synthetic: queue file locked")
            return real_save(path, data, *a, **k)
        monkeypatch.setattr(rpr, "save_yaml", flaky_save)
    monkeypatch.setattr(rpr, "run_loop", _on_run_loop(campaign_root, _fail, {}))
    camp.process_once()
    log = _log(root)
    assert "not enqueued when step 1a completed (OSError: synthetic: queue file locked)" in log
    _assert_cards_queued_once(campaign_root)
    state = yaml.safe_load((root / "runs" / "run_001" / "pipeline_state.yaml")
                           .read_text(encoding="utf-8"))
    assert state["last_error"].startswith("grid evaluation raised")  # the run's own failure


# ---------------------------------------------------------------------------
# The real run_loop calls the hook once, right after 1a is recorded completed
# ---------------------------------------------------------------------------

def _real_run_loop_run(campaign_root, monkeypatch, after_1a_check=None):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    (run_dir / "artifacts" / "brief_hypotheses_context.yaml").write_text(
        "already_produced: []\n", encoding="utf-8")
    for stage in ("hypothesis_generation", "strategy_config_authoring"):
        rpr.save_yaml(run_dir / "handoffs" / rpr.STAGE_CONFIGS[stage]["handoff"],
                      {"required_inputs": [], "deliverables": []})
    monkeypatch.setattr(rpr, "_check_specialist_readers_preflight", lambda run_dir: None)
    invoked = []

    def agent(stage, run_id, run_dir_, expected, state):
        invoked.append(stage)
        if stage == "hypothesis_generation":
            _stage_cards(run_dir_, n=3, context=False)
            raise FileNotFoundError("hypothesis_card.yaml")  # three cards, not one
        raise RuntimeError(f"synthetic failure in {stage}")
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", agent)
    hook_calls = []

    def hook():
        state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
        hook_calls.append((list(state["completed_stages"]), state["status"], list(invoked)))
    rpr.run_loop("run_001", after_1a=hook)
    return run_dir, hook_calls, invoked


def test_real_run_loop_calls_after_1a_once_when_1a_is_recorded(campaign_root, monkeypatch):
    run_dir, hook_calls, invoked = _real_run_loop_run(campaign_root, monkeypatch)
    # once, after 1a was recorded completed and before the next stage was invoked
    assert hook_calls == [(["hypothesis_generation"], "active", ["hypothesis_generation"])]
    assert invoked == ["hypothesis_generation", "strategy_config_authoring"]
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "failed" and "strategy_config_authoring" in state["last_error"]


def test_real_run_loop_does_not_call_after_1a_when_1a_fails(campaign_root, monkeypatch):
    def refuse(*a, **k):
        raise ValueError("synthetic: a later 1a check refused the output")
    monkeypatch.setattr(rpr, "_write_pass_rule_from_card", refuse)
    run_dir, hook_calls, invoked = _real_run_loop_run(campaign_root, monkeypatch)
    assert hook_calls == [] and invoked == ["hypothesis_generation"]
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "failed"
    assert "hypothesis_generation" not in (state.get("completed_stages") or [])
