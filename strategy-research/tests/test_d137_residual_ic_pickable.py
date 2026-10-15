"""D-137 (direction ruling 2026-10-15, confirmed by the operator: smaller version only; card A):
step 1a MAY name `residual_ic` on its card, and code keeps adding it exactly as before.

Naming it is accepted only where code adds it anyway (orchestrator.composition_runs on, a
forecast-block idea): the named copy is replaced by code's own code_added_criteria entry
(_with_residual_ic_criterion), so a card that names it gives the same pass_rule as one that does
not. Not naming it removes nothing. It never counts as the card's own criterion: a card naming
only residual_ic is refused, as on master (at least one menu entry is required). Anywhere else a card naming it is refused, as before D-137.
No flag, no new check: the larger version (1a decides, code no longer forces it) has no path.
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
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e060_s2_residual_ic import COMP_ON  # noqa: E402
import test_c51_menu_criterion_lint as t51  # noqa: E402

MENU = yaml.safe_load((SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
RIC = "residual_ic"
OTHER = "sign_consistent_by_era"
CODE_ENTRY = rpr._code_added_criterion(MENU, RIC)   # what code adds (meta keys stripped)


def _card(*items, added=True):
    return rpr._pass_rule_from_card({"criteria": list(items)}, MENU, "card.yaml",
                                    residual_ic_added=added)


def _ids(rule):
    return [c["id"] for c in rule["criteria"]]


# -- the menu: residual_ic stays a code-added entry, not a `criteria:` entry -------------------

def test_residual_ic_is_still_only_in_code_added_criteria():
    assert RIC not in [e["id"] for e in MENU["criteria"]]
    assert [e["id"] for e in MENU["code_added_criteria"]].count(RIC) == 1
    entry = next(e for e in MENU["code_added_criteria"] if e["id"] == RIC)
    assert entry["card_overridable"] == []


# -- the card seam ------------------------------------------------------------------------------

def test_not_where_code_adds_it_a_card_naming_it_is_refused_as_before():
    with pytest.raises(ValueError, match="not a live entry"):
        _card({"id": OTHER}, {"id": RIC}, added=False)
    with pytest.raises(ValueError, match="not a live entry"):   # the default is the old behaviour
        rpr._pass_rule_from_card({"criteria": [{"id": RIC}]}, MENU, "card.yaml")


def test_named_where_code_adds_it_is_accepted_and_is_codes_own_entry():
    out = _card({"id": OTHER}, {"id": RIC})
    assert _ids(out) == [OTHER, RIC]
    assert out["criteria"][-1] == CODE_ENTRY
    assert out["criteria"][-1]["threshold"] == 0.02 and out["criteria"][-1]["max_p_value"] == 0.05
    assert out["criteria"][-1]["floor"] == {"min_n_eff": 30}


def test_named_gives_the_same_rule_as_not_named_plus_code():
    not_named = rpr._with_residual_ic_criterion(_card({"id": OTHER}), MENU)
    assert _card({"id": OTHER}, {"id": RIC}) == not_named
    assert _card({"id": RIC}, {"id": OTHER}) == not_named          # position on the card is irrelevant
    assert _card({"id": RIC}, {"id": OTHER}, {"id": RIC}) == not_named   # twice is still once


def test_a_card_naming_only_residual_ic_is_refused_as_on_master():
    """It never counts as the card's own criterion: at least one menu entry is still required."""
    for items in ([{"id": RIC}], [{"id": RIC}, {"id": RIC}]):
        with pytest.raises(ValueError, match="residual_ic does not count toward the card's own "
                                             "criteria") as exc:
            _card(*items)
        assert "pick at least one entry from the menu" in str(exc.value)
    # [menu entry + residual_ic] still gives the same rule as [menu entry] alone (plus code's add)
    assert _card({"id": OTHER}, {"id": RIC}) == rpr._with_residual_ic_criterion(
        _card({"id": OTHER}), MENU)


def test_restating_codes_own_values_is_not_an_override():
    out = _card({"id": OTHER}, {"id": RIC, "threshold": 0.02, "max_p_value": 0.05})
    assert out["criteria"].count(CODE_ENTRY) == 1 and _ids(out).count(RIC) == 1


@pytest.mark.parametrize("override", [
    {"threshold": 0.01}, {"max_p_value": 0.5}, {"floor": {"min_n_eff": 10}},
    {"comparator": ">="}, {"metric": "forecast_return_corr_all_bars"}, {"source": "window"},
])
def test_a_card_trying_to_override_it_is_refused(override):
    with pytest.raises(ValueError, match="does not let a criterion override") as exc:
        _card({"id": OTHER}, {"id": RIC, **override})
    assert "Refusing before 1b" in str(exc.value)


def test_an_unknown_id_message_lists_residual_ic_only_where_it_is_accepted():
    with pytest.raises(ValueError) as on:
        _card({"id": "nope"})
    with pytest.raises(ValueError) as off:
        _card({"id": "nope"}, added=False)
    assert repr(RIC) in str(on.value) and repr(RIC) not in str(off.value)


# -- the 1a writer (_write_pass_rule_from_card): code keeps adding it ---------------------------

def _card_run(sandbox, run_id, criteria, brief_extra=None):
    t51._seed_real_menu(sandbox)
    brief = t51._fresh_launch_brief(None)
    brief.pop("evaluation")
    brief["candidate"] = {"criteria_from": rpr.PASS_RULE_PENDING_AT_1A,
                          "source": {"hypothesis_id": "H__p-1"}, **(brief_extra or {})}
    camp._materialize_run(run_id, brief)
    run_dir = camp.ROOT / "runs" / run_id
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "H__p-1", "criteria": criteria}), encoding="utf-8")
    return run_dir


