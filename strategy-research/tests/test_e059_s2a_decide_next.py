"""
E-059 S2a -- decide_next core + queue fields (delivery_plan_v26.md slice 6b,
flag off). Spec: engineering/roadmap/E-059/S1_FINDINGS_6B.md and its operator
decision of 2026-09-24.

Proven here, all with synthetic inputs (no LLM, no backtest, no trial row, no
holdout):
  * flag off: process_once's DONE branch and campaign_queue.yaml are
    byte-identical; register_hypothesis's defaults are unchanged;
  * the pure decide(): ranking order + tie-break, exact-match novelty refuses,
    the legacy digest never refuses, operator entries first, collapse, patch
    resolution (unique / ambiguous / missing / stale / bad field), regime
    sketch infeasible, stop, determinism, no retired field, NO lineage
    demotion, scores never touch idea_status or the memory;
  * decision 2: a proposal-sourced candidate's brief carries no criteria, its
    pre_registration is pending at 1a, and the pass_rule is written from 1a's
    card -- never the source run's;
  * the 5a pass-through hash check; the flag reader; the schema fields;
  * flag on, end to end through process_once with run_loop stubbed: outcome
    := idea_status citing idea_status.yaml (no _save_queue crash), one ready
    agent entry, a decision record, and _select_entry picking it next.
"""
from __future__ import annotations

import copy
import json
import re
import shutil
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
import json_pointer as jp  # noqa: E402
import record_schema as rs  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import campaign_memory as cm  # noqa: E402
import build_exclusion_digest as bed  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _entry, _save_queue_entries, _write_campaign_state, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)

CATS = ["profitability", "trade_efficiency", "forecast_power", "regime_power",
        "component_attribution"]
CLS = "strategies.strategy_components.FundingRateMeanReversionComponent"


# ---------------------------------------------------------------------------
# Synthetic fixtures
# ---------------------------------------------------------------------------

def _base_config(min_abs=0.5, lookback=500):
    return {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                            "default_regime": "unknown"},
        "strategies": {"warmup": 10, "regimes": {"unknown": {"components": [{
            "id": "funding_mr", "class": CLS, "lookback": lookback, "weight": 1.0,
            "params": {"z": 2.0},
            "transforms": [{"op": "clip"}, {"op": "scale"},
                           {"op": "threshold_filter", "params": {"min_abs": min_abs}}],
        }]}}},
    }


_MANIFEST = {"block": {"kind": "forecast",
                       "config_paths": ["/strategies/regimes/unknown/components/0"]},
             "scaffolding": ["/regime_detector"], "rationale": "the funding MR block"}


def _patch(pid, after=0.8, before=0.5, conf=2, dist=1, mech=2, field="transforms[2].params.min_abs",
           component_id="funding_mr"):
    return {"proposal_id": pid, "kind": "patch",
            "patch": [{"component_id": component_id, "field": field,
                       "before": before, "after": after}],
            "evidence": ["slices.overall.x=1"],
            "scores": {"confidence_real": conf, "distance_to_profitable": dist,
                       "mechanism_plausibility": mech},
            "model_id": "m", "rubric_version": "profitability-reader-v1"}


def _sketch(pid, kind="forecast", conf=1, dist=1):
    return {"proposal_id": pid, "kind": "new_block",
            "block": {"kind": kind, "config_paths": ["/strategies/regimes/unknown/components/1"],
                      "rationale": "a new block"},
            "evidence": ["slices.overall.y=2"],
            "scores": {"confidence_real": conf, "distance_to_profitable": dist,
                       "mechanism_plausibility": 1},
            "model_id": "m", "rubric_version": "profitability-reader-v1"}


def _memory_entry(run_id, hyp="FOO", fh="f" * 64, symbols=("BTCUSDT",), n_windows=8,
                  timeframe="1h", protocol_ref="protocols/p8.json", idea_status="refuted",
                  proposal_ids=()):
    return {
        "run_id": run_id, "hypothesis_id": hyp, "legacy": False, "recorded_at": "t",
        "idea_status": idea_status, "idea_status_reason": "r",
        "idea_status_ref": f"runs/{run_id}/artifacts/idea_status.yaml",
        "engineering_fault": None, "engineering_fault_detail": [],
        "grid": {}, "trial_ids": [f"{run_id}:base"],
        "variants": {"base": {"status": "tested", "reason": None,
                              "config_ref": f"runs/{run_id}/artifacts/variants/base/strategy_config.json",
                              "forecast_hash": fh, "symbols": list(symbols),
                              "n_windows": n_windows, "trial_id": f"{run_id}:base"}},
        "protocol_ref": protocol_ref, "timeframe": timeframe,
        "proposals": [{"category": "profitability",
                       "ref": f"runs/{run_id}/artifacts/proposals/profitability.yaml",
                       "proposal_ids": list(proposal_ids), "count": len(proposal_ids)}],
        "registry": {"skipped": "not_validated"}, "profit_bars": None,
        "profit_bars_reason": cm.PROFIT_BARS_NOT_EVALUATED, "kb_entry_id": None,
    }


_SOURCE_PASS_RULE = {"criteria": [{"id": "realized_edge_to_cost_ratio",
                                   "metric": "realized_edge_to_cost_ratio", "source": "pooled",
                                   "comparator": ">", "threshold": 0.3}]}


