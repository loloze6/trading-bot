"""
One-row-per-bar invariant for PortfolioStateTracker / portfolio_states.csv.

DEFECT (found 2026-08-11, fixed 2026-08-15). Two writers record into the same
tracker for the same instant:

  * the per-bar loop, TradingBot._process_symbol_candle_completion, records every
    processed bar exactly once;
  * TradingBot._close_all_positions_at_end, reached unconditionally from stop() at
    the end of every backtest, re-reads the SAME final bar
    (data_manager.get_data_history(symbol) defaults to count=1) and, when a
    position is still open, force-closes it and records again.

PortfolioStateTracker.record_state was a pure append, so a backtest ending with an
open position wrote TWO rows carrying one timestamp -- portfolio state before the
forced close, and after it. Wrong for a time series, and a silent +1 on the bar
count of every consumer that reads the file as one row per bar (performance/
bar_equity.py is the live one).

A backtest ending FLAT is unaffected: _close_all_positions_at_end returns early on
`if not open_positions` and never reaches its record_state call. That is why the
reference window (2024-04-01..2024-05-30, default strategy_config.json) never saw
this -- it ends flat -- and why the fix cannot move any reference baseline.

WHY THIS FILE OWNS NO CACHE GUARD. The sibling regression file
test_close_positions_at_end.py drives the real windows out of local_data and skips
wherever those caches are absent. This one instead replays a synthetic in-memory
series through the real BacktestEngine: engine.historical_data is pre-seeded, so
load_data takes its "data was already loaded" branch and neither the price fetch
nor any aux-feed fetcher is constructed. No network, no caches, deterministic --
and it therefore runs on machines where the Binance caches do not exist, which is
where an invariant this cheap should not go silently unchecked.

The strategy is a config the test owns: a single BuyAndHoldStrategy component under
the `unknown` regime, whose raw value is a constant +10. Forecast +10 -> allocation
+1.0 -> the engine opens a long early and never has a reason to leave it, so the
final bar is guaranteed to hold a position and the forced close is guaranteed to
run. test_fixture_actually_ends_holding_a_position fails loudly if that ever stops
being true, since a flat ending would make the rest of this file vacuous.
"""

import inspect
import json
import math
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SYMBOL = "BTCUSDT"
INTERVAL_SECONDS = 3600
N_BARS = 300

# A component spec needs an explicit `lookback`: ConfigDrivenStrategyEngine derives
# self.lookback from component_effective_lookback, which is 1 for a component
# requiring 0 periods under an identity transform, and forecast() returns 0.0 while
# a history deque holds fewer than 2 values -- a maxlen-1 deque never gets there, so
# without this the fixture would trade nothing and prove nothing.
_ALWAYS_LONG_CONFIG = {
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

# The flat-ending control. PriceEvolutionComponent forecasts trend_pct * scaling,
# so on the constant-price series below it forecasts exactly 0.0 on every bar: no
# position is ever opened and _close_all_positions_at_end takes its
# `if not open_positions: return` early exit -- the reference window's shape.
# (An empty `unknown` regime would be the shorter way to say "never trades" and is
# correctly refused by validator rule V10, so the zero comes from the data instead.)
# Honest limit: this control never trades, where the reference window trades 24
# times and exits by itself. It pins the early-return path, not the exit logic.
_NEVER_TRADES_CONFIG = {
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
                        "id": "price_evo",
                        "class": "strategies.strategy_components.PriceEvolutionComponent",
                        "params": {"period": 20, "scaling_factor": 2.0},
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


def _bars(close) -> pd.DataFrame:
    timestamps = pd.date_range("2024-04-01", periods=len(close), freq="1h")
    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "open": close,
            "high": [c * 1.001 for c in close],
            "low": [c * 0.999 for c in close],
            "close": close,
            "volume": [10.0] * len(close),
        }
    )


def _synthetic_bars() -> pd.DataFrame:
    """A deterministic hourly OHLCV series. Shape is irrelevant to the invariant --
    the constant-forecast strategy above ignores price -- it only has to be long
    enough to clear warmup and cheap enough to replay in a fast test."""
    return _bars([100.0 + 5.0 * math.sin(i / 17.0) + 0.05 * i for i in range(N_BARS)])


def _flat_price_bars() -> pd.DataFrame:
    """Constant close, so PriceEvolutionComponent's trend_pct is exactly 0.0."""
    return _bars([100.0] * N_BARS)


class _Replay:
    """What one synthetic backtest produced."""

    def __init__(self, bars, states, open_positions_at_end, closed_trades):
        self.bars = bars
        self.states = states
        self.open_positions_at_end = open_positions_at_end
        self.closed_trades = closed_trades


