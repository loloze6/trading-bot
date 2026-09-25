"""
E-059 S2b -- brief-sourced queue entries, brief status, R2 (delivery_plan_v26.md
slice 6b, flag off). Spec: engineering/roadmap/E-059/S1_FINDINGS_6B.md §4.3, §6,
§7 and the operator decision of 2026-09-24 (4, 7, 9).

All synthetic: no LLM, no backtest, no trial row, no holdout.
  * flag off: the multi-card split, the 1a prompt, the exhausted signal and
    process_once's queue are unchanged;
  * flag on: extra cards go to the queue (queued, card_ref, origin brief) and
    skip authoring when picked; they rank on their 1a scores; R2 fires only
    for open briefs; the exhausted signal gives completed_brief_exhausted and
    flips the owner; the stop fires only when no brief is open; legacy briefs
    are tagged "[obsolete]" once and their files are never touched;
  * completed_brief_exhausted is registered in every outcome list.
"""
from __future__ import annotations

import copy
import json
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
import record_schema as rs  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _save_queue_entries, _write_campaign_state, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_s2a_decide_next import (  # noqa: E402
    _ALL_ON, _write_flags, _patch, _one_source, _decide,
)

_BRIEF = ("---\nstrategy_domain: crypto\nmarket_universe: BTCUSDT\ntimeframe: 1h\n"
          "research_goal: g\nvenue: binance\nproduct: perp\n"
          "machine_constraints:\n  protocol_ref: protocols/p2.json\n---\n\n# Funding brief\n\nprose\n")
_SCORES = {"confidence_real": 1, "distance_to_profitable": 1, "mechanism_plausibility": 2}


def _brief(root: Path, name="OWNER") -> Path:
    path = root / "briefs" / f"{name}.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text(_BRIEF, encoding="utf-8")
    return path


def _protocol(root: Path):
    (root / "protocols").mkdir(exist_ok=True)
    (root / "protocols" / "p2.json").write_text(json.dumps({
        "symbols": ["BTCUSDT"], "timeframe": "1h",
        "windows": [{"label": "a"}, {"label": "b"}]}), encoding="utf-8")


def _owner(eid="OWNER", status="done", brief_status="open", priority=1, **kw):
    e = {"id": eid, "brief_path": f"briefs/{eid}.md", "status": status, "priority": priority,
         "source": "operator_ratified", "relation": "new_registration", "notes": "n",
         "run_ids": ["run_001"] if status != "ready" else []}
    if brief_status is not None:
        e["brief_status"] = brief_status
    e.update(kw)
    return e


def _card_entry(eid, owner="OWNER", card_ref="campaign_record/queued_cards/run_001/hypothesis_card_2.yaml",
                status="queued"):
    return {"id": eid, "brief_path": f"briefs/{owner}.md", "status": status, "priority": 999,
            "source": "agent", "notes": "n", "run_ids": [], "origin": "brief", "card_ref": card_ref}


def _card_info(conf=1, dist=1, backtests=6, hid="H2"):
    return {"source_run": "run_001", "hypothesis_id": hid,
            "scores": {"confidence_real": conf, "distance_to_profitable": dist,
                       "mechanism_plausibility": 1, "model_id": "m", "rubric_version": "brief-card-v1"},
            "cost_backtests": backtests, "cost_basis": "b"}


def _empty_inputs(queue_entries, brief_cards=None):
    inputs = _one_source([])
    inputs["runs"] = {}
    inputs["queue"] = {"queue": queue_entries}
    inputs["brief_cards"] = brief_cards or {}
    return inputs


# ---------------------------------------------------------------------------
# Outcome-list drift
# ---------------------------------------------------------------------------

