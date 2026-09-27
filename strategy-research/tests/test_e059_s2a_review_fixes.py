"""
E-059 S2a code-review fixes (review of d0038635..69b684f9). Every test here
fails on 69b684f9 and passes after the fix commit. Numbering follows the
review: 1 novelty key, 2 collapse, 3 DONE-branch atomicity, 4 1a pass_rule
checks, 5 1a re-run, 6 SKILL.md, 7 stop condition, 8 proposal ids, 9 truthful
record, 10 quarantine path, plus the 5a manifest check.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import decide_next as dn  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _entry, _prescreen_row, _save_queue_entries, _stage_halt, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_s2a_decide_next import (  # noqa: E402
    _ALL_ON, _MANIFEST, _base_config, _copy_menu, _decide, _inputs, _memory_entry,
    _one_source, _patch, _sketch, _src, _stage_5a, _stage_flag_on_source,
    _write_candidate_run, _write_flags,
)

_WINDOWS = [{"label": "2024-01", "test": {"start": "2024-01-01", "end": "2024-02-01"}},
            {"label": "2024-02", "test": {"start": "2024-02-01", "end": "2024-03-01"}}]


def _read_queue(campaign_root):
    return yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]


# ---------------------------------------------------------------------------
# 1. Novelty key: protocol CONTENT, normalised timeframe and paths
# ---------------------------------------------------------------------------

def _write_protocol(root: Path, name: str, timeframe="1h", windows=_WINDOWS):
    (root / "protocols").mkdir(exist_ok=True)
    (root / "protocols" / name).write_text(json.dumps(
        {"symbols": ["BTCUSDT"], "timeframe": timeframe, "windows": windows}), encoding="utf-8")


def test_generated_protocol_return_to_a_tested_config_is_a_repeat(tmp_path):
    """run_050 tested config X on protocols/run_050_generated.json; run_061 (a
    different config) ran on protocols/run_061_generated.json with the SAME
    windows. A patch of run_061 that returns to X is a REPEAT."""
    _write_protocol(tmp_path, "run_050_generated.json", timeframe="1H")
    _write_protocol(tmp_path, "run_061_generated.json")
    p = _patch("profitability-run_061-1", after=0.8)
    inputs = _one_source([p])
    inputs["memory"]["runs"]["run_061"]["protocol_ref"] = "protocols/run_061_generated.json"
    inputs["memory"]["runs"]["run_050"] = _memory_entry(
        "run_050", fh=dn.config_sha256(_base_config(min_abs=0.8)),
        protocol_ref="protocols\\run_050_generated.json", timeframe="1H")
    inputs["protocol_specs"] = {
        ref: dn.protocol_spec(tmp_path, ref)
        for ref in ("protocols/run_050_generated.json", "protocols/run_061_generated.json")}
    c = _decide(inputs)["candidates"][0]
    assert c["gates"]["novelty"]["exact_match"] == "REPEAT"
    assert c["gates"]["novelty"]["matched_runs"] == ["run_050"]
    # different windows -> a different window set -> NOVEL
    _write_protocol(tmp_path, "run_050_generated.json", windows=_WINDOWS[:1])
    inputs["protocol_specs"]["protocols/run_050_generated.json"] = dn.protocol_spec(
        tmp_path, "protocols/run_050_generated.json")
    assert _decide(inputs)["candidates"][0]["gates"]["novelty"]["exact_match"] == "NOVEL"


def test_load_inputs_reads_protocol_specs(tmp_path):
    _write_protocol(tmp_path, "run_061_generated.json", timeframe="1H")
    (tmp_path / "campaign_record").mkdir()
    mem = {"schema_version": 1, "legacy_note": "", "runs": {"run_061": _memory_entry(
        "run_061", protocol_ref="protocols/run_061_generated.json")}}
    mem["runs"]["run_061"]["proposals"] = []
    (tmp_path / "campaign_record" / "campaign_memory.yaml").write_text(yaml.safe_dump(mem),
                                                                        encoding="utf-8")
    inputs = dn.load_inputs(tmp_path, {"queue": []}, categories=["profitability"])
    spec = inputs["protocol_specs"]["protocols/run_061_generated.json"]
    assert spec["timeframe"] == "1h" and len(spec["windows_sha256"]) == 64


# ---------------------------------------------------------------------------
# 2. Collapse among eligible candidates only, on the full novelty key
# ---------------------------------------------------------------------------

def test_an_ineligible_duplicate_never_shadows_an_eligible_one():
    """Same patched config from two source runs: on run_061's symbols it was
    already tested (REPEAT, ineligible, higher score); on run_062's symbols it
    is new. The eligible one must survive and be picked."""
    patched = dn.config_sha256(_base_config(min_abs=0.8))
    a = _src([_patch("profitability-run_061-1", conf=3)])
    b = _src([_patch("profitability-run_062-1", conf=1)])
    memory = {
        "run_061": _memory_entry("run_061", proposal_ids=["profitability-run_061-1"]),
        "run_062": _memory_entry("run_062", symbols=("ETHUSDT",), fh="e" * 64,
                                 proposal_ids=["profitability-run_062-1"]),
        "run_050": _memory_entry("run_050", fh=patched),  # BTCUSDT, same protocol
    }
    rec = _decide(_inputs({"run_061": a, "run_062": b}, memory))
    by_id = {c["candidate_id"]: c for c in rec["candidates"]}
    assert by_id["profitability-run_061-1"]["eligible"] is False
    assert by_id["profitability-run_062-1"]["eligible"] is True
    assert rec["picked"]["candidate_id"] == "profitability-run_062-1"


# ---------------------------------------------------------------------------
# 3. DONE-branch atomicity: decide-next is retryable
# ---------------------------------------------------------------------------

def test_a_failed_decision_leaves_the_entry_retryable(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = campaign_root["root"]
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    real_decide = dn.decide

    def boom(*a, **k):
        raise RuntimeError("decide failed")
    monkeypatch.setattr(dn, "decide", boom)
    with pytest.raises(RuntimeError, match="decide failed"):
        camp.process_once()
    queue = _read_queue(campaign_root)
    assert [e["status"] for e in queue] == ["in_progress"]
    assert not (root / "runs" / "run_061" / "artifacts" / "decision_record.yaml").exists()

    monkeypatch.setattr(dn, "decide", real_decide)
    assert camp.process_once() is True  # retried: same entry selected again
    queue = _read_queue(campaign_root)
    assert queue[0]["status"] == "done" and queue[0]["outcome"] == "refuted"
    assert queue[1]["id"] == "profitability-run_061-1"


def test_a_refused_registration_rolls_the_brief_back(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = campaign_root["root"]
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    monkeypatch.setattr(camp, "register_hypothesis", lambda *a, **k: 1)
    with pytest.raises(RuntimeError, match="refused"):
        camp.process_once()
    assert not (root / "campaign_record" / "candidate_briefs" / "profitability-run_061-1.md").exists()
    assert not (root / "runs" / "run_061" / "artifacts" / "decision_record.yaml").exists()
    assert [e["status"] for e in _read_queue(campaign_root)] == ["in_progress"]


# ---------------------------------------------------------------------------
# 4. 1a pass_rule checks
# ---------------------------------------------------------------------------

def _candidate_run(campaign_root, mc=None):
    root = campaign_root["root"]
    _copy_menu(root)
    inputs = _one_source([_patch("profitability-run_061-1")])
    if mc is not None:
        inputs["runs"]["run_061"]["pre_registration"]["machine_constraints"] = mc
    return _write_candidate_run(root, "run_062", inputs, _decide(inputs))


def _card(run_dir, criteria, hid="FOO__profitability-run_061-1"):
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": hid, "criteria": criteria}), encoding="utf-8")


@pytest.mark.parametrize("criterion,match", [
    ({"id": "realized_edge_to_cost_ratio", "threshold": 0.01}, "does not let a card set"),
    ({"id": "realized_edge_to_cost_ratio", "comparator": ">="}, "does not let a card set"),
    ({"id": "sign_consistent_by_era", "null_handling": "fails_threshold"}, "does not let a card set"),
    ({"id": "sign_consistent_by_era", "notes": "x"}, "does not let a card set"),
])
def test_card_overrides_and_stray_keys_are_refused(campaign_root, criterion, match):
    run_dir = _candidate_run(campaign_root)
    _card(run_dir, [criterion])
    with pytest.raises(ValueError, match=match):
        rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True)


def test_a_menu_allowed_override_is_kept(campaign_root):
    run_dir = _candidate_run(campaign_root)
    _card(run_dir, [{"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}])
    rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True)
    pre = yaml.safe_load((run_dir / "artifacts" / "pre_registration.yaml").read_text(encoding="utf-8"))
    crit = pre["pass_rule"]["criteria"][0]
    assert crit["metric"] == "forecast_return_corr" and crit["reducer"] == "sign_consistent_by_era"
    assert "basis" not in crit and "card_overridable" not in crit


def test_k3_lint_runs_on_the_1a_pass_rule(campaign_root):
    run_dir = _candidate_run(campaign_root)
    pre_path = run_dir / "artifacts" / "pre_registration.yaml"
    pre = yaml.safe_load(pre_path.read_text(encoding="utf-8"))
    pre["machine_constraints"] = {"protocol_ref": "protocols/nested/p.json"}
    pre_path.write_text(yaml.safe_dump(pre), encoding="utf-8")
    _card(run_dir, [{"id": "sign_consistent_by_era"}])
    with pytest.raises(ValueError, match="K3"):
        rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True)


# ---------------------------------------------------------------------------
# 5. 1a re-run rewrites the pass_rule from the CURRENT card
# ---------------------------------------------------------------------------

def test_a_1a_rerun_rewrites_the_pass_rule_and_rechecks_the_id(campaign_root):
    run_dir = _candidate_run(campaign_root)
    pre_path = run_dir / "artifacts" / "pre_registration.yaml"
    _card(run_dir, [{"id": "sign_consistent_by_era"}])
    rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True)
    _card(run_dir, [{"id": "realized_edge_to_cost_ratio"}])  # 1a re-run, new card
    assert rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True) is True
    pre = yaml.safe_load(pre_path.read_text(encoding="utf-8"))
    assert [c["id"] for c in pre["pass_rule"]["criteria"]] == ["realized_edge_to_cost_ratio"]
    assert pre["pass_rule_pending"] == "hypothesis_generation"
    _card(run_dir, [{"id": "realized_edge_to_cost_ratio"}], hid="SOMETHING_ELSE")
    with pytest.raises(ValueError, match="not the candidate"):
        rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True)
    # after the marker is cleared (run advanced), a rewound 1a still rewrites
    rpr._clear_pass_rule_pending(run_dir, "strategy_config_authoring")
    _card(run_dir, [{"id": "sign_consistent_by_era"}])
    assert rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True) is True
    pre = yaml.safe_load(pre_path.read_text(encoding="utf-8"))
    assert [c["id"] for c in pre["pass_rule"]["criteria"]] == ["sign_consistent_by_era"]


# ---------------------------------------------------------------------------
# 6. SKILL.md unchanged; the addendum is injected only under the flag
# ---------------------------------------------------------------------------

# sha256 of workflow_artifacts/skills/hypothesis-design/SKILL.md at master
# d0038635 (LF line endings), measured with `git show d0038635:<path> | sha256sum`,
# was ba59fb3df0a62aca10991fedd112992f47f2881219c7697a161eec5aa4baef6d.
# RE-PINNED by E-036 S2a (2026-09-27): a DECLARED change to the skill's
# IMPROVEMENT 05 section only (rewritten to describe either "already tried"
# input -- artifacts/tried_ideas.yaml when campaign memory exists, else the
# legacy exclusion digest; S1_FINDINGS_SLICE8.md operator decision 3). decide_next's addendum is still
# not in the skill -- this pin keeps guarding that.
_MASTER_SKILL_SHA256 = "773051a327b81f4b9f6cd616a220e35ad2982cb3a11110df3bac3a2dfa4c545a"


def test_hypothesis_design_skill_is_byte_identical_to_master():
    raw = (_SR / "workflow_artifacts" / "skills" / "hypothesis-design" / "SKILL.md").read_bytes()
    assert hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest() == _MASTER_SKILL_SHA256


def _hg_handoff():
    return {"required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "r"}]}


@pytest.mark.parametrize("flags", [None, {"decide_next": False}])
def test_flag_off_1a_prompt_is_byte_identical(campaign_root, monkeypatch, flags):
    monkeypatch.chdir(_SR)
    run_dir = _candidate_run(campaign_root)  # a candidate brief, but the flag is off
    if flags is not None:
        _write_flags(campaign_root["root"], **flags)
    handoff = _hg_handoff()
    before = copy.deepcopy(handoff)
    rpr._apply_decide_next_context("hypothesis_generation", handoff, run_dir)
    assert handoff == before
    assert rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir) == \
        rpr._build_stage_prompt("hypothesis_generation", before, run_dir)


def test_flag_on_injects_the_addendum_for_candidates_only(campaign_root, monkeypatch):
    monkeypatch.chdir(_SR)
    run_dir = _candidate_run(campaign_root)
    _write_flags(campaign_root["root"], **_ALL_ON)
    handoff = _hg_handoff()
    rpr._apply_decide_next_context("hypothesis_generation", handoff, run_dir)
    paths = [r["path"] for r in handoff["required_inputs"]]
    assert paths[-1].endswith("hypothesis-design/DECIDE_NEXT_CANDIDATES.md")
    # run-dir relative, like the other ../../ inputs: resolves under ROOT
    assert (run_dir / paths[-1]).resolve() == (
        campaign_root["root"] / "workflow_artifacts" / "skills" / "hypothesis-design"
        / "DECIDE_NEXT_CANDIDATES.md").resolve()
    text = (_SR / "workflow_artifacts" / "skills" / "hypothesis-design"
            / "DECIDE_NEXT_CANDIDATES.md").read_text(encoding="utf-8")
    assert "EXCEPTION to IMPROVEMENT 08" in text
    other = _write_fresh_scaffold(campaign_root["runs_dir"], "run_070")
    handoff2 = _hg_handoff()
    rpr._apply_decide_next_context("hypothesis_generation", handoff2, other)
    assert handoff2 == _hg_handoff()


# ---------------------------------------------------------------------------
# 7 + 9. The record's pick is what the scheduler runs; no stop while it has work
# ---------------------------------------------------------------------------

def test_no_stop_while_an_in_progress_entry_remains():
    inputs = _one_source([_sketch("profitability-run_061-1", kind="regime")])
    inputs["queue"] = {"queue": [{"id": "OTHER", "status": "in_progress", "run_ids": ["run_050"]}]}
    rec = _decide(inputs)
    assert rec["stop"] is None and rec["picked"]["operator_entry"] == "OTHER"


def test_recorded_pick_matches_the_scheduler(campaign_root, monkeypatch):
    """An operator entry at priority 1500 and an agent entry at 999: the
    scheduler runs the agent entry, so the record must say so."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = campaign_root["root"]
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    queue = _read_queue(campaign_root)
    queue += [{"id": "OPERATOR", "brief_path": "b.md", "status": "ready", "priority": 1500,
               "source": "operator_ratified", "relation": "new_registration", "notes": "n",
               "run_ids": []},
              {"id": "AGENT", "brief_path": "a.md", "status": "ready", "priority": 999,
               "source": "agent", "origin": "reader", "notes": "n", "run_ids": []}]
    _save_queue_entries(campaign_root["queue_path"], queue)
    assert camp.process_once() is True
    after = _read_queue(campaign_root)
    record = yaml.safe_load((root / "runs" / "run_061" / "artifacts" /
                             "decision_record.yaml").read_text(encoding="utf-8"))
    scheduled = camp._select_entry(after)["id"]
    assert scheduled == "AGENT"
    assert (record["picked"].get("queue_entry_id") or record["picked"].get("operator_entry")) \
        == scheduled
    assert len(after) == 3  # nothing minted


