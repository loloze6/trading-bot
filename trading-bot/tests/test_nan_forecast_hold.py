"""
CUL-274: a NaN forecast never reaches an order.

Before: forecast NaN -> target NaN -> abs(NaN) != 0.0 is True and every risk
comparison against NaN is False, so a rebalance with an undefined size was
attempted. Policy (operator 2026-10-01): HOLD -- the target becomes the current
allocation, so nothing trades on that bar; the risk gate and the gap tiers still
apply afterwards (a kill switch or a large gap can still force flat). The bar is
still recorded, counted per symbol, sampled, and reported in metrics.json under
"nan_forecast" only when it happened.

Driven through TradingBot._process_symbol_candle_completion over the stub
harness of tests/test_portfolio_risk_gate.py (no engine, no I/O).
"""
import json
import math
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from risk.portfolio_risk_gate import PortfolioRiskGate  # noqa: E402
from reporting.run_artifact import write_metrics_json  # noqa: E402
from tests.test_portfolio_risk_gate import (  # noqa: E402
    _CaptureExec, _FixedPortfolio, _Strategy, _Tracker, _bot, _drive,
)

NAN = float("nan")


def _nan_bot(allocation, gate=None, forecast=NAN):
    execn, tracker = _CaptureExec(success=True), _Tracker()
    bot = _bot(_FixedPortfolio(equity=100.0, allocation=allocation), gate, execn, tracker)
    bot.strategy = _Strategy(forecast=forecast)
    return bot, execn, tracker


@pytest.mark.parametrize("allocation", [0.0, 0.5, -0.8])
def test_a_nan_forecast_holds_the_position_and_never_trades(allocation):
    bot, execn, tracker = _nan_bot(allocation)
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    assert execn.calls == []                                  # no order at all
    assert len(tracker.rows) == 1                             # the bar is still recorded
    assert bot.nan_forecast_bars == {"BTCUSDT": 1}
    assert bot.nan_forecast_samples == [{"symbol": "BTCUSDT", "timestamp": "2024-04-01 00:00:00"}]


def test_nan_bars_are_counted_and_samples_capped():
    bot, execn, _ = _nan_bot(0.5)
    for h in range(25):
        _drive(bot, f"2024-04-01 {h % 24:02d}:00:00" if h < 24 else "2024-04-02 00:00:00", equity=100.0)
    assert bot.nan_forecast_bars == {"BTCUSDT": 25}
    assert len(bot.nan_forecast_samples) == 20
    assert execn.calls == []


def test_a_real_forecast_still_trades_and_counts_nothing():
    bot, execn, _ = _nan_bot(0.0, forecast=10.0)              # wants +1.0 from flat
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    assert len(execn.calls) == 1
    assert bot.nan_forecast_bars == {} and bot.nan_forecast_samples == []


def test_the_kill_switch_still_forces_flat_on_a_nan_bar():
    """Hold is the decision for the strategy's own target only: a latched
    drawdown kill still flattens the position on a NaN bar."""
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    bot, execn, _ = _nan_bot(0.5, gate=gate, forecast=10.0)
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)          # sets the peak
    execn.calls.clear()
    bot.strategy = _Strategy(forecast=NAN)
    _drive(bot, "2024-04-01 01:00:00", equity=70.0)           # 30% drawdown -> kill trips
    assert gate.killed is True
    assert len(execn.calls) == 1 and execn.calls[0]["target_allocation"] == 0.0
    assert bot.nan_forecast_bars == {"BTCUSDT": 1}


def test_a_large_gap_still_forces_flat_on_a_nan_bar():
    bot, execn, _ = _nan_bot(0.5)
    bot._active_gap_tier["BTCUSDT"] = "large"
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    targets = [c["target_allocation"] for c in execn.calls]
    assert targets == [0.0]


# ---------------------------------------------------------------------------
# metrics.json
# ---------------------------------------------------------------------------

def _write(tmp_path, **kw):
    write_metrics_json(tmp_path, {"trade_count": 0}, {}, {}, {}, **kw)
    return json.loads((tmp_path / "metrics.json").read_text())


def test_no_nan_no_key(tmp_path):
    assert "nan_forecast" not in _write(tmp_path)


def test_nan_block_written_when_given(tmp_path):
    block = {"policy": "hold", "bars": 3, "bars_by_symbol": {"BTCUSDT": 3},
             "samples": [{"symbol": "BTCUSDT", "timestamp": "2024-04-01 00:00:00"}]}
    assert _write(tmp_path, nan_forecast=block)["nan_forecast"] == block


def test_backtester_block_from_the_bot_counters():
    """The block BacktestEngine writes, built from the bot's own counters
    after a real NaN bar; None (no key) on a run without one."""
    from core.backtester import nan_forecast_block
    bot, _, _ = _nan_bot(0.5)
    assert nan_forecast_block(bot) is None
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    assert nan_forecast_block(bot) == {
        "policy": "hold", "bars": 1, "bars_by_symbol": {"BTCUSDT": 1},
        "samples": [{"symbol": "BTCUSDT", "timestamp": "2024-04-01 00:00:00"}]}
