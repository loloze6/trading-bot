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