@pytest.mark.parametrize("entries", [
    [],
    [{"id": "a", "status": "ready", "priority": 5}, {"id": "b", "status": "ready", "priority": 2}],
    [{"id": "a", "status": "ready", "priority": 1}, {"id": "b", "status": "in_progress"}],
    [{"id": "a", "status": "ready"}, {"id": "b", "status": "ready", "priority": 999}],
    [{"id": "a", "status": "queued", "priority": 1}, {"id": "b", "status": "done"}],
])
def test_select_entry_mirror_matches_the_scheduler(entries):
    assert dn.select_entry_rule(copy.deepcopy(entries)) == camp._select_entry(copy.deepcopy(entries))


# ---------------------------------------------------------------------------
# 8. Proposal ids are safe names tied to their run; collisions are refused
# ---------------------------------------------------------------------------

def _raw_proposal(pid):
    p = _patch("profitability-run_061-1")
    p["proposal_id"] = pid
    return p


@pytest.mark.parametrize("pid", [
    "profitability-run_999-1",          # middle segment is not the source run
    "profitability-run_061/../x-1",
    "profitability-run_061#x-1",
    "profitability-..-1",
])
def test_unsafe_or_foreign_proposal_ids_are_ineligible(pid):
    inputs = _one_source([_raw_proposal(pid)])
    rec = _decide(inputs)
    c = rec["candidates"][0]
    assert c["eligible"] is False
    assert c["gates"]["feasibility"]["reasons"][0].startswith("unsafe_proposal_id")
    assert rec["picked"] is None


