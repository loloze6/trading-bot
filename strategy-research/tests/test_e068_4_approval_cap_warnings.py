"""
E-068 PR 4 (D-071): four operator-approved changes.

  1. A reader's component class names are checked against the real classes
     (reader_proposals.unknown_class_names); an unknown one is a WARNING on the
     decide-next candidate (`warnings`, only when non-empty) and a console line.
  2. Review S3b of PR 3a: a brief with >= BRIEF_MAX_COMPONENT_QUARANTINES (3)
     component-quarantined entries (owner + R2 requests, after any reopen
     marker) is no longer asked by R2 (`quarantine_capped_briefs`); it is not
     closed.
  3. CUL-399: orchestrator.operator_approval -- every entry the agent creates
     or flips ready is held as blocked_on_operator_approval until
     `run_campaign.py --approve <id>`. Off: byte-identical.
  4. token_budget_per_run_weighted_units 1,500,000 -> 1,800,000.
"""
from __future__ import annotations

import ast
import json
import shutil
import sys
from pathlib import Path

import jsonschema
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
import campaign_lock  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _save_queue_entries, _write_campaign_state, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_s2a_decide_next import (  # noqa: E402
    _ALL_ON, _write_flags, _sketch, _patch, _one_source, _decide, _stage_flag_on_source, CLS)
from test_e059_s2b_briefs import (  # noqa: E402
    _brief, _protocol, _card_entry, _empty_inputs, _stage_done, _SCORES,
    _owner as _s2b_owner)
from test_retry_robustness_r2_hold import _owner, _req  # noqa: E402

TBOT = _SR.parent / "trading-bot"
FIXTURE = _SR / "tests" / "fixtures" / "run_070_regime_power_reader_unknown_class.yaml"
SCHEMA = json.loads((_SR / "workflow_artifacts" / "schemas" /
                     "decision_record.schema.json").read_text(encoding="utf-8"))
HELD = "blocked_on_operator_approval"
# operator_approval requires decide_next AND verdict_routing_retired (review round 1).
APPROVAL_ON = {**_ALL_ON, "profit_bars_file": True, "profit_bars_every_backtest": True,
               "verdict_routing_retired": True, "operator_approval": True}


def _valid(record):
    errors = sorted(e.message for e in
                    jsonschema.Draft202012Validator(SCHEMA).iter_errors(
                        yaml.safe_load(yaml.safe_dump(record))))
    assert errors == []


def _queue(campaign_root):
    return yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]


def _log(root):
    return (root / "campaign_log.md").read_text(encoding="utf-8")


# ===========================================================================
# 1. Reader class-name warnings
# ===========================================================================

def _known():
    return dn.known_component_classes(TBOT)


def test_run_070_regime_power_names_a_class_that_does_not_exist():
    """run_070's regime_power reader wrote VarianceRatioRegimeComponent; the
    real class is VarianceRatioComponent. EfficiencyRatioRegimeComponent is real."""
    (proposal,) = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
    out = rp.unknown_class_names(proposal, _known(), None)
    assert out == {"unknown": [{"name": "VarianceRatioRegimeComponent",
                                "suggestion": "VarianceRatioComponent"}],
                   "quoted_from_card": []}
    assert "strategies.strategy_components.EfficiencyRatioRegimeComponent" in _known()


def test_the_fixture_is_a_valid_reader_file_and_load_proposals_is_untouched(tmp_path):
    d = tmp_path / "proposals"
    d.mkdir()
    shutil.copy(FIXTURE, d / "regime_power.yaml")
    loaded = rp.load_proposals(d, ["regime_power"])
    assert [p["proposal_id"] for p in loaded["regime_power"]] == ["regime_power-run_070-1"]
    assert sorted(x.name for x in d.iterdir()) == ["regime_power.yaml"]  # nothing written


@pytest.mark.parametrize("text", [
    "a Component", "Component", "the SubStrategyComponent base",
    "myFooComponent",          # no word boundary before the capital
    "FooComponentX",           # no word boundary after the suffix
    "FooComponents", "fooComponent", "Foo_Component"])
def test_the_pattern_needs_a_whole_capitalised_name(text):
    p = {"proposal_id": "x", "evidence": [text]}
    assert rp.unknown_class_names(p, _known(), None)["unknown"] == []


