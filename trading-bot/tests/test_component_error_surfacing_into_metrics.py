"""
E-039 step 5 follow-up (2026-09-12): F5b's component-error counters
(AdvancedStrategy.component_error_count/component_error_samples, 2026-07-04 --
see test_main_strategy_error_surfacing.py for the counting mechanism itself)
have always been computed on every backtest. The only code that ever read them
was prescreen_signal.py's own F5c check (strategy-research), removed along
with the rest of that stage this session. Nothing on the trading-bot side ever
surfaced them into metrics.json, so a real component bug went from "silently
swallowed" (pre-F5b) to "counted but discarded" (post-F5b, pre this fix).

This is NOT a new detector -- generate_signals() already tags its output
regime="ERROR" (an exception was actually caught) vs regime="NOT_READY" (not
ready yet, expected) at the source, and F5b already counts/samples exceptions
on the strategy object. This just wires that existing count through to the
artifact, the same "exists but doesn't flow" shape CUL-263 found and fixed for
metrics.json's data_quality block.

Two tests:
1. Direct contract test on write_metrics_json's new optional key.
2. End-to-end proof: a real BacktestEngine run with a component that always
   throws must produce a metrics.json whose component_errors.count matches
   the number of bars replayed, not a healthy 0.

Uses the same synthetic-bars, no-cache, no-network replay pattern as
test_portfolio_states_one_row_per_bar.py.
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reporting.run_artifact import write_metrics_json
from strategies.strategy_base import SubStrategyComponent

SYMBOL = "BTCUSDT"
INTERVAL_SECONDS = 3600
N_BARS = 20


# ---------------------------------------------------------------------------
# 1. Direct contract test
# ---------------------------------------------------------------------------

def test_write_metrics_json_component_errors_optional_key(tmp_path):
    write_metrics_json(
        tmp_path, core={"sharpe": 1.0}, per_regime={}, forecast_bins={}, dynamic={},
        component_errors={"count": 3, "samples": [{"error_type": "ZeroDivisionError"}]},
    )
    payload = json.loads((tmp_path / "metrics.json").read_text())
    assert payload["component_errors"] == {
        "count": 3, "samples": [{"error_type": "ZeroDivisionError"}]
    }


def test_write_metrics_json_omits_component_errors_when_none(tmp_path):
    """Matches the existing optional-key idiom (regime_validity/bar_equity/
    risk_controls): omitting the argument must not add the key at all."""
    write_metrics_json(tmp_path, core={"sharpe": 1.0}, per_regime={}, forecast_bins={}, dynamic={})
    payload = json.loads((tmp_path / "metrics.json").read_text())
    assert "component_errors" not in payload


# ---------------------------------------------------------------------------
# 2. End-to-end: a real backtest with a broken component
# ---------------------------------------------------------------------------

class _AlwaysThrowsComponent(SubStrategyComponent):
    """Deliberately broken component, standing in for any real component bug
    (F5a's own ZeroDivisionError is fixed and can no longer be used to
    reproduce this directly)."""

    def __init__(self, name="broken", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})

    def update(self, data: pd.DataFrame):
        self.data = data
        raise ZeroDivisionError("simulated component bug")

    def is_ready(self) -> bool:
        return True

    def get_required_periods(self) -> int:
        return 0


_BROKEN_CONFIG = {
    "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
    "strategies": {"warmup": 3, "regimes": {
        "unknown": {"components": [{
            "id": "broken",
            "class": "tests.test_component_error_surfacing_into_metrics._AlwaysThrowsComponent",
            "weight": 1.0, "lookback": 1, "transforms": [{"op": "identity"}], "params": {},
        }]},
        "trending": None, "mean_reversion": None, "chop": None,
    }},
    "aux_feeds": [],
}

_HEALTHY_CONFIG = {
    "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
    "strategies": {"warmup": 3, "regimes": {
        "unknown": {"components": [{
            "id": "price_evo",
            "class": "strategies.strategy_components.PriceEvolutionComponent",
            "weight": 1.0, "lookback": 24, "transforms": [{"op": "identity"}],
            "params": {"period": 5, "scaling_factor": 1.0},
        }]},
        "trending": None, "mean_reversion": None, "chop": None,
    }},
    "aux_feeds": [],
}


def _synthetic_bars(n=N_BARS) -> pd.DataFrame:
    close = [100.0 + 5.0 * math.sin(i / 7.0) for i in range(n)]
    timestamps = pd.date_range("2024-04-01", periods=n, freq="1h")
    return pd.DataFrame({
        "timestamp": timestamps, "open": close,
        "high": [c * 1.001 for c in close], "low": [c * 0.999 for c in close],
        "close": close, "volume": [10.0] * n,
    })


def _run_and_read_metrics(config: dict, tmp_dir: Path) -> dict:
    from core.backtester import BacktestEngine
    from core.launcher import DEFAULT_INITIAL_BALANCE, Launcher, TradingParams
    from strategies.main_strategy import AdvancedStrategy

    config_path = tmp_dir / "strategy_config.json"
    config_path.write_text(json.dumps(config))

    launcher = Launcher()
    params = TradingParams(
        symbols=[SYMBOL], interval=INTERVAL_SECONDS, check_interval=INTERVAL_SECONDS, test_mode=True,
    )
    stack = launcher._build_mock_stack(
        params, DEFAULT_INITIAL_BALANCE,
        trades_log_file=str(tmp_dir / "interim_trades.json"),
    )
    stack.portfolio_state_tracker.output_dir = str(tmp_dir)

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
        price_fetch_interval=INTERVAL_SECONDS,
        candle_interval_seconds=INTERVAL_SECONDS,
        test_mode=True,
        symbols=[SYMBOL],
        initial_capital=DEFAULT_INITIAL_BALANCE,
    )

    bars = _synthetic_bars()
    engine.historical_data[SYMBOL] = bars
    engine.load_data(start_date="2024-04-01", end_date="2024-04-02", extra_feeds={})
    engine.simulate_on_loaded_data()

    run_dir = engine._last_run_dir
    return json.loads((Path(run_dir) / "metrics.json").read_text())


def test_broken_component_error_count_reaches_metrics_json(tmp_path_factory):
    metrics = _run_and_read_metrics(_BROKEN_CONFIG, tmp_path_factory.mktemp("broken"))
    assert "component_errors" in metrics, (
        "metrics.json must carry a component_errors block whenever a real "
        "strategy ran the backtest"
    )
    assert metrics["component_errors"]["count"] == N_BARS, (
        f"every one of the {N_BARS} replayed bars should have thrown and been "
        f"counted, got {metrics['component_errors']}"
    )
    samples = metrics["component_errors"]["samples"]
    assert samples, "a broken run must carry at least one error sample"
    assert samples[0]["error_type"] == "ZeroDivisionError"
    assert "simulated component bug" in samples[0]["error_message"]


def test_healthy_component_reports_zero_count_not_absent(tmp_path_factory):
    """Non-regression: a healthy strategy must report an explicit zero, not a
    false positive, and the key must still be present (not silently dropped
    just because there was nothing to report)."""
    metrics = _run_and_read_metrics(_HEALTHY_CONFIG, tmp_path_factory.mktemp("healthy"))
    assert metrics["component_errors"] == {"count": 0, "samples": []}
