"""
Fast guard tests for model_funding (fix/funding-accrual-wiring). No caches, no network.

Covers the two fail-loud contracts that do not need a real backtest run:
  * BacktestEngine rejects model_funding on sub-daily bars -- the daily-summed funding
    series would multiple-charge each intraday bar and charge settlements not yet
    occurred at the bar's decision time (look-ahead);
  * simulate_on_loaded_data refuses to run with model_funding on but no daily funding
    series for a symbol, rather than silently reporting a fee-only run as funding-costed.
"""

import json
import logging
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _engine(**kwargs):
    from core.backtester import BacktestEngine

    return BacktestEngine(
        logger=logging.getLogger("test_model_funding_guard"), **kwargs
    )


# --- interval guard ---


def test_engine_rejects_model_funding_on_intraday_bars():
    """model_funding on with a sub-daily interval must raise at construction -- the
    guard that keeps the daily-summed funding series off intraday bars."""
    with pytest.raises(ValueError, match="model_funding"):
        _engine(model_funding=True, candle_interval_seconds=3600)


def test_engine_accepts_model_funding_on_daily_bars():
    """The same flag on daily bars (86400) constructs cleanly and records the flag."""
    engine = _engine(model_funding=True, candle_interval_seconds=86400)
    assert engine.model_funding is True


def test_run_backtest_rejects_model_funding_on_default_intraday_config(tmp_path):
    """run_backtest(model_funding=True) without a daily interval override resolves to the
    default 1h config and must raise at engine construction, before any data fetch."""
    from core.launcher import run_backtest

    with pytest.raises(ValueError, match="model_funding"):
        run_backtest(
            config_path=str(PROJECT_ROOT / "strategy_config.json"),
            symbol="BTCUSDT",
            start="2024-04-01",
            end="2024-04-02",
            results_root=str(tmp_path),
            trades_log_file=str(tmp_path / "interim_trades.json"),
            model_funding=True,
        )


# --- missing-series fail-loud (synthetic, no caches) ---

# A config the test owns: one BuyAndHoldStrategy component under `unknown`, no aux
# feeds, so load_data's V1 feed check passes with extra_feeds={} and neither a cache
# nor the network is touched (precedent: test_portfolio_states_one_row_per_bar.py).
_NO_FEED_CONFIG = {
    "regime_detector": {
        "mode": "threshold_rules",
        "components": [],
        "rules": [],
        "default_regime": "unknown",
    },
    "strategies": {
        "warmup": 51,
        "regimes": {
            "unknown": {
                "components": [
                    {
                        "id": "bh",
                        "class": "strategies.strategy_components.BuyAndHoldStrategy",
                        "params": {},
                        "weight": 1.0,
                        "lookback": 24,
                        "transforms": [{"op": "identity"}],
                    }
                ]
            },
            "trending": None,
            "mean_reversion": None,
            "chop": None,
        },
    },
    "aux_feeds": [],
}

FAKE_SYMBOL = "FAKEUSDT"


def _daily_bars(n: int = 200) -> pd.DataFrame:
    ts = pd.date_range("2024-01-01", periods=n, freq="1D")
    close = [100.0 + i for i in range(n)]
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": close,
            "high": [c * 1.001 for c in close],
            "low": [c * 0.999 for c in close],
            "close": close,
            "volume": [10.0] * n,
        }
    )


def test_model_funding_missing_series_fails_loud(tmp_path):
    """model_funding on for a symbol with no {symbol}_funding_8h.csv must raise, naming
    the symbol -- a silent empty series would report fee-only economics as funding-
    costed. Uses a synthetic fake symbol so no real funding cache can satisfy it, and
    raises in simulate_on_loaded_data before the bot is even built."""
    from core.backtester import BacktestEngine
    from core.launcher import DEFAULT_INITIAL_BALANCE, Launcher, TradingParams
    from strategies.main_strategy import AdvancedStrategy

    config_path = tmp_path / "strategy_config.json"
    config_path.write_text(json.dumps(_NO_FEED_CONFIG))

    launcher = Launcher()
    params = TradingParams(
        symbols=[FAKE_SYMBOL], interval=86400, check_interval=86400, test_mode=True
    )
    stack = launcher._build_mock_stack(
        params,
        DEFAULT_INITIAL_BALANCE,
        trades_log_file=str(tmp_path / "interim_trades.json"),
    )
    stack.portfolio_state_tracker.output_dir = str(tmp_path)

    engine = BacktestEngine(
        data_manager=stack.data_manager,
        strategy=AdvancedStrategy(config_path=str(config_path)),
        execution_handler=stack.execution_handler,
        logger=launcher.logger,
        portfolio_info=stack.portfolio_info,
        portfolio_state_tracker=stack.portfolio_state_tracker,
        forecast_manager=stack.forecast_manager,
        risk_manager=stack.risk_manager,
        performance_tracker=stack.performance_tracker,
        price_fetch_interval=86400,
        candle_interval_seconds=86400,
        test_mode=True,
        symbols=[FAKE_SYMBOL],
        initial_capital=DEFAULT_INITIAL_BALANCE,
        model_funding=True,
    )
    engine.historical_data[FAKE_SYMBOL] = _daily_bars()
    engine.load_data(start_date="2024-01-01", end_date="2024-01-14", extra_feeds={})

    with pytest.raises(ValueError, match=FAKE_SYMBOL):
        engine.simulate_on_loaded_data()