def test_the_pattern_finds_names_in_every_string_leaf_once_in_order():
    p = {"proposal_id": "regime_power-run_070-1", "kind": "new_block",
         "block": {"kind": "regime", "rationale": "use BarComponent", "config_paths": ["/x"],
                   "scaffolding": ["FooComponent"]},
         "patch": [{"component_id": "c", "field": "class", "before": 1,
                    "after": "strategies.strategy_components.BazComponent"}],
         "evidence": ["FooComponent again, and (QuxComponent)"]}
    names = [u["name"] for u in rp.unknown_class_names(p, _known(), None)["unknown"]]
    assert names == ["BarComponent", "FooComponent", "BazComponent", "QuxComponent"]


@pytest.mark.parametrize("key", ["proposal_id", "model_id", "rubric_version"])
def test_provenance_fields_are_never_scanned(key):
    p = {key: "GhostComponent", "evidence": ["nothing here"]}
    assert rp.unknown_class_names(p, _known(), None)["unknown"] == []
    p = {"evidence": ["GhostComponent"]}
    assert rp.unknown_class_names(p, _known(), None)["unknown"][0]["name"] == "GhostComponent"


def test_a_name_quoted_from_the_card_is_not_a_warning():
    p = {"evidence": ["the card's MadeUpComponent and VarianceRatioRegimeComponent"]}
    card = "thesis: uses MadeUpComponent to gate\n"
    out = rp.unknown_class_names(p, _known(), card)
    assert out["quoted_from_card"] == ["MadeUpComponent"]
    assert [u["name"] for u in out["unknown"]] == ["VarianceRatioRegimeComponent"]
    # a partial match in the card does not count as a quote
    out = rp.unknown_class_names(p, _known(), "XMadeUpComponentY\n")
    assert out["quoted_from_card"] == []


def test_no_close_real_name_gives_no_suggestion():
    p = {"evidence": ["QqqqqqqqqqqqqqqqqqqqqqqqComponent"]}
    assert rp.unknown_class_names(p, _known(), None)["unknown"] == [
        {"name": "QqqqqqqqqqqqqqqqqqqqqqqqComponent", "suggestion": None}]


def test_known_accepts_bare_names_and_dotted_paths():
    p = {"evidence": ["FooComponent"]}
    assert rp.unknown_class_names(p, ["FooComponent"], None)["unknown"] == []
    assert rp.unknown_class_names(p, ["a.b.FooComponent"], None)["unknown"] == []


def test_the_base_allow_list_is_strategy_base_s_matching_classes():
    tree = ast.parse((TBOT / "strategies" / "strategy_base.py").read_text(encoding="utf-8"))
    names = {n.name for n in tree.body if isinstance(n, ast.ClassDef)
             and rp.COMPONENT_CLASS_NAME_RE.fullmatch(n.name)}
    assert names == set(rp.BASE_COMPONENT_CLASS_NAMES)


def test_decide_records_the_warning_only_when_there_is_one():
    bad = _sketch("profitability-run_061-1")
    bad["block"]["rationale"] = "gate with VarianceRatioRegimeComponent"
    good = _sketch("profitability-run_061-2", kind="forecast")
    good["block"]["config_paths"] = ["/strategies/regimes/unknown/components/2"]  # no collapse
    inputs = _one_source([bad, good])
    inputs["known_classes"] = _known()
    rec = _decide(inputs)
    by = {c["candidate_id"]: c for c in rec["candidates"]}
    assert by["profitability-run_061-1"]["warnings"] == [
        {"kind": "unknown_component_class", "name": "VarianceRatioRegimeComponent",
         "suggestion": "VarianceRatioComponent"}]
    assert "warnings" not in by["profitability-run_061-2"]  # byte-identical record otherwise
    # warning only: eligibility, feasibility and rank are untouched
    assert by["profitability-run_061-1"]["eligible"] is True
    assert by["profitability-run_061-1"]["gates"]["feasibility"]["result"] == "UNKNOWN"
    _valid(rec)


def test_no_known_class_set_no_warning_and_a_card_quote_no_warning():
    bad = _sketch("profitability-run_061-1")
    bad["evidence"] = ["GhostComponent"]
    inputs = _one_source([bad])
    inputs["known_classes"] = None
    assert "warnings" not in _decide(inputs)["candidates"][0]
    inputs = _one_source([bad])
    inputs["runs"]["run_061"]["card_text"] = "thesis: GhostComponent\n"
    assert "warnings" not in _decide(inputs)["candidates"][0]
    inputs["runs"]["run_061"]["card_text"] = None
    assert _decide(inputs)["candidates"][0]["warnings"][0]["name"] == "GhostComponent"


