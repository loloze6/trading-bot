"""Tests of step 5's answer checks: the status rules code enforces on the function's result."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_verdict as m  # noqa: E402

BASE = {"status": "confirmed", "situation_check": {"agreement": 0.95, "passed": True},
        "main_measure": {"value": 0.01, "statistic": {"name": "t", "value": 2.5}}, "counts": {"cases": 100},
        "decided_by": "the confirm rule", "reading": "none"}


def test_a_confirm_needs_its_supporting_check():
    m.check_result(dict(BASE, supporting_check=None))
    m.check_result(dict(BASE, supporting_check={"name": "s", "value": 1.0, "passed": True}))
    with pytest.raises(ValueError, match="supporting check failed"):
        m.check_result(dict(BASE, supporting_check={"name": "s", "value": -1.0, "passed": False}))
    m.check_result(dict(BASE, status="inconclusive", supporting_check={"name": "s", "value": -1.0, "passed": False}))


def test_mismatch_exactly_when_the_situation_check_fails():
    with pytest.raises(ValueError, match="mismatch"):
        m.check_result(dict(BASE, situation_check={"agreement": 0.5, "passed": False}))
    m.check_result({"status": "mismatch", "situation_check": {"agreement": 0.5, "passed": False},
                    "decided_by": "the forecast is active outside the situation", "reading": "none"})


def test_unknown_status_and_missing_counts_are_refused():
    with pytest.raises(ValueError):
        m.check_result(dict(BASE, status="probably"))
    with pytest.raises(ValueError):
        m.check_result(dict(BASE, counts={}))


def test_the_size_line_says_how_sure_the_size_is_and_reads_an_older_size_too():
    old = {"horizon_bars": 2, "cases": 10, "unusual_move": 0.004, "normal_drift": 0.001, "total_move": 0.005, "usual_move": 0.05, "strength": 0.08}
    assert "(t " not in m.size_line(old) and "+0.40 % per case" in m.size_line(old)   # written before 2026-11-23
    new = dict(old, unusual_move_t=2.345, case_days=7)
    assert "+0.40 % (t 2.35, the cases of one day together: 7 days)" in m.size_line(new)


def test_the_direction_check_on_the_check_folds():
    full = {"main_measure": {"value": 0.004}}
    same = {"main_measure": {"value": 0.002}, "counts": {"cases": 400, "days": 300}}
    other = {"main_measure": {"value": -0.001}, "counts": {"cases": 400, "days": 300}}
    few = {"main_measure": {"value": -0.003}, "counts": {"cases": 40, "days": 25}}
    assert m.direction_check(full, same)[0] is True
    assert m.direction_check(full, other)[0] is False
    assert m.direction_check(full, few)[0] is None            # too few cases: not judged, the verdict stands
    assert m.direction_check(full, None)[0] is None           # the measure could not run on the check folds alone
    assert m.direction_check({"main_measure": {"value": -0.004}}, other)[0] is True   # a negative main measure, same way


def test_the_check_folds_windows_follow_the_plans_fold_order(tmp_path):
    import lib
    plan = "---\ndata-period: folds A, B, C, D\n---\n"
    rec = tmp_path / "rec"
    (rec / "BTCUSD" / "fold_A").mkdir(parents=True)
    assert lib.windows_of(plan, lib.CHECK_FOLDS, rec) == [f"w{i}" for i in list(range(1, 7)) + list(range(19, 25))]
    assert lib.windows_of(plan, lib.EXPLORATION_FOLDS, rec) == [f"w{i}" for i in range(7, 19)]
    unseen = tmp_path / "unseen"; (unseen / "BTCUSD" / "windows").mkdir(parents=True)
    assert lib.windows_of(plan, lib.CHECK_FOLDS, unseen) == []   # an unseen-dates record: no check


def test_the_check_reads_the_measures_own_count_names():
    full = {"main_measure": {"value": 0.004}}
    named = {"main_measure": {"value": 0.002}, "counts": {"grid cases with forecast > 0": 500, "distinct days": 200}}
    unnamed = {"main_measure": {"value": -0.002}, "counts": {"active bars": 900}}
    few_days = {"main_measure": {"value": -0.002}, "counts": {"independent cases": 500, "distinct days": 12}}
    assert m.direction_check(full, named)[0] is True
    assert m.direction_check(full, unnamed)[0] is False        # no count names cases: the smallest count is taken
    assert m.direction_check(full, few_days)[0] is None


def test_the_new_data_use_checks_on_the_check_half(tmp_path):
    """A record in the new data use (its data_use.json): step 7 explores the windows before 2022, step 5 checks on the
    windows from 2022 (common/explore_and_check.md); the plan's folds are not read."""
    import json, lib
    rec = tmp_path / "rec"
    (rec / "BTCUSD" / "w1").mkdir(parents=True)
    (rec / "data_use.json").write_text(json.dumps({"version": 2, "research_coins": ["BTC"],
                                                   "windows": "04_backtest/windows/research_2016.json"}))
    plan = "---\ndata-period: folds A, B, C, D\n---\n"
    on, check = lib.check_windows(plan, rec)
    seen, explore = lib.exploration_windows(plan, rec)
    assert on == "the check half (2022 onward)" and seen == "the explore half"
    assert explore == [f"w{i}" for i in range(1, 19)] and check == [f"w{i}" for i in range(19, 33)]
    old = tmp_path / "old"
    (old / "BTCUSD" / "fold_A").mkdir(parents=True)
    assert lib.check_windows(plan, old) == ("folds A, D", lib.windows_of(plan, lib.CHECK_FOLDS, old))
    assert lib.exploration_windows(plan, old) == ("folds B, C", lib.windows_of(plan, lib.EXPLORATION_FOLDS, old))


