"""
Known-answer tests for prescreen_signal._compute_turnover_proxy (2026-07-07).

The prior sign-flip-only trade counter tracked "last NONZERO sign" across flat
gaps, so it silently merged every long-only (or short-only) signal's separate
active episodes into a SINGLE trade whenever the signal never flipped sign --
flat gaps were invisible to it. Found via the P4_ts_trend SmaTrendLongOnlyComponent
shakedown: it inflated avg_holding_bars from a real ~193-bar estimate to 3058 (the
ENTIRE pooled active-bar count treated as one trade) and the cost ratio to 44.9x.

These fixtures build records with trade counts known BY CONSTRUCTION (not just a
routing outcome) and assert the exact implied_trades_estimated / avg_holding_bars.
"""
import inspect
import sys
from pathlib import Path

import pandas as pd

TOOLS_PATH = Path(__file__).parent.parent / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import prescreen_signal as ps


def _bars(*forecasts):
    return [{"forecast": f, "next_return_bps": 0.0} for f in forecasts]


_STEP = pd.Timedelta(1, unit="h")
_BASE = pd.Timestamp("2020-01-01 00:00:00")


def _bars_ts(forecasts, hole_after=None):
    """Timestamped records at a 1h step. `hole_after` is an index after which a
    2h jump (one missing bar) is inserted, so a data gap falls between that
    record and the next."""
    recs, h = [], 0
    for i, f in enumerate(forecasts):
        recs.append({"forecast": f, "next_return_bps": 0.0,
                     "timestamp": _BASE + pd.Timedelta(h, unit="h")})
        h += 2 if i == hole_after else 1
    return recs


def test_long_only_twelve_round_trips():
    """12 blocks of (5 active, 5 flat) -- exactly 12 discrete long episodes,
    each 5 bars long, never sign-flipping. The old counter would have found
    ZERO sign changes here (long-only never flips sign) and collapsed this to
    implied_trades=1, avg_holding_bars=60 (all 60 active bars as one trade)."""
    forecasts = []
    for _ in range(12):
        forecasts += [10.0] * 5 + [0.0] * 5
    records_by_symbol = {"SYNTH": _bars(*forecasts)}

    result = ps._compute_turnover_proxy(records_by_symbol)

    assert result["active_bars_total"] == 60
    assert result["implied_trades_estimated"] == 12
    assert result["avg_holding_bars"] == 5.0


def test_short_only_flat_gaps_never_flips_sign():
    """Short-only signal (always -10 when active), same flat-gap-blind-spot
    shape as long-only -- the fix must be symmetric, not long-specific."""
    forecasts = []
    for _ in range(7):
        forecasts += [-10.0] * 3 + [0.0] * 4
    records_by_symbol = {"SYNTH": _bars(*forecasts)}

    result = ps._compute_turnover_proxy(records_by_symbol)

    assert result["active_bars_total"] == 21
    assert result["implied_trades_estimated"] == 7
    assert result["avg_holding_bars"] == 3.0


def test_two_sided_signal_with_flat_gaps_and_a_direct_flip():
    """
    long(3) -> flat(2) -> short(4) -> flat(2) -> long(2) -> DIRECT FLIP to
    short(3, no flat bar between) -> flat(1).
    Opens, by construction: flat->long(#1), flat->short(#2), flat->long(#3),
    long->short direct flip(#4, closes the long and opens the short in the
    same bar) = 4 opens. Active bars = 3+4+2+3 = 12. avg_holding = 12/4 = 3.0.
    """
    forecasts = (
        [10.0] * 3 + [0.0] * 2 +
        [-10.0] * 4 + [0.0] * 2 +
        [10.0] * 2 + [-10.0] * 3 +
        [0.0] * 1
    )
    records_by_symbol = {"SYNTH": _bars(*forecasts)}

    result = ps._compute_turnover_proxy(records_by_symbol)

    assert result["active_bars_total"] == 12
    assert result["implied_trades_estimated"] == 4
    assert result["avg_holding_bars"] == 3.0


