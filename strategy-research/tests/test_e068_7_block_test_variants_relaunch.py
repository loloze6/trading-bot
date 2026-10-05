"""
E-068 follow-ups from run_073 (operator decisions, 2026-10-05; D-076).

CUL-409: when the idea is a block (manifest kind forecast or regime), the claim
must have at least one test that reads the block's output -- criteria_refs alone
are not enough. A claim without one goes through the existing single claim
revision with a message saying so; the run continues either way, with the
warning recorded. Pass-through cards follow the same rule.

CUL-410: the v3 readers' claim digest carries each variant's exact patch
(variant_patches.yaml compacted), so a reader never guesses a variant's
parameters (run_073: forecast_power stated periods 1 and 2; they were 2 and 3).

CUL-408: `run_campaign.py --relaunch <id>` starts a failed entry again as a fresh
run; the old run is kept as a record (ORPHANED_README.md, the repo's convention).

No real LLM call, no backtest, no market data.
"""
import copy
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import claim_card as cc  # noqa: E402
import reader_findings as rf  # noqa: E402
import campaign_lock  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e056_1b_block_manifest import GOOD  # noqa: E402
from test_e068_s2_claim_card import CARD, UPPER, _claim  # noqa: E402
from test_e068_3b_claim_visibility import (  # noqa: E402
    ON, CLOSE_Q, FC_Q, REGIME_MANIFEST, FakeLLM, _answer, _revised, _rev)
from test_halt_quarantine_policy import (  # noqa: E402
    _save_queue_entries, _write_campaign_state,
    campaign_root,  # noqa: F401  (fixture)
)

CRIT = [{"id": "realized_edge_to_cost_ratio"}]
CRITERIA_ONLY = _claim(kind="cost_turnover", tests=None,
                       criteria_refs=["realized_edge_to_cost_ratio"])


# ---------------------------------------------------------------------------
# CUL-409: the rule
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("claim,kind,want", [
    (_claim(), "forecast", None),                                   # a forecast event test
    (_claim(tests=[copy.deepcopy(CLOSE_Q)]), "forecast", "blind"),  # price level only
    (CRITERIA_ONLY, "forecast", "no_block_test"),
    (_claim(kind="lead_lag", tests="none", missing_block="mb"), "forecast", None),  # exempt
    (CRITERIA_ONLY, "regime", "no_block_test"),
    (CRITERIA_ONLY, None, None),                                    # no manifest
    (CRITERIA_ONLY, "detector", None),                              # not a block kind
    (None, "forecast", None),                                       # no claim mapping
])
def test_block_test_gap(claim, kind, want):
    assert cc.block_test_gap(claim, kind) == want


@pytest.fixture
def criteria_run(monkeypatch):
    """A flag-on run past 1b: forecast manifest, a card whose claim is criteria-only."""
    monkeypatch.chdir(SR_ROOT)
    _set_orchestrator(ON)
    run_dir = _minimal_run(rpr.ROOT, "run_970")
    arts = run_dir / "artifacts"
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(GOOD), encoding="utf-8")
    rpr.save_yaml(arts / "hypothesis_card.yaml",
                  dict(CARD, criteria=CRIT, claim=copy.deepcopy(CRITERIA_ONLY)))
    rpr.update_state(path=run_dir, claim_check_retry={"attempts": 0, "last_error": None,
                                                      "last_check": None})
    return run_dir


def test_a_criteria_only_claim_gets_the_revision_with_its_own_message(criteria_run, monkeypatch):
    fake = FakeLLM(_answer(_revised(CRITERIA_ONLY, FC_Q)))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    assert len(fake.prompts) == 1
    msg = rpr.CLAIM_NO_BLOCK_TEST_MESSAGE.format(kind="forecast", column="forecast")
    prompt = " ".join(fake.prompts[0].split())   # yaml.dump wraps and escapes the message
    assert "criteria_refs alone are not enough" in msg and "criteria_refs alone are not" in prompt
    assert "the idea is a forecast block, but your claim has no test" in prompt
    doc = _rev(criteria_run)
    assert doc["status"] == "accepted" and doc["trigger"] == "no_block_test"
    assert doc["visibility_before"] == "not_applicable" and doc["visibility_after"] == "ok"
    assert doc["message"] == msg and "warning" not in doc
    card = rpr.load_yaml(criteria_run / "artifacts" / "hypothesis_card.yaml")
    assert card["claim"]["criteria_refs"] == ["realized_edge_to_cost_ratio"]  # refs kept
    assert card["claim"]["tests"][0]["name"] == FC_Q["name"]
    # the claim checks re-ran on the spliced card: it is now usable and measurable
    status = rpr.load_yaml(criteria_run / "artifacts" / "claim_test_status.yaml")
    assert status["usable"] is True and status["reason"] is None