PLAN_UP = "- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting check passes.\n- Reject: below 0 with t ≤ -2.\n"
PLAN_DOWN = "- Confirm: The slope is negative with t ≤ −2, and the check passes.\n- Reject: The slope is positive with t ≥ 2.\n"


def test_the_idea_direction_is_the_side_of_the_confirm_rule():
    assert m.idea_direction(PLAN_UP) == 1 and m.idea_direction(PLAN_DOWN) == -1
    assert m.idea_direction("- Confirm: The slope's t is -2 or less.\n- Reject: x\n") == -1
    assert m.idea_direction("- Confirm: The slope's t is 2 or more.\n- Reject: t of -2 or less\n") == 1
    assert m.idea_direction("no criterion") is None


def test_no_effect_rule():
    """common/verdicts.md (B11): rejected, or unclear with 30 cases and a t below 1 in the idea's direction."""
    u = lambda t, n: dict(BASE, status="inconclusive", main_measure={"value": t, "statistic": {"name": "t", "value": t}},
                          counts={"cases": n})
    assert m.effect_check(dict(BASE, status="rejected"), PLAN_UP)["no_effect"]
    assert m.effect_check(u(0.99, 30), PLAN_UP)["no_effect"]
    assert m.effect_check(u(-3.0, 30), PLAN_UP)["no_effect"]
    assert not m.effect_check(u(1.0, 30), PLAN_UP)["no_effect"]            # a sign of the effect: unclear
    assert not m.effect_check(u(0.2, 29), PLAN_UP)["no_effect"]            # too few cases to show absence
    assert not m.effect_check(u(-1.8, 500), PLAN_DOWN)["no_effect"]        # a falling slope: t -1.8 is a sign of it
    assert m.effect_check(u(0.10, 500), PLAN_DOWN)["no_effect"]
    assert not m.effect_check(dict(u(0.1, 500), main_measure={"value": 0.1, "statistic": None}), PLAN_UP)["no_effect"]
    assert m.effect_check(BASE, PLAN_UP) is None                          # a confirm: the rule does not apply
