"""
CUL-359: gap rule defects found while reviewing the switch-on-by-default.

  1. A large gap left the symbol flat for the rest of the run (the large tier
     was never cleared) -> it clears after a full warmup of real bars.
  2. The buffer filled gaps of '< ignore_max_bars' while the engine ignored
     '<= ignore_max_bars' -> both use '<='.
  3. An ignore-tier gap cancelled an active middle/large tier -> it no longer
     does; and a middle gap during a large re-warm keeps 'large'.
  4. Gap settings were not part of run identity -> folded when on.
  5. data_quality events carry bars_missing and tier.
  6. gap_policy without gap_detection is refused before any data is fetched.
Plus an end-to-end run on synthetic bars WITH gaps: rule on vs off.
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from strategies.strategy_base import RollingBuffer  # noqa: E402
from tests.test_gap_detection_bit_identical import _make_bot  # noqa: E402

T0 = pd.Timestamp("2024-01-01 00:00:00")
H = pd.Timedelta(hours=1)


def _hours(*offsets):
    return [T0 + h * H for h in offsets]


def _run_bars(bot, n):
    for _ in range(n):
        bot._process_symbol_candle_completion("BTCUSDT")


# ---------------------------------------------------------------------------
# 1. the large tier clears after re-warm
# ---------------------------------------------------------------------------

def test_large_tier_clears_after_a_full_warmup_and_trading_resumes():
    """required_bars=5 (harness). A 10-bar gap is large: forced flat while the
    strategy re-warms, then -- 5 real bars later -- the tier clears and the
    strategy's own target trades again. Before CUL-359 it stayed 'large' and
    every later allocation change was 0."""
    ts = _hours(0, 11, 12, 13, 14, 15, 16, 17)            # gap of 10 missing, then 6 real bars
    bot, tracker = _make_bot(gap_detection=True,
                             gap_policy={"ignore_max_bars": 2, "large_min_bars": 5},
                             timestamps=ts, closes=[100.0] * len(ts))
    _run_bars(bot, len(ts))
    traded = [c["allocation_change"] != 0.0 for c in tracker.calls]
    assert bot._active_gap_tier.get("BTCUSDT") is None
    # bar 0 trades; the gap bar and the next 4 real bars are forced flat
    # (bars_since_gap 0..4 < required_bars=5); the tier clears on the 5th real
    # bar after the gap (bars_since_gap == 5) and the strategy trades again.
    assert traded == [True, False, False, False, False, False, True, True]


# ---------------------------------------------------------------------------
# 3. an ignore gap does not cancel an active tier; severity wins
# ---------------------------------------------------------------------------

def test_middle_tier_clears_on_the_exact_bar():
    """Pins the recovery bar (review F2: '>' or '>= R-1' must fail)."""
    ts = _hours(0, 4, 5, 6, 7, 8, 9, 10)                 # middle (3 missing), then 6 real bars
    bot, tracker = _make_bot(gap_detection=True,
                             gap_policy={"ignore_max_bars": 2, "large_min_bars": 50},
                             timestamps=ts, closes=[100.0] * len(ts))
    _run_bars(bot, len(ts))
    assert [c["allocation_change"] != 0.0 for c in tracker.calls] == [
        True, False, False, False, False, False, True, True]


def test_an_ignore_gap_does_not_cancel_an_active_middle_tier():
    ts = _hours(0, 4, 5, 7)                               # middle (3 missing), normal, ignore (1 missing)
    bot, tracker = _make_bot(gap_detection=True,
                             gap_policy={"ignore_max_bars": 2, "large_min_bars": 50},
                             timestamps=ts, closes=[100.0] * len(ts))
    _run_bars(bot, len(ts))
    assert bot._active_gap_tier.get("BTCUSDT") == "middle"
    assert tracker.calls[-1]["allocation_change"] == 0.0  # the new entry is still blocked
    assert bot._bars_since_gap["BTCUSDT"] == 2            # the ignore bar counted as one real bar


def test_a_middle_gap_during_a_large_rewarm_keeps_large():
    ts = _hours(0, 11, 12, 16)                            # large (10 missing), normal, middle (3 missing)
    bot, _ = _make_bot(gap_detection=True,
                       gap_policy={"ignore_max_bars": 2, "large_min_bars": 5},
                       timestamps=ts, closes=[100.0] * len(ts))
    _run_bars(bot, len(ts))
    assert bot._active_gap_tier.get("BTCUSDT") == "large"
    bot.strategy.reset_history.assert_called_once()      # only the large gap splits the segment
    assert [(e["tier"], e.get("active_tier")) for e in bot.gap_events] == [
        ("large", "large"), ("middle", "large")]


# ---------------------------------------------------------------------------
# 5. events say what each gap did
# ---------------------------------------------------------------------------

def test_events_carry_bars_missing_and_tier():
    ts = _hours(0, 2, 6, 17)                              # ignore (1), middle (3), large (10)
    bot, _ = _make_bot(gap_detection=True,
                       gap_policy={"ignore_max_bars": 2, "large_min_bars": 5},
                       timestamps=ts, closes=[100.0] * len(ts))
    _run_bars(bot, len(ts))
    assert [(e["bars_missing"], e["tier"]) for e in bot.gap_events] == [
        (1, "ignore"), (3, "middle"), (10, "large")]


# ---------------------------------------------------------------------------
# 2. buffer and engine agree at exactly ignore_max_bars
# ---------------------------------------------------------------------------

def _buffer_with_gap(missing, ignore_max_bars=3):
    buf = RollingBuffer(max_size=100, candle_interval_seconds=3600, ignore_max_bars=ignore_max_bars)
    times = [T0 + i * H for i in range(5)] + [T0 + (5 + missing + i) * H for i in range(5)]
    for i, t in enumerate(times):
        buf.add_data({"timestamp": t, "open": 100.0 + i, "high": 100.0 + i, "low": 100.0 + i,
                      "close": 100.0 + i, "volume": 1.0})
    return buf.get_df()


def test_a_gap_of_exactly_ignore_max_bars_is_filled_not_nan():
    df = _buffer_with_gap(missing=3)
    assert len(df) == 13 and df["close"].notna().all()


def test_a_gap_above_ignore_max_bars_leaves_nan_rows():
    df = _buffer_with_gap(missing=4)
    assert len(df) == 14 and int(df["close"].isna().sum()) == 4


# ---------------------------------------------------------------------------
# 6. refused before any data is fetched
# ---------------------------------------------------------------------------

def test_gap_policy_without_gap_detection_is_refused_before_loading(tmp_path):
    from core.launcher import run_backtest
    with pytest.raises(ValueError, match="requires gap_detection=True"):
        run_backtest(config_path=str(tmp_path / "does_not_exist.json"), symbol="BTCUSDT",
                     start="2024-01-01", end="2024-01-02", results_root=str(tmp_path),
                     gap_detection=False, gap_policy={"ignore_max_bars": 2})


# ---------------------------------------------------------------------------
# End to end on synthetic bars WITH gaps (real BacktestEngine, no caches):
# rule on vs off, and run identity (4)
# ---------------------------------------------------------------------------

_CONFIG = {
    "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
    "strategies": {"warmup": 3, "regimes": {
        "unknown": {"components": [{
            "id": "pe", "class": "strategies.strategy_components.PriceEvolutionComponent",
            "weight": 1.0, "lookback": 24, "transforms": [{"op": "identity"}],
            "params": {"period": 5, "scaling_factor": 1.0}}]},
        "trending": None, "mean_reversion": None, "chop": None}},
    "aux_feeds": [],
}


def _gapped_bars():
    """Hourly bars with a 2-bar gap (ignore), a 6-bar gap (middle) and a
    40-bar gap (large, >= the 24-bar warmup floor), then 60 bars -- long
    enough for the real strategy to re-warm and trade again (review F4)."""
    offsets = list(range(0, 30)) + list(range(32, 50)) + list(range(56, 80)) + list(range(120, 180))
    ts = [T0 + h * H for h in offsets]
    close = [100.0 + 5.0 * math.sin(i / 5.0) + 0.05 * i for i in range(len(ts))]
    return pd.DataFrame({"timestamp": ts, "open": close, "high": [c * 1.001 for c in close],
                         "low": [c * 0.999 for c in close], "close": close, "volume": 10.0})


def _run(tmp_dir, **gap_kwargs):
    from core.backtester import BacktestEngine
    from core.launcher import DEFAULT_INITIAL_BALANCE, Launcher, TradingParams
    from strategies.main_strategy import AdvancedStrategy

    cfg = tmp_dir / "strategy_config.json"
    cfg.write_text(json.dumps(_CONFIG))
    launcher = Launcher()
    params = TradingParams(symbols=["BTCUSDT"], interval=3600, check_interval=3600, test_mode=True)
    stack = launcher._build_mock_stack(params, DEFAULT_INITIAL_BALANCE,
                                       trades_log_file=str(tmp_dir / "interim_trades.json"))
    stack.portfolio_state_tracker.output_dir = str(tmp_dir)
    engine = BacktestEngine(
        data_manager=stack.data_manager, strategy=AdvancedStrategy(config_path=str(cfg)),
        execution_handler=stack.execution_handler, logger=launcher.logger,
        portfolio_info=stack.portfolio_info, portfolio_state_tracker=stack.portfolio_state_tracker,
        forecast_manager=stack.forecast_manager, risk_manager=stack.risk_manager,
        performance_tracker=stack.performance_tracker, price_fetch_interval=3600,
        candle_interval_seconds=3600, test_mode=True, symbols=["BTCUSDT"],
        initial_capital=DEFAULT_INITIAL_BALANCE, **gap_kwargs)
    engine.historical_data["BTCUSDT"] = _gapped_bars()
    engine.load_data(start_date="2024-01-01", end_date="2024-01-08", extra_feeds={})
    engine.simulate_on_loaded_data()
    run_dir = Path(engine._last_run_dir)
    states = pd.read_csv(run_dir / "portfolio_states.csv")
    return run_dir, json.loads((run_dir / "metrics.json").read_text()), states


POLICY = {"ignore_max_bars": 3, "on_large_gap": "flatten"}


def test_on_gapped_data_the_rule_acts_and_off_does_not(tmp_path_factory):
    off_dir, off_m, off_states = _run(tmp_path_factory.mktemp("off"))
    on_dir, on_m, on_states = _run(tmp_path_factory.mktemp("on"), gap_detection=True, gap_policy=POLICY)
    assert "data_quality" not in off_m
    tiers = [(e["bars_missing"], e["tier"]) for e in on_m["data_quality"]["events"]]
    assert tiers == [(2, "ignore"), (6, "middle"), (40, "large")]
    assert len(off_states) == len(on_states)
    assert not off_states["allocation_change"].equals(on_states["allocation_change"])
    # 1. after the large gap the real strategy trades again once re-warmed
    after = on_states[pd.to_datetime(on_states["timestamp"]) >= T0 + 150 * H]
    assert (after["allocation_change"].abs() > 0).any()
    # 4. run identity: the two runs no longer share a config hash
    assert off_dir.name.split("_")[-1] != on_dir.name.split("_")[-1]