def _src(proposals, config=None, manifest=_MANIFEST, pass_rule_nested=False):
    mc = {"protocol_ref": "protocols/p8.json"}
    if pass_rule_nested:
        mc["pass_rule"] = copy.deepcopy(_SOURCE_PASS_RULE)
    return {
        "proposals": [{"category": "profitability", "proposal": p} for p in proposals],
        "base_variant": "base",
        "base_config": copy.deepcopy(config if config is not None else _base_config()),
        "base_config_ref": "runs/run_061/artifacts/variants/base/strategy_config.json",
        "manifest": copy.deepcopy(manifest),
        "pre_registration": {"pass_rule": copy.deepcopy(_SOURCE_PASS_RULE),
                             "machine_constraints": mc},
        "research_brief": {"strategy_domain": "crypto", "market_universe": "BTCUSDT",
                           "timeframe": "1h", "research_goal": "old goal", "venue": "binance",
                           "product": "perp"},
        "card": {"hypothesis_id": "FOO", "thesis": "funding mean reversion"},
    }


def _inputs(runs: dict, memory_runs: dict, queue=None, known=(CLS,), digest=None, revision=0):
    return {
        "memory": {"schema_version": 1, "legacy_note": "", "runs": memory_runs},
        "memory_sha256": "m" * 64, "registry_revision": revision,
        "queue": queue if queue is not None else {"queue": []},
        "known_classes": sorted(known) if known is not None else None, "digest": digest,
        "runs": runs, "component_requests_count": 0, "data_requests_count": 0,
    }


def _one_source(proposals, **kw):
    pids = [p["proposal_id"] for p in proposals]
    return _inputs({"run_061": _src(proposals, **kw)},
                   {"run_061": _memory_entry("run_061", proposal_ids=pids)})


def _decide(inputs):
    return dn.decide(inputs, now="2026-09-24T00:00:00+00:00",
                     trigger={"after_run": "run_061", "after_entry": "E", "idea_status": "refuted"})


def _by_id(record):
    return {c["candidate_id"]: c for c in record["candidates"]}


# ---------------------------------------------------------------------------
# Schema (tools/record_schema.py, closed)
# ---------------------------------------------------------------------------

def test_schema_accepts_queued_and_the_new_fields():
    entry = {"id": "x", "brief_path": "b.md", "status": "queued", "priority": 999,
             "source": "agent", "run_ids": [], "origin": "reader", "brief_status": "open",
             "proposal_ref": "runs/run_061/artifacts/proposals/profitability.yaml#p-run_061-1",
             "card_ref": "campaign_record/queued_cards/run_061/hypothesis_card_2.yaml",
             "decision_ref": "runs/run_061/artifacts/decision_record.yaml",
             "parked_reason": "waiting for a component"}
    assert rs.validate_queue_entry(entry) is entry
    for origin in ("brief", "reader", "composition", "campaign_review", "external"):
        rs.validate_queue_entry({"id": "x", "origin": origin})


@pytest.mark.parametrize("field,value", [
    ("origin", "operator"), ("brief_status", "closed"), ("status", "waiting"),
    ("parked_reason", "refine_later"), ("proposal_ref", "kill"), ("card_ref", 3),
])
def test_schema_refuses_bad_values(field, value):
    with pytest.raises(rs.RecordSchemaError):
        rs.validate_queue_entry({"id": "x", field: value})


def test_real_queue_still_validates_unchanged():
    queue = yaml.safe_load((_SR / "config" / "campaign_queue.yaml").read_text(encoding="utf-8"))
    for e in queue["queue"]:
        rs.validate_queue_entry(e)


def test_schedulability_treats_queued_as_not_blocked():
    assert "queued" in camp._SCHEDULABILITY_NON_BLOCKED_STATUSES


def test_select_entry_never_picks_queued():
    entries = [{"id": "a", "status": "queued", "priority": 1},
               {"id": "b", "status": "ready", "priority": 5}]
    assert camp._select_entry(entries)["id"] == "b"
    assert camp._select_entry([entries[0]]) is None


# ---------------------------------------------------------------------------
# The patch helper moved to tools/json_pointer.py
# ---------------------------------------------------------------------------

def test_patch_helper_moved_behaviour_preserving():
    assert rpr.PatchApplicationError is jp.PatchApplicationError
    base = _base_config()
    patch = [{"path": "/strategies/warmup", "value": 20}]
    assert rpr._apply_json_pointer_patch(base, patch) == jp.apply_json_pointer_patch(base, patch)
    assert base["strategies"]["warmup"] == 10  # never mutated
    with pytest.raises(rpr.PatchApplicationError):
        rpr._apply_json_pointer_patch(base, [{"path": "/nope/x", "value": 1}])


# ---------------------------------------------------------------------------
# register_hypothesis keyword args
# ---------------------------------------------------------------------------

_BRIEF_FRONT = ("---\nstrategy_domain: crypto\nmarket_universe: BTCUSDT\ntimeframe: 1h\n"
                "research_goal: g\nvenue: binance\nproduct: perp\n---\n\nprose\n")