def test_symbol_boundary_does_not_merge_trailing_and_leading_same_sign_bars():
    """
    Symbol A: 5 active bars (all +10), ending active. Symbol B: 5 active bars
    (all +10), starting active. If the per-symbol reset were missing (pooling
    both into one flat sequence), B's leading +10 bar would read as a
    continuation of A's trailing +10 bar (same sign, no visible transition) --
    underclaiming opens. Must be counted as 2 separate episodes (2 opens),
    since B's bars were never actually contiguous with A's in time.
    """
    records_by_symbol = {
        "SYMBOL_A": _bars(*([10.0] * 5)),
        "SYMBOL_B": _bars(*([10.0] * 5)),
    }

    result = ps._compute_turnover_proxy(records_by_symbol)

    assert result["active_bars_total"] == 10
    assert result["implied_trades_estimated"] == 2
    assert result["avg_holding_bars"] == 5.0


def test_never_active_gives_zero_active_and_fallback_one_trade():
    records_by_symbol = {"SYNTH": _bars(*([0.0] * 10))}

    result = ps._compute_turnover_proxy(records_by_symbol)

    assert result["active_bars_total"] == 0
    assert result["implied_trades_estimated"] == 1  # fallback floor, not 0 (avoid div-by-zero)
    assert result["avg_holding_bars"] == 0.0


# ---------------------------------------------------------------------------
# Gap-awareness (GH#64, CUL-15 D1a). A holding that spans a real data hole is
# closed and reopened instead of read as one continuous trade.
# ---------------------------------------------------------------------------


def test_turnover_proxy_gap_forces_reopen():
    """Same-sign active bars either side of a hole: gap-aware counts two opens
    (the hole closes the first holding), positional counts one."""
    recs = _bars_ts([10.0] * 5 + [10.0] * 5, hole_after=4)  # hole between idx4/idx5
    rbs = {"SYNTH": recs}

    gap_aware = ps._compute_turnover_proxy(rbs, {"SYNTH": _STEP})
    positional = ps._compute_turnover_proxy(rbs, None)

    assert gap_aware["active_bars_total"] == 10
    assert gap_aware["implied_trades_estimated"] == 2
    assert gap_aware["avg_holding_bars"] == 5.0
    # the hole is the only difference: positional reads one continuous holding
    assert positional["implied_trades_estimated"] == 1
    assert positional["avg_holding_bars"] == 10.0


def test_turnover_proxy_no_expected_step_is_byte_identical():
    """Bit-identity gate: with expected_step_by_symbol=None the output on a
    gappy fixture is the pre-gap-aware (positional) result -- the hole is
    invisible, exactly as before the patch."""
    recs = _bars_ts([10.0] * 5 + [10.0] * 5, hole_after=4)
    result = ps._compute_turnover_proxy({"SYNTH": recs}, None)

    assert result["active_bars_total"] == 10
    assert result["implied_trades_estimated"] == 1
    assert result["avg_holding_bars"] == 10.0


def test_turnover_proxy_gapfree_unchanged():
    """On a gap-free fixture (one segment) the result is identical with and
    without expected_step -- gap-awareness only bites on real holes."""
    recs = _bars_ts([10.0] * 3 + [0.0] * 2 + [-10.0] * 4)  # contiguous, no hole
    rbs = {"SYNTH": recs}

    assert (ps._compute_turnover_proxy(rbs, {"SYNTH": _STEP})
            == ps._compute_turnover_proxy(rbs, None))


def test_turnover_proxy_sign_flip_across_gap_is_one_open():
    """A sign flip that also spans a gap contributes exactly one open at the
    boundary (the gap-close and the flip-open coincide on the same bar) -- the
    same count as a same-sign holding spanning the gap, not two."""
    flip = ps._compute_turnover_proxy(
        {"SYNTH": _bars_ts([10.0] * 3 + [-10.0] * 3, hole_after=2)}, {"SYNTH": _STEP})
    same = ps._compute_turnover_proxy(
        {"SYNTH": _bars_ts([10.0] * 3 + [10.0] * 3, hole_after=2)}, {"SYNTH": _STEP})

    assert flip["implied_trades_estimated"] == 2
    assert flip["implied_trades_estimated"] == same["implied_trades_estimated"]


def test_turnover_proxy_wiring_passes_expected_step():
    """PR #65 isolation lesson: guard the production wiring itself. run_prescreen
    must pass expected_step_by_symbol into _compute_turnover_proxy, or the
    gap-awareness silently turns off in production while unit tests stay green."""
    src = inspect.getsource(ps.run_prescreen)
    assert "_compute_turnover_proxy(all_records_by_symbol, expected_step_by_symbol)" in src
