"""D-122 (operator decision 2026-10-13, ruling 2 item 4): `run_campaign.py refold`, the
operator's fold re-run command. It writes a brief that re-runs a finished run's authored
base config (exact config, D-110) and block manifest on another fold, and registers it
ready; the operator launches it with --once. Readers off unless --readers (code-written
skipped readings, rule operator_refold_readers_off). Registered without brief_status, so
decide-next never asks step 1a for more of the brief. Only the existing checks apply.
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
import reader_proposals as rpp  # noqa: E402
import research_folds as rf  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
import test_e059_s2a_decide_next as t59  # noqa: E402

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
FLAGS = {"brief_criteria": {"enabled": True}, "folds": {"enabled": True}}


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
    }
    for name, doc in docs.items():
        (arts / name).write_text(yaml.safe_dump(doc), encoding="utf-8")
    return arts


def _front(text):
    return yaml.safe_load(text.split("---", 2)[1])


def _folds_doc():
    return rf.load_folds(REAL_FOLDS, policy_path=REAL_POLICY)


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
        "end": end, "window_months": 4}}            # per_symbol_start dropped, as for a fold child
    assert front["refold"] == {"source_run": SRC, "fold": "C", "readers": False}
    assert "criteria_from" not in front and "research_only" not in front
    assert "pass_rule" not in front["machine_constraints"]
    cfg, man = front["constraints"]
    assert cfg.startswith(rpr.BRIEF_EXACT_CONFIG_PREFIX)
    assert json.loads(cfg.split("\n", 1)[1]) == t59._base_config()
    assert man.startswith(rpr.BRIEF_EXACT_MANIFEST_PREFIX)
    assert json.loads(man.split("\n", 1)[1]) == t59._MANIFEST


def test_criteria_come_from_the_flag_else_the_source_else_step_1a(_seed):
    _source(_seed)
    _r, text = camp.refold_brief(SRC, "C", criteria=["whole_test_sharpe_positive"])
    assert _front(text)["evaluation"] == {"pass_rule": {"criteria": [
        {"id": "whole_test_sharpe_positive"}]}}
    _r, text = camp.refold_brief(SRC, "C")
    assert _front(text)["evaluation"] == {"pass_rule": {"criteria": [
        {"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}]}}
    shutil.rmtree(_seed / "runs" / SRC)
    _source(_seed, rule={"criteria": [{"metric": "x", "metric_basis": "legacy"}]})
    _r, text = camp.refold_brief(SRC, "C")
    front = _front(text)
    assert front["criteria_from"] == "hypothesis_generation" and "evaluation" not in front


@pytest.mark.parametrize("missing", ["backtest_spec.yaml", "block_manifest.yaml",
                                     "pre_registration.yaml", "research_brief.yaml"])
def test_a_source_without_its_authored_config_or_manifest_is_refused(_seed, missing):
    arts = _source(_seed)
    (arts / missing).unlink()
    with pytest.raises(ValueError, match=f"missing .*{missing}"):
        camp.refold_brief(SRC, "C")


def test_a_pinned_protocol_source_is_refused(_seed):
    arts = _source(_seed)
    (arts / "pre_registration.yaml").write_text(yaml.safe_dump(
        {"machine_constraints": {"protocol_ref": "protocols/p.json"}}), encoding="utf-8")
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
    assert camp._refold_from_cli(SRC, "C", None, False, 0) == 1
    assert not (_seed / "briefs").exists()
    assert yaml.safe_load((_seed / "config" / "campaign_queue.yaml").read_text(
        encoding="utf-8")) == {"queue": []}


# -- registration, materialization and the launch pre-flight ----------------------------------

def _register(root, fold="C", **kw):
    _set_orchestrator(FLAGS)
    assert camp._refold_from_cli(SRC, fold, kw.get("criteria"), kw.get("readers", False), 0) == 0
    queue = yaml.safe_load((root / "config" / "campaign_queue.yaml").read_text(encoding="utf-8"))
    return queue["queue"][-1]


@pytest.mark.parametrize("fold", ["C", "D"])
def test_a_refold_brief_round_trips_through_registration_and_the_pre_flight(_seed, fold):
    _source(_seed)
    entry = _register(_seed, fold, criteria=["whole_test_sharpe_positive"])
    assert entry == {"id": f"refold_{SRC}_fold_{fold}",
                     "brief_path": f"briefs/refold_{SRC}_fold_{fold}.md", "status": "ready",
                     "priority": 0, "source": "operator_ratified",
                     "relation": "new_registration",
                     "notes": f"Refold of {SRC} on fold {fold} (D-122); readers off.",
                     "run_ids": []}
    run_id = "run_801"
    brief = camp._parse_brief_frontmatter(_seed / entry["brief_path"])
    camp._materialize_run(run_id, brief)
    run_dir = _seed / "runs" / run_id
    pre = yaml.safe_load((run_dir / "artifacts" / "pre_registration.yaml").read_text(
        encoding="utf-8"))
    assert [c["id"] for c in pre["pass_rule"]["criteria"]] == ["whole_test_sharpe_positive"]
    assert camp._protocol_preflight_refusal(run_dir, run_id, promotion_retired=True,
                                            folds_enabled=True) is None
    # the exact config and manifest reach step 1b unchanged (D-110)
    assert rpr._brief_exact_config(run_dir) == t59._base_config()
    assert rpr._brief_exact_manifest(run_dir) == t59._MANIFEST
    windows = rpr._ensure_protocol_from_constraints(
        run_dir, run_id, pre["machine_constraints"], promotion_retired=True, folds_enabled=True)
    doc = json.loads(Path(windows).read_text(encoding="utf-8"))
    assert doc["windows"] == rf.fold_windows(_folds_doc(), fold)


def test_the_same_brief_twice_is_refused_and_the_first_is_kept(_seed):
    _source(_seed)
    _register(_seed)
    before = (_seed / "briefs" / f"refold_{SRC}_fold_C.md").read_bytes()
    assert camp._refold_from_cli(SRC, "C", ["whole_test_sharpe_positive"], True, 0) == 1
    assert (_seed / "briefs" / f"refold_{SRC}_fold_C.md").read_bytes() == before


def test_a_refused_registration_leaves_no_brief(_seed):
    _source(_seed)
    (_seed / "config" / "campaign_queue.yaml").write_text(yaml.safe_dump(
        {"queue": [{"id": f"refold_{SRC}_fold_C", "brief_path": "gone.md", "status": "done",
                    "priority": 0, "source": "operator_ratified", "notes": "n",
                    "run_ids": []}]}), encoding="utf-8")
    _set_orchestrator(FLAGS)
    assert camp._refold_from_cli(SRC, "C", None, False, 0) == 1
    assert not (_seed / "briefs" / f"refold_{SRC}_fold_C.md").exists()


def test_the_criteria_argument_and_the_cli():
    assert camp._criteria_arg(" a, b ,,") == ["a", "b"]
    import subprocess
    out = subprocess.run([sys.executable, str(SR / "workflow" / "run_campaign.py"), "refold",
                          "--help"], capture_output=True, text=True, encoding="utf-8",
                         errors="replace", cwd=SR)
    assert out.returncode == 0 and "{A,B,C,D}" in out.stdout and "--readers" in out.stdout


# -- readers off by default, on with --readers ------------------------------------------------

def _materialized(root, readers):
    _source(root)
    entry = _register(root, readers=readers)
    camp._materialize_run("run_802", camp._parse_brief_frontmatter(root / entry["brief_path"]))
    return root / "runs" / "run_802"


def test_readers_off_every_reading_is_a_code_written_skip(_seed, monkeypatch):
    run_dir = _materialized(_seed, readers=False)
    monkeypatch.setattr(rpr, "run_reader_worker",
                        lambda *a, **k: pytest.fail("a reader was called"))
    rpr._run_specialist_readers("run_802", run_dir)
    for cat in rpr._reader_categories():
        doc = yaml.safe_load((run_dir / "artifacts" / "proposals" / f"{cat}.yaml").read_text(
            encoding="utf-8"))
        assert doc["skipped"]["rule"] == "operator_refold_readers_off"
        assert "run_800 on fold C" in doc["skipped"]["reason"]
    assert "operator_refold_readers_off" in rpp.SKIP_RULES


def test_readers_on_the_readers_run(_seed, monkeypatch):
    run_dir = _materialized(_seed, readers=True)
    assert rpr._refold_readers_off(run_dir) is None
    called = []

    def _reader(category, *_a, **_k):
        called.append(category)
        raise RuntimeError("stop after the first reader call")

    monkeypatch.setattr(rpr, "_check_reader_budget", lambda *a: None)
    monkeypatch.setattr(rpr, "run_reader_worker", _reader)
    with pytest.raises(RuntimeError, match="stop after"):
        rpr._run_specialist_readers("run_802", run_dir)
    assert called == [rpr._reader_categories()[0]]


def test_any_other_brief_reads_no_refold_rule(_seed):
    arts = _seed / "runs" / "run_803" / "artifacts"
    arts.mkdir(parents=True)
    (arts / "research_brief.yaml").write_text(yaml.safe_dump({"venue": "kraken"}),
                                              encoding="utf-8")
    assert rpr._refold_readers_off(arts.parent) is None
    assert rpr._refold_readers_off(_seed / "runs" / "absent") is None


# -- decide-next queues nothing from the brief; register and decide-next unchanged ------------

def test_the_entry_is_a_brief_without_brief_status(_seed):
    """No brief_status: decide-next's R2 asks step 1a for more only of an open owner
    (decide_next.r2_eligible_owner), and a brief without an owner gets no brief context, so
    step 1a gets no extra-card addendum (run_campaign._write_brief_hypotheses_context)."""
    _source(_seed)
    entry = _register(_seed)
    assert "brief_status" not in entry
    assert dn.brief_owner(entry, [entry]) is None and not dn.r2_eligible_owner(entry)
    queue = {"queue": [entry]}
    camp._write_brief_hypotheses_context(queue, entry, "run_804")
    assert not (_seed / "runs" / "run_804" / "artifacts" / rpr.BRIEF_CONTEXT_FILE).exists()


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


def test_the_help_says_a_repeat_is_refused():
    assert "same config on the same fold is refused as a repeat" in camp.REFOLD_HELP