def test_register_defaults_are_byte_identical(campaign_root):
    brief = campaign_root["root"] / "briefs" / "MY_IDEA.md"
    brief.parent.mkdir()
    brief.write_text(_BRIEF_FRONT, encoding="utf-8")
    assert camp.register_hypothesis(brief, 3, "n") == 0
    text = campaign_root["queue_path"].read_text(encoding="utf-8")
    expected = yaml.safe_dump({"queue": [{
        "id": "MY_IDEA", "brief_path": "briefs/MY_IDEA.md", "status": "ready", "priority": 3,
        "source": "operator_ratified", "relation": "new_registration", "notes": "n",
        "run_ids": []}]}, sort_keys=False, allow_unicode=True)
    assert text == expected


def test_register_kwargs_write_an_agent_entry(campaign_root):
    brief = campaign_root["root"] / "b.md"
    brief.write_text(_BRIEF_FRONT, encoding="utf-8")
    assert camp.register_hypothesis(
        brief, 999, "n", entry_id="profitability-run_061-1", source="agent", relation=None,
        extra={"origin": "reader", "proposal_ref": "runs/r/artifacts/proposals/p.yaml#x",
               "decision_ref": "runs/r/artifacts/decision_record.yaml"}) == 0
    e = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert e["id"] == "profitability-run_061-1" and e["source"] == "agent"
    assert "relation" not in e and e["origin"] == "reader" and e["status"] == "ready"
    with pytest.raises(ValueError, match="not registrable"):
        camp.register_hypothesis(brief, 1, "n", entry_id="y", extra={"outcome": "refuted"})


# ---------------------------------------------------------------------------
# decide(): pure
# ---------------------------------------------------------------------------

def test_ranking_order_and_tie_break():
    props = [_patch("profitability-run_061-1", after=0.6, conf=1, dist=3),
             _patch("profitability-run_061-2", after=0.7, conf=3, dist=0),
             _patch("profitability-run_061-3", after=0.8, conf=3, dist=2),
             _patch("profitability-run_061-4", after=0.9, conf=3, dist=2)]  # tie -> id asc
    rec = _decide(_one_source(props))
    ranked = [c["candidate_id"] for c in rec["candidates"] if c["rank"]]
    assert ranked == ["profitability-run_061-3", "profitability-run_061-4",
                      "profitability-run_061-2", "profitability-run_061-1"]
    assert rec["picked"]["candidate_id"] == "profitability-run_061-3"
    assert rec["stop"] is None


def test_cost_breaks_a_score_tie_cheapest_first():
    a = _src([_patch("profitability-run_061-1", conf=2, dist=2)])
    b = _src([_patch("profitability-run_062-1", after=0.9, conf=2, dist=2)])  # distinct config
    inputs = _inputs({"run_061": a, "run_062": b},
                     {"run_061": _memory_entry("run_061", n_windows=11,
                                               proposal_ids=["profitability-run_061-1"]),
                      "run_062": _memory_entry("run_062", n_windows=4, protocol_ref="p4",
                                               proposal_ids=["profitability-run_062-1"])})
    rec = _decide(inputs)
    assert [c["candidate_id"] for c in rec["candidates"]] == [
        "profitability-run_062-1", "profitability-run_061-1"]
    assert rec["candidates"][0]["cost"]["backtests"] == 4 * 3 * 1


def test_exact_match_repeat_is_refused_and_a_legacy_run_never_matches():
    p = _patch("profitability-run_061-1", after=0.8)
    patched_sha = dn.config_sha256(_base_config(min_abs=0.8))
    inputs = _one_source([p])
    # an earlier memory run tested exactly this config on the same symbols/tf/protocol
    inputs["memory"]["runs"]["run_050"] = _memory_entry("run_050", fh=patched_sha)
    rec = _decide(inputs)
    c = _by_id(rec)["profitability-run_061-1"]
    assert c["gates"]["novelty"]["exact_match"] == "REPEAT"
    assert c["gates"]["novelty"]["matched_runs"] == ["run_050"]
    assert c["eligible"] is False and c["rank"] is None
    assert rec["picked"] is None and rec["stop"]["reason"] == "no_eligible_candidate"
    # different protocol -> not the same trial key -> NOVEL
    inputs["memory"]["runs"]["run_050"]["protocol_ref"] = "protocols/other.json"
    assert _by_id(_decide(inputs))["profitability-run_061-1"]["gates"]["novelty"][
        "exact_match"] == "NOVEL"
    # a legacy run (not in memory) cannot match: remove it -> NOVEL
    del inputs["memory"]["runs"]["run_050"]
    assert _by_id(_decide(inputs))["profitability-run_061-1"]["eligible"] is True


def test_legacy_digest_is_recorded_but_never_refuses():
    p = _patch("profitability-run_061-1", after=0.8)
    card = {"hypothesis_id": "FOO", "thesis": "funding mean reversion"}
    family, _ = bed.classify_family(card)
    fp = bed.composition_fingerprint(_base_config(min_abs=0.8))
    digest = {"families": {family: {"triples": [{
        "instrument": "BTCUSDT", "timeframe": "1h", "fidelity": "structured",
        "fingerprint": fp, "run_ids": ["run_010"]}]}}}
    inputs = _one_source([p])
    inputs["digest"] = digest
    rec = _decide(inputs)
    c = _by_id(rec)["profitability-run_061-1"]
    assert c["gates"]["novelty"]["digest_advisory"]["outcome"] == "repeat"
    assert c["eligible"] is True and rec["picked"]["candidate_id"] == c["candidate_id"]


