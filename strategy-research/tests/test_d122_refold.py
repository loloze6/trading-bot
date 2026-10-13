"""D-122 (operator decisions 2026-10-13): `run_campaign.py refold --run <run_id> --fold <X>`,
the operator's fold re-run, BRANCH 3 ONLY.

It writes a brief from the source run and registers it ready (no brief_status); the operator
launches it with --once. The re-run makes no model call: the source's hypothesis card is
copied at launch (step 1a skipped), its config and block manifest are an exact config (D-110:
steps 1b and 2 written by code), its criteria are the source's pass_rule. After the backtest
only branch 3 runs: no category reports, no readers (rule operator_refold), no claim checks,
no block registered; the grid is computed (memory needs it) but never routed on. A passing
variant stops at profit_bars_reached; otherwise the run ends completed_refold. Decide-next
never runs after a re-run. Only the existing checks apply.
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "tests"))
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import decide_next as dn  # noqa: E402
import block_registry as br  # noqa: E402
import reader_proposals as rpp  # noqa: E402
import research_folds as rf  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
import test_e059_s2a_decide_next as t59  # noqa: E402
from test_e059_6c_s2a_route_retirement import RETIRED_ON  # noqa: E402

REAL_FOLDS = SR / "config" / "folds.yaml"
REAL_MENU = SR / "config" / "criterion_menu.yaml"
REAL_POLICY = SR / "config" / "campaign_data_policy.yaml"
SRC = "run_800"
SRC_PROTO = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1d", "fold": "B",
             "start": "2018-05-01", "end": "2021-12-31", "window_months": 4,
             "per_symbol_start": {"ETHUSDT": "2018-06-01"}}
SRC_RULE = rpr._pass_rule_from_card(
    {"criteria": [{"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}]},
    yaml.safe_load(REAL_MENU.read_text(encoding="utf-8")), "t")
SRC_CARD = {"hypothesis_id": "L1_SRC", "claim": {"statement": "s"}}
# The operator's flag set where it matters: retired routing (so no promotion block is
# required at registration), config-direct authoring and exact-config 1b, folds on.
FLAGS = {**RETIRED_ON, "folds": {"enabled": True}, "exact_config_1b": {"enabled": True}}


@pytest.fixture(autouse=True)
def _seed(_sandbox_by_default):
    root = _sandbox_by_default
    for src in (REAL_FOLDS, REAL_MENU):
        shutil.copyfile(src, root / "config" / src.name)
    (root / "config" / "campaign_queue.yaml").write_text(yaml.safe_dump({"queue": []}),
                                                         encoding="utf-8")
    return root


def _source(root, *, rule=SRC_RULE, proto=SRC_PROTO, run_id=SRC):
    arts = root / "runs" / run_id / "artifacts"
    arts.mkdir(parents=True)
    docs = {
        "research_brief.yaml": {"strategy_domain": "time_series_trend",
                                "market_universe": ["BTCUSDT", "ETHUSDT"], "timeframe": "1d",
                                "venue": "kraken", "product": "perp",
                                "research_goal": "Does the  trend\n earn its costs?",
                                "criteria_from": "hypothesis_generation",
                                "research_only": False},
        "pre_registration.yaml": {"machine_constraints": {"protocol": copy.deepcopy(proto),
                                                          "pass_rule": {"criteria": []}},
                                  "pass_rule": copy.deepcopy(rule)},
        "backtest_spec.yaml": {"status": "spec_ready", "config": t59._base_config()},
        "block_manifest.yaml": copy.deepcopy(t59._MANIFEST),
        "hypothesis_card.yaml": copy.deepcopy(SRC_CARD),
    }
    for name, doc in docs.items():
        (arts / name).write_text(yaml.safe_dump(doc), encoding="utf-8")
    return arts


def _front(text):
    return yaml.safe_load(text.split("---", 2)[1])


def _folds_doc():
    return rf.load_folds(REAL_FOLDS, policy_path=REAL_POLICY)


def _queue(root):
    return yaml.safe_load((root / "config" / "campaign_queue.yaml").read_text(encoding="utf-8"))


# -- the brief ------------------------------------------------------------------------------

def test_the_brief_carries_the_source_config_manifest_and_the_fold_protocol(_seed):
    _source(_seed)
    rel, text = camp.refold_brief(SRC, "C")
    front = _front(text)
    assert rel == "briefs/refold_run_800_fold_C.md"
    assert {k: front[k] for k in ("strategy_domain", "market_universe", "timeframe", "venue",
                                  "product")} == {
        "strategy_domain": "time_series_trend", "market_universe": ["BTCUSDT", "ETHUSDT"],
        "timeframe": "1d", "venue": "kraken", "product": "perp"}
    start, end = rf.fold_span(_folds_doc(), "C")
    assert front["machine_constraints"] == {"protocol": {
        "symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1d", "fold": "C", "start": start,
        "end": end, "window_months": 4}}            # per_symbol_start and pass_rule dropped
    assert front["refold"] == {"source_run": SRC, "fold": "C"}
    for key in ("criteria_from", "evaluation", "research_only"):
        assert key not in front                      # criteria come from the source at launch
    cfg, man = front["constraints"]
    assert cfg.startswith(rpr.BRIEF_EXACT_CONFIG_PREFIX)
    assert json.loads(cfg.split("\n", 1)[1]) == t59._base_config()
    assert man.startswith(rpr.BRIEF_EXACT_MANIFEST_PREFIX)
    assert json.loads(man.split("\n", 1)[1]) == t59._MANIFEST


@pytest.mark.parametrize("missing", camp.REFOLD_SOURCE_FILES)
def test_a_source_missing_a_file_it_is_built_from_is_refused(_seed, missing):
    arts = _source(_seed)
    (arts / missing).unlink()
    with pytest.raises(ValueError, match=f"missing .*{missing}"):
        camp.refold_brief(SRC, "C")


@pytest.mark.parametrize("rule", [None, {"criteria": []}])
def test_a_source_without_a_pass_rule_is_refused(_seed, rule):
    _source(_seed, rule=rule)
    with pytest.raises(ValueError, match="no menu-shaped pass_rule"):
        camp.refold_brief(SRC, "C")


def test_a_pinned_protocol_source_is_refused(_seed):
    arts = _source(_seed)
    (arts / "pre_registration.yaml").write_text(yaml.safe_dump(
        {"machine_constraints": {"protocol_ref": "protocols/p.json"}, "pass_rule": SRC_RULE}),
        encoding="utf-8")
    with pytest.raises(ValueError, match="no generated machine_constraints.protocol"):
        camp.refold_brief(SRC, "C")


# -- folds: D accepted, holdout refused --------------------------------------------------------

@pytest.mark.parametrize("fold", ["A", "B", "C", "D"])
def test_every_fold_of_the_folds_file_is_accepted(_seed, fold):
    _source(_seed)
    _r, text = camp.refold_brief(SRC, fold)
    assert _front(text)["machine_constraints"]["protocol"]["fold"] == fold


def test_a_fold_the_file_does_not_define_is_refused(_seed):
    _source(_seed)
    with pytest.raises(rf.FoldsError, match="is not one of"):
        camp.refold_brief(SRC, "E")


def test_a_fold_inside_the_holdout_is_refused_and_nothing_is_written(_seed):
    """A synthetic holdout over fold C's first block (no sealed date written here)."""
    _source(_seed)
    policy = yaml.safe_load(REAL_POLICY.read_text(encoding="utf-8"))
    first = _folds_doc()["folds"]["C"][0]
    policy["holdout_range"] = [first["start"], first["end"]]
    (_seed / "config" / "campaign_data_policy.yaml").write_text(yaml.safe_dump(policy),
                                                                encoding="utf-8")
    assert camp._refold_from_cli(SRC, "C", 0) == 1
    assert not (_seed / "briefs").exists()
    assert _queue(_seed) == {"queue": []}


