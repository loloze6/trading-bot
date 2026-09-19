"""
CUL-264 follow-up: minimum-observations safeguard for the post-backtest
go/no-go gate (`performance/signal_statistics.py::determine_route`).

Problem this closes (verified directly in the code before this test was
written): `determine_route()` classified purely from a p-value and a cost
ratio, with no check anywhere for whether there were even enough
observations to trust the test computing them. A hypothesis that failed
because it had almost no data got the exact same label as one that failed
on an abundant sample -- "we don't know yet" and "we now know it doesn't
work" were indistinguishable. This file proves the fix: a new
`inconclusive_insufficient_data` route, checked first, before the old
significance/cost math runs at all, keyed on two DIFFERENT quantities for
the two DIFFERENT call sites:

  - the estimated path (CUL-264) keys on `n_eff`, the block-adjusted
    effective sample size;
  - the real path (CUL-272) keys on `n_trades`, the completed-trade count.

Both floors default to 5 (`_MIN_N_EFF_FOR_ROUTE`/`_MIN_TRADES_FOR_ROUTE` in
signal_statistics.py) -- see that module's own comment for the reasoning
(n_eff's floor is derived from the z-test's own `dof = max(n_eff - 3, 1)`
clamp; the trade-count floor is a separate, more conservative
floor-of-floors). Both are PROPOSED DEFAULTS pending explicit sign-off, not
settled numbers -- these tests pin behavior AT the chosen defaults, not the
specific numbers as immutable facts.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from performance.signal_statistics import (
    determine_route, _MIN_N_EFF_FOR_ROUTE, _MIN_TRADES_FOR_ROUTE,
)
from reporting.run_artifact import build_core


# ---------------------------------------------------------------------------
# Unit-level tests directly against determine_route -- fast, isolate the
# safeguard itself from build_core's data-shaping around it.
# ---------------------------------------------------------------------------

# A cost dict that would pass the cost hurdle outright if the significance/
# cost math were reached -- used so a positive, significant IC falls through
# to `proceed_to_interpretation` when the new safeguard does NOT fire, making
# "did NOT route to inconclusive" unambiguous in these tests.
_PASSING_COST = {
    "estimated_gross_edge_bps_per_trade": 100.0,
    "cost_bps_per_trade":                 10.0,
    "edge_to_cost_ratio":                 10.0,
    "safety_factor_required":             2.0,
    "pass":                               True,
}


def test_n_eff_just_below_floor_routes_inconclusive():
    below = _MIN_N_EFF_FOR_ROUTE - 1
    route, rationale = determine_route(0.5, 0.001, _PASSING_COST, n_eff=below)
    assert route == "inconclusive_insufficient_data"
    assert f"n_eff={below}" in rationale
    assert f"min_n_eff={_MIN_N_EFF_FOR_ROUTE}" in rationale


def test_n_eff_at_floor_does_not_route_inconclusive():
    route, _ = determine_route(0.5, 0.001, _PASSING_COST, n_eff=_MIN_N_EFF_FOR_ROUTE)
    assert route != "inconclusive_insufficient_data"
    assert route == "proceed_to_interpretation"


def test_n_eff_just_above_floor_does_not_route_inconclusive():
    above = _MIN_N_EFF_FOR_ROUTE + 1
    route, _ = determine_route(0.5, 0.001, _PASSING_COST, n_eff=above)
    assert route == "proceed_to_interpretation"


def test_n_trades_just_below_floor_routes_inconclusive():
    below = _MIN_TRADES_FOR_ROUTE - 1
    route, rationale = determine_route(0.5, 0.001, _PASSING_COST, n_trades=below)
    assert route == "inconclusive_insufficient_data"
    assert f"n_trades={below}" in rationale
    assert f"min_n_trades={_MIN_TRADES_FOR_ROUTE}" in rationale


def test_n_trades_at_floor_does_not_route_inconclusive():
    route, _ = determine_route(0.5, 0.001, _PASSING_COST, n_trades=_MIN_TRADES_FOR_ROUTE)
    assert route == "proceed_to_interpretation"


def test_n_trades_just_above_floor_does_not_route_inconclusive():
    above = _MIN_TRADES_FOR_ROUTE + 1
    route, _ = determine_route(0.5, 0.001, _PASSING_COST, n_trades=above)
    assert route == "proceed_to_interpretation"


def test_placeholder_sigma_routes_inconclusive_even_with_abundant_n_eff():
    """The propagation requirement: a cost check resting on a placeholder
    sigma must route to inconclusive regardless of how large n_eff is --
    sigma_bar_bps_is_placeholder is an independent insufficiency reason, not
    subsumed by the sample-size checks."""
    route, rationale = determine_route(
        0.5, 0.001, _PASSING_COST,
        n_eff=_MIN_N_EFF_FOR_ROUTE * 100, sigma_is_placeholder=True,
    )
    assert route == "inconclusive_insufficient_data"
    assert "placeholder" in rationale.lower()


def test_omitting_sample_size_args_preserves_pre_existing_3_arg_call_shape():
    """The old callers (before this safeguard existed) invoked
    determine_route(pooled_ic, p_value, cost) with no sample-size
    information at all. That must keep working exactly as before -- the
    safeguard is opt-in via the new keyword args, not silently mandatory."""
    route, _ = determine_route(0.5, 0.001, _PASSING_COST)
    assert route == "proceed_to_interpretation"


def test_insufficient_data_route_never_collapses_into_a_kill_route():
    """Distinctness: the SAME ic/p-value pair must classify differently
    depending purely on whether the sample size backing it is trustworthy --
    proving inconclusive_insufficient_data is a genuinely separate label,
    not a relabeling of kill_no_ic under a different name."""
    ic, p = 0.02, 0.5  # not significant either way
    too_few, _ = determine_route(ic, p, _PASSING_COST, n_eff=1)
    plenty, _ = determine_route(ic, p, _PASSING_COST, n_eff=50)
    assert too_few == "inconclusive_insufficient_data"
    assert plenty == "kill_no_ic"
    assert too_few != plenty


def test_kill_no_ic_unaffected_when_sample_adequate():
    cost = {**_PASSING_COST, "pass": False, "edge_to_cost_ratio": None,
            "estimated_gross_edge_bps_per_trade": None}
    route, _ = determine_route(0.02, 0.5, cost, n_eff=50, n_trades=50)
    assert route == "kill_no_ic"


def test_refine_inverted_ic_unaffected_when_sample_adequate():
    route, _ = determine_route(-0.5, 0.001, _PASSING_COST, n_eff=50, n_trades=50)
    assert route == "refine_inverted_ic"


def test_kill_cost_hurdle_unaffected_when_sample_adequate():
    failing_cost = {
        "estimated_gross_edge_bps_per_trade": 1.0,
        "cost_bps_per_trade":                 10.0,
        "edge_to_cost_ratio":                 0.1,
        "safety_factor_required":             2.0,
        "pass":                               False,
    }
    # p=0.08 is significant (< _SIG_THRESHOLD=0.10) AND marginal (> 0.05),
    # landing in the "structural cost barrier" branch rather than kill_no_ic.
    route, _ = determine_route(0.5, 0.08, failing_cost, n_eff=50, n_trades=50)
    assert route == "kill_cost_hurdle"


def test_proceed_to_interpretation_unaffected_when_sample_adequate():
    route, _ = determine_route(0.5, 0.001, _PASSING_COST, n_eff=50, n_trades=50)
    assert route == "proceed_to_interpretation"


# ---------------------------------------------------------------------------
# Integration-level tests through build_core -- prove the two call sites in
# reporting/run_artifact.py actually thread n_eff/n_trades/sigma-placeholder
# through, not just that determine_route supports the arguments in isolation.
# ---------------------------------------------------------------------------

def _bars(forecasts, closes, freq="h", start="2020-01-01"):
    return pd.DataFrame({
        "timestamp": pd.date_range(start, periods=len(forecasts), freq=freq),
        "forecast": forecasts,
        "close": closes,
    })


def _fake_trade(duration_minutes, net_pnl=1.0, gross_pnl=1.5, commission=0.5,
                 total_commission_percent=0.05, profit_loss_percent=1.5):
    return SimpleNamespace(
        net_profit_loss_absolute=net_pnl,
        profit_loss_absolute=gross_pnl,
        total_commission=commission,
        duration_minutes=duration_minutes,
        total_commission_percent=total_commission_percent,
        profit_loss_percent=profit_loss_percent,
    )


def _varying_series(n):
    """Single-bar-alternation series (same shape as the other build_core test
    files' _varying_series) -- forecast never lines up persistently with the
    next bar's return, so its significance is purely a function of how much
    data (n_eff) is fed in. Used here only to control n_eff via n; the actual
    IC/p-value values are read back from build_core's own output rather than
    assumed, matching this repo's "verify claims by execution" rule."""
    forecasts = [((-1) ** i) * (5 + i % 5) for i in range(n)]
    closes = [100 + sum(forecasts[:i + 1]) * 0.01 for i in range(n)]
    return forecasts, closes


def _trending_significant_series(n=300, block=5):
    """Persistent, block-run directional content -- clears the block-adjusted
    significance gate at a small n_eff, so this shape isolates the REAL
    path's trade-count floor from the estimated path's n_eff floor (n_eff
    stays comfortably adequate throughout while trade count varies)."""
    forecasts = [5.0 if (i // block) % 2 == 0 else -5.0 for i in range(n)]
    closes = [100.0]
    for f in forecasts:
        true_ret = 0.001 if f > 0 else -0.001
        closes.append(closes[-1] * (1 + true_ret))
    return forecasts, closes[:n]


def test_build_core_estimated_path_routes_inconclusive_below_n_eff_floor():
    """n=120 measured to give n_eff=4 (< the 5 floor) for this exact series
    shape/block size (86400 // 3600 = 24-bar blocks) -- verified directly
    against gap_aware_active_block_count before writing this assertion, not
    assumed from the arithmetic alone."""
    forecasts, closes = _varying_series(n=120)
    bars = _bars(forecasts, closes)
    trades = [_fake_trade(120) for _ in range(40)]

    core = build_core({}, trades, bars, candle_interval_seconds=3600, symbol="BTCUSDT")

    assert core["forecast_return_corr_n_eff"] == 4
    assert core["post_backtest_route"] == "inconclusive_insufficient_data"
    assert "n_eff=4" in core["post_backtest_route_rationale"]


def test_build_core_estimated_path_unaffected_at_and_above_n_eff_floor():
    """n=121 -> n_eff=5 (at the floor) and n=145 -> n_eff=6 (just above) must
    both proceed to a REAL classification, not inconclusive -- and, since
    p crosses the 0.10 significance threshold between them, the two must
    differ from each other too (kill_no_ic vs refine_inverted_ic), proving
    this isn't just a second frozen label."""
    trades = [_fake_trade(120) for _ in range(40)]

    forecasts_at, closes_at = _varying_series(n=121)
    core_at = build_core(
        {}, trades, _bars(forecasts_at, closes_at),
        candle_interval_seconds=3600, symbol="BTCUSDT",
    )
    assert core_at["forecast_return_corr_n_eff"] == 5
    assert core_at["post_backtest_route"] not in (None, "inconclusive_insufficient_data")

    forecasts_above, closes_above = _varying_series(n=145)
    core_above = build_core(
        {}, trades, _bars(forecasts_above, closes_above),
        candle_interval_seconds=3600, symbol="BTCUSDT",
    )
    assert core_above["forecast_return_corr_n_eff"] == 6
    assert core_above["post_backtest_route"] not in (None, "inconclusive_insufficient_data")

    assert core_at["post_backtest_route"] != core_above["post_backtest_route"]


def test_build_core_real_path_routes_inconclusive_below_trade_floor():
    """4 completed trades (< the 5-trade floor) on a series with abundant
    n_eff (measured 12 for this fixture) must still route the REAL path to
    inconclusive -- proving the trade-count check applies independently of
    an adequate n_eff, and that it targets post_backtest_route_real
    specifically, not the estimated post_backtest_route."""
    forecasts, closes = _trending_significant_series(n=300, block=5)
    bars = _bars(forecasts, closes)
    trades = [_fake_trade(120) for _ in range(4)]

    core = build_core({}, trades, bars, candle_interval_seconds=3600, symbol="BTCUSDT")

    assert core["forecast_return_corr_n_eff"] is not None
    assert core["forecast_return_corr_n_eff"] >= _MIN_N_EFF_FOR_ROUTE
    assert core["post_backtest_route_real"] == "inconclusive_insufficient_data"
    assert "n_trades=4" in core["post_backtest_route_real_rationale"]
    # The estimated route must NOT be affected by a trade-count shortfall --
    # trade count is exclusively a real-path quantity.
    assert core["post_backtest_route"] != "inconclusive_insufficient_data"


def test_build_core_real_path_unaffected_at_and_above_trade_floor():
    """5 and 6 completed trades (at, and just above, the floor) on the same
    abundant-n_eff series must both reach a real classification -- and,
    since fees/edge are unchanged from the below-floor case above, both
    should agree with each other (proceed_to_interpretation), isolating the
    trade-count floor as the only thing that changed."""
    forecasts, closes = _trending_significant_series(n=300, block=5)
    bars = _bars(forecasts, closes)

    trades_at = [_fake_trade(120) for _ in range(5)]
    core_at = build_core({}, trades_at, bars, candle_interval_seconds=3600, symbol="BTCUSDT")
    assert core_at["post_backtest_route_real"] == "proceed_to_interpretation"

    trades_above = [_fake_trade(120) for _ in range(6)]
    core_above = build_core({}, trades_above, bars, candle_interval_seconds=3600, symbol="BTCUSDT")
    assert core_above["post_backtest_route_real"] == "proceed_to_interpretation"


def test_build_core_real_path_below_floor_does_not_disturb_estimated_route_value():
    """Byte-identity-adjacent check: the estimated post_backtest_route must
    be EXACTLY the same whether or not the real path's trade count clears
    its own floor -- the two floors are wired independently, not coupled
    through a shared code path that could leak one into the other."""
    forecasts, closes = _trending_significant_series(n=300, block=5)
    bars = _bars(forecasts, closes)

    core_below = build_core(
        {}, [_fake_trade(120) for _ in range(4)], bars,
        candle_interval_seconds=3600, symbol="BTCUSDT",
    )
    core_above = build_core(
        {}, [_fake_trade(120) for _ in range(6)], bars,
        candle_interval_seconds=3600, symbol="BTCUSDT",
    )
    assert core_below["post_backtest_route"] == core_above["post_backtest_route"]
    assert core_below["post_backtest_cost_check"] == core_above["post_backtest_cost_check"]