def _pass_rule(run_id):
    return yaml.safe_load((camp.ROOT / "runs" / run_id / "artifacts" / "pre_registration.yaml")
                          .read_text(encoding="utf-8"))["pass_rule"]


def test_flag_on_named_and_not_named_register_the_same_single_criterion(_sandbox_by_default):
    _set_orchestrator(COMP_ON)
    assert rpr._composition_runs_enabled() is True
    rules = {}
    for run_id, crit in (("run_d137_1", [{"id": OTHER}]),
                         ("run_d137_2", [{"id": OTHER}, {"id": RIC}]),
                         ("run_d137_3", [{"id": RIC}, {"id": OTHER}])):
        run_dir = _card_run(_sandbox_by_default, run_id, crit)
        assert rpr._write_pass_rule_from_card(run_dir, run_id, False) is True
        rules[run_id] = _pass_rule(run_id)
    assert rules["run_d137_1"] == rules["run_d137_2"] == rules["run_d137_3"]
    assert _ids(rules["run_d137_1"]) == [OTHER, RIC]          # not named: code still adds it
    assert rules["run_d137_1"]["criteria"][-1] == CODE_ENTRY


def test_flag_on_an_override_is_refused_and_nothing_is_written(_sandbox_by_default):
    _set_orchestrator(COMP_ON)
    run_dir = _card_run(_sandbox_by_default, "run_d137_4", [{"id": OTHER}, {"id": RIC, "threshold": 0.0}])
    before = _pass_rule("run_d137_4")
    with pytest.raises(ValueError, match="does not let a criterion override"):
        rpr._write_pass_rule_from_card(run_dir, "run_d137_4", False)
    assert _pass_rule("run_d137_4") == before


def test_flag_on_a_card_naming_only_residual_ic_is_refused_and_nothing_is_written(
        _sandbox_by_default):
    _set_orchestrator(COMP_ON)
    run_dir = _card_run(_sandbox_by_default, "run_d137_11", [{"id": RIC}])
    before = _pass_rule("run_d137_11")
    with pytest.raises(ValueError, match="does not count toward the card's own criteria"):
        rpr._write_pass_rule_from_card(run_dir, "run_d137_11", False)
    assert _pass_rule("run_d137_11") == before


def test_flag_off_naming_it_is_refused_and_not_naming_it_is_unchanged(_sandbox_by_default):
    assert rpr._composition_runs_enabled() is False
    run_dir = _card_run(_sandbox_by_default, "run_d137_5", [{"id": OTHER}, {"id": RIC}])
    with pytest.raises(ValueError, match="not a live entry"):
        rpr._write_pass_rule_from_card(run_dir, "run_d137_5", False)
    run_dir = _card_run(_sandbox_by_default, "run_d137_6", [{"id": OTHER}])
    assert rpr._write_pass_rule_from_card(run_dir, "run_d137_6", False) is True
    assert _ids(_pass_rule("run_d137_6")) == [OTHER]


def test_flag_on_regime_block_is_exempt_naming_it_is_refused(_sandbox_by_default):
    _set_orchestrator(COMP_ON)
    regime = {"manifest": {"block": {"kind": "regime"}}}
    run_dir = _card_run(_sandbox_by_default, "run_d137_7", [{"id": OTHER}, {"id": RIC}], regime)
    assert rpr._residual_ic_exempt_reason(run_dir) == "regime block"
    with pytest.raises(ValueError, match="not a live entry"):
        rpr._write_pass_rule_from_card(run_dir, "run_d137_7", False)
    run_dir = _card_run(_sandbox_by_default, "run_d137_8", [{"id": OTHER}], regime)
    assert rpr._write_pass_rule_from_card(run_dir, "run_d137_8", False) is True
    assert _ids(_pass_rule("run_d137_8")) == [OTHER]


# -- the larger version has no path: 1a's choice never removes or changes code's entry ----------

def test_a_1a_written_pass_rule_gets_codes_entry_whatever_1a_wrote(_sandbox_by_default):
    """The other 1a seam (a pass_rule 1a wrote itself, _ensure_residual_ic_in_pre_registration):
    left out -> appended; named with its own numbers -> replaced by code's entry; one criterion."""
    t51._seed_real_menu(_sandbox_by_default)
    for run_id, crit in (("run_d137_9", [{"id": OTHER, "source": "window"}]),
                         ("run_d137_10", [{"id": OTHER, "source": "window"},
                                          {"id": RIC, "threshold": 0.0, "max_p_value": 1.0}])):
        run_dir = _sandbox_by_default / "runs" / run_id
        (run_dir / "artifacts").mkdir(parents=True)
        rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                      {"pass_rule": {"criteria": crit}})
        assert rpr._ensure_residual_ic_in_pre_registration(run_dir) is True
        rule = _pass_rule(run_id)
        assert _ids(rule) == [OTHER, RIC] and rule["criteria"][-1] == CODE_ENTRY


def test_with_residual_ic_criterion_never_drops_it():
    """Code's append keys on nothing 1a writes: every input rule comes out with exactly one copy."""
    for rule in ({"criteria": []}, {"criteria": [{"id": OTHER}]},
                 {"criteria": [{"id": RIC, "threshold": 9}]}, {"criteria": [{"id": RIC}, {"id": RIC}]}):
        out = rpr._with_residual_ic_criterion(rule, MENU)
        assert _ids(out).count(RIC) == 1 and out["criteria"][-1] == CODE_ENTRY