def test_schema_refuses_an_empty_or_malformed_warnings_list():
    cand_schema = {**SCHEMA["$defs"]["candidate"], "$defs": SCHEMA["$defs"]}
    rec = _decide(_one_source([_sketch("profitability-run_061-1")]))
    cand = yaml.safe_load(yaml.safe_dump(rec["candidates"][0]))
    jsonschema.validate(cand, cand_schema)
    for bad in ([], [{"kind": "other", "name": "X", "suggestion": None}],
                [{"kind": "unknown_component_class", "name": "X"}]):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate({**cand, "warnings": bad}, cand_schema)


def test_done_step_logs_the_warning_from_the_proposal_on_disk(campaign_root, monkeypatch):
    """End to end: load_inputs reads the card text, decide records the warning,
    run_campaign prints one WARNING line."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    p = _patch("profitability-run_061-1")
    p["evidence"] = ["slices.overall.x=1 with VarianceRatioRegimeComponent"]
    _stage_flag_on_source(campaign_root, [p])
    root = campaign_root["root"]
    tb = root.parent / "tbot"
    (tb / "strategies").mkdir(parents=True)
    shutil.copy(TBOT / "strategies" / "strategy_components.py",
                tb / "strategies" / "strategy_components.py")
    monkeypatch.setattr(camp, "_TRADING_BOT_ROOT", tb)
    assert camp.process_once() is True
    rec = yaml.safe_load((root / "runs" / "run_061" / "artifacts" / "decision_record.yaml")
                         .read_text(encoding="utf-8"))
    assert rec["candidates"][0]["warnings"][0]["suggestion"] == "VarianceRatioComponent"
    assert ("WARNING profitability-run_061-1: reader names unknown component class "
            "VarianceRatioRegimeComponent (nearest real class: VarianceRatioComponent)") in _log(root)


def test_warning_log_lines_survive_a_side_finding_warning_without_a_name():
    """A reader_findings side-finding warning has no `name`: logging it must not
    raise KeyError (it left the entry in_progress with the brief already written),
    and a class-name warning must still log its name and suggestion."""
    record = {"candidates": [
        {"candidate_id": "side-1", "warnings": [
            {"kind": "repeats_measured_spec", "spec_hash": "abc", "own_claim": False, "runs": []},
            {"kind": "block_claim_cannot_see_block", "block_kind": "forecast", "message": "m"}]},
        {"candidate_id": "cls-1", "warnings": [
            {"kind": "unknown_component_class", "name": "GhostComponent", "suggestion": "RealComponent"},
            {"kind": "unknown_component_class", "name": "Other", "suggestion": None}]},
        {"candidate_id": "none-1"}]}
    assert camp._candidate_warning_lines(record, "ref.yaml") == [
        "WARNING side-1: repeats_measured_spec -- warning only, see ref.yaml",
        "WARNING side-1: block_claim_cannot_see_block -- warning only, see ref.yaml",
        "WARNING cls-1: reader names unknown component class GhostComponent "
        "(nearest real class: RealComponent) -- warning only, see ref.yaml",
        "WARNING cls-1: reader names unknown component class Other -- warning only, see ref.yaml"]
    assert camp._candidate_warning_lines({}, "ref.yaml") == []
    assert camp._candidate_warning_lines({"candidates": [{"candidate_id": "x", "warnings": [{}]}]},
                                         "r") == ["WARNING x: warning -- warning only, see r"]


def test_done_step_reads_the_card_on_disk_for_quotes(campaign_root, monkeypatch):
    """load_inputs hands decide the card's raw text: a name the card uses is a
    quote, not a warning."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    p = _patch("profitability-run_061-1")
    p["evidence"] = ["slices.overall.x=1 as the card's CardOnlyComponent says"]
    run_dir = _stage_flag_on_source(campaign_root, [p])
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        "hypothesis_id: FOO\nthesis: gate with CardOnlyComponent\n", encoding="utf-8")
    assert camp.process_once() is True
    rec = yaml.safe_load((run_dir / "artifacts" / "decision_record.yaml").read_text(encoding="utf-8"))
    assert "warnings" not in rec["candidates"][0]
    assert "WARNING" not in _log(campaign_root["root"])


