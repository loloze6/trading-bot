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
