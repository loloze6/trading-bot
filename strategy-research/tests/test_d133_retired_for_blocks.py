"""D-133 (operator decision 2026-10-14): the lot-based `realized_edge_to_cost_ratio` is retired
for blocks (`retired_for: [block]` in config/criterion_menu.yaml, no flag).

Refused where a NEW choice of criteria is made for a block idea: step 1a's card
(run_phase1_research._pass_rule_from_card, reached through _write_pass_rule_from_card) and an
operator brief's own evaluation.pass_rule (verdict_criteria_evaluator.lint_menu_shaped_pass_rule,
called from run_campaign._materialize_run). NOT changed: a refinement brief's pass_rule
(_materialize_refinement_run copies it verbatim from the source brief), a fold
child's copy of its source's already-pre-registered criteria (D-121), the grid evaluating an
existing pass_rule, a composition run (its criteria are written by code, never picked here).
"""
from __future__ import annotations

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
from _reader_test_helpers import _set_orchestrator  # noqa: E402
import test_c51_menu_criterion_lint as t51  # noqa: E402

MENU = yaml.safe_load((SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
RETIRED = "realized_edge_to_cost_ratio"
ON = {"brief_criteria": {"enabled": True}}
REFUSAL = r"retired for blocks.*D-107, D-128, D-133"


def _pre_reg(run_id):
    return yaml.safe_load((camp.ROOT / "runs" / run_id / "artifacts" / "pre_registration.yaml")
                          .read_text(encoding="utf-8"))


# -- (e) the menu loader treats retired_for as meta ------------------------------------------

def test_the_menu_entry_is_retired_for_blocks_and_stays_in_place():
    ids = [e["id"] for e in MENU["criteria"]]
    assert ids[0] == RETIRED                       # not deleted, not moved
    entry = MENU["criteria"][0]
    assert entry["retired_for"] == ["block"]
    assert all("retired_for" not in e for e in MENU["criteria"][1:])


def test_retired_for_is_a_menu_meta_key_never_a_criterion_field():
    assert "retired_for" in rpr._MENU_META_KEYS
    resolved = rpr._pass_rule_from_card({"criteria": [{"id": "sign_consistent_by_era"}]},
                                        MENU, "t")["criteria"][0]
    assert not set(rpr._MENU_META_KEYS) & set(resolved)
    # a copy that does name the retired entry (composition-run seam) is stripped the same way
    kept = rpr._pass_rule_from_card({"criteria": [{"id": RETIRED}]}, MENU, "t",
                                    block_run=False)["criteria"][0]
    assert "retired_for" not in kept and "basis" not in kept and kept["id"] == RETIRED


def test_resolving_a_retired_entry_against_the_menu_still_works():
    out = vce.resolve_criteria_against_menu([{"id": RETIRED}], MENU)
    assert out[0]["metric"] == RETIRED and out[0]["threshold"] == 2.2
    # restating the menu's own retired_for is not an "override" (no violation of that kind)
    assert vce.menu_criterion_overrides_violations(out[0], MENU["criteria"][0]) == []


# -- (a) step 1a's card -----------------------------------------------------------------------

def test_a_card_naming_the_retired_entry_is_refused_with_the_message():
    with pytest.raises(ValueError, match=REFUSAL) as exc:
        rpr._pass_rule_from_card({"criteria": [{"id": RETIRED}]}, MENU, "card.yaml")
    assert "criteria[0]" in str(exc.value) and "Refusing before 1b" in str(exc.value)


def test_a_card_mixing_live_and_retired_entries_is_refused():
    with pytest.raises(ValueError, match=REFUSAL):
        rpr._pass_rule_from_card({"criteria": [{"id": "sign_consistent_by_era"},
                                               {"id": RETIRED}]}, MENU, "card.yaml")


def test_the_unknown_id_message_no_longer_lists_the_retired_entry():
    with pytest.raises(ValueError, match="not a live entry") as exc:
        rpr._pass_rule_from_card({"criteria": [{"id": "no_such"}]}, MENU, "card.yaml")
    assert RETIRED not in str(exc.value) and "sign_consistent_by_era" in str(exc.value)


def _candidate_brief(source_hid="H__p-1", **candidate):
    brief = t51._fresh_launch_brief(None)
    brief.pop("evaluation")
    brief["candidate"] = {"criteria_from": rpr.PASS_RULE_PENDING_AT_1A,
                          "source": {"hypothesis_id": source_hid}, **candidate}
    return brief


def _run_with_card(sandbox, run_id, brief, criteria):
    t51._seed_real_menu(sandbox)
    camp._materialize_run(run_id, brief)
    run_dir = camp.ROOT / "runs" / run_id
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "H__p-1", "criteria": criteria}), encoding="utf-8")
    return run_dir


