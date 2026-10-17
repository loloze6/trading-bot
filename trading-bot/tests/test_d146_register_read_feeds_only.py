"""
D-146: the backtester registers only the feeds the strategy reads.

Before: BacktestEngine.load_data registered EVERY feed in extra_feeds (the launcher
passes the whole FEED_REGISTRY: funding_rate and fear_greed) and used the strategy's
required_feeds only to refuse a MISSING feed. An unread feed was fetched, merged and
written to bars.csv, and the analyst's list_columns offered it.

After: with a strategy, a feed outside required_feeds is not registered (no factory
call, no fetch, no column). With no strategy the old behaviour is kept -- the
strategy-less aux-feed tests rely on it.

Pins:
  (i)   results are identical (a) when an unread feed is merely offered on the menu
        vs none offered, and (b) when an unread feed is really registered on the
        DataManager (as load_data did before D-146) vs not registered -- (b) is the
        test that can see an unread column leak into results; (a) holds with or
        without the fix;
  (ii)  a required feed that is missing still raises FeedRequirementError;
  (iii) with a strategy, registration, manifest feeds.registered and the bars.csv
        columns carry only the read feeds, and the unread feed's factory is never
        called;
  (iv)  with no strategy, every feed in extra_feeds is registered, as before.

No network and no local_data: the price fetch is replaced on the engine's own
DataManager instance and the feeds are in-memory stubs.
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

from core.backtester import BacktestEngine, FeedRequirementError  # noqa: E402

SYMBOL = "BTCUSDT"
INTERVAL_SECONDS = 3600
N_BARS = 300
START = pd.Timestamp("2024-04-01")
AUX = ("fear_greed", "funding_rate")


# --------------------------------------------------------------------------
# Strategy configs (the test owns them; one reads fear_greed, one reads nothing)
# --------------------------------------------------------------------------

def _config(component_id, cls, params):
    return {
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
                            "id": component_id,
                            "class": cls,
                            "params": params,
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


# Reads no feed. Trades: the price series below swings, so the forecast changes sign.
_PRICE_ONLY = _config(
    "price_evo", "strategies.strategy_components.PriceEvolutionComponent",
    {"period": 20, "scaling_factor": 2.0},
)
# Reads fear_greed only (consumes_feeds == ("fear_greed",)).
_READS_FEAR_GREED = _config(
    "fg", "strategies.strategy_components.FearGreedComponent", {},
)


# --------------------------------------------------------------------------
# Synthetic data + stub feeds
# --------------------------------------------------------------------------

def _bars() -> pd.DataFrame:
    close = [100.0 + 8.0 * math.sin(i / 11.0) + 0.05 * i for i in range(N_BARS)]
    return pd.DataFrame({
        "timestamp": pd.date_range(START, periods=N_BARS, freq="1h"),
        "open": close,
        "high": [c * 1.001 for c in close],
        "low": [c * 0.999 for c in close],
        "close": close,
        "volume": [10.0] * N_BARS,
    })


class _StubFetcher:
    exchange_id = "binance"

    def __init__(self, df):
        self._df = df

    def get_data(self, symbol=None):
        return self._df

    def cache_key(self, symbol):
        return "stub"


def _fear_greed_df() -> pd.DataFrame:
    days = pd.date_range(START - pd.Timedelta(days=3), periods=20, freq="D")
    return pd.DataFrame({"timestamp": days, "fear_greed": [10.0 + 4.0 * i for i in range(len(days))]})


def _funding_df() -> pd.DataFrame:
    prints = pd.date_range(START - pd.Timedelta(days=1), periods=60, freq="8h")
    return pd.DataFrame({"timestamp": prints, "funding_rate": [0.0001 * ((i % 5) - 2) for i in range(len(prints))]})


class _FactoryLog:
    """The extra_feeds menu handed to load_data; records which factories were called."""

    def __init__(self):
        self.called = []
        frames = self.frames = {"fear_greed": _fear_greed_df(), "funding_rate": _funding_df()}

        def make(name):
            def factory(symbols, start, end, data_dir, exchange="binance", **kw):
                self.called.append(name)
                return _StubFetcher(frames[name])
            return factory

        self.menu = {name: make(name) for name in AUX}


# --------------------------------------------------------------------------
# A real end-to-end replay (real DataManager, strategy, risk, artifacts)
# --------------------------------------------------------------------------

class _Run:
    def __init__(self, run_dir, engine, factories):
        self.run_dir = Path(run_dir)
        self.engine = engine
        self.factories = factories
        self.manifest = json.loads((self.run_dir / "manifest.json").read_text())
        self.bars = pd.read_csv(self.run_dir / "bars.csv")
        self.states = pd.read_csv(self.run_dir / "portfolio_states.csv")
        self.states_columns = list(self.states.columns)
        self.trades_text = (self.run_dir / "trades.json").read_text()
        self.metrics = json.loads((self.run_dir / "metrics.json").read_text())
        self.completed = list(engine.performance_tracker.completed_trades)


def _replay(config, tmp_dir: Path, menu_names, drop_feeds=(), preregister=()) -> _Run:
    """`preregister` names stub feeds registered directly on the engine's DataManager
    before load_data, with the real FEED_* declarations -- exactly what load_data did
    for every feed in extra_feeds before D-146. It is how a test puts an UNREAD feed
    into the run (the menu path no longer can)."""
    from core.launcher import DEFAULT_INITIAL_BALANCE, Launcher, TradingParams
    from data.feed_registry import FEED_AGG, FEED_DELAY_SECONDS, FEED_FILL, FEED_WINDOW_SECONDS
    from strategies.main_strategy import AdvancedStrategy

    config_path = tmp_dir / "strategy_config.json"
    config_path.write_text(json.dumps(config))

    launcher = Launcher()
    params = TradingParams(
        symbols=[SYMBOL], interval=INTERVAL_SECONDS, check_interval=INTERVAL_SECONDS,
        test_mode=True,
    )
    stack = launcher._build_mock_stack(
        params, DEFAULT_INITIAL_BALANCE,
        trades_log_file=str(tmp_dir / "interim_trades.json"),
    )
    stack.portfolio_state_tracker.output_dir = str(tmp_dir / "results")
    bars = _bars()
    # No network: the price fetch is replaced on this engine's own DataManager.
    stack.data_manager.fetch_historical_data = (
        lambda symbol, start_date, end_date, exchange="binance", **kw: bars.copy()
    )

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
        # non-None drop_feeds is what makes the manifest carry its "feeds" block
        drop_feeds=list(drop_feeds),
    )
    factories = _FactoryLog()
    for name in preregister:
        engine.data_manager.register_feed(
            name=name,
            fetcher=_StubFetcher(factories.frames[name]),
            window_seconds=FEED_WINDOW_SECONDS[name],
            agg=FEED_AGG[name],
            fill=FEED_FILL[name],
            delay_seconds=FEED_DELAY_SECONDS[name],
            required=False,
        )
    engine.load_data(
        start_date="2024-04-01", end_date="2024-04-14",
        extra_feeds={n: factories.menu[n] for n in menu_names},
    )
    engine.simulate_on_loaded_data()
    return _Run(engine._last_run_dir, engine, factories)


def _non_aux(df: pd.DataFrame) -> pd.DataFrame:
    return df[[c for c in df.columns if c not in AUX]]


@pytest.fixture(scope="module")
def price_only_with_unread_feeds(tmp_path_factory):
    return _replay(_PRICE_ONLY, tmp_path_factory.mktemp("price_unread"), AUX)


@pytest.fixture(scope="module")
def price_only_no_feeds(tmp_path_factory):
    return _replay(_PRICE_ONLY, tmp_path_factory.mktemp("price_none"), ())


@pytest.fixture(scope="module")
def reads_fear_greed_with_both(tmp_path_factory):
    return _replay(_READS_FEAR_GREED, tmp_path_factory.mktemp("fg_both"), AUX)


@pytest.fixture(scope="module")
def reads_fear_greed_only_feed(tmp_path_factory):
    return _replay(_READS_FEAR_GREED, tmp_path_factory.mktemp("fg_only"), ("fear_greed",))


@pytest.fixture(scope="module")
def price_only_with_registered_unread_feeds(tmp_path_factory):
    """Both feeds REALLY registered on the DataManager (pre-D-146 load_data behaviour),
    for a strategy that reads neither."""
    return _replay(_PRICE_ONLY, tmp_path_factory.mktemp("price_prereg"), (), preregister=AUX)


@pytest.fixture(scope="module")
def reads_fear_greed_with_registered_unread_funding(tmp_path_factory):
    """fear_greed read and registered through the menu; funding_rate (unread) really
    registered on the DataManager."""
    return _replay(_READS_FEAR_GREED, tmp_path_factory.mktemp("fg_prereg"),
                   ("fear_greed",), preregister=("funding_rate",))


# --------------------------------------------------------------------------
# (i-a) a menu offering an unread feed equals a menu offering none
#       (holds with or without the fix: under the fix neither run registers it;
#       the registered-feed tests in (i-b) are the ones that can see a leak)
# --------------------------------------------------------------------------

def test_fixture_trades(price_only_no_feeds):
    """Anti-vacuity: the comparison below is over a run that actually traded."""
    assert len(price_only_no_feeds.completed) >= 2
    assert len(price_only_no_feeds.bars) > 100


def test_run_with_unread_feeds_offered_on_the_menu_equals_run_with_none_offered_trades(
        price_only_with_unread_feeds, price_only_no_feeds):
    a, b = price_only_with_unread_feeds, price_only_no_feeds
    assert a.trades_text == b.trades_text
    assert len(a.completed) == len(b.completed)


def test_run_with_unread_feeds_offered_on_the_menu_equals_run_with_none_offered_metrics(
        price_only_with_unread_feeds, price_only_no_feeds):
    assert price_only_with_unread_feeds.metrics == price_only_no_feeds.metrics


def test_run_with_unread_feeds_offered_on_the_menu_equals_run_with_none_offered_bars(
        price_only_with_unread_feeds, price_only_no_feeds):
    a, b = price_only_with_unread_feeds.bars, price_only_no_feeds.bars
    pd.testing.assert_frame_equal(_non_aux(a), _non_aux(b))
    # and the whole file, aux columns included: under the fix nothing unread is written
    pd.testing.assert_frame_equal(a, b)


def test_a_strategy_that_reads_fear_greed_sees_the_same_with_the_unread_funding_feed_offered_or_not(
        reads_fear_greed_with_both, reads_fear_greed_only_feed):
    """The read feed is untouched by dropping its unread neighbour from the menu."""
    a, b = reads_fear_greed_with_both, reads_fear_greed_only_feed
    assert a.trades_text == b.trades_text
    assert a.metrics == b.metrics
    pd.testing.assert_frame_equal(a.bars, b.bars)
    assert a.bars["fear_greed"].notna().any(), "fixture: the read feed must actually carry values"


# --------------------------------------------------------------------------
# (i-b) an unread feed REALLY registered does not move the results
#       (the test that can fail: the aux column is present in the registered run)
# --------------------------------------------------------------------------

def test_registered_unread_feeds_really_put_their_columns_in_the_run(
        price_only_with_registered_unread_feeds, reads_fear_greed_with_registered_unread_funding):
    """Anti-vacuity: the registered runs below do carry the unread aux columns."""
    run = price_only_with_registered_unread_feeds
    assert sorted(run.engine.data_manager._aux_feeds) == ["fear_greed", "funding_rate"]
    for name in AUX:
        assert name in run.bars.columns and run.bars[name].notna().any()
        assert name in run.states_columns and run.states[name].notna().any()
    run = reads_fear_greed_with_registered_unread_funding
    assert sorted(run.engine.data_manager._aux_feeds) == ["fear_greed", "funding_rate"]
    assert "funding_rate" in run.bars.columns and run.bars["funding_rate"].notna().any()
    assert "funding_rate" in run.states_columns and run.states["funding_rate"].notna().any()


def test_price_only_strategy_ignores_registered_unread_feeds(
        price_only_with_registered_unread_feeds, price_only_no_feeds):
    a, b = price_only_with_registered_unread_feeds, price_only_no_feeds
    assert a.trades_text == b.trades_text
    assert len(a.completed) == len(b.completed) >= 2
    assert a.metrics == b.metrics
    pd.testing.assert_frame_equal(_non_aux(a.bars), _non_aux(b.bars))
    pd.testing.assert_frame_equal(_non_aux(a.states), _non_aux(b.states))


def test_fear_greed_strategy_ignores_a_registered_unread_funding_feed(
        reads_fear_greed_with_registered_unread_funding, reads_fear_greed_only_feed):
    a, b = reads_fear_greed_with_registered_unread_funding, reads_fear_greed_only_feed
    assert a.trades_text == b.trades_text
    assert a.metrics == b.metrics
    pd.testing.assert_frame_equal(a.bars.drop(columns=["funding_rate"]), b.bars)
    pd.testing.assert_frame_equal(a.states.drop(columns=["funding_rate"]), b.states)
    assert a.bars["fear_greed"].notna().any(), "fixture: the read feed must actually carry values"


# --------------------------------------------------------------------------
# (iii) what is registered and what lands on disk
# --------------------------------------------------------------------------

def test_registered_feeds_are_only_the_read_ones(reads_fear_greed_with_both):
    run = reads_fear_greed_with_both
    assert sorted(run.engine.data_manager._aux_feeds) == ["fear_greed"]
    assert run.manifest["feeds"] == {
        "registered": ["fear_greed"], "dropped": [], "required": ["fear_greed"],
    }


def test_unread_feed_is_never_constructed_or_fetched(reads_fear_greed_with_both):
    assert reads_fear_greed_with_both.factories.called == ["fear_greed"]


def test_bars_csv_carries_only_the_read_aux_column(reads_fear_greed_with_both):
    run = reads_fear_greed_with_both
    for cols in (list(run.bars.columns), run.states_columns):   # bars.csv, portfolio_states.csv
        assert "fear_greed" in cols
        assert "funding_rate" not in cols


def test_strategy_reading_no_feed_registers_none(price_only_with_unread_feeds):
    run = price_only_with_unread_feeds
    assert sorted(run.engine.data_manager._aux_feeds) == []
    assert run.manifest["feeds"] == {"registered": [], "dropped": [], "required": []}
    assert run.factories.called == []
    assert not set(run.bars.columns) & set(AUX)
    assert not set(run.states_columns) & set(AUX)


# --------------------------------------------------------------------------
# (ii) a required feed that is missing still raises
# --------------------------------------------------------------------------

def test_required_feed_missing_still_raises(tmp_path):
    # fear_greed is required; the menu holds only the unread funding_rate
    with pytest.raises(FeedRequirementError) as exc_info:
        _replay(_READS_FEAR_GREED, tmp_path, ("funding_rate",))
    assert "fear_greed" in str(exc_info.value)


def test_required_feed_missing_from_an_empty_menu_still_raises(tmp_path):
    with pytest.raises(FeedRequirementError):
        _replay(_READS_FEAR_GREED, tmp_path, ())


# --------------------------------------------------------------------------
# Registration seen from the DataManager, with the stub engine used by the
# neighbouring aux-feed tests (no strategy / a strategy stub)
# --------------------------------------------------------------------------

class _StubStrategy:
    def __init__(self, required):
        self._required = required

    @property
    def required_feeds(self):
        return self._required


class _RecordingDataManager:
    def __init__(self):
        self.historical_data = {}
        self._aux_feeds = {}
        self.required_flags = {}

    def fetch_historical_data(self, symbol, start_date, end_date, exchange="binance"):
        return pd.DataFrame({"timestamp": [pd.Timestamp("2022-01-01")], "close": [1.0]})

    def register_feed(self, name, fetcher, window_seconds, agg, required=False, fill="none",
                      delay_seconds=0.0):
        self._aux_feeds[name] = fetcher
        self.required_flags[name] = required

    def initialize(self):
        pass


def _factory(symbols, start, end, data_dir, exchange="binance"):
    return object()


def _load(strategy, menu):
    import logging

    dm = _RecordingDataManager()
    kwargs = {} if strategy is None else {"strategy": strategy}
    engine = BacktestEngine(data_manager=dm, logger=logging.getLogger("test_d146"),
                            symbols=["BTCUSD"], **kwargs)
    engine.load_data(start_date="2022-01-01", end_date="2022-01-02", extra_feeds=menu)
    return dm


def test_with_a_strategy_only_required_feeds_are_registered_and_flagged_required():
    dm = _load(_StubStrategy({"fear_greed": ("c",)}),
               {"fear_greed": _factory, "funding_rate": _factory})
    assert sorted(dm._aux_feeds) == ["fear_greed"]
    assert dm.required_flags == {"fear_greed": True}


def test_with_a_strategy_that_requires_nothing_nothing_is_registered():
    dm = _load(_StubStrategy({}), {"fear_greed": _factory, "funding_rate": _factory})
    assert dm._aux_feeds == {}


# --------------------------------------------------------------------------
# (iv) no strategy: today's behaviour, pinned
# --------------------------------------------------------------------------

def test_without_a_strategy_every_feed_in_extra_feeds_is_registered_unrequired():
    dm = _load(None, {"fear_greed": _factory, "funding_rate": _factory})
    assert sorted(dm._aux_feeds) == ["fear_greed", "funding_rate"]
    assert dm.required_flags == {"fear_greed": False, "funding_rate": False}


def test_without_a_strategy_an_empty_menu_registers_nothing():
    assert _load(None, {})._aux_feeds == {}
    assert _load(None, None)._aux_feeds == {}
