"""
CUL-250: run_backtest()'s fetch_interval_seconds override must reach the
DataManager the engine is actually constructed with -- run_backtest() is the
module-level entry point the research pipeline (run_protocol.py) calls, a
separate path from Launcher.simulate() with its own TradingParams
construction, so it needs its own wiring test (same shape as
test_exchange_selection.py's run_backtest coverage for `exchange`).
"""
import logging
import sys
from pathlib import Path
from typing import ClassVar

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core import launcher as launcher_mod  # noqa: E402

_RUN_BACKTEST_CONFIG = PROJECT_ROOT / "tests" / "fixtures" / "warmup_prefetch_check_config.json"

ABSENT = "<no fetch_interval_seconds argument>"


class _RecordingRunBacktestEngine:
    """Stands in for BacktestEngine inside run_backtest(): records
    construction kwargs (including the real data_manager it was handed),
    touches no data, runs no strategy."""

    kwargs: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        type(self).kwargs = kwargs
        self._last_run_dir = None
        self._symbols = kwargs.get("symbols") or ["BTCUSDT"]
        self.historical_data = {}

    def load_data(self, **kwargs):
        self.historical_data[self._symbols[0]] = pd.DataFrame(
            {"timestamp": [pd.Timestamp("2024-04-01")], "close": [1.0]})

    def simulate_on_loaded_data(self):
        pass


@pytest.fixture
def run_backtest_with(monkeypatch, tmp_path):
    def _run(**kwargs):
        _RecordingRunBacktestEngine.kwargs = {}
        monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingRunBacktestEngine)
        from core.launcher import run_backtest
        run_backtest(
            config_path=str(_RUN_BACKTEST_CONFIG),
            symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
            results_root=str(tmp_path / "results"),
            trades_log_file=str(tmp_path / "trades.json"),
            **kwargs,
        )
        dm = _RecordingRunBacktestEngine.kwargs.get("data_manager")
        return dm.fetch_interval_seconds if dm is not None else ABSENT
    return _run


def test_run_backtest_forwards_an_explicit_fetch_interval(run_backtest_with):
    assert run_backtest_with(interval_seconds=14400, fetch_interval_seconds=3600) == 3600


def test_run_backtest_without_fetch_interval_matches_interval_seconds(run_backtest_with):
    """The real tracked config.json declares no trading.fetch_interval_seconds
    key, so the None -> config-read -> absent -> None -> interval_seconds
    chain must resolve to interval_seconds itself, byte-identical to prior
    behavior."""
    assert run_backtest_with(interval_seconds=14400) == 14400


def test_run_backtest_fetch_interval_validation_still_fails_loud(tmp_path):
    """A bad override (doesn't evenly divide) must still raise from
    DataManager's constructor, not be silently accepted."""
    import logging as _logging

    from core.launcher import run_backtest

    with pytest.raises(ValueError, match="evenly divisible"):
        run_backtest(
            config_path=str(_RUN_BACKTEST_CONFIG),
            symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
            results_root=str(tmp_path / "results"),
            trades_log_file=str(tmp_path / "trades.json"),
            interval_seconds=14400,
            fetch_interval_seconds=1000,
        )