def test_1a_writer_refuses_the_retired_entry_for_a_block_run(_sandbox_by_default):
    run_dir = _run_with_card(_sandbox_by_default, "run_d133_1", _candidate_brief(),
                             [{"id": RETIRED}])
    before = _pre_reg("run_d133_1")
    with pytest.raises(ValueError, match=REFUSAL):
        rpr._write_pass_rule_from_card(run_dir, "run_d133_1", False)
    assert _pre_reg("run_d133_1") == before           # nothing written


def test_1a_writer_still_writes_the_other_live_entries(_sandbox_by_default):
    run_dir = _run_with_card(_sandbox_by_default, "run_d133_2", _candidate_brief(),
                             [{"id": "sign_consistent_by_era"}, {"id": "whole_test_sharpe_positive"}])
    assert rpr._write_pass_rule_from_card(run_dir, "run_d133_2", False) is True
    assert [c["id"] for c in _pre_reg("run_d133_2")["pass_rule"]["criteria"]] == [
        "sign_consistent_by_era", "whole_test_sharpe_positive"]


def test_a_composition_run_is_not_a_block_run(_sandbox_by_default):
    """candidate.composition marks a composition run (_residual_ic_exempt_reason); its
    criteria are written by code, so `[block]` does not apply to it."""
    brief = _candidate_brief(composition={"manifest_ref": "x"})
    run_dir = _run_with_card(_sandbox_by_default, "run_d133_3", brief, [{"id": RETIRED}])
    assert rpr._residual_ic_exempt_reason(run_dir) == "composition run"
    assert rpr._write_pass_rule_from_card(run_dir, "run_d133_3", False) is True
    assert [c["id"] for c in _pre_reg("run_d133_3")["pass_rule"]["criteria"]] == [RETIRED]


def test_a_regime_block_is_still_a_block(_sandbox_by_default):
    brief = _candidate_brief()
    brief["candidate"]["source"]["proposal"] = {"block": {"kind": "regime"}}
    run_dir = _run_with_card(_sandbox_by_default, "run_d133_4", brief, [{"id": RETIRED}])
    assert rpr._residual_ic_exempt_reason(run_dir) == "regime block"
    with pytest.raises(ValueError, match=REFUSAL):
        rpr._write_pass_rule_from_card(run_dir, "run_d133_4", False)


# -- (b) an operator brief's own pass_rule (D-121 lint) ------------------------------------------

def test_the_lint_refuses_the_retired_entry_in_a_brief_pass_rule():
    violations = vce.lint_menu_shaped_pass_rule({"criteria": [{"id": RETIRED}]}, MENU)
    assert len(violations) == 1
    assert "criteria[0]" in violations[0] and "D-107" in violations[0] and "D-128" in violations[0]
    assert "retired for blocks" in violations[0]


def test_the_lint_refuses_a_fully_resolved_copy_of_it_too():
    resolved = vce.resolve_criteria_against_menu([{"id": RETIRED}], MENU)
    assert len(vce.lint_menu_shaped_pass_rule({"criteria": resolved}, MENU)) == 1


def test_a_flag_on_operator_brief_naming_it_is_refused_at_materialization(_sandbox_by_default):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    with pytest.raises(ValueError, match=r"(?s)C5\.1 menu lint.*retired for blocks"):
        camp._materialize_run("run_d133_5", t51._fresh_launch_brief({"criteria": [{"id": RETIRED}]}))