def test_done_step_without_a_warning_logs_none(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    assert camp.process_once() is True
    assert "WARNING" not in _log(campaign_root["root"])


# ===========================================================================
# 2. The component-quarantine cap on R2 (review S3b)
# ===========================================================================

Q = "blocked_on_component:Foo"


@pytest.mark.parametrize("n,capped", [(2, False), (3, True), (4, True)])
def test_r2_stops_asking_a_brief_at_three_quarantined_requests(n, capped):
    entries = [_owner("B")] + [_req("B", i, Q) for i in range(1, n + 1)]
    out = dn._r2(entries, select=True)
    assert dn.BRIEF_MAX_COMPONENT_QUARANTINES == 3
    if capped:
        assert out["quarantine_capped_briefs"] == ["B"]
        assert out["eligible_briefs"] == [] and out["ready"] == [] and out["fired"] is False
        assert out["reason"].endswith(", 1 capped after 3 component quarantines: B")
    else:
        assert "quarantine_capped_briefs" not in out  # absent: old records unchanged
        assert out["eligible_briefs"] == ["B"] and out["ready"] == [f"B__more_{n + 1}"]


def test_the_owner_s_own_quarantine_counts():
    entries = [{**_owner("B"), "status": Q}, _req("B", 1, Q), _req("B", 2, Q)]
    assert dn.component_quarantines(entries[0], entries) == ["B", "B__more_1", "B__more_2"]
    assert dn._r2(entries, select=True)["quarantine_capped_briefs"] == ["B"]
    entries[0]["status"] = "done"
    assert "quarantine_capped_briefs" not in dn._r2(entries, select=True)


def test_a_reopen_marker_resets_the_count():
    owner = {**_owner("B"), "status": Q}
    entries = [owner] + [_req("B", i, Q) for i in (1, 2, 3)]
    assert dn._r2(entries, select=True)["quarantine_capped_briefs"] == ["B"]
    owner[dn.REOPENED_AFTER_KEY] = "B__more_2"   # only B__more_3 counts now
    assert dn.component_quarantines(owner, entries) == ["B__more_3"]
    out = dn._r2(entries, select=True)
    assert "quarantine_capped_briefs" not in out and out["eligible_briefs"] == ["B"]
    owner[dn.REOPENED_AFTER_KEY] = "B"           # the owner's own entry stops counting
    assert dn.component_quarantines(owner, entries) == ["B__more_1", "B__more_2", "B__more_3"]


def test_released_entries_no_longer_count_and_the_brief_is_never_closed():
    entries = [_owner("B")] + [_req("B", i, Q) for i in (1, 2, 3)]
    out = dn._r2(entries, select=True)
    assert out["quarantine_capped_briefs"] == ["B"] and out["exhausted_briefs"] == []
    assert entries[0]["brief_status"] == "open"
    entries[1]["status"] = "ready"               # the operator released one
    out = dn._r2(entries, select=True)
    assert "quarantine_capped_briefs" not in out and "B" in out["eligible_briefs"]


def test_operator_holds_are_held_briefs_not_capped():
    entries = [_owner("B")] + [_req("B", i, "blocked_on_e068") for i in (1, 2, 3)]
    out = dn._r2(entries, select=True)
    assert out["held_briefs"] == ["B"] and "quarantine_capped_briefs" not in out
    assert dn.component_quarantines(entries[0], entries) == []


def test_a_capped_brief_does_not_stop_another():
    entries = [_owner("B")] + [_req("B", i, Q) for i in (1, 2, 3)] + [_owner("C", priority=2)]
    out = dn._r2(entries, select=True)
    assert out["quarantine_capped_briefs"] == ["B"] and out["ready"] == ["C__more_1"]


def test_the_stop_line_names_the_capped_brief():
    queue = [_owner("H")] + [_req("H", i, Q) for i in (1, 2, 3)]
    rec = _decide(_empty_inputs(queue))
    assert rec["picked"] is None and rec["stop"]["reason"] == "no_eligible_candidate"
    assert rec["stop"]["detail"].endswith(
        "0 exhausted, 0 legacy, 1 capped after 3 component quarantines: H)")
    _valid(rec)
    queue[1]["status"] = "done"
    queue[1]["outcome"] = "refuted"
    assert "capped" not in (_decide(_empty_inputs(queue))["stop"] or {}).get("detail", "")


def test_the_schema_accepts_the_capped_list():
    r2 = dn._r2([_owner("B")] + [_req("B", i, Q) for i in (1, 2, 3)], select=True)
    jsonschema.validate({k: v for k, v in r2.items() if not k.startswith("_")},
                        SCHEMA["properties"]["rules"]["properties"]["r2"])


# ===========================================================================
# 3. Operator approval mode (CUL-399)
# ===========================================================================

def test_the_two_status_constants_match_and_fit_the_queue_schema():
    assert camp.OPERATOR_APPROVAL_STATUS == dn.OPERATOR_APPROVAL_STATUS == HELD
    assert rs._QUEUE_STATUS_RE.match(HELD)
    assert HELD in camp._REGISTER_STATUSES


def test_a_held_entry_is_an_operator_hold_and_never_picked():
    e = {"id": "X", "status": HELD, "priority": 1}
    assert dn.r2_request_operator_held(e) is True
    assert camp._select_entry([e]) is None and dn.select_entry_rule([e]) is None
    entries = [_owner("B"), _req("B", 1, HELD)]
    out = dn._r2(entries, select=True)
    assert out["held_briefs"] == ["B"] and out["ready"] == [] and out["enqueued"] == []
    assert dn.r2_request_yielded(entries[1]) is None


def test_flag_reader(campaign_root):
    root = campaign_root["root"]
    _write_flags(root)
    assert camp._operator_approval_enabled() is False
    _write_flags(root, operator_approval="true")
    with pytest.raises(ValueError, match="not a real boolean"):
        camp._operator_approval_enabled()
    _write_flags(root, operator_approval=True)
    with pytest.raises(ValueError, match="requires orchestrator.decide_next.enabled=true"):
        camp._operator_approval_enabled()
    _write_flags(root, **{**APPROVAL_ON, "verdict_routing_retired": False})
    with pytest.raises(ValueError,
                       match="requires orchestrator.verdict_routing_retired.enabled=true"):
        camp._operator_approval_enabled()
    _write_flags(root, **APPROVAL_ON)
    assert camp._operator_approval_enabled() is True


def test_the_launch_preflight_refuses_approval_without_decide_next(campaign_root):
    _write_flags(campaign_root["root"], operator_approval=True)
    values, refusal = camp._flag_preflight()
    assert refusal and "orchestrator.operator_approval.enabled=true requires" in refusal
    _write_flags(campaign_root["root"], **{**APPROVAL_ON, "verdict_routing_retired": False})
    values, refusal = camp._flag_preflight()
    assert refusal and ("orchestrator.operator_approval.enabled=true requires "
                        "orchestrator.verdict_routing_retired.enabled=true") in refusal
    _write_flags(campaign_root["root"], **APPROVAL_ON)
    values, refusal = camp._flag_preflight()
    assert refusal is None and values["operator_approval"] is True


def test_flag_is_off_in_the_real_config_and_registered():
    cfg = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["operator_approval"]["enabled"] is False
    reg = yaml.safe_load((_SR / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    entry = next(f for f in reg["flags"] if f["name"] == "operator_approval")
    assert entry["state"] == "off_incomplete"
    assert entry["reader"] == "run_campaign._operator_approval_enabled"


# ---- creation path A: decide-next's reader candidate -----------------------

@pytest.mark.parametrize("approval", [False, True])
def test_reader_candidate(campaign_root, monkeypatch, approval):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    root = campaign_root["root"]
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    if approval:
        _write_flags(root, **APPROVAL_ON)
    assert camp.process_once() is True
    _done, new = _queue(campaign_root)
    rec = yaml.safe_load((root / new["decision_ref"]).read_text(encoding="utf-8"))
    cid = "profitability-run_061-1"
    if approval:
        assert new["status"] == HELD and rec["picked"]["status"] == HELD
        assert camp._select_entry(_queue(campaign_root)) is None
        assert f"awaiting operator approval: {cid} (run_campaign.py --approve {cid})" in _log(root)
        assert f"-> queue entry {cid} ({HELD})" in _log(root)
    else:
        assert new["status"] == "ready" and "status" not in rec["picked"]
        assert "awaiting operator approval" not in _log(root)
    _valid(rec)


# ---- creation path B: a brief's extra card, queued -> ready -----------------

def _stage_card(campaign_root, approval):
    root = _stage_done(campaign_root, [_s2b_owner(status="in_progress"), _card_entry("OWNER__h2")],
                       pending="completed_refined")
    if approval:
        _write_flags(root, **APPROVAL_ON)
    _brief(root)
    _protocol(root)
    card = root / "campaign_record" / "queued_cards" / "run_001" / "hypothesis_card_2.yaml"
    card.parent.mkdir(parents=True)
    card.write_text("hypothesis_id: H2\n")
    (root / "runs" / "run_001" / "artifacts" / "queued_hypotheses.yaml").write_text(yaml.safe_dump({
        "enqueued": True, "cards": [{"n": 2, "card_ref": _card_entry("x")["card_ref"],
                                     "hypothesis_id": "H2", "scores": _SCORES, "model_id": "m",
                                     "rubric_version": "brief-card-v1"}]}))
    return root


@pytest.mark.parametrize("approval", [False, True])
def test_extra_card(campaign_root, monkeypatch, approval):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    root = _stage_card(campaign_root, approval)
    assert camp.process_once() is True
    by = {e["id"]: e for e in _queue(campaign_root)}
    rec = yaml.safe_load((root / by["OWNER__h2"]["decision_ref"]).read_text(encoding="utf-8"))
    assert rec["picked"]["card_ref"]
    if approval:
        assert by["OWNER__h2"]["status"] == HELD and rec["picked"]["status"] == HELD
        assert "awaiting operator approval: OWNER__h2 (run_campaign.py --approve OWNER__h2)" \
            in _log(root)
    else:
        assert by["OWNER__h2"]["status"] == "ready" and "status" not in rec["picked"]
    _valid(rec)


# ---- creation paths C + D: R2's new requests and waiting ones flipped -------

@pytest.mark.parametrize("approval", [False, True])
def test_r2_new_and_waiting_requests(campaign_root, monkeypatch, approval):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    waiting = {**_card_entry("OTHER__more_1", owner="OTHER"), "status": "queued"}
    del waiting["card_ref"]
    root = _stage_done(campaign_root, [_s2b_owner(status="in_progress"), _s2b_owner("OTHER"),
                                       waiting])
    if approval:
        _write_flags(root, **APPROVAL_ON)
    _brief(root)
    _brief(root, "OTHER")
    assert camp.process_once() is True
    by = {e["id"]: e for e in _queue(campaign_root)}
    rec = yaml.safe_load((root / "runs" / "run_001" / "artifacts" / "decision_record.yaml")
                         .read_text(encoding="utf-8"))
    r2 = rec["rules"]["r2"]
    assert sorted(r2["ready"]) == ["OTHER__more_1", "OWNER__more_1"]
    assert [q["entry_id"] for q in r2["enqueued"]] == ["OWNER__more_1"]   # new
    want = HELD if approval else "ready"
    assert by["OWNER__more_1"]["status"] == want                         # path C
    assert by["OTHER__more_1"]["status"] == want                         # path D
    assert [q["status"] for q in r2["enqueued"]] == [want]
    if approval:
        assert sorted(r2["awaiting_approval"]) == ["OTHER__more_1", "OWNER__more_1"]
        assert rec["picked"]["status"] == HELD
        assert camp._select_entry(_queue(campaign_root)) is None
        for rid in ("OWNER__more_1", "OTHER__more_1"):
            assert f"awaiting operator approval: {rid} (run_campaign.py --approve {rid})" \
                in _log(root)
        # the held requests hold their briefs: the next decision never re-mints
        nxt = dn._r2(_queue(campaign_root), select=True)
        assert sorted(nxt["held_briefs"]) == ["OTHER", "OWNER"] and nxt["enqueued"] == []
    else:
        assert "awaiting_approval" not in r2 and "status" not in rec["picked"]
    _valid(rec)


# ---- creation path E: R1's composition --------------------------------------

@pytest.mark.parametrize("approval", [False, True])
def test_r1_composition(campaign_root, monkeypatch, approval):
    import test_e060_s3b_composition_wiring as s3b
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    root = campaign_root["root"]
    s3b._stage_campaign(campaign_root)
    if approval:
        _write_flags(root, **s3b.FLAT_COMP_ON, operator_approval=True)
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    assert camp.process_once() is True
    _done, new = _queue(campaign_root)
    rec = yaml.safe_load((root / "runs" / "run_061" / "artifacts" / "decision_record.yaml")
                         .read_text(encoding="utf-8"))
    assert new["origin"] == "composition" and rec["picked"]["composition"] == new["id"]
    if approval:
        assert new["status"] == HELD and rec["picked"]["status"] == HELD
        assert f"awaiting operator approval: {new['id']}" in _log(root)
    else:
        assert new["status"] == "ready" and "status" not in rec["picked"]
    _valid(rec)


# ---- creation path F: the campaign-review reframe ---------------------------

@pytest.mark.parametrize("approval", [False, True])
def test_campaign_review_reframe(campaign_root, monkeypatch, approval):
    from test_e059_6c_s2b_campaign_review import _finished_reframe_run
    from test_e059_6c_s2a_route_retirement import FLAT_ON
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir, rel = _finished_reframe_run(campaign_root)
    if approval:
        _write_flags(campaign_root["root"], **APPROVAL_ON)
    entry = camp._load_queue()["queue"][0]
    assert camp._register_campaign_review_reframe(entry, "run_061", _state(run_dir)) is True
    new = camp._load_queue()["queue"][1]
    assert new["id"] == "run_061__reframe"
    log = _log(campaign_root["root"])
    if approval:
        assert new["status"] == HELD
        assert ("awaiting operator approval: run_061__reframe "
                "(run_campaign.py --approve run_061__reframe)") in log
    else:
        assert new["status"] == "ready" and "awaiting operator approval" not in log
    rs.validate_queue_entry(new)


def _state(run_dir):
    return yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))


# ---- operator actions are unchanged -----------------------------------------

def test_register_cli_is_an_operator_action_never_held(campaign_root):
    root = campaign_root["root"]
    _write_flags(root, **APPROVAL_ON)
    brief = _brief(root, "OP")
    assert camp._register_from_cli(brief, 5, "n") == 0
    (entry,) = _queue(campaign_root)
    assert entry["status"] == "ready" and entry["brief_status"] == "open"


# ---- --approve ----------------------------------------------------------------

def _held_queue(campaign_root, status=HELD):
    _save_queue_entries(campaign_root["queue_path"], [
        {"id": "A", "brief_path": "briefs/A.md", "status": status, "priority": 999,
         "source": "agent", "notes": "n", "run_ids": [], "origin": "reader"}])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[], trial_sharpes=[])