def _replay(config: dict, tmp_dir: Path, bars: pd.DataFrame = None) -> _Replay:
    from core.backtester import BacktestEngine
    from core.launcher import DEFAULT_INITIAL_BALANCE, Launcher, TradingParams
    from strategies.main_strategy import AdvancedStrategy

    config_path = tmp_dir / "strategy_config.json"
    config_path.write_text(json.dumps(config))

    launcher = Launcher()
    params = TradingParams(
        symbols=[SYMBOL],
        interval=INTERVAL_SECONDS,
        check_interval=INTERVAL_SECONDS,
        test_mode=True,
    )
    stack = launcher._build_mock_stack(
        params,
        DEFAULT_INITIAL_BALANCE,
        # Never the shared trading-bot/results/trades.json -- conftest.py fails the
        # session on any test that dirties a tracked file under results/.
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

    bars = _synthetic_bars() if bars is None else bars
    # Pre-seeding historical_data makes load_data skip BOTH the price fetch and the
    # aux-feed registration -- the whole `if not self.historical_data` block. Nothing
    # in this test touches the network or local_data.
    engine.historical_data[SYMBOL] = bars
    engine.load_data(start_date="2024-04-01", end_date="2024-04-14", extra_feeds={})
    engine.simulate_on_loaded_data()

    return _Replay(
        bars=bars,
        states=list(stack.portfolio_state_tracker.states),
        open_positions_at_end=sorted(stack.performance_tracker.get_open_positions()),
        closed_trades=list(stack.performance_tracker.completed_trades),
    )


@pytest.fixture(scope="module")
def ends_long(tmp_path_factory):
    return _replay(_ALWAYS_LONG_CONFIG, tmp_path_factory.mktemp("ends_long"))


@pytest.fixture(scope="module")
def ends_flat(tmp_path_factory):
    return _replay(
        _NEVER_TRADES_CONFIG, tmp_path_factory.mktemp("ends_flat"), _flat_price_bars()
    )


# --------------------------------------------------------------------------
# Anti-vacuity: the fixture must reach the forced close
# --------------------------------------------------------------------------


def test_fixture_actually_ends_holding_a_position(ends_long):
    """Without an open position at the last bar, _close_all_positions_at_end returns
    early and every duplicate-row test below passes for the wrong reason."""
    last_bar = ends_long.states[-1]
    assert last_bar["previous_allocation"] != 0.0, (
        "the final bar's pre-close allocation is 0.0, so nothing was force-closed "
        "and this file proves nothing about the duplicate-row defect"
    )
    assert ends_long.closed_trades, "the fixture never traded at all"


def test_fixture_forced_close_actually_executed(ends_long):
    """The recorded final row must be the POST-close one, not the pre-close one."""
    last_bar = ends_long.states[-1]
    assert last_bar["succcess_execute_portfolio_rebalance"] is True, (
        "the forced close did not report success, so the surviving final row is not "
        "the post-close snapshot this fix is about"
    )


# --------------------------------------------------------------------------
# The invariant
# --------------------------------------------------------------------------


def test_one_state_row_per_bar_when_the_run_ends_long(ends_long):
    """The defect's direct signature: 301 rows for 300 bars, the last timestamp twice."""
    recorded = [s["timestamp"] for s in ends_long.states]
    expected = list(ends_long.bars["timestamp"])
    duplicates = sorted({str(ts) for ts in recorded if recorded.count(ts) > 1})
    assert not duplicates, (
        "portfolio_states carries more than one row for the same instant "
        f"{duplicates}; two rows claiming one bar is wrong for a time series and "
        "inflates the bar count for every consumer that reads the file per-bar"
    )
    assert recorded == expected, (
        f"expected exactly one row per replayed bar ({len(expected)}), got "
        f"{len(recorded)}"
    )


def test_surviving_final_row_holds_the_post_close_portfolio_state(ends_long):
    """The single surviving row must be the AFTER-close one.

    Pins the values that actually differ between the two snapshots: the forced close
    flattens the position, so postRebalance_current_allocation is 0.0 while
    previous_allocation still shows what was held going in. Keeping the pre-close row
    instead would leave the file claiming the backtest ended holding a position it
    does not hold.
    """
    last_bar = ends_long.states[-1]
    assert last_bar["postRebalance_current_allocation"] == 0.0, (
        "the surviving row for the final bar records a non-flat post-rebalance "
        f"allocation ({last_bar['postRebalance_current_allocation']!r}) -- it is the "
        "pre-close snapshot, not the post-close one"
    )
    assert last_bar["allocation_change"] == pytest.approx(
        -last_bar["previous_allocation"]
    ), (
        "the surviving row's allocation_change is not the forced close's "
        "0.0 - actual_allocation, so it came from the per-bar loop rather than from "
        "_close_all_positions_at_end"
    )


def test_surviving_final_row_keeps_the_bar_signal_fields(ends_long):
    """The merge, not a blind overwrite.

    _close_all_positions_at_end passes signal={}, so its state dict carries no
    forecast/regime at all. Replacing the per-bar row wholesale would punch a NaN
    hole through the forecast and regime series at the final bar of every affected
    run -- read by build_per_regime, build_dynamic and build_regime_validity. The
    forced close is an end-of-backtest artifact, not a strategy decision, so the
    bar keeps the forecast the strategy actually produced for it.
    """
    last_bar = ends_long.states[-1]
    assert last_bar.get("forecast") == pytest.approx(10.0), (
        "the final bar lost the forecast the strategy produced for it; the "
        "post-close row overwrote it instead of merging onto it"
    )
    assert last_bar.get("regime") == "unknown", "the final bar lost its regime label"


# --------------------------------------------------------------------------
# The default (reference) path must be untouched
# --------------------------------------------------------------------------


def test_run_ending_flat_records_one_row_per_bar_and_never_force_closes(ends_flat):
    """The reference window's shape: no open position, so the close path returns
    early and record_state's new branch is never reached. Row count is one per bar
    for the ordinary reason, not because anything was de-duplicated."""
    assert ends_flat.open_positions_at_end == [], (
        "the never-trades control ended holding a position; it is no longer a "
        "control for the early-return path"
    )
    recorded = [s["timestamp"] for s in ends_flat.states]
    assert recorded == list(ends_flat.bars["timestamp"])


def test_record_state_default_is_still_a_pure_append():
    """The per-bar loop's call is unchanged, byte for byte in behaviour.

    Called without the new flag, record_state must still append unconditionally --
    including for a repeated timestamp. This is the guarantee that no default run's
    portfolio_states.csv can move: the flag defaults to False and the per-bar caller
    does not pass it.
    """
    from execution.portfolio_info import PortfolioStateTracker

    tracker = PortfolioStateTracker.__new__(PortfolioStateTracker)  # no output dir
    tracker.states = []
    bar = pd.DataFrame(
        [{"timestamp": pd.Timestamp("2024-04-01 00:00:00"), "close": 1.0}]
    )

    tracker.record_state(data=bar, marker="first")
    tracker.record_state(data=bar, marker="second")

    assert [s["marker"] for s in tracker.states] == ["first", "second"], (
        "record_state's default behaviour changed: it must remain a pure append"
    )


def test_replace_if_same_bar_appends_when_the_timestamp_differs():
    """The new branch is keyed on the bar, not on 'is there a previous row'.

    Guards the paths that record nothing for the final bar (a warmup-gated bar, or a
    per-bar body that raised before its record_state): there the close's row is the
    bar's FIRST row and must be appended, never folded onto some earlier bar.
    """
    from execution.portfolio_info import PortfolioStateTracker

    tracker = PortfolioStateTracker.__new__(PortfolioStateTracker)
    tracker.states = []
    first = pd.DataFrame(
        [{"timestamp": pd.Timestamp("2024-04-01 00:00:00"), "close": 1.0}]
    )
    second = pd.DataFrame(
        [{"timestamp": pd.Timestamp("2024-04-01 01:00:00"), "close": 2.0}]
    )

    tracker.record_state(data=first, marker="bar_0")
    tracker.record_state(data=second, replace_if_same_bar=True, marker="bar_1")

    assert [s["marker"] for s in tracker.states] == ["bar_0", "bar_1"], (
        "replace_if_same_bar clobbered a row belonging to a DIFFERENT bar"
    )


def test_only_the_close_path_opts_into_replacement():
    """Static call-site guard: the per-bar loop must never pass the flag.

    The whole 'no default run changes' argument rests on this one fact, and it is
    one careless copy-paste away from being false. Cheaper to pin here than to
    rediscover it as a moved baseline.
    """
    from core.trading_bot import TradingBot

    per_bar = inspect.getsource(TradingBot._process_symbol_candle_completion)
    closing = inspect.getsource(TradingBot._close_all_positions_at_end)

    assert "replace_if_same_bar" not in per_bar, (
        "the per-bar candle path now opts into row replacement; it records each bar "
        "exactly once and must stay a pure append, or every prior baseline is void"
    )
    assert "replace_if_same_bar" in closing, (
        "_close_all_positions_at_end no longer opts into row replacement, so the "
        "duplicate final-bar row is back"
    )
