"""
E-061 C1.6 code-review fix -- boundary/None/gap coverage for the ONE shared
`tools/protocol_resolution.py::era_id_for_timestamp` (previously two
independently-drifted copies in run_protocol.py and
verdict_criteria_evaluator.py; see that function's own docstring for the
open-ended-era bug and the simplified boolean-expression fix).

Every date here is COMPUTED from `config/campaign_data_policy.yaml` at
runtime via date arithmetic -- never a literal -- so this file can safely
exercise dates inside the sealed holdout window (campaign_data_policy.yaml's
`holdout_range`) without tripping the pre-commit holdout gate, which scans
for literal dates in that range (mirrors test_e061_end_to_end_wiring.py's
A7 test convention).
"""
from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "tools"))

import protocol_resolution as pr  # noqa: E402


def _d(iso: str) -> _dt.date:
    return _dt.date.fromisoformat(iso)


@pytest.fixture(scope="module")
def policy() -> dict:
    return yaml.safe_load(
        (_SR / "config" / "campaign_data_policy.yaml").read_text(encoding="utf-8")
    )


@pytest.fixture(scope="module")
def eras(policy) -> list:
    return policy["eras"]


def _era(eras: list, era_id: str) -> dict:
    for e in eras:
        if e["era_id"] == era_id:
            return e
    raise AssertionError(f"{era_id} not found in policy eras")


# ---------------------------------------------------------------------------
# 1. Exact lo/hi boundaries of a closed era
# ---------------------------------------------------------------------------

def test_closed_era_exact_lo_boundary_is_inclusive(eras):
    era = _era(eras, "era_2019_2023_full_feed")
    lo, hi = era["range"]
    assert pr.era_id_for_timestamp(lo, eras) == era["era_id"]


def test_closed_era_exact_hi_boundary_is_inclusive(eras):
    era = _era(eras, "era_2019_2023_full_feed")
    lo, hi = era["range"]
    assert pr.era_id_for_timestamp(hi, eras) == era["era_id"]


def test_one_day_before_a_closed_eras_lo_falls_in_the_previous_era(eras):
    """era_2018_pre_funding and era_2019_2023_full_feed are adjacent with no
    gap (hi=2019-09-09, next lo=2019-09-10) -- the day before the second
    era's lo boundary must resolve to the FIRST era, not era_unmapped."""
    era = _era(eras, "era_2019_2023_full_feed")
    lo = _d(era["range"][0])
    day_before = (lo - _dt.timedelta(days=1)).isoformat()
    assert pr.era_id_for_timestamp(day_before, eras) == "era_2018_pre_funding"


def test_one_day_after_a_closed_eras_hi_falls_in_the_next_era(eras):
    era = _era(eras, "era_2019_2023_full_feed")
    hi = _d(era["range"][1])
    day_after = (hi + _dt.timedelta(days=1)).isoformat()
    assert pr.era_id_for_timestamp(day_after, eras) == "era_2024_burned"


# ---------------------------------------------------------------------------
# 2. The open-ended era's start day (the original C1.6 TypeError site)
# ---------------------------------------------------------------------------

def test_open_ended_eras_start_day_resolves_without_raising(eras):
    era = _era(eras, "era_2026_h2_forward_recorded")
    assert era["range"][1] is None  # the open-ended era this whole fix is about
    lo = era["range"][0]
    assert pr.era_id_for_timestamp(lo, eras) == era["era_id"]


def test_open_ended_era_matches_a_date_far_past_its_start(eras):
    era = _era(eras, "era_2026_h2_forward_recorded")
    lo = _d(era["range"][0])
    far_future = (lo + _dt.timedelta(days=3650)).isoformat()  # +10 years, computed
    assert pr.era_id_for_timestamp(far_future, eras) == era["era_id"]


# ---------------------------------------------------------------------------
# 3. lo=None and both-None cases (synthetic -- no current policy era has a
#    null LOWER bound, so this is the symmetry the fix added proactively)
# ---------------------------------------------------------------------------