def test_a_refinement_brief_naming_it_is_accepted_it_is_a_copy(_sandbox_by_default, tmp_path):
    t51._seed_real_menu(_sandbox_by_default)
    resolved = vce.resolve_criteria_against_menu([{"id": RETIRED}], MENU)
    brief = {"brief_id": "REFINE", "evaluation": {"pass_rule": {
        "criteria": resolved,
        "outcomes": [{"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
                     {"branch": f"FAIL-{RETIRED}", "hypothesis_verdict": "kill",
                      "lineage_routing": "terminate"}]}}}
    path = tmp_path / "refinement_brief.yaml"
    path.write_text(yaml.safe_dump(brief), encoding="utf-8")
    # the pass_rule is copied verbatim from the source brief: not a new choice, never refused
    camp._materialize_refinement_run("run_d133_6", brief, path)
    assert [c["id"] for c in _pre_reg("run_d133_6")["pass_rule"]["criteria"]] == [RETIRED]


# -- (c) pre-registered criteria keep working --------------------------------------------------

# a source run's pre-registered rule, as 1a resolved it BEFORE the retirement
SRC_RULE = {"criteria": [{k: v for k, v in c.items() if k not in rpr._MENU_META_KEYS}
                         for c in vce.resolve_criteria_against_menu(
                             [{"id": RETIRED}, {"id": "sign_consistent_by_era"}], MENU)]}


def test_an_unknown_id_message_lists_only_the_live_entries():
    (msg,) = vce.lint_menu_shaped_pass_rule({"criteria": [{"id": "no_such_criterion"}]}, MENU)
    assert "no_such_criterion" in msg and "sign_consistent_by_era" in msg
    assert RETIRED not in msg.split("legacy")[0]   # the live-entries list omits the retired ratio


def test_the_lint_accepts_it_when_the_caller_says_the_criteria_are_already_pre_registered():
    assert vce.lint_menu_shaped_pass_rule(SRC_RULE, MENU, allow_retired=True) == []
    # ...and other violations are still reported in that mode
    bad = {"criteria": [{"id": RETIRED, "threshold": 99}]}
    assert vce.lint_menu_shaped_pass_rule(bad, MENU, allow_retired=True) != []


def test_a_source_rule_with_the_retired_entry_is_copied_to_a_fold_child():
    assert dn._criteria_for_child(SRC_RULE, MENU) == [{"id": RETIRED},
                                                         {"id": "sign_consistent_by_era", "metric": "net_return_pct"}]


def test_a_fold_child_carrying_it_materializes_unchanged(_sandbox_by_default):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    brief = t51._fresh_launch_brief({"criteria": dn._criteria_for_child(SRC_RULE, MENU)})
    brief["candidate"] = {"source": {"hypothesis_id": "H__p-1", "run_id": "run_074"},
                          "fold_assignment": {"fold": "B"}}
    camp._materialize_run("run_d133_7", brief)
    rule = _pre_reg("run_d133_7")["pass_rule"]
    assert [c["id"] for c in rule["criteria"]] == [RETIRED, "sign_consistent_by_era"]
    assert rule["criteria"][0]["threshold"] == 2.2 and "retired_for" not in rule["criteria"][0]
    # the very same criteria in a brief that is NOT a fold child are refused
    plain = t51._fresh_launch_brief({"criteria": dn._criteria_for_child(SRC_RULE, MENU)})
    with pytest.raises(ValueError, match=REFUSAL):
        camp._materialize_run("run_d133_8", plain)


def _protocol_result(ratio, trades_per_window=25, n_windows=5):
    windows = [{"symbol": "BTCUSDT", "window": f"2020-{i + 1:02d}",
                "core": {"sharpe": 1.0, "net_return_pct": 1.0, "trade_count": trades_per_window,
                         "max_drawdown_pct": -5.0, "win_rate": 0.5}}
               for i in range(n_windows)]
    return {"results": windows, "per_symbol_summary": {},
            "trade_diagnostics_summary": {RETIRED: ratio},
            "hypothesis_verdict": {"diagnostics": {}}}


@pytest.mark.parametrize("ratio, result", [(3.0, "PASS"), (1.5, "FAIL")])
def test_the_grid_still_evaluates_a_pre_registered_pass_rule_naming_it(ratio, result):
    grid = vce.evaluate_grid({"v1": _protocol_result(ratio)}, {"pass_rule": SRC_RULE}, {}, MENU)
    cell = grid["grid"][RETIRED]["v1"]
    assert cell["result"] == result and cell["value"] == ratio
    # a rule resolved against the menu with `retired_for` still attached evaluates as well
    resolved = {"criteria": vce.resolve_criteria_against_menu([{"id": RETIRED}], MENU)}
    assert "retired_for" in resolved["criteria"][0]
    grid = vce.evaluate_grid({"v1": _protocol_result(ratio)}, {"pass_rule": resolved}, {}, MENU)
    assert grid["grid"][RETIRED]["v1"]["result"] == result


# -- (d) the other live entries still pass ------------------------------------------------------

@pytest.mark.parametrize("cid", ["sign_consistent_by_era", "whole_test_sharpe_positive"])
def test_the_other_live_entries_pass_card_and_lint(cid):
    assert rpr._pass_rule_from_card({"criteria": [{"id": cid}]}, MENU, "t")["criteria"][0]["id"] == cid
    assert vce.lint_menu_shaped_pass_rule({"criteria": [{"id": cid}]}, MENU) == []
    assert vce.retired_for_block_violation(next(e for e in MENU["criteria"] if e["id"] == cid)) is None


def test_the_helper_reads_retired_for_exactly():
    assert vce.retired_for_block_violation({"id": "x"}) is None
    assert vce.retired_for_block_violation({"id": "x", "retired_for": []}) is None
    assert vce.retired_for_block_violation({"id": "x", "retired_for": ["composition"]}) is None
    assert "retired for blocks" in vce.retired_for_block_violation(
        {"id": "x", "retired_for": ["block"]})
    assert vce.retired_for_block_violation(None) is None