# -- registration, launch (no model call) and the pre-flight -----------------------------------

def _register(root, fold="C"):
    _set_orchestrator(FLAGS)
    assert camp._refold_from_cli(SRC, fold, 0) == 0
    return _queue(root)["queue"][-1]


def _launch(root, fold="C"):
    _register(root, fold)
    queue = _queue(root)
    entry = queue["queue"][-1]
    run_id = camp._launch_run(queue, entry, "fresh_launch", True, [], promotion_retired=True)
    return entry, run_id, root / "runs" / run_id


@pytest.mark.parametrize("fold", ["C", "D"])
def test_a_refold_registers_and_launches_at_1b_with_the_sources_card_and_pass_rule(_seed, fold):
    _source(_seed)
    entry = _register(_seed, fold)
    assert entry == {"id": f"refold_{SRC}_fold_{fold}",
                     "brief_path": f"briefs/refold_{SRC}_fold_{fold}.md", "status": "ready",
                     "priority": 0, "source": "operator_ratified",
                     "relation": "new_registration",
                     "notes": f"Refold of {SRC} on fold {fold} (D-122), branch 3 only.",
                     "run_ids": []}
    shutil.rmtree(_seed / "briefs")
    (_seed / "config" / "campaign_queue.yaml").write_text(yaml.safe_dump({"queue": []}),
                                                         encoding="utf-8")
    _e, run_id, run_dir = _launch(_seed, fold)
    arts = run_dir / "artifacts"
    assert yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8")) == SRC_CARD
    assert not (arts / rpr.BRIEF_CONTEXT_FILE).exists()
    pre = yaml.safe_load((arts / "pre_registration.yaml").read_text(encoding="utf-8"))
    assert pre["pass_rule"] == SRC_RULE
    assert pre["pass_rule_source_ref"] == f"runs/{SRC}/artifacts/pre_registration.yaml#pass_rule"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["pending_stage"] == "strategy_config_authoring"
    assert state["completed_stages"] == ["hypothesis_generation"]
    assert rpr.refold_of(run_dir) == {"source_run": SRC, "fold": fold}
    assert camp._protocol_preflight_refusal(run_dir, run_id, promotion_retired=True,
                                            folds_enabled=True) is None
    # step 1b by code copies the source's config and manifest (D-110), no model call
    assert rpr._exact_config_1b_mode(run_dir)
    rpr._exact_config_1b(run_dir, run_id)
    spec = yaml.safe_load((arts / "backtest_spec.yaml").read_text(encoding="utf-8"))
    assert spec["config"] == t59._base_config() and spec["hypothesis_id"] == "L1_SRC"
    windows = rpr._ensure_protocol_from_constraints(
        run_dir, run_id, pre["machine_constraints"], promotion_retired=True, folds_enabled=True)
    doc = json.loads(Path(windows).read_text(encoding="utf-8"))
    assert doc["windows"] == rf.fold_windows(_folds_doc(), fold)