def test_operator_ready_entry_goes_first_unranked():
    queue = {"queue": [{"id": "OP_B", "status": "ready", "priority": 5},
                       {"id": "OP_A", "status": "ready", "priority": 2},
                       {"id": "EXT", "status": "ready", "priority": 9, "origin": "external"}]}
    inputs = _one_source([_patch("profitability-run_061-1")])
    inputs["queue"] = queue
    rec = _decide(inputs)
    assert rec["picked"]["operator_entry"] == "OP_A"
    assert rec["operator_entries"] == ["OP_A", "OP_B", "EXT"]


def test_an_already_ready_agent_entry_mints_nothing():
    inputs = _one_source([_patch("profitability-run_061-1")])
    inputs["queue"] = {"queue": [{"id": "AG", "status": "ready", "origin": "reader"}]}
    rec = _decide(inputs)
    assert rec["picked"]["queue_entry_id"] == "AG" and "candidate_id" not in rec["picked"]


def test_a_queued_proposal_leaves_the_pool():
    inputs = _one_source([_patch("profitability-run_061-1")])
    inputs["queue"] = {"queue": [{"id": "profitability-run_061-1", "status": "done",
                                  "proposal_ref": "runs/run_061/artifacts/proposals/"
                                                  "profitability.yaml#profitability-run_061-1"}]}
    rec = _decide(inputs)
    assert rec["candidates"] == [] and rec["stop"]["reason"] == "no_eligible_candidate"


def test_identical_patches_collapse_keeping_the_best_scores():
    props = [_patch("profitability-run_061-1", after=0.8, conf=1),
             _patch("profitability-run_061-2", after=0.8, conf=3)]
    rec = _decide(_one_source(props))
    assert [c["candidate_id"] for c in rec["candidates"]] == ["profitability-run_061-2"]
    assert rec["candidates"][0]["collapsed_sources"] == [
        "runs/run_061/artifacts/proposals/profitability.yaml#profitability-run_061-1"]


@pytest.mark.parametrize("kw,reason", [
    ({"component_id": "nope"}, "patch_unresolvable"),
    ({"field": "transforms[9].params.min_abs"}, "patch_unresolvable"),
    ({"field": "transforms[2]..min_abs"}, "patch_unresolvable"),
    ({"before": 0.4}, "stale_before"),
])
def test_patch_resolution_failures_are_infeasible(kw, reason):
    rec = _decide(_one_source([_patch("profitability-run_061-1", **kw)]))
    c = rec["candidates"][0]
    assert c["gates"]["feasibility"]["result"] == "INFEASIBLE"
    assert c["gates"]["feasibility"]["reasons"][0].startswith(reason)
    assert c["eligible"] is False


def test_ambiguous_component_id_is_infeasible():
    cfg = _base_config()
    cfg["strategies"]["regimes"]["trend"] = copy.deepcopy(cfg["strategies"]["regimes"]["unknown"])
    rec = _decide(_one_source([_patch("profitability-run_061-1")], config=cfg))
    assert "matches 2 components" in rec["candidates"][0]["gates"]["feasibility"]["reasons"][0]


def test_unknown_component_class_is_infeasible():
    p = _patch("profitability-run_061-1", field="class", before=CLS,
               after="strategies.strategy_components.MadeUpComponent")
    rec = _decide(_one_source([p]))
    assert rec["candidates"][0]["gates"]["feasibility"]["reasons"][0].startswith(
        "unknown_component_class")


def test_regime_sketch_is_infeasible_forecast_sketch_is_eligible():
    rec = _decide(_one_source([_sketch("profitability-run_061-1", kind="regime"),
                               _sketch("profitability-run_061-2", kind="forecast")]))
    c = _by_id(rec)
    assert c["profitability-run_061-1"]["gates"]["feasibility"]["reasons"][0].startswith(
        "regime_block_needs_composition")
    assert c["profitability-run_061-2"]["eligible"] is True
    assert c["profitability-run_061-2"]["gates"]["feasibility"]["result"] == "UNKNOWN"
    assert c["profitability-run_061-2"]["gates"]["novelty"]["exact_match"] == "NOT_APPLICABLE"


def test_r1_is_a_recorded_no_op():
    inputs = _one_source([_patch("profitability-run_061-1")])
    inputs["registry_revision"] = 2
    r1 = _decide(inputs)["rules"]["r1"]
    assert r1["would_fire"] is True and r1["fired"] is False


def test_decide_is_deterministic_and_carries_no_retired_field():
    inputs = _one_source([_patch("profitability-run_061-1"), _sketch("profitability-run_061-2")])
    a = yaml.safe_dump(_decide(copy.deepcopy(inputs)))
    b = yaml.safe_dump(_decide(copy.deepcopy(inputs)))
    assert a == b
    assert cm._find_retired(yaml.safe_load(a)) == []


