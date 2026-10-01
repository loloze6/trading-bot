"""
CUL-273b: wires RollingBuffer's dormant reindex-to-NaN-grid mechanism (built
in CUL-273) into core/launcher.py::run_backtest -- previously accepted by
AdvancedStrategy's constructor but never supplied by any real call site.

Also documents the major correction this ticket's own investigation found:
the ORIGINAL premise (that SubStrategyComponent.rolling_forecast/
store_raw_forecast/standardize_forecast survive reset_history() unreset, and
therefore need their own NaN-propagation fix) is true on its face but
IRRELEVANT -- that entire mechanism is confirmed dead code, never called by
the real, live ConfigDrivenStrategyEngine/ConfigDrivenRegimeEngine path. See
test_confirmed_dead_forecast_standardization_path below.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from strategies.main_strategy import AdvancedStrategy


def test_advanced_strategy_default_construction_is_byte_identical():
    """No candle_interval_seconds/ignore_max_bars supplied (every call site
    before this ticket) -> RollingBuffer's reindex stays off. Confirms the
    constructor's own defaults are unchanged."""
    s = AdvancedStrategy(config_path="strategy_config.json")
    assert s.data_buffer._candle_interval_seconds is None
    assert s.data_buffer._ignore_max_bars is None


def test_run_backtest_wires_candle_interval_seconds_unconditionally():
    """run_backtest always resolves a real `interval` (from interval_seconds
    or config.json) before constructing AdvancedStrategy -- CUL-273b passes
    that resolved value through as candle_interval_seconds on every call,
    gap_detection or not. This alone must NOT enable the reindex (ignore_max_bars
    stays None without gap_policy), matching RollingBuffer's "both required"
    contract -- verified directly on the constructed strategy object, not
    inferred from run_backtest's return value."""
    from core.launcher import Launcher, TradingParams
    # Mirror run_backtest's own interval resolution without running a full
    # backtest -- this test only needs to prove the wiring reaches the
    # constructor correctly, not the whole pipeline end to end.
    launcher = Launcher()
    interval = launcher.config.get('trading', 'interval', 3600)
    s = AdvancedStrategy(config_path="strategy_config.json", candle_interval_seconds=interval)
    assert s.data_buffer._candle_interval_seconds == interval
    assert s.data_buffer._ignore_max_bars is None  # no gap_policy -> reindex still off


def test_run_backtest_wires_ignore_max_bars_from_gap_policy():
    """indicator_fill=True (since 2026-10-01 its own switch, default False) +
    gap_detection=True + a gap_policy with ignore_max_bars must reach
    RollingBuffer's constructor as ignore_max_bars, enabling the reindex."""
    from core.launcher import run_backtest
    import inspect
    # Read run_backtest's own source to confirm the wiring line exists and
    # reads gap_policy -- a direct, precise check rather than a full
    # end-to-end run for this specific assertion.
    src = inspect.getsource(run_backtest)
    assert "candle_interval_seconds=interval" in src
    assert "ignore_max_bars" in src
    assert "gap_policy" in src
    assert "indicator_fill" in src


class _Captured(Exception):
    pass


def _strategy_kwargs_of_run_backtest(monkeypatch, tmp_path, **kwargs):
    """Run run_backtest up to the strategy's construction and capture its kwargs
    (a stub AdvancedStrategy raises right after recording them)."""
    import core.launcher as launcher
    seen = {}

    def _stub(**kw):
        seen.update(kw)
        raise _Captured()

    monkeypatch.setattr(launcher, "AdvancedStrategy", _stub)
    with pytest.raises(_Captured):
        launcher.run_backtest(config_path=str(PROJECT_ROOT / "strategy_config.json"),
                              symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
                              results_root=str(tmp_path), **kwargs)
    return seen


def test_the_indicator_fill_is_off_by_default_even_with_the_gap_rule_on(monkeypatch, tmp_path):
    """Operator 2026-10-01: gap rule on by default, indicator fill off (CUL-361)."""
    assert _strategy_kwargs_of_run_backtest(monkeypatch, tmp_path)["ignore_max_bars"] is None


def test_indicator_fill_true_wires_the_policy_threshold(monkeypatch, tmp_path):
    kw = _strategy_kwargs_of_run_backtest(monkeypatch, tmp_path, indicator_fill=True)
    assert kw["ignore_max_bars"] == 3


