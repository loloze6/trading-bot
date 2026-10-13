"""D-121 (operator decision 2026-10-13, ruling 2 item 3): one criteria field for every brief
origin, orchestrator.brief_criteria (off by default).

On: a brief's own criteria -- evaluation.pass_rule whose every criterion is a menu id --
are checked only by lint_menu_shaped_pass_rule and resolved against the menu exactly as a
step-1a card's; decide-next copies a fold child's source criteria into that field. Off:
byte-identical. Also: the menu entry whole_test_sharpe_positive, graded on the same
whole-test Sharpe the profit bar sharpe_min reads.
"""
from __future__ import annotations

import copy
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
import verdict_criteria_evaluator as vce  # noqa: E402
import decide_next as dn  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
import test_c51_menu_criterion_lint as t51  # noqa: E402
import test_e077_folds as t77  # noqa: E402
import test_e062_s2b1_profit_bars_v2 as t62  # noqa: E402

MENU = yaml.safe_load((SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
ON = {"brief_criteria": {"enabled": True}}


def _pre_reg(run_id):
    return yaml.safe_load((camp.ROOT / "runs" / run_id / "artifacts" / "pre_registration.yaml")
                          .read_text(encoding="utf-8"))


# -- the flag ----------------------------------------------------------------------------

def test_the_flag_is_off_by_default_and_strict():
    assert rpr._brief_criteria_enabled({}) is False
    assert rpr._brief_criteria_enabled({"orchestrator": {"brief_criteria": {"enabled": True}}})
    with pytest.raises(ValueError):
        rpr._brief_criteria_enabled({"orchestrator": {"brief_criteria": {"enabled": "yes"}}})
    shipped = yaml.safe_load((SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert shipped["orchestrator"]["brief_criteria"]["enabled"] is False


# -- materialization: the one field ---------------------------------------------------------

def test_flag_on_menu_ids_alone_register_resolved_like_a_card(_sandbox_by_default):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    camp._materialize_run("run_d121_1", t51._fresh_launch_brief(
        {"criteria": [{"id": "whole_test_sharpe_positive"},
                      {"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}]}))
    rule = _pre_reg("run_d121_1")["pass_rule"]
    card_shape = rpr._pass_rule_from_card(
        {"criteria": [{"id": "whole_test_sharpe_positive"},
                      {"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}]},
        MENU, "test")
    assert rule == card_shape                      # the same shape as a step-1a card's
    assert "outcomes" not in rule                   # B11's table is not asked of it
    assert vce._is_menu_shaped_pass_rule(rule)


def test_flag_off_the_same_brief_is_refused_by_b11_as_before(_sandbox_by_default):
    _set_orchestrator({})
    t51._seed_real_menu(_sandbox_by_default)
    with pytest.raises(ValueError, match="B11"):
        camp._materialize_run("run_d121_2", t51._fresh_launch_brief(
            {"criteria": [{"id": "whole_test_sharpe_positive"}]}))


@pytest.mark.parametrize("criteria, match", [
    ([{"id": "no_such_entry"}], "C5.1 menu lint"),
    ([{"id": "whole_test_sharpe_positive", "threshold": 1.0}], "C5.1 menu lint"),
])
def test_flag_on_the_menu_lint_is_the_gate(_sandbox_by_default, criteria, match):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    with pytest.raises(ValueError, match=match):
        camp._materialize_run("run_d121_3", t51._fresh_launch_brief({"criteria": criteria}))


_LEGACY = {"metric": "sharpe", "comparator": ">", "threshold": 0, "metric_basis": "x"}


@pytest.mark.parametrize("criteria", [[_LEGACY],
                                      [{"id": "whole_test_sharpe_positive"}, _LEGACY]])
def test_flag_on_a_rule_not_all_menu_ids_keeps_every_lint(_sandbox_by_default, criteria):
    """A rule that is not menu ids only (a legacy criterion, alone or mixed with a menu
    id) is linted as before."""
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    with pytest.raises(ValueError, match="B11"):
        camp._materialize_run("run_d121_4", t51._fresh_launch_brief({"criteria": criteria}))


def test_criteria_from_and_criteria_together_still_raise(_sandbox_by_default):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    brief = t51._fresh_launch_brief({"criteria": [{"id": "whole_test_sharpe_positive"}]})
    brief["criteria_from"] = rpr.PASS_RULE_PENDING_AT_1A
    with pytest.raises(ValueError, match="criteria come from step 1a"):
        camp._materialize_run("run_d121_5", brief)


# -- decide-next: a fold child keeps its source's criteria ----------------------------------

def _fold_child(menu=None, *, folds=True, src_rule=None):
    inputs, pid = t77._scenario("run_074", "ROOT__x-run_070-1",
                                {"run_074": t77.FOLD_A, "run_070": t77.FOLD_A}, folds=folds)
    if src_rule is not None:
        for s in (inputs.get("sources") or inputs.get("runs") or {}).values():
            if isinstance(s, dict) and "pre_registration" in s:
                s["pre_registration"]["pass_rule"] = copy.deepcopy(src_rule)
    record = t77._decide(inputs, "run_074")
    kw = {} if menu is None else {"copy_criteria_menu": menu}
    rel, text = dn.candidate_brief(record, inputs, decision_ref="d", **kw)
    return yaml.safe_load(text.split("---", 2)[1]), text


SRC_RULE = rpr._pass_rule_from_card(
    {"criteria": [{"id": "whole_test_sharpe_positive"},
                  {"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}]}, MENU, "t")


def test_a_fold_child_copies_its_sources_criteria_into_the_one_field():
    front, text = _fold_child(MENU, src_rule=SRC_RULE)
    assert front["evaluation"]["pass_rule"] == {"criteria": [
        {"id": "whole_test_sharpe_positive"},
        {"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}]}
    assert "criteria_from" not in front["candidate"]
    assert "D-121" in text


def test_without_the_menu_a_fold_child_leaves_criteria_to_step_1a():
    """The campaign passes no menu with the flag off (the wiring test below), so the
    child brief is the pre-D-121 one."""
    _front, text = _fold_child(None, src_rule=SRC_RULE)
    assert "criteria_from: hypothesis_generation" in text and "evaluation:" not in text


def test_a_source_without_menu_criteria_leaves_them_to_step_1a():
    front, _t = _fold_child(MENU, src_rule={"criteria": [{"metric": "x", "metric_basis": "y"}]})
    assert front["candidate"]["criteria_from"] == "hypothesis_generation"
    assert "evaluation" not in front


def test_criteria_for_child_keeps_only_id_and_card_overridable_fields():
    out = dn._criteria_for_child(SRC_RULE, MENU)
    assert out == [{"id": "whole_test_sharpe_positive"},
                   {"id": "sign_consistent_by_era", "metric": "forecast_return_corr"}]
    assert dn._criteria_for_child({"criteria": []}, MENU) is None
    assert dn._criteria_for_child({"criteria": [{"id": "gone"}]}, MENU) is None


# -- the menu entry: one Sharpe definition --------------------------------------------------

def test_the_grid_reads_the_profit_bars_own_whole_test_sharpe(tmp_path):
    run_dir = tmp_path / "run"
    pr = t62._build(run_dir)
    t62._write_cost_model()
    rule = {"criteria": [{"id": "whole_test_sharpe_positive"}]}
    rule = rpr._pass_rule_from_menu_ids(rule, MENU)
    summaries = rpr._with_whole_test_sharpe({"base": pr}, run_dir, rule)
    injected = summaries["base"]["hypothesis_verdict"]["diagnostics"]["whole_test_sharpe"]
    bar = rpr._whole_test_profit_metrics(run_dir, pr, t62.V2_BARS)["sharpe_min"]["actual"]
    assert injected == bar                                   # one definition
    assert "whole_test_sharpe" not in ((pr.get("hypothesis_verdict") or {}).get("diagnostics") or {})
    grid = vce.evaluate_grid(summaries, {"pass_rule": rule}, {}, MENU)
    cell = grid["grid"]["whole_test_sharpe_positive"]["base"]
    assert cell["result"] == ("PASS" if injected > 0 else "FAIL") and cell["value"] == injected


def test_without_the_criterion_the_summaries_are_untouched(tmp_path):
    summaries = {"base": {"results": []}}
    rule = {"criteria": [{"id": "sign_consistent_by_era", "metric": "net_return_pct"}]}
    assert rpr._with_whole_test_sharpe(summaries, tmp_path, rule) is summaries


def test_a_sharpe_that_cannot_be_computed_reads_inconclusive(tmp_path):
    run_dir = tmp_path / "run"
    pr = t62._build(run_dir, strat=lambda _l, _k: 0.0)   # flat: zero stdev
    t62._write_cost_model()
    rule = rpr._pass_rule_from_menu_ids({"criteria": [{"id": "whole_test_sharpe_positive"}]}, MENU)
    summaries = rpr._with_whole_test_sharpe({"base": pr}, run_dir, rule)
    assert summaries["base"]["hypothesis_verdict"]["diagnostics"]["whole_test_sharpe"] is None
    grid = vce.evaluate_grid(summaries, {"pass_rule": rule}, {}, MENU)
    assert grid["grid"]["whole_test_sharpe_positive"]["base"]["result"] == "INCONCLUSIVE"


def test_the_template_now_documents_the_one_field():
    text = (SR / "workflow_artifacts" / "templates" / "research_brief_new_pipeline.md").read_text(
        encoding="utf-8")
    assert "D-121" in text and "whole_test_sharpe_positive" in text
    assert "do not add one here" not in text


# -- the campaign passes the menu to decide-next only under the flag -------------------------

from test_halt_quarantine_policy import campaign_root  # noqa: E402,F401
import test_e059_s2a_decide_next as t59  # noqa: E402


@pytest.mark.parametrize("flag", [False, True])
def test_the_campaign_hands_decide_next_the_menu_only_under_the_flag(campaign_root, monkeypatch,
                                                                     flag):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = campaign_root["root"]
    t59._stage_flag_on_source(campaign_root, [t59._patch("profitability-run_061-1", conf=3)])
    t59._write_flags(root, **t59._ALL_ON, brief_criteria=flag)
    seen = []
    real = dn.candidate_brief

    def spy(record, inputs, **kw):
        seen.append(kw)
        return real(record, inputs, **kw)

    monkeypatch.setattr(dn, "candidate_brief", spy)
    assert camp.process_once() is True
    assert len(seen) == 1
    if flag:
        assert seen[0]["copy_criteria_menu"] == yaml.safe_load(
            (root / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
    else:
        assert "copy_criteria_menu" not in seen[0]


def test_a_child_without_a_fold_assignment_still_leaves_criteria_to_step_1a():
    front, _t = _fold_child(MENU, folds=False, src_rule=SRC_RULE)
    assert front["candidate"].get("fold_assignment") is None
    assert front["candidate"]["criteria_from"] == "hypothesis_generation"
    assert "evaluation" not in front


@pytest.mark.parametrize("value, result", [(0.0, "FAIL"), (1e-9, "PASS"), (-0.5, "FAIL")])
def test_the_entry_is_strictly_above_zero(value, result):
    rule = rpr._pass_rule_from_menu_ids({"criteria": [{"id": "whole_test_sharpe_positive"}]}, MENU)
    summary = {"hypothesis_verdict": {"diagnostics": {"whole_test_sharpe": value}}}
    grid = vce.evaluate_grid({"base": summary}, {"pass_rule": rule}, {}, MENU)
    assert grid["grid"]["whole_test_sharpe_positive"]["base"]["result"] == result


# -- review fixes ---------------------------------------------------------------------------

def test_a_menu_id_rule_with_other_keys_is_refused_not_dropped(_sandbox_by_default):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    with pytest.raises(ValueError, match=r"carries only `criteria`.*'outcomes'"):
        camp._materialize_run("run_d121_6", t51._fresh_launch_brief(
            {"criteria": [{"id": "whole_test_sharpe_positive"}],
             "outcomes": {"PASS": "promote"}}))


def _materialize_fold_child(sandbox, run_id):
    _set_orchestrator(ON)
    t51._seed_real_menu(sandbox)
    brief = t51._fresh_launch_brief({"criteria": [{"id": "whole_test_sharpe_positive"}]})
    brief["candidate"] = {"source": {"hypothesis_id": "H__p-1", "run_id": "run_074"},
                          "fold_assignment": {"fold": "B"}}
    camp._materialize_run(run_id, brief)
    return camp.ROOT / "runs" / run_id


def test_a_fold_child_with_fixed_criteria_is_still_a_decide_next_candidate(_sandbox_by_default):
    run_dir = _materialize_fold_child(_sandbox_by_default, "run_d121_7")
    cand = rpr._decide_next_candidate(run_dir)
    assert cand is not None and cand["source"]["hypothesis_id"] == "H__p-1"
    before = _pre_reg("run_d121_7")
    arts = run_dir / "artifacts"
    (arts / "hypothesis_card.yaml").write_text(yaml.safe_dump(
        {"hypothesis_id": "H__p-1", "criteria": [{"id": "sign_consistent_by_era",
                                                  "metric": "net_return_pct"}]}),
        encoding="utf-8")
    assert rpr._write_pass_rule_from_card(run_dir, "run_d121_7", False) is True
    assert _pre_reg("run_d121_7") == before        # the card does not rewrite the criteria
    (arts / "hypothesis_card.yaml").write_text(yaml.safe_dump({"hypothesis_id": "OTHER"}),
                                               encoding="utf-8")
    with pytest.raises(ValueError, match="is not the candidate's"):
        rpr._write_pass_rule_from_card(run_dir, "run_d121_7", False)


def test_a_plain_operator_brief_is_not_a_candidate(_sandbox_by_default):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    camp._materialize_run("run_d121_8", t51._fresh_launch_brief(
        {"criteria": [{"id": "whole_test_sharpe_positive"}]}))
    assert rpr._decide_next_candidate(camp.ROOT / "runs" / "run_d121_8") is None


def test_an_unresolved_id_only_rule_still_gets_the_sharpe(tmp_path):
    run_dir = tmp_path / "run"
    pr = t62._build(run_dir)
    t62._write_cost_model()
    out = rpr._with_whole_test_sharpe({"base": pr}, run_dir,
                                      {"criteria": [{"id": "whole_test_sharpe_positive"}]})
    assert "whole_test_sharpe" in out["base"]["hypothesis_verdict"]["diagnostics"]


def test_every_grid_call_reads_the_injected_summaries():
    """Static: each evaluate_grid call in run_tool_worker (variant loop, composition,
    single column) takes _with_whole_test_sharpe(...) as its first argument."""
    import inspect
    import re
    src = inspect.getsource(rpr.run_tool_worker)
    calls = re.findall(r"_vce\.evaluate_grid\(\s*(\S+)", src)
    assert len(calls) == 3 and all(c.startswith("_with_whole_test_sharpe(") for c in calls), calls


def test_a_candidate_block_without_a_source_is_not_a_candidate(_sandbox_by_default):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    brief = t51._fresh_launch_brief({"criteria": [{"id": "whole_test_sharpe_positive"}]})
    brief["candidate"] = {"fold_assignment": {"fold": "B"}}
    camp._materialize_run("run_d121_9", brief)
    assert rpr._decide_next_candidate(camp.ROOT / "runs" / "run_d121_9") is None