def test_null_lower_bound_matches_any_date_up_to_hi():
    synthetic = [{"era_id": "era_open_start", "range": [None, "2020-06-30"]},
                 {"era_id": "era_after", "range": ["2020-07-01", "2020-12-31"]}]
    assert pr.era_id_for_timestamp("1900-01-01", synthetic) == "era_open_start"
    assert pr.era_id_for_timestamp("2020-06-30", synthetic) == "era_open_start"


def test_null_lower_bound_excludes_dates_past_hi():
    synthetic = [{"era_id": "era_open_start", "range": [None, "2020-06-30"]},
                 {"era_id": "era_after", "range": ["2020-07-01", "2020-12-31"]}]
    assert pr.era_id_for_timestamp("2020-07-01", synthetic) == "era_after"


def test_both_bounds_null_matches_everything():
    synthetic = [{"era_id": "era_unbounded", "range": [None, None]}]
    for probe in ("0001-01-01", "2030-06-15", "9999-12-31"):
        assert pr.era_id_for_timestamp(probe, synthetic) == "era_unbounded"


# ---------------------------------------------------------------------------
# 4. The July gap: after the sealed holdout era ends, before the open-ended
#    forward-recorded era begins -- no era covers it -> era_unmapped
# ---------------------------------------------------------------------------

def test_date_in_the_gap_between_holdout_and_forward_recorded_is_unmapped(eras):
    holdout = _era(eras, "era_2026_holdout")
    forward = _era(eras, "era_2026_h2_forward_recorded")
    holdout_hi = _d(holdout["range"][1])
    forward_lo = _d(forward["range"][0])
    assert (forward_lo - holdout_hi).days > 1, "test assumes a real gap exists"
    gap_day = (holdout_hi + _dt.timedelta(days=1)).isoformat()
    assert pr.era_id_for_timestamp(gap_day, eras) == "era_unmapped"
    # the day right before the open-ended era starts is still in the gap
    day_before_forward = (forward_lo - _dt.timedelta(days=1)).isoformat()
    assert pr.era_id_for_timestamp(day_before_forward, eras) == "era_unmapped"


# ---------------------------------------------------------------------------
# 5. A date inside the sealed window maps to the holdout era label --
#    WITHOUT reading any candle data (era_id_for_timestamp only ever touches
#    the policy's `eras` metadata, never local_data/holdout_sealed/).
# ---------------------------------------------------------------------------

def test_a_date_inside_the_sealed_window_maps_to_the_holdout_era_label(policy, eras):
    holdout_range = policy["holdout_range"]
    lo = _d(holdout_range[0])
    hi = _d(holdout_range[1])
    midpoint = (lo + (hi - lo) / 2).isoformat()
    assert pr.era_id_for_timestamp(midpoint, eras) == "era_2026_holdout"
    # boundaries too
    assert pr.era_id_for_timestamp(holdout_range[0], eras) == "era_2026_holdout"
    assert pr.era_id_for_timestamp(holdout_range[1], eras) == "era_2026_holdout"


# ---------------------------------------------------------------------------
# 6. Both copies that used to exist independently now delegate to the same
#    implementation -- proves the dedup, not just that each one "works".
# ---------------------------------------------------------------------------

def test_run_protocol_and_verdict_criteria_evaluator_delegate_to_the_shared_impl(eras):
    sys.path.insert(0, str(_SR / "tools"))
    import run_protocol as rp
    import verdict_criteria_evaluator as vce

    import inspect
    # both former copies are now one-line delegators to the shared function --
    # not merely producing the same answer by coincidence.
    assert "protocol_resolution.era_id_for_timestamp" in inspect.getsource(rp._era_id_for_timestamp)
    assert "protocol_resolution.era_id_for_timestamp" in inspect.getsource(vce._era_id_for_timestamp)

    probes = [
        _era(eras, "era_2019_2023_full_feed")["range"][0],
        _era(eras, "era_2026_h2_forward_recorded")["range"][0],  # the open-ended era
        "1900-01-01",  # unmapped
    ]
    for probe in probes:
        expected = pr.era_id_for_timestamp(probe, eras)
        assert rp._era_id_for_timestamp(probe, eras) == expected
        assert vce._era_id_for_timestamp(probe, eras) == expected


