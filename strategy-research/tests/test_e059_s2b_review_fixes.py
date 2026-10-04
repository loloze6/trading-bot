"""
E-059 S2b code-review fixes (review of 754cc2a3..b910554f). One regression
test (or more) per fix; each fails on b910554f. All synthetic: no LLM, no
backtest, no trial row, no holdout.
"""
from __future__ import annotations

import copy
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
import decide_next as dn  # noqa: E402
import reader_proposals as rp  # noqa: E402
import record_schema as rs  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _save_queue_entries, _write_campaign_state, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_s2a_decide_next import _ALL_ON, _write_flags, _decide  # noqa: E402
from test_e059_s2b_briefs import (  # noqa: E402
    _SCORES, _brief, _card_entry, _empty_inputs, _owner, _stage_cards,
)


def _request(eid, owner="OWNER", status="done", outcome=None, run_ids=()):
    e = {**_card_entry(eid, owner=owner, status=status), "run_ids": list(run_ids)}
    del e["card_ref"]
    if outcome is not None:
        e["outcome"] = outcome
    return e


def _queue(campaign_root):
    return yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]


# ---------------------------------------------------------------------------
# Fix 1 -- R2 must terminate
# ---------------------------------------------------------------------------

def test_no_new_hypothesis_outcome_is_registered_in_every_list():
    o = "completed_no_new_hypothesis"
    assert dn.NO_NEW_HYPOTHESIS_OUTCOME == rpr.NO_NEW_HYPOTHESIS_STAGE == o
    assert o in vce._NON_VERDICT_OUTCOMES and not vce.outcome_is_verdict_bearing(o)
    vce.validate_verdict_provenance({"id": "x", "status": "done", "outcome": o},
                                    schema=rs.QUEUE_ENTRY_SCHEMA)
    assert o in (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert o in (_SR / "docs" / "USER_GUIDE.md").read_text(encoding="utf-8")
    assert isinstance(dn.BRIEF_MAX_CONSECUTIVE_EMPTY_R2, int) and dn.BRIEF_MAX_CONSECUTIVE_EMPTY_R2 >= 1
    rs.validate_queue_entry({"id": "x", "brief_status_reason": dn.AUTO_EXHAUSTED_REASON})


def test_split_rejects_cards_the_brief_already_produced(campaign_root):
    _write_flags(campaign_root["root"], **_ALL_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    _stage_cards(run_dir, n=4, produced=["OLD"], ids=["OLD", "NEW1", "NEW1", "NEW2"])
    assert rpr._handle_hypothesis_generation_multi_card_split("run_001", run_dir) is True
    arts = run_dir / "artifacts"
    assert yaml.safe_load((arts / "hypothesis_card.yaml").read_text())["hypothesis_id"] == "NEW1"
    q = yaml.safe_load((arts / "queued_hypotheses.yaml").read_text(encoding="utf-8"))
    assert [c["hypothesis_id"] for c in q["cards"]] == ["NEW2"]
    assert [r["hypothesis_id"] for r in q["rejected"]] == ["OLD", "NEW1"]
    assert rpr._brief_card_is_repeat(run_dir) is False


def test_single_card_repeat_ends_the_run_no_new_hypothesis(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    arts = run_dir / "artifacts"
    (arts / "brief_hypotheses_context.yaml").write_text(yaml.safe_dump({"already_produced": ["H1"]}))
    rpr.save_yaml(run_dir / "handoffs" / "research_brief_to_hypothesis.yaml",
                  {"required_inputs": [], "deliverables": ["hypothesis_card.yaml"]})
    monkeypatch.setattr(rpr, "_check_specialist_readers_preflight", lambda run_dir: None)
    monkeypatch.setattr(rpr, "_write_pass_rule_from_card",
                        lambda *a, **k: pytest.fail("a rejected card must not reach 1b"))

    def one_card(*a, **k):
        (arts / "hypothesis_card.yaml").write_text("hypothesis_id: H1\n")
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", one_card)
    rpr.run_loop("run_001")
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["pending_stage"] == "completed_no_new_hypothesis"
    assert state["status"] != "failed"
    assert (arts / "brief_repeat.yaml").exists()


@pytest.mark.parametrize("status,outcome,empty", [
    ("done", "completed_no_new_hypothesis", True),
    ("done", "quarantined_engineering_failure", True),
    ("paused:unhandled_exception", None, True),
    ("superseded", None, True),
    ("done", "refuted", False),
    # CUL-398 (operator, 2026-10-04): a held request (blocked_on_*) is outstanding --
    # it neither counts nor breaks the streak (it used to count as a new card).
    ("blocked_on_component:X", None, None),
])
def test_consecutive_empty_counts_quarantine_and_failure(status, outcome, empty):
    owner = _owner()
    reqs = [_request("OWNER__more_1", outcome="completed_no_new_hypothesis"),
            _request("OWNER__more_2", status=status, outcome=outcome),
            _request("OWNER__more_3", status="ready")]  # outstanding: ignored
    streak = dn.consecutive_empty_r2(owner, [owner] + reqs)
    expected = {True: ["OWNER__more_1", "OWNER__more_2"], False: [], None: ["OWNER__more_1"]}
    assert streak == expected[empty]


def test_r2_stops_when_1a_keeps_repeating_the_same_card(campaign_root, monkeypatch):
    """End to end through process_once: every R2 run's 1a writes the SAME old
    card. After BRIEF_MAX_CONSECUTIVE_EMPTY_R2 such runs the brief is marked
    exhausted (no_new_hypothesis) and the loop stops -- it never runs forever."""
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _brief(root)
    first = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001", status="active",
                                  pending_stage="completed_refined")
    (first / "artifacts" / "hypothesis_card.yaml").write_text("hypothesis_id: H1\n")
    _save_queue_entries(campaign_root["queue_path"], [_owner(status="done"),
                                                      _request("OWNER__more_1", status="ready")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_001"])

    def repeating_1a(run_id):
        run_dir = root / "runs" / run_id
        (run_dir / "artifacts" / "hypothesis_card.yaml").write_text("hypothesis_id: H1\n")
        assert rpr._brief_card_is_repeat(run_dir) is True
        rpr.update_state(path=run_dir, status="active", completed_stages=["hypothesis_generation"],
                         pending_stage="completed_no_new_hypothesis")
    monkeypatch.setattr(rpr, "run_loop", repeating_1a)
    steps = 0
    while camp.process_once():
        steps += 1
        assert steps < 10, "R2 did not terminate"
    by = {e["id"]: e for e in _queue(campaign_root)}
    assert by["OWNER"]["brief_status"] == "exhausted"
    assert by["OWNER"]["brief_status_reason"] == "no_new_hypothesis"
    requests = sorted(k for k in by if "__more_" in k)
    assert len(requests) == dn.BRIEF_MAX_CONSECUTIVE_EMPTY_R2
    assert all(by[r]["outcome"] == "completed_no_new_hypothesis" for r in requests)


# ---------------------------------------------------------------------------
# Fix 2 -- contradiction first; never enqueue from a failed/refused run
# ---------------------------------------------------------------------------

def test_split_checks_the_exhausted_contradiction_before_writing(campaign_root):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    _stage_cards(run_dir, n=2)
    arts = run_dir / "artifacts"
    (arts / "brief_status.yaml").write_text(yaml.safe_dump(
        {"brief_status": "exhausted", "reason": "r"}))
    with pytest.raises(ValueError, match="contradictory"):
        rpr._handle_hypothesis_generation_multi_card_split("run_001", run_dir)
    assert not (arts / "hypothesis_card.yaml").exists()
    assert not (arts / "queued_hypotheses.yaml").exists()
    assert not (root / "campaign_record" / "queued_cards").exists()


def test_enqueue_refuses_a_failed_run(campaign_root):
    root = campaign_root["root"]
    _brief(root)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001", status="failed")
    (run_dir / "artifacts" / "queued_hypotheses.yaml").write_text(yaml.safe_dump({
        "enqueued": False, "cards": [{"n": 2, "card_ref": _card_entry("x")["card_ref"],
                                      "hypothesis_id": "H2", "scores": _SCORES, "model_id": "m",
                                      "rubric_version": "brief-card-v1"}]}))
    owner = _owner(status="in_progress")
    _save_queue_entries(campaign_root["queue_path"], [owner])
    assert camp._enqueue_queued_hypotheses(owner, "run_001") is False
    assert [e["id"] for e in _queue(campaign_root)] == ["OWNER"]


# ---------------------------------------------------------------------------
# Fix 3 -- R2 fairness
# ---------------------------------------------------------------------------

def test_every_eligible_open_brief_gets_a_ready_request():
    queue = [_owner("A", priority=1), _owner("B", priority=2),
             _request("B__more_1", owner="B", status="queued")]
    rec = _decide(_empty_inputs(queue))
    r2 = rec["rules"]["r2"]
    assert r2["ready"] == ["A__more_1", "B__more_1"]
    assert r2["enqueued"] == [{"entry_id": "A__more_1", "owner": "A", "status": "ready"}]
    # the scheduler's own rule picks among them: B's waiting request is earlier in the queue
    assert rec["picked"]["queue_entry_id"] == "B__more_1"


def test_no_brief_waits_behind_another(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _brief(root, "A")
    _brief(root, "B")
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_001", status="active",
                          pending_stage="completed_refined")
    _save_queue_entries(campaign_root["queue_path"], [
        _owner("A", status="in_progress"), _owner("B", status="done", priority=2)])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_001"])
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    assert camp.process_once() is True
    by = {e["id"]: e for e in _queue(campaign_root)}
    assert by["A__more_1"]["status"] == "ready" and by["B__more_1"]["status"] == "ready"


# ---------------------------------------------------------------------------
# Fix 4 -- brief_heading skips frontmatter; pure YAML uses title/name
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("brief,expected", [
    ("briefs/H-041-C-v2.md", None),
    ("briefs/research_brief_XS_momentum.md", "Research brief: XS-momentum — cross-sectional momentum"),
    ("briefs/P4_ts_trend_r1_er_gate.yaml", None),
])
def test_brief_heading_on_the_real_legacy_briefs(brief, expected):
    assert dn.brief_heading(_SR, brief) == expected
    entry = {"id": Path(brief).stem}
    assert dn.obsolete_title(entry, dn.brief_heading(_SR, brief)) == (
        f"[obsolete] {expected or entry['id']}")


def test_brief_heading_pure_yaml_title_then_name(tmp_path):
    (tmp_path / "a.yaml").write_text("# comment\ntitle: The title\nname: n\n", encoding="utf-8")
    (tmp_path / "b.yml").write_text("# comment\nname: The name\n", encoding="utf-8")
    assert dn.brief_heading(tmp_path, "a.yaml") == "The title"
    assert dn.brief_heading(tmp_path, "b.yml") == "The name"


# ---------------------------------------------------------------------------
# Fix 5 -- rubric_version must be brief-card-v1
# ---------------------------------------------------------------------------

def test_card_scores_require_the_brief_card_rubric():
    item = {"scores": dict(_SCORES), "model_id": "m", "rubric_version": "profitability-reader-v1"}
    with pytest.raises(dn.DecideNextError, match="rubric_version"):
        dn.validate_card_scores(item, "w")
    item["rubric_version"] = dn.BRIEF_CARD_RUBRIC
    assert dn.validate_card_scores(item, "w")["rubric_version"] == "brief-card-v1"


# ---------------------------------------------------------------------------
# Fix 6 -- R2 skips superseded/paused/blocked owners
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("status", ["superseded", "paused:unhandled_exception",
                                    "blocked_on_component:X"])
def test_r2_skips_ineligible_owners(status):
    rec = _decide(_empty_inputs([_owner("A", status=status)]))
    assert rec["rules"]["r2"]["fired"] is False and rec["stop"] is not None
    assert rec["rules"]["r2"]["eligible_briefs"] == []


# ---------------------------------------------------------------------------
# Fix 7 -- missing card: pause before any run dir exists
# ---------------------------------------------------------------------------

def test_missing_queued_card_pauses_without_an_orphan_run(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _brief(root)
    _save_queue_entries(campaign_root["queue_path"], [_card_entry("OWNER__h2", status="ready")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[])
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: pytest.fail("must not run"))
    assert camp.process_once() is False
    e = _queue(campaign_root)[0]
    assert e["status"] == "paused:queued_card_missing" and e["run_ids"] == []
    assert list(campaign_root["runs_dir"].iterdir()) == []
    assert "HALT — queued_card_missing" in (root / "campaign_log.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Fix 8 -- ambiguous single-card output; scores naming no card
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("stray", ["hypothesis_card_2.yaml", "extra_card_scores.yaml"])
def test_single_card_with_stray_multi_card_files_fails_loud(campaign_root, stray):
    _write_flags(campaign_root["root"], **_ALL_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    arts = run_dir / "artifacts"
    (arts / "brief_hypotheses_context.yaml").write_text("already_produced: []\n")
    (arts / "hypothesis_card.yaml").write_text("hypothesis_id: H1\n")
    (arts / stray).write_text("x: 1\n")
    with pytest.raises(ValueError, match="ambiguous"):
        rpr._brief_single_card_check(run_dir)


def test_scores_for_a_card_that_does_not_exist_are_refused(campaign_root):
    _write_flags(campaign_root["root"], **_ALL_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    _stage_cards(run_dir, n=2)
    arts = run_dir / "artifacts"
    doc = yaml.safe_load((arts / "extra_card_scores.yaml").read_text())
    doc["cards"].append({"card": "hypothesis_card_9.yaml", "scores": dict(_SCORES),
                         "model_id": "m", "rubric_version": "brief-card-v1"})
    (arts / "extra_card_scores.yaml").write_text(yaml.safe_dump(doc))
    with pytest.raises(ValueError, match="hypothesis_card_9.yaml"):
        rpr._handle_hypothesis_generation_multi_card_split("run_001", run_dir)


# ---------------------------------------------------------------------------
# Fix 9 -- legacy briefs get no addendum
# ---------------------------------------------------------------------------

def test_legacy_brief_launch_gets_no_brief_context(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _brief(root, "LEGACY")
    _save_queue_entries(campaign_root["queue_path"],
                        [_owner("LEGACY", status="ready", brief_status=None)])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[])
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: rpr.update_state(
        path=root / "runs" / run_id, status="paused_for_human", pending_stage="human_pause"))
    camp.process_once()
    run_dir = root / "runs" / "run_001"
    assert run_dir.exists()
    assert not (run_dir / "artifacts" / "brief_hypotheses_context.yaml").exists()
    handoff = {"required_inputs": [], "optional_inputs": []}
    before = copy.deepcopy(handoff)
    rpr._apply_brief_hypotheses_context("hypothesis_generation", handoff, run_dir)
    assert handoff == before


# ---------------------------------------------------------------------------
# Fix 10 -- reuse reader_proposals' validator; no repeated sys.path insert
# ---------------------------------------------------------------------------

def test_card_scores_reuse_the_reader_proposals_validator(monkeypatch):
    calls = []
    real = rp.check_scores
    monkeypatch.setattr(rp, "check_scores", lambda s, w: calls.append(w) or real(s, w))
    dn.validate_card_scores({"scores": dict(_SCORES), "model_id": "m",
                             "rubric_version": dn.BRIEF_CARD_RUBRIC}, "where")
    assert calls == ["where"]
    with pytest.raises(dn.DecideNextError, match="0..3"):
        dn.validate_card_scores({"scores": dict(_SCORES, confidence_real=7), "model_id": "m",
                                 "rubric_version": dn.BRIEF_CARD_RUBRIC}, "w")


def test_no_repeated_sys_path_insert():
    assert "sys.path.insert" not in inspect.getsource(rpr._decide_next_tools)
