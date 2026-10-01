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


# ---------------------------------------------------------------------------
# Review additions
# ---------------------------------------------------------------------------

def test_the_recorded_row_on_a_nan_bar():
    bot, _, tracker = _nan_bot(0.5)
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    row = tracker.rows[0]
    assert math.isnan(row["signal"].forecast)                 # the strategy's NaN, kept
    assert row["allocation_change"] == 0.0
    assert row["approved_rebalance"] is None
    assert row["previous_allocation"] == 0.5


def test_a_cap_only_gate_no_longer_crashes_on_a_nan_bar():
    """Before CUL-274 PortfolioRiskGate.apply raised on a NaN target, so the bar
    was dropped (no row). Now the held target is within the cap: no trade, the
    row is recorded, and the raw target says NaN, not the held allocation."""
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    bot, execn, tracker = _nan_bot(0.5, gate=gate)
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    assert execn.calls == [] and len(tracker.rows) == 1
    assert math.isnan(tracker.rows[0]["risk_target_raw"])


def test_the_cap_still_trims_a_drifted_position_on_a_nan_bar():
    """A held position above the cap is trimmed, exactly as on any held bar:
    the risk control still applies (documented policy, not the strategy's
    trade). The recorded raw target is NaN."""
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 0.5}})
    bot, execn, tracker = _nan_bot(0.8, gate=gate)
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    assert [(c["target_allocation"], c["allocation_change"]) for c in execn.calls] == [
        (0.5, pytest.approx(-0.3))]
    assert math.isnan(tracker.rows[0]["risk_target_raw"])
    assert bot.nan_forecast_bars == {"BTCUSDT": 1}


@pytest.mark.parametrize("forecast", [float("inf"), float("-inf")])
def test_an_infinite_forecast_is_held_like_nan(forecast):
    bot, execn, _ = _nan_bot(0.5, forecast=forecast)
    _drive(bot, "2024-04-01 00:00:00", equity=100.0)
    assert execn.calls == [] and bot.nan_forecast_bars == {"BTCUSDT": 1}


# ---------------------------------------------------------------------------
# End to end through BacktestEngine: a component that always reports NaN
# (the real engine, synthetic bars, no caches) -- proves the backtester wires
# the block into metrics.json and that a healthy run has no key.
# ---------------------------------------------------------------------------

from strategies.strategy_base import SubStrategyComponent  # noqa: E402


class _AlwaysNaNComponent(SubStrategyComponent):
    def __init__(self, name="always_nan", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = float("nan")

    def update(self, data):
        self.data = data
        self._raw_value = float("nan")

    def is_ready(self):
        return True

    def get_required_periods(self):
        return 0


def _config(cls_path):
    return {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                            "default_regime": "unknown"},
        "strategies": {"warmup": 3, "regimes": {
            "unknown": {"components": [{
                "id": "c", "class": cls_path, "weight": 1.0, "lookback": 24,
                "transforms": [{"op": "identity"}], "params": {}}]},
            "trending": None, "mean_reversion": None, "chop": None}},
        "aux_feeds": [],
    }


def test_a_nan_strategy_backtest_reports_the_block_and_never_trades(tmp_path_factory, monkeypatch):
    """60 bars: the strategy is ready after 24 (AdvancedStrategy's floor), so
    its NaN forecasts reach the guard on the bars after that."""
    import tests.test_component_error_surfacing_into_metrics as harness
    original = harness._synthetic_bars
    monkeypatch.setattr(harness, "_synthetic_bars", lambda n=60: original(60))
    from tests.test_component_error_surfacing_into_metrics import _run_and_read_metrics
    metrics = _run_and_read_metrics(_config("tests.test_nan_forecast_hold._AlwaysNaNComponent"),
                                    tmp_path_factory.mktemp("nan"))
    block = metrics["nan_forecast"]
    assert block["policy"] == "hold" and block["bars"] > 0
    assert block["bars_by_symbol"] == {"BTCUSDT": block["bars"]}
    assert metrics["core"]["trade_count"] == 0


def test_a_healthy_backtest_has_no_nan_block(tmp_path_factory):
    from tests.test_component_error_surfacing_into_metrics import _HEALTHY_CONFIG, _run_and_read_metrics
    metrics = _run_and_read_metrics(_HEALTHY_CONFIG, tmp_path_factory.mktemp("healthy"))
    assert "nan_forecast" not in metrics