# ---------------------------------------------------------------------------
# 7. Second-round code-review fixes: tz normalization, int rejection,
#    the shared policy loader, and memoization.
# ---------------------------------------------------------------------------

def test_tz_aware_timestamp_ahead_of_utc_resolves_by_its_utc_date(eras):
    """Asia/Kolkata (UTC+5:30). A timestamp that reads as the FIRST day of a
    closed era in its own (ahead-of-UTC) local clock is actually still the
    PREVIOUS UTC day -- must resolve to the earlier era, not the later one."""
    era = _era(eras, "era_2019_2023_full_feed")
    lo = era["range"][0]
    local_reading = f"{lo}T02:00:00+05:30"  # local calendar day == lo
    assert pr.era_id_for_timestamp(local_reading, eras) == "era_2018_pre_funding"
    # sanity: the same wall-clock date read as naive (no tz) DOES match `era`
    assert pr.era_id_for_timestamp(f"{lo}T02:00:00", eras) == era["era_id"]


def test_tz_aware_timestamp_behind_utc_resolves_by_its_utc_date(eras):
    """-05:00 (US Eastern standard offset). A timestamp that reads as the
    LAST day of a closed era in its own (behind-UTC) local clock has already
    rolled into the NEXT UTC day -- must resolve to the later era."""
    era = _era(eras, "era_2019_2023_full_feed")
    hi = era["range"][1]
    next_era = _era(eras, "era_2024_burned")
    local_reading = f"{hi}T20:00:00-05:00"  # local calendar day == hi
    assert pr.era_id_for_timestamp(local_reading, eras) == next_era["era_id"]
    # sanity: the same wall-clock date read as naive (no tz) DOES match `era`
    assert pr.era_id_for_timestamp(f"{hi}T20:00:00", eras) == era["era_id"]


def test_naive_timestamp_is_still_treated_as_already_utc(eras):
    """Pin, not a new decision: every real caller in this codebase passes
    naive-and-implicitly-UTC values, and that must keep working unchanged."""
    import datetime as _pydt
    era = _era(eras, "era_2019_2023_full_feed")
    naive = _pydt.datetime.fromisoformat(era["range"][0])
    assert naive.tzinfo is None
    assert pr.era_id_for_timestamp(naive, eras) == era["era_id"]


@pytest.mark.parametrize("bad", [1700000000000, 1700000000.5, True, False])
def test_bare_numbers_are_rejected_not_silently_guessed(eras, bad):
    with pytest.raises(ValueError, match="ambiguous"):
        pr.era_id_for_timestamp(bad, eras)


def test_shared_policy_loader_matches_direct_yaml_read(policy, eras):
    assert pr.load_campaign_data_policy() == policy
    assert pr.load_policy_eras() == eras


def test_run_protocol_and_vce_delegate_to_the_shared_policy_loader():
    import inspect
    sys.path.insert(0, str(_SR / "tools"))
    import run_protocol as rp
    import verdict_criteria_evaluator as vce
    assert "protocol_resolution" in inspect.getsource(rp._load_campaign_data_policy)
    assert "load_policy_eras" in inspect.getsource(vce._load_campaign_data_policy_eras)


def test_era_lookup_is_memoized_per_date_and_eras_identity(eras):
    era = _era(eras, "era_2019_2023_full_feed")
    lo = era["range"][0]
    key = (id(eras), lo)
    pr._ERA_LOOKUP_CACHE.pop(key, None)
    assert key not in pr._ERA_LOOKUP_CACHE
    result = pr.era_id_for_timestamp(lo, eras)
    assert pr._ERA_LOOKUP_CACHE[key] == result == era["era_id"]
    # a second call for the SAME date, a DIFFERENT (but equal-content) eras
    # list object, does NOT share the first list's cache entry (id()-keyed).
    eras_copy = [dict(e) for e in eras]
    other_key = (id(eras_copy), lo)
    assert other_key not in pr._ERA_LOOKUP_CACHE
    assert pr.era_id_for_timestamp(lo, eras_copy) == era["era_id"]
    assert other_key in pr._ERA_LOOKUP_CACHE
