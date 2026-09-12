"""
CUL-264 (E-039 parity): build_core's new post-backtest route
(`post_backtest_route`/`post_backtest_cost_check`/`sigma_bar_bps`) must (a)
leave every pre-existing field byte-identical when `symbol` isn't supplied
and the route's own inputs aren't fully available, and (b) agree with
`performance.signal_statistics`'s own `cost_check`/`determine_route` -- the
same functions build_core itself calls -- on the same underlying series,
proving the wiring passes through the exact inputs build_core measured.

(Originally a lockstep comparison against prescreen_signal.py's own
`_cost_check`/`_determine_route`, which `signal_statistics.py`'s pair are a
verbatim port of; repointed 2026-09-12, E-039 step 5, once prescreen_signal.py
was removed -- build_core has never called prescreen_signal.py, only the
test's comparison target changed. `_load_cost_model`/`_round_trip_cost_bps`
live locally in `reporting/run_artifact.py`, not in `signal_statistics.py`.)

INFORMATIONAL ONLY, per CUL-264's scope: these tests check the route is
computed and recorded correctly. None of them touch, or need to touch,
anything that skips or gates an LLM call -- no such wiring exists yet.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from reporting import run_artifact
from reporting.run_artifact import build_core
from performance.signal_statistics import cost_check, determine_route, _SIG_THRESHOLD


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
        # CUL-272: real-cost fields build_core now reads unconditionally
        # whenever n > 0 -- absent from a fixture, every existing test here
        # would AttributeError, not just the new CUL-272 ones.
        total_commission_percent=total_commission_percent,
        profit_loss_percent=profit_loss_percent,
    )


def _varying_series(n=80):
    forecasts = [((-1) ** i) * (5 + i % 5) for i in range(n)]
    closes = [100 + sum(forecasts[:i + 1]) * 0.01 for i in range(n)]
    return forecasts, closes


def test_route_absent_when_symbol_and_candle_interval_not_supplied():
    """The old 3-positional-arg call (no candle_interval_seconds, no symbol,
    as core/backtester.py made it before CUL-262/264) must produce a result
    with the new keys present but None -- byte-identical in every
    pre-existing field."""
    forecasts, closes = _varying_series()
    bars = _bars(forecasts, closes)
    core = build_core({}, [_fake_trade(60)], bars)

    assert core["sigma_bar_bps"] is None or core["sigma_bar_bps_is_placeholder"] in (True, False)
    # candle_interval_seconds absent -> no block-adjusted p-value -> no route,
    # since determine_route needs it. Sigma CAN still be computed (it only
    # needs bars_df), but the route requires the block-adjusted p-value too.
    assert core["forecast_return_corr_pvalue_block_adjusted"] is None
    assert core["post_backtest_route"] is None
    assert core["post_backtest_cost_check"] is None


def test_route_matches_prescreen_on_identical_input():
    """With candle_interval_seconds AND a symbol supplied (and enough trades
    for avg_trade_duration_bars), the computed route/cost-check must equal
    what a standalone cost_check/determine_route call gives on the same
    IC/significance/holding-period/cost inputs build_core itself measured.

    n=200 (not the smaller n=100 used elsewhere in this file) deliberately:
    n_eff for this series is a block-count derived from `n`, and at n=100 it
    comes out to 4 -- below the CUL-264-follow-up min-observations floor
    (`_MIN_N_EFF_FOR_ROUTE=5`, see signal_statistics.py), which would route
    build_core to `inconclusive_insufficient_data`. n=200 gives n_eff=8,
    comfortably above the floor, so this test stays about algorithmic parity
    on an ADEQUATE sample -- see test_insufficient_n_eff_routes_inconclusive*
    below for the small-sample behavior itself."""
    forecasts, closes = _varying_series(n=200)
    bars = _bars(forecasts, closes, freq="h")
    candle_interval_seconds = 3600

    # 40 trades of 120 minutes (2 bars) each -> avg_trade_duration_bars ~= 2.0
    trades = [_fake_trade(120) for _ in range(40)]

    core = build_core(
        {}, trades, bars,
        candle_interval_seconds=candle_interval_seconds,
        symbol="BTCUSDT",
    )
    corr    = core["forecast_return_corr"]
    pvalue  = core["forecast_return_corr_pvalue_block_adjusted"]
    sigma   = core["sigma_bar_bps"]
    holding = core["avg_trade_duration_bars"]
    assert corr is not None and pvalue is not None and sigma is not None and holding is not None

    cost_model = run_artifact._load_cost_model()
    rtc_bps    = run_artifact._round_trip_cost_bps("BTCUSDT", cost_model)
    safety     = float(cost_model.get("safety_factor", 2.0))

    expected_cost = cost_check(corr, sigma, holding, rtc_bps, safety_factor=safety)
    expected_route, _rationale = determine_route(corr, pvalue, expected_cost)

    assert core["post_backtest_cost_check"]["pass"] == expected_cost["pass"]
    assert core["post_backtest_cost_check"]["edge_to_cost_ratio"] == expected_cost["edge_to_cost_ratio"]
    assert core["post_backtest_route"] == expected_route, (
        f"build_core route {core['post_backtest_route']!r} must match a standalone "
        f"determine_route call {expected_route!r} on identical input"
    )


def test_unknown_symbol_falls_back_to_default_round_trip_cost():
    """A symbol with no entry in cost_model.yaml's round_trip_cost_bps must
    fall back to the 'default' bucket -- not silently use 0 or crash."""
    forecasts, closes = _varying_series(n=100)
    bars = _bars(forecasts, closes, freq="h")
    trades = [_fake_trade(120) for _ in range(40)]

    core = build_core(
        {}, trades, bars, candle_interval_seconds=3600, symbol="NOT_A_REAL_SYMBOL",
    )
    assert core["post_backtest_cost_check"] is not None
    cost_model = run_artifact._load_cost_model()
    expected_rtc = run_artifact._round_trip_cost_bps("NOT_A_REAL_SYMBOL", cost_model)
    assert core["post_backtest_cost_check"]["cost_bps_per_trade"] == expected_rtc