def test_a_resumed_pass_keeps_the_trigger_and_the_warning(criteria_run, monkeypatch):
    """Review: a later 1b pass in the same run (one call per run) still says so."""
    changed = dict(_revised(CRITERIA_ONLY, FC_Q), statement="a different statement")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(changed)))
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)   # refused
    rpr._clear_claim_revision_files("strategy_config_authoring", criteria_run)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM())       # never called again
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    doc = _rev(criteria_run)
    assert doc["status"] == "skipped" and doc["trigger"] == "no_block_test"
    assert doc["warning"] == rpr.CLAIM_STILL_NO_BLOCK_TEST_WARNING


def test_a_tests_none_claim_is_not_asked_again(criteria_run, monkeypatch):
    arts = criteria_run / "artifacts"
    none = _claim(kind="lead_lag", tests="none", missing_block="a lead-lag outcome")
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=none))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM())
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    assert _rev(criteria_run)["status"] == "not_needed"


def test_the_finding_names_a_missing_block_test(criteria_run):
    import claim_findings as cf
    finding = cf.build_finding(criteria_run, criteria_run.name, {"variants": {}})
    assert finding["block_test_gap"] == "no_block_test"
    arts = criteria_run / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=_claim(tests=[UPPER])))
    assert "block_test_gap" not in cf.build_finding(criteria_run, criteria_run.name,
                                                    {"variants": {}})
    blind = _claim(tests=[copy.deepcopy(CLOSE_Q)])
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=blind))
    assert "block_test_gap" not in cf.build_finding(criteria_run, criteria_run.name,
                                                    {"variants": {}})


def test_a_refused_revision_keeps_the_claim_with_the_warning(criteria_run, monkeypatch):
    changed = dict(_revised(CRITERIA_ONLY, FC_Q), statement="a different statement")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(changed)))
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)   # never raises
    doc = _rev(criteria_run)
    assert doc["status"] == "refused" and doc["warning"] == rpr.CLAIM_STILL_NO_BLOCK_TEST_WARNING
    assert rpr.load_yaml(criteria_run / "artifacts" / "hypothesis_card.yaml")["claim"] == \
        CRITERIA_ONLY


def test_an_accepted_answer_still_without_a_block_test_is_warned(criteria_run, monkeypatch):
    same = {k: v for k, v in CRITERIA_ONLY.items() if k not in ("statement", "kind")}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(same)))
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    doc = _rev(criteria_run)
    assert doc["status"] == "accepted" and doc["visibility_after"] == "not_applicable"
    assert doc["warning"] == rpr.CLAIM_STILL_NO_BLOCK_TEST_WARNING


def test_a_budget_skip_records_the_warning(criteria_run, monkeypatch):
    monkeypatch.setattr(rpr, "_claim_llm_budget", lambda run_dir: (False, 2e6, 1.8e6))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM())   # never called
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    doc = _rev(criteria_run)
    assert doc["status"] == "skipped_budget"
    assert doc["warning"] == rpr.CLAIM_STILL_NO_BLOCK_TEST_WARNING


def test_a_regime_block_names_the_regime_column(criteria_run, monkeypatch):
    arts = criteria_run / "artifacts"
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(REGIME_MANIFEST), encoding="utf-8")
    fake = FakeLLM(_answer(dict(_revised(CRITERIA_ONLY))))     # tests: [] -> refused
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    doc = _rev(criteria_run)
    assert doc["message"] == rpr.CLAIM_NO_BLOCK_TEST_MESSAGE.format(kind="regime",
                                                                     column="regime")
    assert doc["warning"] == rpr.CLAIM_STILL_NO_BLOCK_TEST_WARNING


def test_a_pass_through_card_follows_the_same_rule(criteria_run, monkeypatch):
    arts = criteria_run / "artifacts"
    card = rpr.load_yaml(arts / "hypothesis_card.yaml")
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(card, pass_through=True))
    rpr.save_yaml(arts / "research_brief.yaml", {"candidate": {
        "config": {"a": 1}, "manifest": GOOD,
        "source": {"expected_config_sha256": "c" * 64}}})
    fake = FakeLLM(_answer(_revised(CRITERIA_ONLY, FC_Q)))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    assert len(fake.prompts) == 1 and _rev(criteria_run)["trigger"] == "no_block_test"


def test_a_composition_run_stays_exempt(criteria_run, monkeypatch):
    monkeypatch.setattr(rpr, "_claim_check_exempt", lambda *a: "composition run")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM())
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    assert _rev(criteria_run)["status"] == "not_applicable"


def test_a_blind_claim_keeps_its_original_message_and_record(criteria_run, monkeypatch):
    arts = criteria_run / "artifacts"
    blind = _claim(tests=[copy.deepcopy(CLOSE_Q)])
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=blind))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(_revised(blind, FC_Q))))
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    doc = _rev(criteria_run)
    assert doc["message"] == rpr.CLAIM_BLIND_MESSAGE and "trigger" not in doc


