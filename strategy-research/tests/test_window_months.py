"""
machine_constraints.protocol.window_months: fewer, longer test windows.

The generator cut only monthly windows. A slow strategy tested in monthly
pieces pays an artificial entry and exit every month (each window starts flat
and closes at its end, O-9), and per-window reports grow with the window count
(CUL-370). `window_months` (1, 2, 3, 4, 6 or 12; default 1 = unchanged) cuts
calendar windows of that many months, aligned on the year so none crosses a
year (and so never an era boundary set on a year).
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import holdout_policy as hp  # noqa: E402
import run_campaign as camp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

from test_e061_c1_4_5_pauses_preflight import RUN, _NON_GENERIC, _scaffold  # noqa: E402

_FAR_SEAL = ("2030-01-01", "2030-06-30")


def _spans(ws):
    return [(w["label"], w["test"]["start"], w["test"]["end"]) for w in ws]


def test_the_default_is_the_monthly_generator_unchanged():
    a = rpr._generate_monthly_windows("2022-01-01", "2023-12-31", holdout_range=_FAR_SEAL)
    b = rpr._generate_monthly_windows("2022-01-01", "2023-12-31", holdout_range=_FAR_SEAL,
                                      window_months=1)
    assert a == b and len(a) == 24
    assert _spans(a)[:2] == [("2022-01", "2022-01-01", "2022-01-31"),
                             ("2022-02", "2022-02-01", "2022-02-28")]


def test_four_month_windows_over_two_years():
    ws = rpr._generate_monthly_windows("2022-01-01", "2023-12-31", holdout_range=_FAR_SEAL,
                                       window_months=4)
    assert _spans(ws) == [
        ("2022-01", "2022-01-01", "2022-04-30"), ("2022-05", "2022-05-01", "2022-08-31"),
        ("2022-09", "2022-09-01", "2022-12-31"), ("2023-01", "2023-01-01", "2023-04-30"),
        ("2023-05", "2023-05-01", "2023-08-31"), ("2023-09", "2023-09-01", "2023-12-31")]
    assert hp.windows_overlap(ws) is None


@pytest.mark.parametrize("months,count", [(2, 12), (3, 8), (6, 4), (12, 2)])
def test_every_allowed_length_tiles_the_years_exactly(months, count):
    ws = rpr._generate_monthly_windows("2022-01-01", "2023-12-31", holdout_range=_FAR_SEAL,
                                       window_months=months)
    assert len(ws) == count and hp.windows_overlap(ws) is None
    assert ws[0]["test"]["start"] == "2022-01-01" and ws[-1]["test"]["end"] == "2023-12-31"
    assert all(w["test"]["start"][:4] == w["test"]["end"][:4] for w in ws)  # none crosses a year


def test_a_short_last_window_ends_on_the_requested_end():
    ws = rpr._generate_monthly_windows("2022-01-01", "2022-10-31", holdout_range=_FAR_SEAL,
                                       window_months=4)
    assert _spans(ws)[-1] == ("2022-09", "2022-09-01", "2022-10-31")


@pytest.mark.parametrize("bad", [0, 5, 7, 24, True, "4", None])
def test_a_length_that_does_not_divide_the_year_is_refused(bad):
    with pytest.raises(ValueError, match="window_months"):
        rpr._generate_monthly_windows("2022-01-01", "2023-12-31", holdout_range=_FAR_SEAL,
                                      window_months=bad)


def test_a_start_off_the_calendar_boundary_is_refused():
    with pytest.raises(ValueError, match="calendar boundary"):
        rpr._generate_monthly_windows("2022-02-01", "2023-12-31", holdout_range=_FAR_SEAL,
                                      window_months=4)


def test_longer_windows_still_cannot_reach_the_seal():
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        rpr._generate_monthly_windows("2029-07-01", "2030-03-31", holdout_range=_FAR_SEAL,
                                      window_months=6)


def _constraints(**extra):
    return {"protocol": {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2022-01-01",
                         "end": "2023-12-31", "promotion": _NON_GENERIC, **extra}}


def test_the_brief_key_reaches_the_generated_protocol_and_the_preflight_agrees():
    run_dir = _scaffold(constraints=_constraints(window_months=4))
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints(window_months=4))
    written = json.loads(path.read_text(encoding="utf-8"))
    assert len(written["windows"]) == 6
    assert "window_months" not in written  # the windows themselves are the record
    assert camp._expected_generated_protocol(_constraints(window_months=4)["protocol"], RUN,
                                             promotion_retired=False, run_dir=run_dir) == written
    assert camp._generated_protocol_plan(run_dir, RUN, _constraints(window_months=4)["protocol"],
                                         {}, promotion_retired=False) == (None, None)


def test_a_brief_without_the_key_generates_monthly_windows():
    run_dir = _scaffold(constraints=_constraints())
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints())
    assert len(json.loads(path.read_text(encoding="utf-8"))["windows"]) == 24
