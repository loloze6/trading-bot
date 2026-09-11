"""
CUL-272: build_core's real, measured cost-check counterpart
(`post_backtest_cost_check_real`/`post_backtest_route_real`) must (a) leave
every pre-existing field byte-identical, and (b) actually diverge from the
IC-estimated route on cases where real fees and the theoretical IC*sigma*
sqrt(holding) estimate disagree -- proving this isn't just a relabeled copy
of the same number.

Jerome's finding (2026-09-04): cost_check/determine_route (CUL-264) is a
verbatim port of prescreen's own estimate-based logic, appropriate there
because prescreen never executes a real trade. Once a backtest has run, the
real fees (CompletedTrade.total_commission_percent) and real gross edge
(CompletedTrade.profit_loss_percent) already exist a few lines above in
build_core -- re-deriving a theoretical number when a measured one exists is
the same estimate-vs-measurement gap already fixed for IC and turnover.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from reporting.run_artifact import build_core


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


def _varying_series(n=80):
    forecasts = [((-1) ** i) * (5 + i % 5) for i in range(n)]
    closes = [100 + sum(forecasts[:i + 1]) * 0.01 for i in range(n)]
    return forecasts, closes


def _trending_significant_series(n=300, block=5):
    """A forecast series with enough real, persistent (block-run) directional
    content to clear the block-adjusted significance gate -- unlike
    _varying_series (single-bar alternation), which stays insignificant at
    any n_eff this codebase would plausibly compute. Deterministic sign match
    between forecast and the next bar's return by construction."""
    forecasts = [5.0 if (i // block) % 2 == 0 else -5.0 for i in range(n)]
    closes = [100.0]
    for f in forecasts:
        true_ret = 0.001 if f > 0 else -0.001
        closes.append(closes[-1] * (1 + true_ret))
    return forecasts, closes[:n]


def test_real_fields_absent_and_byte_identical_without_trades():
    """No trades -> n == 0 -> every CUL-272 field stays None, and every
    pre-existing field (from CUL-262/264) is untouched. Old 3-positional-arg
    call shape."""
    forecasts, closes = _varying_series()
    bars = _bars(forecasts, closes)
    core = build_core({}, [], bars)

    assert core["real_round_trip_cost_bps"] is None
    assert core["real_gross_edge_bps_per_trade"] is None
    assert core["post_backtest_cost_check_real"] is None
    assert core["post_backtest_route_real"] is None
    assert core["post_backtest_route_real_rationale"] is None
    # Pre-existing fields (CUL-262/264) still behave exactly as their own tests pin
    assert core["post_backtest_route"] is None
    assert core["post_backtest_cost_check"] is None


def test_real_cost_fields_computed_from_completed_trades_directly():
    """real_round_trip_cost_bps/real_gross_edge_bps_per_trade must be the
    trade-averaged CompletedTrade.total_commission_percent/profit_loss_percent,
    converted from percent to bps (x100) -- not re-derived from IC/sigma."""
    forecasts, closes = _varying_series(n=100)
    bars = _bars(forecasts, closes, freq="h")
    trades = [
        _fake_trade(120, total_commission_percent=0.10, profit_loss_percent=0.20),
        _fake_trade(120, total_commission_percent=0.20, profit_loss_percent=0.40),
    ]
    core = build_core({}, trades, bars, candle_interval_seconds=3600, symbol="BTCUSDT")

    assert core["real_round_trip_cost_bps"] == round((0.10 + 0.20) / 2 * 100, 4)
    assert core["real_gross_edge_bps_per_trade"] == round((0.20 + 0.40) / 2 * 100, 4)


def test_real_route_diverges_from_estimated_route_on_real_fee_shock():
    """The headline case: identical forecast/price/holding-period inputs (so
    the estimated route's IC/sigma/holding are unchanged), but real fees are
    far higher than cost_model.yaml's BTCUSDT assumption (2% round-trip vs
    ~0.17%) and the real gross edge is far smaller than the IC-implied
    estimate. The estimated route must NOT already be a hard kill (so there
    is room to diverge), and the real route must be strictly worse --
    demonstrating this is a genuine, not cosmetic, divergence."""
    forecasts, closes = _trending_significant_series(n=300, block=5)
    bars = _bars(forecasts, closes, freq="h")
    trades = [
        _fake_trade(120, total_commission_percent=2.0, profit_loss_percent=0.05)
        for _ in range(40)
    ]

    core = build_core({}, trades, bars, candle_interval_seconds=3600, symbol="BTCUSDT")

    # Significance must actually be real here, or this test proves nothing
    assert core["forecast_return_corr"] is not None and core["forecast_return_corr"] > 0
    assert core["forecast_return_corr_pvalue_block_adjusted"] is not None
    assert core["forecast_return_corr_pvalue_block_adjusted"] < 0.10

    assert core["post_backtest_cost_check"]["pass"] is False
    assert core["post_backtest_cost_check_real"]["pass"] is False
    # Real edge_to_cost_ratio must be far smaller -- real fees are ~12x the
    # cost_model.yaml assumption and real edge is far below the IC estimate
    assert core["post_backtest_cost_check_real"]["edge_to_cost_ratio"] < core["post_backtest_cost_check"]["edge_to_cost_ratio"]
    # The ROUTE, not just the ratio, must actually differ -- estimated reads
    # as a marginal/fixable cost problem, real reads as a structural one
    assert core["post_backtest_route"] == "refine_cost_hurdle"
    assert core["post_backtest_route_real"] == "kill_cost_hurdle"
    assert core["post_backtest_route"] != core["post_backtest_route_real"]


def test_real_cost_check_dict_shape_matches_determine_route_expectations():
    """post_backtest_cost_check_real must use the SAME key names as
    cost_check()'s own return shape (estimated_gross_edge_bps_per_trade,
    cost_bps_per_trade, ...) so determine_route()'s rationale-string lookups
    resolve correctly, despite the values being real, not estimated. A
    'basis': 'real' marker distinguishes it from the estimated dict."""
    forecasts, closes = _trending_significant_series(n=300, block=5)
    bars = _bars(forecasts, closes, freq="h")
    trades = [
        _fake_trade(120, total_commission_percent=2.0, profit_loss_percent=0.05)
        for _ in range(40)
    ]
    core = build_core({}, trades, bars, candle_interval_seconds=3600, symbol="BTCUSDT")

    real = core["post_backtest_cost_check_real"]
    assert set(real.keys()) >= {
        "estimated_gross_edge_bps_per_trade", "cost_bps_per_trade",
        "edge_to_cost_ratio", "safety_factor_required", "pass", "basis",
    }
    assert real["basis"] == "real"
    assert real["estimated_gross_edge_bps_per_trade"] == core["real_gross_edge_bps_per_trade"]
    assert real["cost_bps_per_trade"] == core["real_round_trip_cost_bps"]
    # The rationale string must actually reference the real numbers, not
    # print "N/A" from a key mismatch
    assert "N/A" not in core["post_backtest_route_real_rationale"] or (
        core["real_gross_edge_bps_per_trade"] is None
    )