def test_a_claim_with_a_block_test_needs_nothing(criteria_run, monkeypatch):
    arts = criteria_run / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=_claim(tests=[UPPER])))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM())
    rpr._claim_revision_after_1b(criteria_run, criteria_run.name)
    assert _rev(criteria_run)["status"] == "not_needed"


def test_the_instruction_files_state_the_rule():
    for rel in ("hypothesis-design/CLAIM_TESTS.md", "claim-revision/SKILL.md"):
        text = (SR_ROOT / "workflow_artifacts" / "skills" / rel).read_text(encoding="utf-8")
        assert "criteria_refs" in text and "alone are not enough" in text or \
            "only `criteria_refs` (no tests)" in text


# ---------------------------------------------------------------------------
# CUL-410: the variants' patches in the readers' digest
# ---------------------------------------------------------------------------

VP = {"base_config_ref": "artifacts/backtest_spec.yaml", "variants": [
    {"variant_id": "base", "kind": "base", "symbol": "BTCUSDT", "patch": [],
     "rationale": "Period-2 shock reversal ... predicts lower churn"},
    {"variant_id": "design_period_3", "kind": "design", "symbol": "BTCUSDT",
     "patch": [{"path": "/strategies/regimes/unknown/components/0/params/period", "value": 3}],
     "rationale": "Sensitivity test ..."},
    {"variant_id": "asset_xrp", "kind": "asset", "symbol": "XRPUSDT", "patch": []}]}


def test_the_digest_carries_each_variants_exact_patch(tmp_path):
    arts = tmp_path / "artifacts"
    arts.mkdir()
    (arts / "variant_patches.yaml").write_text(yaml.safe_dump(VP), encoding="utf-8")
    d = rf.claim_result_digest(tmp_path)
    vp = d["variant_patches"]
    assert [v["variant_id"] for v in vp["variants"]] == ["base", "design_period_3", "asset_xrp"]
    assert vp["variants"][1]["patch"] == [
        {"path": "/strategies/regimes/unknown/components/0/params/period", "value": 3}]
    assert vp["variants"][2]["symbol"] == "XRPUSDT"
    assert "rationale" not in yaml.safe_dump(vp["variants"])   # no prose, only settings
    assert "never infer them from its name" in vp["note"]
    keys = list(d)
    assert keys.index("variant_patches") < keys.index("statement") and "status" not in d


@pytest.mark.parametrize("content", [None, "variants: [unclosed\n", "just a string\n"])
def test_no_or_bad_variant_patches_leave_the_digest_whole(tmp_path, content):
    arts = tmp_path / "artifacts"
    arts.mkdir()
    if content is not None:
        (arts / "variant_patches.yaml").write_text(content, encoding="utf-8")
    d = rf.claim_result_digest(tmp_path)
    assert "variant_patches" not in d and "status" not in d


# ---------------------------------------------------------------------------
# CUL-408: --relaunch
# ---------------------------------------------------------------------------

def _queue(campaign_root):
    return yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]


def _failed_entry(campaign_root, status="paused:unhandled_exception", run_ids=("run_900",)):
    _save_queue_entries(campaign_root["queue_path"], [
        {"id": "P", "brief_path": "briefs/P.md", "status": status, "priority": 999,
         "source": "agent", "notes": "n", "run_ids": list(run_ids), "origin": "reader"}])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[], trial_sharpes=[])
    for rid in run_ids:
        (campaign_root["runs_dir"] / rid).mkdir(exist_ok=True)


def test_relaunch_clears_run_ids_and_keeps_the_old_run_as_a_record(campaign_root):
    root = campaign_root["root"]
    _failed_entry(campaign_root)
    assert camp._relaunch_entry("P") is True
    (entry,) = _queue(campaign_root)
    assert entry["status"] == "ready" and entry["run_ids"] == [] and entry["priority"] == 999
    assert "RELAUNCHED" in entry["notes"] and "run_900" in entry["notes"]
    readme = root / "runs" / "run_900" / camp.ORPHANED_README
    assert readme.exists() and "--relaunch P" in readme.read_text(encoding="utf-8")
    assert camp._is_quarantined_orphan("run_900")      # reconcile counts it as known
    assert "RELAUNCH P: run_900 ended 'paused:unhandled_exception'" in (
        root / "campaign_log.md").read_text(encoding="utf-8")
    assert camp._next_action_for_entry(entry) == "fresh_launch"
    assert not campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH).exists()


@pytest.mark.parametrize("status,why", [
    ("paused:waiting_for_component", "--unpark"), ("blocked_on_operator_approval", "--approve"),
    ("ready", "only a failed entry"), ("done", "only a failed entry"),
    ("in_progress", "only a failed entry")])
