"""
A8.6 / prescreen autocorrelation block size: derived, not enumerated.

Guards the bug found by run_060 on 2026-08-27 -- the first real campaign launch
in 39 days, killed `insufficient_power_a_priori` by an arithmetic artifact:

    active_n = 2205
    block 24 (the 1h value, inherited by a silent fallback) -> n_eff  91.9
                                                            -> mde 0.1061 > 0.1 -> KILLED
    block  6 (4h bars per day, correct)                     -> n_eff 367.5
                                                            -> mde 0.0524 < 0.1 -> ADEQUATE

The same bug had already been fixed ONCE, for 1d (2026-07-07, "n_eff off by a
full 24x"). That fix added a table entry and kept a silent default, which
guaranteed the recurrence. Operator ruling 2026-08-27: the fix must cover ANY
timeframe, so nobody meets this again on the next one.

These tests exist so that promise is mechanically enforced rather than
remembered.
"""
import sys
from pathlib import Path

import pytest

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "tools"))
sys.path.insert(0, str(_SR / "workflow"))

from timeframe import bars_per_day, timeframe_seconds  # noqa: E402


# ---------------------------------------------------------------------------
# 1. The derivation reproduces the two values known to be correct.
#    If these ever change, the derivation has changed MEANING, not just form.
# ---------------------------------------------------------------------------

def test_reproduces_the_two_known_good_values():
    assert bars_per_day("1h") == 24, "1h must still be 24 bars/day"
    assert bars_per_day("1d") == 1, "a daily bar is already one episode"


# ---------------------------------------------------------------------------
# 2. Timeframes never used before are correct on FIRST use -- the whole point.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("timeframe,expected", [
    ("4h", 6),      # the run_060 case
    ("30m", 48),
    ("15m", 96),
    ("5m", 288),
    ("1m", 1440),
    ("2h", 12),
    ("12h", 2),
])
def test_covers_timeframes_that_have_never_been_run(timeframe, expected):
    assert bars_per_day(timeframe) == expected


def test_timeframes_of_a_day_or_longer_floor_at_one():
    """A bar spanning >= a day is already at least one independent episode.
    Without the floor, 1w yields 0.14 and the downstream division would INFLATE
    n_eff -- failing in the dangerous direction (wrongly declaring power)."""
    assert bars_per_day("1d") == 1
    assert bars_per_day("1w") == 1


# ---------------------------------------------------------------------------
# 3. Unknown input RAISES. The silent default is the bug's actual mechanism.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", ["banana", "", "h", "1y", "4 hours", None, [], 0, -5])
def test_unparseable_timeframe_raises_rather_than_assuming_1h(bad):
    with pytest.raises(ValueError):
        bars_per_day(bad)


def test_accepts_raw_seconds():
    assert bars_per_day(3600) == 24
    assert timeframe_seconds("4h") == 14400


# ---------------------------------------------------------------------------
# 4. THE MIRROR TEST. Three sites previously held their own copy, kept in sync
#    only by comments saying "both must be updated together" -- and they had
#    ALREADY drifted: the A8.6 gate gave 4h a block of 24 while prescreen_signal
#    gave it 6. Two of those three sites (the A8.6 gate itself, and its
#    standalone power_check.py mirror) were removed entirely 2026-09-11 (E-039:
#    "always backtest", A8.6 dropped) -- their own mirror tests removed with
#    them. prescreen_signal.py's copy is the one still live (used for ITS OWN
#    significance calc, unrelated to A8.6), guarded below.
# ---------------------------------------------------------------------------

def test_prescreen_no_longer_carries_its_own_fallback():
    """prescreen_signal's old `max(_BLOCK_SIZE_1H // 4, 6)` fallback returned 6
    for EVERY non-1h/1d timeframe -- right for 4h by coincidence, but 8x too
    small for 30m and 48x for 5m, inflating n_eff toward false significance."""
    src = (_SR / "tools" / "prescreen_signal.py").read_text(encoding="utf-8")
    assert "block_size = bars_per_day(timeframe)" in src, "must use the shared derivation"
    assert "block_size = max(_BLOCK_SIZE_1H // 4, 6)" not in src, "the guessed fallback must be gone"


# ---------------------------------------------------------------------------
# 5. The reported bug itself, end to end, with run_060's real numbers.
# ---------------------------------------------------------------------------

def test_run_060_case_is_power_adequate_not_killed(tmp_path):
    import math
    active_n = 0.125 * 8820 * 2
    assert active_n == 2205

    n_eff_wrong = active_n / 24
    mde_wrong = 1.0 / math.sqrt(max(n_eff_wrong - 3.0, 1.0))
    assert mde_wrong > 0.1, "the old block DID kill it -- this is the bug being guarded"

    n_eff_right = active_n / bars_per_day("4h")
    mde_right = 1.0 / math.sqrt(max(n_eff_right - 3.0, 1.0))
    assert round(n_eff_right, 1) == 367.5
    assert round(mde_right, 4) == 0.0524
    assert mde_right < 0.1, "on correct arithmetic the hypothesis is adequately powered"