def test_brief_exhausted_outcome_is_registered_in_every_list():
    o = "completed_brief_exhausted"
    assert dn.BRIEF_EXHAUSTED_OUTCOME == rpr.BRIEF_EXHAUSTED_STAGE == o
    assert o in vce._NON_VERDICT_OUTCOMES and not vce.outcome_is_verdict_bearing(o)
    entry = {"id": "x", "status": "done", "outcome": o}
    vce.validate_verdict_provenance(entry, schema=rs.QUEUE_ENTRY_SCHEMA)  # no ref needed
    rs.validate_queue_entry(entry)
    # run_loop's terminal check and the queue runner treat it as finished
    assert o.startswith(("completed", "rejected", "human_pause", "failed_validation"))
    assert o not in rpr.STAGE_CONFIGS
    assert o in (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert o in (_SR / "docs" / "USER_GUIDE.md").read_text(encoding="utf-8")


def test_schema_accepts_title_and_register_accepts_queued_only(campaign_root):
    rs.validate_queue_entry({"id": "x", "title": "[obsolete] X"})
    brief = _brief(campaign_root["root"])
    assert camp.register_hypothesis(brief, 999, "n", entry_id="Q", status="queued") == 0
    e = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert e["status"] == "queued"
    with pytest.raises(ValueError, match="status"):
        camp.register_hypothesis(brief, 1, "n", entry_id="R", status="done")


# ---------------------------------------------------------------------------
# The split (run_phase1_research._handle_hypothesis_generation_multi_card_split)
# ---------------------------------------------------------------------------

def _stage_cards(run_dir: Path, n=3, scores=True, context=True, produced=(), ids=None):
    arts = run_dir / "artifacts"
    arts.mkdir(parents=True, exist_ok=True)
    (arts / "research_brief.yaml").write_text("strategy_domain: crypto\n", encoding="utf-8")
    if context:
        (arts / "brief_hypotheses_context.yaml").write_text(yaml.safe_dump(
            {"already_produced": list(produced)}), encoding="utf-8")
    for i in range(1, n + 1):
        hid = ids[i - 1] if ids else f"H{i}"
        (arts / f"hypothesis_card_{i}.yaml").write_text(
            yaml.safe_dump({"hypothesis_id": hid, "criteria": [{"id": "sign_consistent_by_era"}]}),
            encoding="utf-8")
    if scores:
        (arts / "extra_card_scores.yaml").write_text(yaml.safe_dump({"cards": [
            {"card": f"hypothesis_card_{i}.yaml", "scores": dict(_SCORES, confidence_real=i % 4),
             "model_id": "m", "rubric_version": "brief-card-v1"} for i in range(1, n + 1)]}),
            encoding="utf-8")


def test_split_flag_off_scaffolds_siblings_as_before(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, decide_next=False)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    _stage_cards(run_dir, n=2)
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_001"])
    scaffolded = []
    monkeypatch.setattr(rpr, "_scaffold_next_run",
                        lambda cid: scaffolded.append(cid) or _write_fresh_scaffold(
                            campaign_root["runs_dir"], cid))
    assert rpr._handle_hypothesis_generation_multi_card_split("run_001", run_dir) is True
    state = yaml.safe_load(campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    assert state["hypothesis_splits"][0]["children"] == scaffolded and len(scaffolded) == 1
    assert not (root / "campaign_record" / "queued_cards").exists()
    assert not (run_dir / "artifacts" / "queued_hypotheses.yaml").exists()


def test_split_flag_on_queues_extra_cards_with_scores(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    _stage_cards(run_dir, n=3)
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_001"])
    monkeypatch.setattr(rpr, "_scaffold_next_run", lambda cid: pytest.fail("no sibling run"))
    assert rpr._handle_hypothesis_generation_multi_card_split("run_001", run_dir) is True
    arts = run_dir / "artifacts"
    assert yaml.safe_load((arts / "hypothesis_card.yaml").read_text())["hypothesis_id"] == "H1"
    q = yaml.safe_load((arts / "queued_hypotheses.yaml").read_text(encoding="utf-8"))
    assert q["enqueued"] is False
    assert [c["card_ref"] for c in q["cards"]] == [
        "campaign_record/queued_cards/run_001/hypothesis_card_2.yaml",
        "campaign_record/queued_cards/run_001/hypothesis_card_3.yaml"]
    assert q["cards"][0]["scores"]["confidence_real"] == 2
    assert (root / q["cards"][1]["card_ref"]).exists()
    state = yaml.safe_load(campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    assert "hypothesis_splits" not in state


@pytest.mark.parametrize("mutate,match", [
    (lambda arts: (arts / "extra_card_scores.yaml").unlink(), "extra_card_scores"),
    (lambda arts: (arts / "extra_card_scores.yaml").write_text(yaml.safe_dump({"cards": [
        {"card": "hypothesis_card_2.yaml", "scores": dict(_SCORES, confidence_real=4),
         "model_id": "m", "rubric_version": "brief-card-v1"}]})), "0..3"),
    (lambda arts: (arts / "research_brief.yaml").write_text(yaml.safe_dump(
        {"candidate": {"criteria_from": "hypothesis_generation"}})), "reader candidate"),
])
def test_split_flag_on_fails_loud(campaign_root, mutate, match):
    _write_flags(campaign_root["root"], **_ALL_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    _stage_cards(run_dir, n=2)
    mutate(run_dir / "artifacts")
    with pytest.raises(ValueError, match=match):
        rpr._handle_hypothesis_generation_multi_card_split("run_001", run_dir)
    assert not (run_dir / "artifacts" / "hypothesis_card.yaml").exists()


def _flag_on_split_step(campaign_root, monkeypatch):
    """process_once on a fresh OWNER launch whose 1a writes three cards."""
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _brief(root)
    _protocol(root)
    _save_queue_entries(campaign_root["queue_path"], [_owner(status="ready")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[])

    def fake_run_loop(run_id):
        run_dir = root / "runs" / run_id
        _stage_cards(run_dir, n=3, context=False)  # process_once wrote the context
        assert rpr._handle_hypothesis_generation_multi_card_split(run_id, run_dir)
        rpr.update_state(path=run_dir, status="paused_for_human", pending_stage="human_pause",
                         completed_stages=["hypothesis_generation"])
    monkeypatch.setattr(rpr, "run_loop", fake_run_loop)
    camp.process_once()
    return root


def test_process_once_enqueues_extra_cards_queued_with_card_ref(campaign_root, monkeypatch):
    root = _flag_on_split_step(campaign_root, monkeypatch)
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    owner, c2, c3 = queue
    assert owner["run_ids"] == ["run_001"]
    assert (c2["id"], c3["id"]) == ("OWNER__h2", "OWNER__h3")
    for c in (c2, c3):
        assert c["status"] == "queued" and c["origin"] == "brief" and c["source"] == "agent"
        assert c["brief_path"] == "briefs/OWNER.md" and "relation" not in c
        assert camp._next_action_for_entry(c) == "queued_card"
    assert c2["card_ref"] == "campaign_record/queued_cards/run_001/hypothesis_card_2.yaml"
    assert "confidence_real" not in campaign_root["queue_path"].read_text(encoding="utf-8")
    q = yaml.safe_load((root / "runs" / "run_001" / "artifacts" / "queued_hypotheses.yaml")
                       .read_text(encoding="utf-8"))
    assert q["enqueued"] is True
    # the 1a context was written for this brief run
    ctx = yaml.safe_load((root / "runs" / "run_001" / "artifacts" /
                          "brief_hypotheses_context.yaml").read_text(encoding="utf-8"))
    assert ctx["brief_owner"] == "OWNER" and ctx["request"] == "first_launch"
    # idempotent: a second pass registers nothing
    assert camp._enqueue_queued_hypotheses(owner, "run_001") is False


@pytest.mark.parametrize("config_direct,stage", [(True, "strategy_config_authoring"),
                                                  (False, "innovation_expansion")])
def test_picked_card_skips_authoring(campaign_root, monkeypatch, config_direct, stage):
    root = campaign_root["root"]
    _write_flags(root, **{**_ALL_ON, "decide_next": False, "config_direct_authoring": config_direct})
    _brief(root)
    card = root / "campaign_record" / "queued_cards" / "run_001" / "hypothesis_card_2.yaml"
    card.parent.mkdir(parents=True)
    card.write_text(yaml.safe_dump({"hypothesis_id": "H2"}), encoding="utf-8")
    _save_queue_entries(campaign_root["queue_path"], [_card_entry("OWNER__h2", status="ready")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[])
    seen = {}

    def fake_run_loop(run_id):
        seen["state"] = rpr.load_yaml(root / "runs" / run_id / "pipeline_state.yaml")
        rpr.update_state(path=root / "runs" / run_id, status="paused_for_human",
                         pending_stage="human_pause")
    monkeypatch.setattr(rpr, "run_loop", fake_run_loop)
    camp.process_once()
    assert seen["state"]["pending_stage"] == stage
    assert seen["state"]["completed_stages"] == ["hypothesis_generation"]
    run_card = root / "runs" / "run_001" / "artifacts" / "hypothesis_card.yaml"
    assert run_card.read_bytes() == card.read_bytes()
    assert not (root / "runs" / "run_001" / "artifacts" / "brief_hypotheses_context.yaml").exists()


# ---------------------------------------------------------------------------
# decide(): extra cards ranked by their 1a scores; R2; stop
# ---------------------------------------------------------------------------

def test_extra_cards_are_ranked_by_their_1a_scores_with_proposals():
    inputs = _one_source([_patch("profitability-run_061-1", conf=2, dist=2)])
    inputs["queue"] = {"queue": [_owner(), _card_entry("OWNER__h2"),
                                 _card_entry("OWNER__h3", card_ref="campaign_record/queued_cards/"
                                             "run_001/hypothesis_card_3.yaml")]}
    inputs["brief_cards"] = {"OWNER__h2": _card_info(conf=1, dist=3),
                             "OWNER__h3": _card_info(conf=3, dist=0, hid="H3")}
    rec = _decide(inputs)
    ranked = [c["candidate_id"] for c in rec["candidates"] if c["rank"]]
    assert ranked == ["OWNER__h3", "profitability-run_061-1", "OWNER__h2"]
    assert rec["picked"] == {"candidate_id": "OWNER__h3", "queue_entry_id": "OWNER__h3",
                             "card_ref": "campaign_record/queued_cards/run_001/hypothesis_card_3.yaml",
                             "why": rec["picked"]["why"]}
    card = next(c for c in rec["candidates"] if c["candidate_id"] == "OWNER__h3")
    assert card["origin"] == "brief" and card["kind"] == "card" and card["brief_owner"] == "OWNER"
    assert rec["rules"]["r2"]["fired"] is False and rec["stop"] is None


def test_r2_fires_only_for_open_briefs():
    queue = [_owner("A", brief_status="open", priority=2), _owner("B", brief_status="open", priority=1),
             _owner("C", brief_status="exhausted"), _owner("LEG", brief_status=None)]
    rec = _decide(_empty_inputs(queue))
    r2 = rec["rules"]["r2"]
    assert r2["fired"] is True and r2["open_briefs"] == ["B", "A"]
    assert r2["exhausted_briefs"] == ["C"] and r2["legacy_briefs"] == ["LEG"]
    assert r2["enqueued"] == [{"entry_id": "B__more_1", "owner": "B", "status": "ready"},
                              {"entry_id": "A__more_1", "owner": "A", "status": "ready"}]
    assert r2["ready"] == ["B__more_1", "A__more_1"]
    assert rec["picked"]["r2_request"] == "B__more_1" and rec["picked"]["new"] is True
    assert rec["stop"] is None


def test_r2_reuses_a_waiting_request_and_numbers_new_ones():
    queue = [_owner("A"), {**_card_entry("A__more_1", owner="A"), "status": "done"},
             {**_card_entry("A__more_2", owner="A"), "status": "queued"}]
    del queue[1]["card_ref"], queue[2]["card_ref"]
    rec = _decide(_empty_inputs(queue))
    assert rec["picked"]["r2_request"] == "A__more_2" and rec["picked"]["new"] is False
    assert rec["rules"]["r2"]["enqueued"] == []
    queue[2]["status"] = "done"
    assert _decide(_empty_inputs(queue))["picked"]["r2_request"] == "A__more_3"


@pytest.mark.parametrize("statuses", [("exhausted",), ("exhausted", None), (None,), ()])
def test_stop_only_when_no_brief_is_open(statuses):
    queue = [_owner(f"E{i}", brief_status=s) for i, s in enumerate(statuses)]
    rec = _decide(_empty_inputs(queue))
    assert rec["picked"] is None and rec["stop"]["reason"] == "no_eligible_candidate"
    assert rec["rules"]["r2"]["fired"] is False
    queue.append(_owner("OPEN", brief_status="open"))
    rec = _decide(_empty_inputs(queue))
    assert rec["stop"] is None and rec["picked"]["r2_request"] == "OPEN__more_1"


def test_r2_does_not_fire_while_something_is_scheduled_or_eligible():
    queue = [_owner("A"), _card_entry("A__h2")]
    rec = _decide(_empty_inputs(queue, {"A__h2": _card_info()}))
    assert rec["rules"]["r2"]["fired"] is False and rec["picked"]["candidate_id"] == "A__h2"
    queue[1]["status"] = "ready"
    rec = _decide(_empty_inputs(queue))
    assert rec["rules"]["r2"]["fired"] is False and rec["picked"]["queue_entry_id"] == "A__h2"


def test_decision_records_with_cards_and_r2_match_the_schema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((_SR / "workflow_artifacts" / "schemas" /
                         "decision_record.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    cards = _empty_inputs([_owner(), _card_entry("OWNER__h2")], {"OWNER__h2": _card_info()})
    r2 = _empty_inputs([_owner("A"), _owner("B")])
    stop = _empty_inputs([_owner("A", brief_status="exhausted")])
    for inputs in (cards, r2, stop):
        rec = yaml.safe_load(yaml.safe_dump(_decide(inputs)))
        assert sorted(str(e.message) for e in validator.iter_errors(rec)) == []


# ---------------------------------------------------------------------------
# End to end under the flag: exhausted, owner flip, R2 registration, tagging
# ---------------------------------------------------------------------------

def _stage_done(campaign_root, entries, run_id="run_001", pending="completed_brief_exhausted"):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _write_fresh_scaffold(campaign_root["runs_dir"], run_id, status="active", pending_stage=pending)
    _save_queue_entries(campaign_root["queue_path"], entries)
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[run_id])
    return root


def test_exhausted_request_flips_owner_and_stops_when_none_open(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    req = {**_card_entry("OWNER__more_1", status="in_progress"), "run_ids": ["run_001"]}
    del req["card_ref"]
    root = _stage_done(campaign_root, [_owner(), req])
    _brief(root)
    assert camp.process_once() is False  # the only brief is now exhausted -> stop
    owner, done = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    assert done["status"] == "done" and done["outcome"] == "completed_brief_exhausted"
    assert "verdict_status" not in done and "pass_rule_evaluation_ref" not in done
    assert owner["brief_status"] == "exhausted"
    rec = yaml.safe_load((root / "runs" / "run_001" / "artifacts" / "decision_record.yaml")
                         .read_text(encoding="utf-8"))
    assert rec["stop"]["reason"] == "no_eligible_candidate"
    assert rec["rules"]["r2"]["exhausted_briefs"] == ["OWNER"]


def test_owner_own_run_exhausted_flips_itself(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = _stage_done(campaign_root, [_owner(status="in_progress"), _owner("OTHER")])
    _brief(root)
    _brief(root, "OTHER")
    assert camp.process_once() is True  # OTHER is still open -> R2 asks for more
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    by = {e["id"]: e for e in queue}
    assert by["OWNER"]["brief_status"] == "exhausted" and by["OWNER"]["status"] == "done"
    assert by["OTHER__more_1"]["status"] == "ready" and by["OTHER__more_1"]["origin"] == "brief"
    assert by["OTHER__more_1"]["brief_path"] == "briefs/OTHER.md"
    assert not any(e["id"].startswith("OWNER__more") for e in queue)
    assert camp._select_entry(queue)["id"] == "OTHER__more_1"
    assert camp._next_action_for_entry(by["OTHER__more_1"]) == "fresh_launch"


def test_r2_request_launch_carries_already_produced(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _brief(root)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_001")
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text("hypothesis_id: H1\n")
    card = root / "campaign_record" / "queued_cards" / "run_001" / "hypothesis_card_2.yaml"
    card.parent.mkdir(parents=True)
    card.write_text("hypothesis_id: H2\n")
    req = {**_card_entry("OWNER__more_1", status="ready")}
    del req["card_ref"]
    _save_queue_entries(campaign_root["queue_path"], [_owner(), _card_entry("OWNER__h2"), req])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_001"])
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: rpr.update_state(
        path=root / "runs" / run_id, status="paused_for_human", pending_stage="human_pause"))
    camp.process_once()
    ctx = yaml.safe_load((root / "runs" / "run_002" / "artifacts" /
                          "brief_hypotheses_context.yaml").read_text(encoding="utf-8"))
    assert ctx["request"] == "more_hypotheses" and ctx["brief_owner"] == "OWNER"
    assert ctx["already_produced"] == ["H1", "H2"]


def test_picked_card_is_flipped_ready_by_the_done_branch(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = _stage_done(campaign_root, [_owner(status="in_progress"), _card_entry("OWNER__h2")],
                       pending="completed_refined")
    _brief(root)
    _protocol(root)
    card = root / "campaign_record" / "queued_cards" / "run_001" / "hypothesis_card_2.yaml"
    card.parent.mkdir(parents=True)
    card.write_text("hypothesis_id: H2\n")
    (root / "runs" / "run_001" / "artifacts" / "queued_hypotheses.yaml").write_text(yaml.safe_dump({
        "enqueued": True, "cards": [{"n": 2, "card_ref": _card_entry("x")["card_ref"],
                                     "hypothesis_id": "H2", "scores": _SCORES, "model_id": "m",
                                     "rubric_version": "brief-card-v1"}]}))
    assert camp.process_once() is True
    by = {e["id"]: e for e in yaml.safe_load(
        campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]}
    assert by["OWNER__h2"]["status"] == "ready"
    assert by["OWNER__h2"]["decision_ref"] == "runs/run_001/artifacts/decision_record.yaml"
    rec = yaml.safe_load((root / by["OWNER__h2"]["decision_ref"]).read_text(encoding="utf-8"))
    assert rec["candidates"][0]["cost"]["backtests"] == 2 * 3 * 1  # from the brief's protocol


def test_legacy_briefs_are_tagged_obsolete_once_and_files_untouched(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    legacy_done = _owner("LEGACY", brief_status=None, status="in_progress")
    legacy_ready = _owner("LEG2", brief_status=None, status="queued")
    root = _stage_done(campaign_root, [legacy_done, legacy_ready], pending="completed_refined")
    brief = _brief(root, "LEGACY")
    before = brief.read_bytes()
    assert camp.process_once() is False  # no open brief: legacy never triggers R2
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    by = {e["id"]: e for e in queue}
    assert by["LEGACY"]["title"] == "[obsolete] Funding brief"
    assert by["LEG2"]["title"] == "[obsolete] LEG2"  # no brief file -> id
    assert by["LEG2"]["status"] == "queued"  # tagging never changes status
    assert brief.read_bytes() == before
    assert not any("__more_" in e["id"] for e in queue)
    rec = yaml.safe_load((root / "runs" / "run_001" / "artifacts" / "decision_record.yaml")
                         .read_text(encoding="utf-8"))
    assert rec["rules"]["r2"]["legacy_briefs"] == ["LEG2", "LEGACY"]
    # once: a second pass leaves the titles as they are
    updates = camp._brief_updates({"queue": queue}, by["LEGACY"])
    assert updates == {}
    assert "(" in (root / "campaign_summary.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# The exhausted signal and the 1a prompt
# ---------------------------------------------------------------------------

def _exhausted_run(root: Path, runs_dir: Path, context=True, card=False):
    run_dir = _write_fresh_scaffold(runs_dir, "run_001")
    arts = run_dir / "artifacts"
    (arts / "brief_status.yaml").write_text(yaml.safe_dump(
        {"brief_status": "exhausted", "reason": "nothing new left"}), encoding="utf-8")
    if context:
        (arts / "brief_hypotheses_context.yaml").write_text("already_produced: []\n")
    if card:
        (arts / "hypothesis_card.yaml").write_text("hypothesis_id: X\n")
    return run_dir


def test_exhausted_signal_flag_off_is_ignored(campaign_root):
    _write_flags(campaign_root["root"], decide_next=False)
    run_dir = _exhausted_run(campaign_root["root"], campaign_root["runs_dir"])
    assert rpr._brief_exhausted_signal(run_dir) is False


def test_exhausted_signal_flag_on(campaign_root):
    _write_flags(campaign_root["root"], **_ALL_ON)
    run_dir = _exhausted_run(campaign_root["root"], campaign_root["runs_dir"])
    assert rpr._brief_exhausted_signal(run_dir) is True
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text("hypothesis_id: X\n")
    with pytest.raises(ValueError, match="contradictory"):
        rpr._brief_exhausted_signal(run_dir)
    (run_dir / "artifacts" / "hypothesis_card.yaml").unlink()
    (run_dir / "artifacts" / "brief_hypotheses_context.yaml").unlink()
    with pytest.raises(ValueError, match="only a brief run"):
        rpr._brief_exhausted_signal(run_dir)


def test_run_loop_exhausted_signal_gives_completed_brief_exhausted(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    run_dir = _exhausted_run(root, campaign_root["runs_dir"])
    rpr.save_yaml(run_dir / "handoffs" / "research_brief_to_hypothesis.yaml",
                  {"required_inputs": [], "deliverables": ["hypothesis_card.yaml"]})
    monkeypatch.setattr(rpr, "_check_specialist_readers_preflight", lambda run_dir: None)

    def no_card(*a, **k):
        raise FileNotFoundError("hypothesis_card.yaml")
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", no_card)
    rpr.run_loop("run_001")
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["pending_stage"] == "completed_brief_exhausted"
    assert state["status"] != "failed"
    # flag off: the same output is still a missing deliverable (failed)
    _write_flags(root, decide_next=False)
    rpr.update_state(path=run_dir, pending_stage="hypothesis_generation", status="active")
    rpr.run_loop("run_001")
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "failed" and state["pending_stage"] == "hypothesis_generation"


def _prompt_pair(run_dir):
    base = {"required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "b"}],
            "optional_inputs": []}
    handoff = copy.deepcopy(base)
    rpr._apply_brief_hypotheses_context("hypothesis_generation", handoff, run_dir)
    return (rpr._build_stage_prompt("hypothesis_generation", copy.deepcopy(base), run_dir),
            rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir))


def test_1a_prompt_flag_off_is_byte_identical(campaign_root, monkeypatch):
    monkeypatch.chdir(_SR)
    _write_flags(campaign_root["root"], decide_next=False)
    run_dir = _exhausted_run(campaign_root["root"], campaign_root["runs_dir"])
    (run_dir / "artifacts" / "research_brief.yaml").write_text("strategy_domain: c\n")
    base, after = _prompt_pair(run_dir)
    assert after == base


def test_1a_prompt_flag_on_carries_the_addendum_for_brief_runs_only(campaign_root, monkeypatch):
    monkeypatch.chdir(_SR)
    _write_flags(campaign_root["root"], **_ALL_ON)
    addendum = campaign_root["root"] / "workflow_artifacts" / "skills" / "hypothesis-design"
    addendum.mkdir(parents=True)
    (addendum / "BRIEF_HYPOTHESES.md").write_bytes(
        (_SR / "workflow_artifacts" / "skills" / "hypothesis-design" / "BRIEF_HYPOTHESES.md").read_bytes())
    run_dir = _exhausted_run(campaign_root["root"], campaign_root["runs_dir"])
    (run_dir / "artifacts" / "research_brief.yaml").write_text("strategy_domain: c\n")
    base, after = _prompt_pair(run_dir)
    assert after != base and "brief-card-v1" in after and "already_produced" in after
    # a decide-next reader candidate never gets it
    (run_dir / "artifacts" / "research_brief.yaml").write_text(yaml.safe_dump(
        {"candidate": {"criteria_from": "hypothesis_generation"}}))
    base, after = _prompt_pair(run_dir)
    assert after == base


def test_register_cli_marks_open_only_under_the_flag(campaign_root, monkeypatch):
    root = campaign_root["root"]
    brief = _brief(root)
    calls = []
    monkeypatch.setattr(camp, "register_hypothesis", lambda *a, **k: calls.append(k) or 0)
    for flags, expected in (({"decide_next": False}, {}),
                            (_ALL_ON, {"extra": {"brief_status": "open"}})):
        _write_flags(root, **flags)
        assert camp._register_from_cli(brief, 1, "n") == 0
        assert calls[-1] == expected