def test_approve_sets_a_held_entry_ready(campaign_root):
    root = campaign_root["root"]
    _held_queue(campaign_root)
    assert camp._approve_entry("A") is True
    (entry,) = _queue(campaign_root)
    assert entry["status"] == "ready" and entry["priority"] == 999
    assert "APPROVE A: approved by the operator; entry ready (priority 999)." in _log(root)
    assert "| A | ready |" in (root / "campaign_summary.md").read_text(encoding="utf-8")
    assert (root / "campaign_record" / "loop_health.yaml").exists()
    assert not campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH).exists()  # released


@pytest.mark.parametrize("status", ["ready", "queued", "in_progress", "done",
                                    "blocked_on_component:Foo", "blocked_on_e068",
                                    "paused:waiting_for_component", "paused:stage_exception"])
def test_approve_refuses_anything_not_held(campaign_root, status, capsys):
    _held_queue(campaign_root, status=status)
    before = campaign_root["queue_path"].read_text(encoding="utf-8")
    assert camp._approve_entry("A") is False
    assert campaign_root["queue_path"].read_text(encoding="utf-8") == before
    assert "--approve refused" in capsys.readouterr().out


def test_approve_refuses_an_unknown_id_and_a_held_lock(campaign_root):
    _held_queue(campaign_root)
    assert camp._approve_entry("NOPE") is False
    lock = campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH)
    campaign_lock.acquire(lock)
    try:
        assert camp._approve_entry("A") is False
        assert lock.exists()
    finally:
        campaign_lock.release(lock)
    assert _queue(campaign_root)[0]["status"] == HELD