@pytest.mark.parametrize("off", ["config_direct_authoring", "exact_config_1b", "variant_loop"])
def test_the_launch_refuses_before_spend_when_1b_or_2_would_call_a_model(_seed, off):
    _source(_seed)
    _register(_seed)
    _set_orchestrator({**FLAGS, off: {"enabled": off == "variant_loop"}})
    queue = _queue(_seed)
    with pytest.raises(RuntimeError, match="written by code only"):
        camp._launch_run(queue, queue["queue"][-1], "fresh_launch", True, [],
                         promotion_retired=True)


def test_the_same_brief_twice_is_refused_and_the_first_is_kept(_seed):
    _source(_seed)
    _register(_seed)
    path = _seed / "briefs" / f"refold_{SRC}_fold_C.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nedited\n", encoding="utf-8")
    before = path.read_bytes()
    assert camp._refold_from_cli(SRC, "C", 0) == 1
    assert path.read_bytes() == before


def test_a_refused_registration_leaves_no_brief(_seed):
    _source(_seed)
    (_seed / "config" / "campaign_queue.yaml").write_text(yaml.safe_dump(
        {"queue": [{"id": f"refold_{SRC}_fold_C", "brief_path": "gone.md", "status": "done",
                    "priority": 0, "source": "operator_ratified", "notes": "n",
                    "run_ids": []}]}), encoding="utf-8")
    _set_orchestrator(FLAGS)
    assert camp._refold_from_cli(SRC, "C", 0) == 1
    assert not (_seed / "briefs" / f"refold_{SRC}_fold_C.md").exists()


def test_the_cli():
    import subprocess
    out = subprocess.run([sys.executable, str(SR / "workflow" / "run_campaign.py"), "refold",
                          "--help"], capture_output=True, text=True, encoding="utf-8",
                         errors="replace", cwd=SR)
    assert out.returncode == 0 and "{A,B,C,D}" in out.stdout
    assert "--criteria" not in out.stdout and "--readers" not in out.stdout
    assert "same config on the same fold is refused as a repeat" in camp.REFOLD_HELP


# -- branch 2 off: readers ---------------------------------------------------------------------

def test_every_reading_of_a_refold_is_a_code_written_skip(_seed, monkeypatch):
    _source(_seed)
    _e, run_id, run_dir = _launch(_seed)
    monkeypatch.setattr(rpr, "run_reader_worker",
                        lambda *a, **k: pytest.fail("a reader was called"))
    rpr._run_specialist_readers(run_id, run_dir)
    for cat in rpr._reader_categories():
        doc = yaml.safe_load((run_dir / "artifacts" / "proposals" / f"{cat}.yaml").read_text(
            encoding="utf-8"))
        assert doc["skipped"]["rule"] == "operator_refold"
        assert "run_800 on fold C" in doc["skipped"]["reason"]
    assert "operator_refold" in rpp.SKIP_RULES