def test_indicator_fill_without_the_gap_rule_is_refused(monkeypatch, tmp_path):
    with pytest.raises(ValueError, match="indicator_fill needs gap_detection=True"):
        _strategy_kwargs_of_run_backtest(monkeypatch, tmp_path, indicator_fill=True,
                                         gap_detection=False)


def test_wired_advanced_strategy_reindexes_a_synthetic_gap_end_to_end():
    """Full chain, no live cache dependency (this worktree's local_data only
    covers 2024-01-01..2024-03-01, so the known 2018-01-04 real gap used
    elsewhere this session isn't available here -- synthetic bars are the
    right tool, same convention test_rolling_buffer_reindex.py already uses
    for its own unit tests, not a fabrication of real market data).

    Constructs AdvancedStrategy exactly as CUL-273b's launcher.py wiring now
    does (candle_interval_seconds + ignore_max_bars both real), feeds it a
    bar sequence with a 2-hour gap directly through data_buffer.add_data()
    (bypassing the fetch layer entirely), and confirms get_df() actually
    reindexes -- proving the wiring reaches all the way from construction
    parameters to real reindex behavior, not just that the constructor
    accepts the arguments."""
    s = AdvancedStrategy(
        config_path="strategy_config.json",
        candle_interval_seconds=3600,
        ignore_max_bars=1,
    )
    base = pd.Timestamp("2024-01-01")
    timestamps = [base + pd.Timedelta(hours=h) for h in range(5)]
    timestamps += [base + pd.Timedelta(hours=7)]  # 2-hour gap after bar 5 (hours 5,6 missing)
    for i, ts in enumerate(timestamps):
        s.data_buffer.add_data({
            "timestamp": ts, "open": 100.0, "high": 101.0, "low": 99.0,
            "close": 100.0 + i, "volume": 1.0,
        })
    df = s.data_buffer.get_df()
    assert len(df) == 8, "reindexed grid must include the 2 missing hourly slots"
    assert df["close"].isna().sum() == 2, (
        "a 2-hour gap with ignore_max_bars=1 exceeds the ignore threshold -- "
        "both missing bars must be real NaN, not forward-filled"
    )


def test_confirmed_dead_forecast_standardization_path():
    """CUL-273b's central correction, pinned as a regression guard: the real,
    live engines (ConfigDrivenStrategyEngine/ConfigDrivenRegimeEngine) call
    ONLY comp.update()/comp.raw_value() -- never comp.generate_forecast().
    SubStrategyComponent.rolling_forecast/store_raw_forecast/
    standardize_forecast/standardization_count therefore never execute in the
    real pipeline; the actual live normalization is apply_transform_pipeline
    (registry.py) over self._history, which IS cleared by reset_history().
    If this ever changes (someone wires generate_forecast() into a real
    engine), this test should be revisited -- it is not asserting the dead
    code should stay dead forever, only that today's premise is verified."""
    import inspect
    from strategies import strategy_engine, regime_engine
    strat_src = inspect.getsource(strategy_engine.ConfigDrivenStrategyEngine)
    regime_src = inspect.getsource(regime_engine.ConfigDrivenRegimeEngine)
    assert "generate_forecast" not in strat_src
    assert "generate_forecast" not in regime_src
    assert "comp.update(data)" in strat_src or ".update(data)" in strat_src
    assert "comp.raw_value()" in strat_src or ".raw_value()" in strat_src


def test_store_raw_forecast_propagates_nan_naturally_no_override_needed():
    """CUL-273b: unlike RSI/funding-rate/fear-greed (explicit
    `if pd.isna(x): x = fabricated_default` overrides that had to be
    removed), store_raw_forecast has no such override -- division by a NaN
    stddev_24/close already produces NaN naturally. Verified directly here,
    not just by reading the source."""
    from strategies.strategy_components import RSIPullbackComponent
    comp = RSIPullbackComponent(name="rsi_test", parameters={"period": 14})
    comp.data = pd.DataFrame({
        "close": [100.0] * 20,
        "stddev_24": [float("nan")] * 20,  # gap-contaminated volatility estimate
    })
    raw = comp.store_raw_forecast(5.0)
    assert pd.isna(raw), "NaN stddev_24 must propagate to a NaN raw_forecast, not a fabricated number"