def test_the_cli_has_approve():
    src = (_SR / "workflow" / "run_campaign.py").read_text(encoding="utf-8")
    assert 'parser.add_argument("--approve", metavar="ENTRY_ID"' in src
    assert "sys.exit(0 if _approve_entry(args.approve) else 1)" in src


# ---- summary and the queue-exhausted line --------------------------------------

def test_summary_lists_awaiting_entries_only_when_any(campaign_root):
    root = campaign_root["root"]
    _held_queue(campaign_root, status="ready")
    camp._regenerate_summary(camp._load_queue())
    assert "Awaiting operator approval" not in (root / "campaign_summary.md").read_text(
        encoding="utf-8")
    _held_queue(campaign_root)
    camp._regenerate_summary(camp._load_queue())
    text = (root / "campaign_summary.md").read_text(encoding="utf-8")
    assert "## Awaiting operator approval (approve with --approve <id>)" in text
    assert "| A | reader | 999 | briefs/A.md |" in text


def test_queue_exhausted_names_held_entries(campaign_root):
    root = campaign_root["root"]
    _held_queue(campaign_root)
    assert camp.process_once() is False
    assert ("Queue exhausted — no ready or in_progress entries remain. Awaiting operator "
            "approval: ['A'] -- approve with --approve <id>") in _log(root)
    assert camp._approval_note({"queue": [{"id": "B", "status": "ready"}]}) == ""