def test_relaunch_refuses_anything_not_failed(campaign_root, status, why, capsys):
    _failed_entry(campaign_root, status=status)
    before = campaign_root["queue_path"].read_text(encoding="utf-8")
    assert camp._relaunch_entry("P") is False
    assert campaign_root["queue_path"].read_text(encoding="utf-8") == before
    out = capsys.readouterr().out
    assert "--relaunch refused" in out and why in out


@pytest.mark.parametrize("status", ["paused:launch_exception", "paused:flag_misconfiguration"])
def test_relaunch_refuses_a_launch_or_preflight_halt(campaign_root, status, capsys):
    """Review must-fix: a failed launch is never in run_ids, so run_ids[-1] is a
    healthy earlier run; --resume handles both halts."""
    _failed_entry(campaign_root, status=status)
    assert camp._relaunch_entry("P") is False
    assert "--resume" in capsys.readouterr().out
    assert not (campaign_root["root"] / "runs" / "run_900" / camp.ORPHANED_README).exists()
    assert _queue(campaign_root)[0]["run_ids"] == ["run_900"]


@pytest.mark.parametrize("status", [
    "paused:refinement_brief_conflicts_with_existing_continuation",
    "paused:legacy_continuation_under_retired_routing", "paused:idea_status_missing_at_done",
    "paused:protocol_promotion_unratified", "paused:budget_breaker"])
def test_relaunch_refuses_halts_where_the_run_did_not_fail(campaign_root, status, capsys):
    """Review round 2: an allowlist (stage_exception, unhandled_exception)."""
    _failed_entry(campaign_root, status=status)
    assert camp._relaunch_entry("P") is False
    assert "not a failed run" in capsys.readouterr().out
    assert _queue(campaign_root)[0]["run_ids"] == ["run_900"]


@pytest.mark.parametrize("status", ["paused:stage_exception", "paused:unhandled_exception"])
def test_relaunch_accepts_the_failed_run_halts(campaign_root, status):
    _failed_entry(campaign_root, status=status)
    assert camp._relaunch_entry("P") is True


def test_relaunch_refuses_an_unconsumed_refinement_brief(campaign_root, capsys):
    _save_queue_entries(campaign_root["queue_path"], [
        {"id": "P", "brief_path": "briefs/P.md", "status": "paused:unhandled_exception",
         "priority": 999, "source": "agent", "notes": "n", "run_ids": ["run_900"],
         "origin": "reader", "refinement_brief_path": "briefs/R.md"}])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[], trial_sharpes=[])
    assert camp._relaunch_entry("P") is False
    assert "carries a refinement brief" in capsys.readouterr().out


def test_relaunch_refuses_a_lineage(campaign_root, capsys):
    _failed_entry(campaign_root, run_ids=("run_900", "run_901"))
    assert camp._relaunch_entry("P") is False
    assert "holds a lineage" in capsys.readouterr().out
    _save_queue_entries(campaign_root["queue_path"], [
        {"id": "P", "brief_path": "briefs/P.md", "status": "paused:unhandled_exception",
         "priority": 999, "source": "agent", "notes": "n", "run_ids": ["run_900"],
         "origin": "reader", "refinement_brief_path": "briefs/R.md",
         "refinement_brief_consumed_for": "briefs/R.md"}])
    assert camp._relaunch_entry("P") is False
    assert "refinement brief" in capsys.readouterr().out


def test_relaunch_with_a_missing_old_folder_cites_no_readme(campaign_root):
    _failed_entry(campaign_root)
    (campaign_root["runs_dir"] / "run_900").rmdir()
    assert camp._relaunch_entry("P") is True
    (entry,) = _queue(campaign_root)
    assert "does not exist (no record written)" in entry["notes"]
    assert camp.ORPHANED_README not in entry["notes"]


def test_relaunch_refuses_an_entry_without_runs_an_unknown_id_and_a_held_lock(campaign_root):
    _failed_entry(campaign_root, run_ids=())
    assert camp._relaunch_entry("P") is False
    assert camp._relaunch_entry("NOPE") is False
    _failed_entry(campaign_root)
    lock = campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH)
    campaign_lock.acquire(lock)
    try:
        assert camp._relaunch_entry("P") is False
    finally:
        campaign_lock.release(lock)
    assert _queue(campaign_root)[0]["status"] == "paused:unhandled_exception"


def test_the_cli_has_relaunch():
    src = (SR_ROOT / "workflow" / "run_campaign.py").read_text(encoding="utf-8")
    assert 'parser.add_argument("--relaunch", metavar="ENTRY_ID"' in src
    assert "sys.exit(0 if _relaunch_entry(args.relaunch) else 1)" in src