def test_no_lineage_demotion():
    """Operator decision 6 (DROPPED): the 5th descendant of one root ranks on
    its scores alone, and the record carries no demotion field."""
    deep = _src([_patch("profitability-run_070-1", conf=3, dist=3)])
    fresh = _src([_patch("profitability-run_071-1", conf=1, dist=1)])
    memory = {"run_071": _memory_entry("run_071", hyp="OTHER", fh="a" * 64,
                                       proposal_ids=["profitability-run_071-1"])}
    hyp = "FOO"
    for i in range(5):  # a chain of descendants of FOO
        rid = f"run_06{i}"
        memory[rid] = _memory_entry(rid, hyp=hyp, fh=f"{i}" * 64)
        hyp = f"{hyp}__profitability-{rid}-1"
    memory["run_070"] = _memory_entry("run_070", hyp=hyp, fh="b" * 64,
                                      proposal_ids=["profitability-run_070-1"])
    rec = _decide(_inputs({"run_070": deep, "run_071": fresh}, memory))
    assert rec["picked"]["candidate_id"] == "profitability-run_070-1"
    dumped = yaml.safe_dump(rec)
    assert "demot" not in dumped and "policy" not in dumped and "descendant" not in dumped


def test_scores_never_touch_idea_status_or_memory():
    inputs = _one_source([_patch("profitability-run_061-1", conf=3, dist=3)])
    before = copy.deepcopy(inputs)
    rec = _decide(inputs)
    assert inputs == before  # decide mutates nothing, the memory included
    assert inputs["memory"]["runs"]["run_061"]["idea_status"] == "refuted"
    assert rec["trigger"]["idea_status"] == "refuted"
    assert "idea_status" not in rec["candidates"][0]


# ---------------------------------------------------------------------------
# Decision 2: criteria at 1a, never inherited
# ---------------------------------------------------------------------------

def test_candidate_brief_carries_no_criteria_and_a_verified_config(tmp_path):
    inputs = _one_source([_patch("profitability-run_061-1", after=0.8)], pass_rule_nested=True)
    rec = _decide(inputs)
    rel, text = dn.candidate_brief(rec, inputs, decision_ref="runs/run_061/artifacts/decision_record.yaml")
    assert rel == "campaign_record/candidate_briefs/profitability-run_061-1.md"
    path = tmp_path / "b.md"
    path.write_text(text, encoding="utf-8")
    front = camp._parse_brief_frontmatter(path)
    assert "evaluation" not in front and "pass_rule" not in front["machine_constraints"]
    cand = front["candidate"]
    assert "criteria" not in cand and cand["criteria_from"] == "hypothesis_generation"
    assert cand["config"] == _base_config(min_abs=0.8)
    assert cand["source"]["expected_config_sha256"] == dn.config_sha256(cand["config"])
    assert cand["source"]["hypothesis_id"] == "FOO__profitability-run_061-1"
    assert "pass_rule" not in yaml.safe_dump(front)


def _write_candidate_run(root: Path, run_id: str, inputs, rec):
    _, text = dn.candidate_brief(rec, inputs, decision_ref="runs/run_061/artifacts/decision_record.yaml")
    brief = root / "cb.md"
    brief.write_text(text, encoding="utf-8")
    _write_fresh_scaffold(root / "runs", run_id)
    camp._materialize_run(run_id, camp._parse_brief_frontmatter(brief))
    return root / "runs" / run_id


def _copy_menu(root: Path):
    (root / "config").mkdir(exist_ok=True)
    shutil.copy(_SR / "config" / "criterion_menu.yaml", root / "config" / "criterion_menu.yaml")


def test_candidate_pre_registration_is_pending_at_1a(campaign_root):
    inputs = _one_source([_patch("profitability-run_061-1")], pass_rule_nested=True)
    run_dir = _write_candidate_run(campaign_root["root"], "run_062", inputs, _decide(inputs))
    pre = yaml.safe_load((run_dir / "artifacts" / "pre_registration.yaml").read_text(encoding="utf-8"))
    assert pre["pass_rule"] is None and "pass_rule" not in pre["machine_constraints"]
    assert pre["pass_rule_pending"] == "hypothesis_generation"
    assert rpr._specialist_readers_preflight_deferred(run_dir, "hypothesis_generation") is True
    assert rpr._specialist_readers_preflight_deferred(run_dir, "strategy_config_authoring") is False


def test_proposal_candidate_gets_fresh_criteria_from_1a_never_the_source(campaign_root):
    root = campaign_root["root"]
    _copy_menu(root)
    inputs = _one_source([_patch("profitability-run_061-1")])
    run_dir = _write_candidate_run(root, "run_062", inputs, _decide(inputs))
    # 1a writes a card for the proposed idea, with ITS criteria (not the source's
    # realized_edge_to_cost_ratio)
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(yaml.safe_dump({
        "hypothesis_id": "FOO__profitability-run_061-1",
        "criteria": [{"id": "sign_consistent_by_era"}]}), encoding="utf-8")
    assert rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True) is True
    pre = yaml.safe_load((run_dir / "artifacts" / "pre_registration.yaml").read_text(encoding="utf-8"))
    ids = [c["id"] for c in pre["pass_rule"]["criteria"]]
    assert ids == ["sign_consistent_by_era"]
    assert pre["pass_rule"] != _SOURCE_PASS_RULE
    assert pre["pass_rule_source_ref"] == "runs/run_062/artifacts/hypothesis_card.yaml#criteria"
    assert vce._is_menu_shaped_pass_rule(pre["pass_rule"])
    rpr._check_specialist_readers_preflight(run_dir)  # passes now
    # the marker stays until the run advances past 1a
    assert pre["pass_rule_pending"] == "hypothesis_generation"
    assert rpr._clear_pass_rule_pending(run_dir, "hypothesis_generation") is False
    assert rpr._clear_pass_rule_pending(run_dir, "strategy_config_authoring") is True
    assert rpr._specialist_readers_preflight_deferred(run_dir, "hypothesis_generation") is False