def test_any_other_run_is_not_a_refold(_seed):
    arts = _seed / "runs" / "run_803" / "artifacts"
    arts.mkdir(parents=True)
    (arts / "research_brief.yaml").write_text(yaml.safe_dump({"venue": "kraken",
                                                              "refold": "not a block"}),
                                              encoding="utf-8")
    assert rpr.refold_of(arts.parent) is None and rpr._refold_readers_off(arts.parent) is None
    assert rpr.refold_of(_seed / "runs" / "absent") is None


def test_a_refold_registers_no_block(tmp_path):
    reg = tmp_path / "block_registry.yaml"
    entry = {"run_id": "run_9", "legacy": False, "idea_status": "validated"}
    assert br.record_run(reg, tmp_path, entry, root=tmp_path, refold_run=True) == \
        {"skipped": "refold"}


def test_completed_refold_is_not_a_verdict():
    assert not vce.outcome_is_verdict_bearing(rpr.REFOLD_TERMINAL)


# -- decide-next never runs after a re-run; register and decide-next unchanged ---------------

def test_the_entry_is_a_brief_without_brief_status(_seed):
    _source(_seed)
    entry = _register(_seed)
    assert "brief_status" not in entry
    assert dn.brief_owner(entry, [entry]) is None and not dn.r2_eligible_owner(entry)


def test_decide_next_is_not_run_after_a_refold(_seed, monkeypatch):
    _source(_seed)
    _e, run_id, _run_dir = _launch(_seed)
    monkeypatch.setattr(dn, "decide", lambda *a, **k: pytest.fail("decide-next ran"))
    queue = _queue(_seed)
    entry = queue["queue"][-1]
    entry["status"], entry["outcome"] = "done", rpr.REFOLD_TERMINAL
    queue, entry, keep_going, msg = camp._finish_lineage_with_decision(queue, entry, run_id)
    assert keep_going and "DECIDE not run" in msg and "refold" in msg
    saved = _queue(_seed)["queue"][-1]
    assert saved["status"] == "done" and saved["outcome"] == "completed_refold"


def test_the_fold_childs_protocol_is_the_shape_it_was_before_the_extraction():
    """decide-next byte-identity: the expression fold_protocol replaced, verbatim."""
    doc = _folds_doc()
    for fold in ("A", "B", "C"):
        start, end = rf.fold_span(doc, fold)
        old = {k: v for k, v in SRC_PROTO.items() if k != "per_symbol_start"}
        old = {**old, "start": start, "end": end, "window_months": rf.BLOCK_MONTHS, "fold": fold}
        assert dn.fold_protocol(copy.deepcopy(SRC_PROTO), doc, fold) == old


def test_register_writes_what_it_wrote_before(_seed):
    """register byte-identity: refold calls register_hypothesis with its defaults."""
    brief = _seed / "briefs" / "x.md"
    brief.parent.mkdir()
    brief.write_text("---\n" + yaml.safe_dump({
        "strategy_domain": "d", "market_universe": ["BTCUSDT"], "timeframe": "1d",
        "research_goal": "g", "venue": "kraken", "product": "perp"}) + "---\n", encoding="utf-8")
    assert camp.register_hypothesis(brief, 3, "n") == 0
    assert (_seed / "config" / "campaign_queue.yaml").read_text(encoding="utf-8") == \
        yaml.safe_dump({"queue": [{"id": "x", "brief_path": "briefs/x.md", "status": "ready",
                                   "priority": 3, "source": "operator_ratified",
                                   "relation": "new_registration", "notes": "n",
                                   "run_ids": []}]}, sort_keys=False, allow_unicode=True)


# -- run_loop: branch 3 only after the backtest ----------------------------------------------

import test_e059_6c_s2a_route_retirement as t6c  # noqa: E402


def _as_refold(run_dir):
    p = run_dir / "artifacts" / "research_brief.yaml"
    brief = (yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None) or {}
    brief["refold"] = {"source_run": SRC, "fold": "C"}
    p.write_text(yaml.safe_dump(brief), encoding="utf-8")


@pytest.mark.usefixtures("reader_docs")
@pytest.mark.parametrize("idea_status", ["validated", "refuted"])
def test_a_refold_with_no_passing_variant_ends_completed_refold(monkeypatch, idea_status):
    _set_orchestrator(t6c.RETIRED_ON)
    run_dir = t6c._graded_run(idea_status, good=False)
    _as_refold(run_dir)
    t6c._forbid(monkeypatch)
    monkeypatch.setattr(rpr, "determine_post_specialist_readers_route",
                        lambda *a, **k: pytest.fail("the grid route ran on a re-run"))
    monkeypatch.setattr(rpr, "_retired_review_route",
                        lambda *a, **k: pytest.fail("a campaign review ran on a re-run"))
    rpr.run_loop(t6c.RUN_ID)
    state = t6c._state(run_dir)
    assert state["pending_stage"] == rpr.REFOLD_TERMINAL and state["status"] == "completed"
    memory = yaml.safe_load((rpr.ROOT / "campaign_record" / "campaign_memory.yaml").read_text(
        encoding="utf-8"))
    assert memory["runs"][t6c.RUN_ID]["registry"] == {"skipped": "refold"}