# ===========================================================================
# 4. Token budget
# ===========================================================================

def test_token_budget_is_1_8_million():
    cfg = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["token_budget_per_run_weighted_units"] == 1800000
    assert rpr._load_token_budget() == 1800000.0


# ===========================================================================
# Review round 1
# ===========================================================================

def _card(eid, owner, status, run="run_001"):
    return {"id": eid, "brief_path": f"briefs/{owner}.md", "status": status, "priority": 999,
            "origin": "brief", "card_ref": f"campaign_record/queued_cards/{run}/hypothesis_card_2.yaml"}


def test_stop_line_names_held_entries(campaign_root, monkeypatch):
    """Fix 1: a decide-next stop names entries awaiting approval."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = campaign_root["root"]
    _stage_flag_on_source(campaign_root, [_sketch("profitability-run_061-1", kind="regime")])
    _write_flags(root, **APPROVAL_ON)
    queue = _queue(campaign_root)
    queue.append({"id": "HELD_ONE", "brief_path": "b.md", "status": HELD, "priority": 999,
                  "source": "agent", "notes": "n", "run_ids": [], "origin": "reader"})
    _save_queue_entries(campaign_root["queue_path"], queue)
    assert camp.process_once() is False
    line = next(l for l in _log(root).splitlines() if "DECIDE stop after" in l)
    assert line.endswith("Awaiting operator approval: ['HELD_ONE'] -- approve with --approve <id> "
                         "(RUNBOOK.md §4 Approval mode).")


@pytest.mark.parametrize("status,held", [(HELD, True), ("blocked_on_e068", True),
                                         ("blocked_on_component:Foo", False),
                                         ("queued", False), ("ready", False)])
def test_a_held_extra_card_holds_its_brief(status, held):
    """Fix 2: an operator-held card is an unrun idea of the brief; R2 waits."""
    entries = [_owner("B"), _card("B__h2", "B", status)]
    out = dn._r2(entries, select=True)
    if held:
        assert out["held_briefs"] == ["B"] and out["enqueued"] == [] and out["ready"] == []
    else:
        assert out["held_briefs"] == []


def test_a_held_card_of_another_brief_does_not_hold_this_one():
    entries = [_owner("B"), _owner("C", priority=2), _card("C__h2", "C", HELD)]
    out = dn._r2(entries, select=True)
    assert out["held_briefs"] == ["C"] and out["ready"] == ["B__more_1"]


def test_quarantined_cards_count_toward_the_cap():
    """Fix 5: owner + 1 request + 1 card = 3 -> capped."""
    owner = {**_owner("B"), "status": Q, "run_ids": ["run_001"]}
    entries = [owner, _req("B", 1, Q), _card("B__h2", "B", Q)]
    assert dn.component_quarantines(owner, entries) == ["B", "B__more_1", "B__h2"]
    assert dn._r2(entries, select=True)["quarantine_capped_briefs"] == ["B"]
    entries[2]["status"] = "queued"
    assert "quarantine_capped_briefs" not in dn._r2(entries, select=True)


def test_a_reopen_marker_drops_cards_written_before_it():
    owner = {**_owner("B"), "status": Q, "run_ids": ["run_001"]}
    req1 = {**_req("B", 1, Q), "run_ids": ["run_002"]}
    req2 = {**_req("B", 2, Q), "run_ids": ["run_003"]}
    entries = [owner, req1, req2, _card("B__h2", "B", Q, run="run_001"),
               _card("B__h3", "B", Q, run="run_003"), _card("B__h4", "B", Q, run="run_999")]
    assert len(dn.component_quarantines(owner, entries)) == 6   # no marker: every card
    owner[dn.REOPENED_AFTER_KEY] = "B__more_1"
    # only B__more_2 and the card its run wrote count; an unclaimed card does not
    assert dn.component_quarantines(owner, entries) == ["B__more_2", "B__h3"]


def test_a_brief_held_and_capped_is_listed_once_as_held():
    entries = [_owner("B")] + [_req("B", i, Q) for i in (1, 2, 3)] + [_req("B", 4, HELD)]
    out = dn._r2(entries, select=True)
    assert out["held_briefs"] == ["B"] and "quarantine_capped_briefs" not in out
    rec = _decide(_empty_inputs(entries))
    assert rec["stop"]["detail"].count("B") == 1 and "capped" not in rec["stop"]["detail"]


def test_docs_carry_the_round_1_fixes():
    guide = (_SR / "docs" / "USER_GUIDE.md").read_text(encoding="utf-8")
    assert "**1,800,000 weighted units** by default" in guide
    runbook = (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert "counts as an EMPTY answer in the" in runbook
    assert "resets the O-20 exhausted-answer count" in runbook