@pytest.mark.parametrize("card,match", [
    ({"hypothesis_id": "FOO__profitability-run_061-1"}, "no `criteria`"),
    ({"hypothesis_id": "FOO__profitability-run_061-1", "criteria": [{"id": "median_sharpe"}]},
     "not a live entry"),
    ({"hypothesis_id": "FOO", "criteria": [{"id": "sign_consistent_by_era"}]}, "not the candidate"),
])
def test_1a_criteria_writer_fails_loud(campaign_root, card, match):
    root = campaign_root["root"]
    _copy_menu(root)
    inputs = _one_source([_patch("profitability-run_061-1")])
    run_dir = _write_candidate_run(root, "run_062", inputs, _decide(inputs))
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(yaml.safe_dump(card), encoding="utf-8")
    with pytest.raises(ValueError, match=match):
        rpr._write_pass_rule_from_card(run_dir, "run_062", sr_flag=True)


def test_1a_writer_is_a_no_op_without_the_marker(tmp_path):
    arts = tmp_path / "artifacts"
    arts.mkdir()
    pre = arts / "pre_registration.yaml"
    pre.write_text(yaml.safe_dump({"pass_rule": _SOURCE_PASS_RULE}), encoding="utf-8")
    before = pre.read_bytes()
    assert rpr._write_pass_rule_from_card(tmp_path, "run_x", sr_flag=True) is False
    assert pre.read_bytes() == before
    assert rpr._specialist_readers_preflight_deferred(tmp_path, "hypothesis_generation") is False


def test_materialize_refuses_marker_plus_pass_rule(campaign_root):
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_063")
    brief = {"strategy_domain": "c", "market_universe": "B", "timeframe": "1h",
             "research_goal": "g", "venue": "binance", "product": "perp",
             "machine_constraints": {"protocol_ref": "protocols/p8.json"},
             "evaluation": {"pass_rule": _SOURCE_PASS_RULE},
             "candidate": {"criteria_from": "hypothesis_generation", "source": {}}}
    with pytest.raises(ValueError, match="inherited criterion"):
        camp._materialize_run("run_063", brief)


def test_materialize_without_marker_adds_nothing(campaign_root):
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_064")
    brief = {"strategy_domain": "c", "market_universe": "B", "timeframe": "1h",
             "research_goal": "g", "venue": "binance", "product": "perp",
             "machine_constraints": {"protocol_ref": "protocols/p8.json"}}
    camp._materialize_run("run_064", brief)
    pre = yaml.safe_load((campaign_root["runs_dir"] / "run_064" / "artifacts" /
                          "pre_registration.yaml").read_text(encoding="utf-8"))
    assert list(pre) == ["run_id", "hypothesis_id", "registered_at", "reactivation_context",
                         "pass_rule", "machine_constraints", "sample_split_design"]


# ---------------------------------------------------------------------------
# 5a pass-through hash check
# ---------------------------------------------------------------------------

def _stage_5a(tmp_path, spec_config, expected):
    arts = tmp_path / "artifacts"
    (arts / "variants" / "base").mkdir(parents=True)
    brief = {"strategy_domain": "c"}
    if expected is not None:
        brief["candidate"] = {"source": {"expected_config_sha256": expected}}
    (arts / "research_brief.yaml").write_text(yaml.safe_dump(brief), encoding="utf-8")
    (arts / "backtest_spec.yaml").write_text(yaml.safe_dump(
        {"status": "spec_ready", "config": spec_config}), encoding="utf-8")
    (arts / "variants" / "base" / "strategy_config.json").write_text(
        json.dumps(spec_config, indent=2), encoding="utf-8")
    return arts


def test_5a_hash_check_passes_on_a_verbatim_copy(tmp_path):
    cfg = _base_config(min_abs=0.8)
    rpr._check_pass_through_config_hash(_stage_5a(tmp_path, cfg, dn.config_sha256(cfg)))


def test_5a_hash_check_stops_on_a_drifted_copy(tmp_path):
    arts = _stage_5a(tmp_path, _base_config(min_abs=0.7), dn.config_sha256(_base_config(0.8)))
    with pytest.raises(RuntimeError, match="pass-through mismatch"):
        rpr._check_pass_through_config_hash(arts)


def test_5a_hash_check_is_a_no_op_without_a_candidate(tmp_path):
    rpr._check_pass_through_config_hash(_stage_5a(tmp_path, _base_config(), None))


def test_resolved_hash_equals_the_trial_forecast_hash(tmp_path):
    cfg = _base_config(min_abs=0.8)
    p = tmp_path / "c.json"
    p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    assert dn.config_sha256(cfg) == rpr._compute_forecast_hash(p)


# ---------------------------------------------------------------------------
# The flag
# ---------------------------------------------------------------------------

def _write_flags(root: Path, **flags):
    (root / "config").mkdir(exist_ok=True)
    cfg = {"orchestrator": {name: {"enabled": v} for name, v in flags.items()}}
    (root / "config" / "campaign_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")


_ALL_ON = dict(grid_evaluation=True, category_reports=True, specialist_readers=True,
               regroup_record=True, config_direct_authoring=True, decide_next=True)