@pytest.mark.usefixtures("reader_docs")
def test_a_passing_refold_stops_then_continue_ends_completed_refold(monkeypatch):
    _set_orchestrator(t6c.RETIRED_ON)
    run_dir = t6c._graded_run("refuted", good=True)
    _as_refold(run_dir)
    t6c._forbid(monkeypatch)
    rpr.run_loop(t6c.RUN_ID)
    paused = t6c._state(run_dir)
    assert paused["status"] == "paused_for_human" and paused["flags"] == {"profit_bars_reached": True}
    rpr.update_state(path=run_dir, status="active", flags={"profit_bars_reached": False})
    t6c._continue_decision(run_dir)
    monkeypatch.setattr(rpr, "determine_post_specialist_readers_route",
                        lambda *a, **k: pytest.fail("the grid route ran on a re-run"))
    rpr.run_loop(t6c.RUN_ID)
    state = t6c._state(run_dir)
    assert state["pending_stage"] == rpr.REFOLD_TERMINAL and state["status"] == "completed"


# -- process_once: the DONE branch of a re-run ------------------------------------------------

from test_halt_quarantine_policy import (  # noqa: E402
    _entry, _save_queue_entries, _write_campaign_state, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)


@pytest.mark.parametrize("pending, verdict_status", [(rpr.REFOLD_TERMINAL, None),
                                                     ("completed_rejected", "ungated")])
def test_done_records_where_the_refold_ended_and_decides_nothing(campaign_root, monkeypatch,
                                                                 pending, verdict_status):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setattr(dn, "decide", lambda *a, **k: pytest.fail("decide-next ran"))
    root = campaign_root["root"]
    t59._write_flags(root, **t6c.FLAT_ON)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_912", status="completed",
                                    pending_stage=pending)
    _as_refold(run_dir)
    # the grid was computed (campaign memory needs it) and says refuted: the outcome is
    # still where the re-run ended, never the grid's idea_status
    _result, _verdict, _routing = rpr._GRID_IDEA_STATUS_ROUTING["refuted"]
    (run_dir / "artifacts" / "idea_status.yaml").write_text(yaml.safe_dump({
        "run_id": "run_912", "idea_status": "refuted", "result": _result,
        "hypothesis_verdict": _verdict, "lineage_routing": _routing,
        "grid_evaluation_ref": "runs/run_912/artifacts/grid_evaluation.yaml", "reason": "r"}),
        encoding="utf-8")
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_912")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_912"], trial_sharpes=[])
    assert camp.process_once() is True
    done = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert done["status"] == "done" and done["outcome"] == pending
    assert done.get("verdict_status") == verdict_status
    assert not (run_dir / "artifacts" / "decision_record.yaml").exists()
    assert "DECIDE not run" in (root / "campaign_log.md").read_text(encoding="utf-8")


def test_a_legacy_shaped_source_pass_rule_is_refused(_seed):
    _source(_seed, rule={"criteria": [{"metric": "sharpe", "metric_basis": "legacy"}]})
    with pytest.raises(ValueError, match="no menu-shaped pass_rule"):
        camp.refold_brief(SRC, "C")


def test_the_cli_refuses_when_1b_or_2_would_call_a_model(_seed):
    _source(_seed)
    _set_orchestrator({**FLAGS, "exact_config_1b": {"enabled": False}})
    assert camp._refold_from_cli(SRC, "C", 0) == 1
    assert not (_seed / "briefs").exists() and _queue(_seed) == {"queue": []}


def test_the_launch_refuses_when_the_source_changed_since_the_brief(_seed):
    arts = _source(_seed)
    _register(_seed)
    changed = t59._base_config(lookback=99)
    (arts / "backtest_spec.yaml").write_text(yaml.safe_dump({"config": changed}),
                                             encoding="utf-8")
    queue = _queue(_seed)
    with pytest.raises(RuntimeError, match="changed since the brief was written"):
        camp._launch_run(queue, queue["queue"][-1], "fresh_launch", True, [],
                         promotion_retired=True)