def test_queue_id_and_brief_collisions_are_ineligible():
    inputs = _one_source([_patch("profitability-run_061-1")])
    inputs["queue"] = {"queue": [{"id": "profitability-run_061-1", "status": "done"}]}
    c = _decide(inputs)["candidates"][0]
    assert c["eligible"] is False and c["gates"]["feasibility"]["reasons"][0].startswith(
        "queue_id_collision")
    inputs = _one_source([_patch("profitability-run_061-1")])
    inputs["existing_candidate_briefs"] = ["profitability-run_061-1.md"]
    c = _decide(inputs)["candidates"][0]
    assert c["eligible"] is False and c["gates"]["feasibility"]["reasons"][0].startswith(
        "brief_collision")


# ---------------------------------------------------------------------------
# 10. The quarantine path that marks a lineage done also runs decide-next
# ---------------------------------------------------------------------------

def test_quarantine_done_path_runs_decide_next(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = campaign_root["root"]
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    cfg = {"orchestrator": {**{k: {"enabled": v} for k, v in _ALL_ON.items()},
                            "halt_policy": {"quarantine_enabled": True}}}
    (root / "config" / "campaign_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    _stage_halt(campaign_root, "run_911", "component_execution_error",
                trial_rows=[_prescreen_row("run_911")])
    assert camp.process_once() is True
    queue = _read_queue(campaign_root)
    assert queue[0]["status"] == "done" and queue[0]["outcome"] == camp._QUARANTINE_OUTCOME
    assert queue[1]["id"] == "profitability-run_061-1" and queue[1]["status"] == "ready"
    record = yaml.safe_load((root / "runs" / "run_911" / "artifacts" /
                             "decision_record.yaml").read_text(encoding="utf-8"))
    assert record["picked"]["candidate_id"] == "profitability-run_061-1"
    assert "DECIDE after TEST_ENTRY (run_911)" in (root / "campaign_log.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 5a: the copied block manifest is checked too
# ---------------------------------------------------------------------------

def test_5a_stops_on_a_drifted_manifest(tmp_path):
    cfg = _base_config(min_abs=0.8)
    arts = _stage_5a(tmp_path, cfg, dn.config_sha256(cfg))
    brief = yaml.safe_load((arts / "research_brief.yaml").read_text(encoding="utf-8"))
    brief["candidate"]["source"]["expected_manifest_sha256"] = dn.config_sha256(_MANIFEST)
    (arts / "research_brief.yaml").write_text(yaml.safe_dump(brief), encoding="utf-8")
    drifted = copy.deepcopy(_MANIFEST)
    drifted["block"]["config_paths"] = ["/strategies"]
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(drifted), encoding="utf-8")
    with pytest.raises(RuntimeError, match="block_manifest.yaml"):
        rpr._check_pass_through_config_hash(arts)
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(_MANIFEST), encoding="utf-8")
    rpr._check_pass_through_config_hash(arts)


def test_candidate_brief_carries_the_expected_manifest_hash(tmp_path):
    inputs = _one_source([_patch("profitability-run_061-1")])
    _, text = dn.candidate_brief(_decide(inputs), inputs, decision_ref="r")
    front = yaml.safe_load(text.split("---\n")[1])
    assert front["candidate"]["source"]["expected_manifest_sha256"] == dn.config_sha256(_MANIFEST)