def test_flag_reader(campaign_root):
    root = campaign_root["root"]
    _write_flags(root)
    assert rpr._decide_next_enabled() is False
    _write_flags(root, decide_next="true")
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._decide_next_enabled()
    _write_flags(root, **{**_ALL_ON, "regroup_record": False})
    with pytest.raises(ValueError, match="regroup_record"):
        rpr._decide_next_enabled()
    _write_flags(root, **{**_ALL_ON, "config_direct_authoring": False})
    with pytest.raises(ValueError, match="config_direct_authoring"):
        rpr._decide_next_enabled()
    _write_flags(root, **_ALL_ON)
    assert rpr._decide_next_enabled() is True


def test_flag_is_off_in_the_real_config_and_registered():
    cfg = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["decide_next"]["enabled"] is False
    reg = yaml.safe_load((_SR / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    entry = next(f for f in reg["flags"] if f["name"] == "decide_next")
    assert entry["state"] == "off_incomplete" and entry["reader"].endswith("_decide_next_enabled")


# ---------------------------------------------------------------------------
# process_once: flag off byte-identity, flag on end to end
# ---------------------------------------------------------------------------

def _strip_ts(log: str) -> str:
    return re.sub(r"^- \S+Z ", "- ", log, flags=re.M)


def _done_step(campaign_root, flag_cfg):
    root = campaign_root["root"]
    if flag_cfg is not None:
        _write_flags(root, **flag_cfg)
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_912",
                          status="completed", pending_stage="completed_reframed")
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_912")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_912"], trial_sharpes=[])
    return camp.process_once()


@pytest.mark.parametrize("flag_cfg", [None, {"decide_next": False}])
def test_flag_off_done_branch_is_byte_identical(campaign_root, monkeypatch, flag_cfg):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    assert _done_step(campaign_root, flag_cfg) is True
    root = campaign_root["root"]
    expected_entry = {**_entry("run_912"), "status": "done", "outcome": "completed_reframed"}
    assert campaign_root["queue_path"].read_text(encoding="utf-8") == yaml.safe_dump(
        {"queue": [expected_entry]}, sort_keys=False, allow_unicode=True)
    log = _strip_ts((root / "campaign_log.md").read_text(encoding="utf-8"))
    assert "- DONE TEST_ENTRY (run_912) -> completed_reframed\n" in log
    assert "DECIDE" not in log
    assert not (root / "runs" / "run_912" / "artifacts" / "decision_record.yaml").exists()
    assert not (root / "campaign_record" / "candidate_briefs").exists()


def test_flag_off_completed_rejected_crash_is_unchanged(campaign_root, monkeypatch):
    """Decision 8's bug stays as it is with the flag off (its own ticket)."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_913",
                          status="rejected", pending_stage="completed_rejected")
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_913")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_913"], trial_sharpes=[])
    with pytest.raises(vce.UngatedVerdictError):
        camp.process_once()


def _stage_flag_on_source(campaign_root, proposals, idea_status="refuted"):
    """A finished, refuted run_061 under every prerequisite flag, with its memory
    entry, reader proposals and source artifacts on disk."""
    root = campaign_root["root"]
    _write_flags(root, **_ALL_ON)
    _copy_menu(root)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_061",
                                    status="rejected", pending_stage="completed_rejected")
    arts = run_dir / "artifacts"
    (arts / "idea_status.yaml").write_text(yaml.safe_dump({
        "run_id": "run_061", "idea_status": idea_status,
        "result": {"refuted": "FAIL", "validated": "PASS"}.get(idea_status, "INCONCLUSIVE"),
        "reason": "r"}), encoding="utf-8")
    (arts / "proposals").mkdir()
    (arts / "proposals" / "profitability.yaml").write_text(yaml.safe_dump(proposals),
                                                            encoding="utf-8")
    (arts / "variants" / "base").mkdir(parents=True)
    (arts / "variants" / "base" / "strategy_config.json").write_text(
        json.dumps(_base_config(), indent=2), encoding="utf-8")
    src = _src([])
    for name, doc in (("block_manifest.yaml", _MANIFEST),
                      ("pre_registration.yaml", src["pre_registration"]),
                      ("research_brief.yaml", src["research_brief"]),
                      ("hypothesis_card.yaml", src["card"])):
        (arts / name).write_text(yaml.safe_dump(doc), encoding="utf-8")
    mem = {"schema_version": 1, "legacy_note": "", "runs": {"run_061": _memory_entry(
        "run_061", idea_status=idea_status,
        proposal_ids=[p["proposal_id"] for p in proposals])}}
    (root / "campaign_record").mkdir(exist_ok=True)
    (root / "campaign_record" / "campaign_memory.yaml").write_text(yaml.safe_dump(mem),
                                                                    encoding="utf-8")
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_061")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_061"], trial_sharpes=[])
    return run_dir


def test_flag_on_refuted_run_decides_and_mints_one_ready_entry(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    # save_yaml checks decision_record.yaml against its schema; make that blocking.
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    root = campaign_root["root"]
    mem_path = root / "campaign_record" / "campaign_memory.yaml"
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1", conf=3),
                                          _patch("profitability-run_061-2", after=0.9, conf=1)])
    mem_before = mem_path.read_bytes()

    assert camp.process_once() is True  # no _save_queue crash (decision 8)

    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    done, new = queue
    assert done["status"] == "done" and done["outcome"] == "refuted"
    assert done["pass_rule_evaluation_ref"] == "runs/run_061/artifacts/idea_status.yaml"
    vce.validate_verdict_provenance(done, root=root, schema=rs.QUEUE_ENTRY_SCHEMA)
    assert new["id"] == "profitability-run_061-1" and new["status"] == "ready"
    assert new["source"] == "agent" and new["origin"] == "reader" and new["priority"] == 999
    assert "relation" not in new
    assert new["decision_ref"] == "runs/run_061/artifacts/decision_record.yaml"
    assert [e["status"] for e in queue].count("ready") == 1
    assert camp._select_entry(queue)["id"] == new["id"]
    assert camp._next_action_for_entry(new) == "fresh_launch"

    record = yaml.safe_load((root / new["decision_ref"]).read_text(encoding="utf-8"))
    assert record["picked"]["candidate_id"] == new["id"]
    assert record["trigger"]["idea_status"] == "refuted"
    assert (root / new["brief_path"]).exists()
    assert mem_path.read_bytes() == mem_before  # decide never writes the memory
    assert "continuation_child" not in yaml.safe_load(
        (root / "runs" / "run_061" / "pipeline_state.yaml").read_text(encoding="utf-8"))
    log = (root / "campaign_log.md").read_text(encoding="utf-8")
    assert "DECIDE after TEST_ENTRY (run_061): picked profitability-run_061-1" in log

    # the next launch materializes the candidate pending at 1a
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_062")
    camp._materialize_run("run_062", camp._parse_brief_frontmatter(root / new["brief_path"]))
    pre = yaml.safe_load((run_dir / "artifacts" / "pre_registration.yaml").read_text(encoding="utf-8"))
    assert pre["pass_rule"] is None and pre["pass_rule_pending"] == "hypothesis_generation"


def test_flag_on_run_without_a_grid_is_declared_ungated_not_a_crash(campaign_root, monkeypatch):
    """A run that ends completed_rejected before the grid (e.g. the data gate's
    decline) has no idea_status.yaml: under the flag the entry is declared
    ungated instead of crashing _save_queue."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir = _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    (run_dir / "artifacts" / "idea_status.yaml").unlink()
    assert camp.process_once() is True
    done = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert done["outcome"] == "completed_rejected" and done["verdict_status"] == "ungated"
    assert "pass_rule_evaluation_ref" not in done


