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

import sys
from pathlib import Path

TOOLS_PATH = Path(__file__).parent.parent / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import prescreen_signal as ps


def _bars(*forecasts):
    return [{"forecast": f, "next_return_bps": 0.0} for f in forecasts]


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
    forecasts = [10.0] * 3 + [0.0] * 2 + [-10.0] * 4 + [0.0] * 2 + [10.0] * 2 + [-10.0] * 3 + [0.0] * 1
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