def test_flag_on_scores_never_change_the_recorded_status(campaign_root, monkeypatch):
    """Top scores on every proposal; the entry's outcome is still the grid's
    refuted, and nothing in the queue or memory carries a score."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1", conf=3, dist=3,
                                                 mech=3)])
    camp.process_once()
    text = campaign_root["queue_path"].read_text(encoding="utf-8")
    queue = yaml.safe_load(text)["queue"]
    assert queue[0]["outcome"] == "refuted"
    assert "confidence_real" not in text and "scores" not in text


def test_flag_on_stop_returns_false(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _stage_flag_on_source(campaign_root, [_sketch("profitability-run_061-1", kind="regime")])
    assert camp.process_once() is False
    root = campaign_root["root"]
    record = yaml.safe_load((root / "runs" / "run_061" / "artifacts" /
                             "decision_record.yaml").read_text(encoding="utf-8"))
    assert record["stop"]["reason"] == "no_eligible_candidate" and record["picked"] is None
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    assert len(queue) == 1 and queue[0]["outcome"] == "refuted"
    assert "DECIDE stop after TEST_ENTRY" in (root / "campaign_log.md").read_text(encoding="utf-8")


def test_flag_on_operator_entry_goes_first(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    queue.append({"id": "OPERATOR", "brief_path": "b.md", "status": "ready", "priority": 1,
                  "source": "operator_ratified", "relation": "new_registration",
                  "notes": "n", "run_ids": []})
    _save_queue_entries(campaign_root["queue_path"], queue)
    assert camp.process_once() is True
    after = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    assert [e["id"] for e in after] == ["TEST_ENTRY", "OPERATOR"]
    assert camp._select_entry(after)["id"] == "OPERATOR"


def test_decision_records_match_the_schema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((_SR / "workflow_artifacts" / "schemas" /
                         "decision_record.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    picked = _one_source([_patch("profitability-run_061-1"), _sketch("profitability-run_061-2"),
                          _patch("profitability-run_061-3", before=0.1)])
    stopped = _one_source([_sketch("profitability-run_061-1", kind="regime")])
    operator = _one_source([_patch("profitability-run_061-1")])
    operator["queue"] = {"queue": [{"id": "OP", "status": "ready", "priority": 1}]}
    agent = _one_source([_patch("profitability-run_061-1")])
    agent["queue"] = {"queue": [{"id": "AG", "status": "ready", "origin": "reader"}]}
    card = {"hypothesis_id": "FOO", "thesis": "funding mean reversion"}
    family, _ = bed.classify_family(card)
    digest = _one_source([_patch("profitability-run_061-1")])
    digest["digest"] = {"families": {family: {"triples": [{
        "instrument": "BTCUSDT", "timeframe": "1h", "fidelity": "coarse", "fingerprint": None,
        "run_ids": ["run_010"]}]}}}
    for inputs in (picked, stopped, operator, agent, digest):
        rec = yaml.safe_load(yaml.safe_dump(_decide(inputs)))
        errors = sorted(str(e.message) for e in validator.iter_errors(rec))
        assert errors == []
