"""
Feed-dependency safety, Step 1/3 (`.omc/plans/feed-dependency-safety-architecture.md`):
declarations + V1 (registration guard).

Pins:
  - `SubStrategyComponent.consumes_feeds` defaults to `()`; the three real aux-feed
    consumers (`FundingRateMeanReversionComponent`, `FearGreedContrarianComponent`,
    `WhaleLargeTradeImbalanceComponent`) declare exactly the columns they read.
  - `required_feeds()` on both engines, and merged on `AdvancedStrategy`, over a
    MIXED config (a funding-consuming regime-detector component + a fear_greed-
    consuming strategy component) -- feed name -> sorted tuple of consumer names.
  - V1: `BacktestEngine.load_data` raises `FeedRequirementError` naming the feed
    and its consuming components when a required feed is missing from
    `extra_feeds`, and passes when it is present.
  - Drift tripwire: every class in `strategy_components.py` that references a
    known feed-column name (real code, not docstring prose) declares it in
    `consumes_feeds`. Static source scan, not runtime machinery.

The strategy-less-engine exemption (self.strategy is None -> required_feeds={})
needs no new test here: five existing call sites already drive
`BacktestEngine.load_data` with no strategy (tests/test_aux_feed_venue.py,
tests/test_exchange_selection.py) and are its regression coverage.
"""
import ast
import inspect
import json
import logging
import socket
import sys
import tempfile
from pathlib import Path
from typing import ClassVar

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from _cache_guard import cache_skip_reason  # noqa: E402
from core import launcher as launcher_mod  # noqa: E402
from core.backtester import BacktestEngine, FeedRequirementError  # noqa: E402
from data.data_manager import DataManager  # noqa: E402
from data.feed_registry import FEED_REGISTRY, WHALE_FOOTPRINT_FEEDS  # noqa: E402
from strategies import strategy_components as sc_module  # noqa: E402
from strategies.main_strategy import AdvancedStrategy  # noqa: E402
from strategies.regime_engine import ConfigDrivenRegimeEngine  # noqa: E402
from strategies.strategy_base import SubStrategyComponent  # noqa: E402
from strategies.strategy_components import (  # noqa: E402
    WHALE_ATTESTED_COLUMN,
    WHALE_LT_IMBALANCE_COLUMN,
    FearGreedContrarianComponent,
    FundingRateMeanReversionComponent,
    PriceEvolutionComponent,
    WhaleLargeTradeImbalanceComponent,
)
from strategies.strategy_engine import ConfigDrivenStrategyEngine  # noqa: E402

TEST_LOGGER = logging.getLogger("test_feed_dependencies")


# ---------------------------------------------------------------------------
# consumes_feeds declarations
# ---------------------------------------------------------------------------

def test_base_default_consumes_feeds_is_empty():
    assert PriceEvolutionComponent.consumes_feeds == ()


def test_funding_component_declares_funding_rate():
    assert FundingRateMeanReversionComponent.consumes_feeds == ("funding_rate",)


def test_feargreed_component_declares_fear_greed():
    assert FearGreedContrarianComponent.consumes_feeds == ("fear_greed",)


def test_whale_component_declares_both_columns():
    assert WhaleLargeTradeImbalanceComponent.consumes_feeds == (
        WHALE_LT_IMBALANCE_COLUMN, WHALE_ATTESTED_COLUMN,
    )


# ---------------------------------------------------------------------------
# required_feeds() -- per engine, over a MIXED config
# ---------------------------------------------------------------------------

def test_regime_engine_required_feeds():
    config = {
        "mode": "threshold_rules",
        "components": [
            {"id": "funding_probe",
             "class": "strategies.strategy_components.FundingRateMeanReversionComponent",
             "params": {}},
        ],
        "rules": [],
        "default_regime": "unknown",
    }
    engine = ConfigDrivenRegimeEngine(config)
    assert engine.required_feeds() == {"funding_rate": ("funding_probe",)}


def test_strategy_engine_required_feeds():
    config = {
        "warmup": 3,
        "regimes": {
            "unknown": {"components": [
                {"id": "fg",
                 "class": "strategies.strategy_components.FearGreedContrarianComponent",
                 "weight": 1.0, "transforms": [{"op": "identity"}], "params": {}},
            ]},
            "trending": None, "mean_reversion": None, "chop": None,
        },
    }
    engine = ConfigDrivenStrategyEngine(config)
    assert engine.required_feeds() == {"fear_greed": ("unknown.fg",)}


def _mixed_config():
    """regime_detector declares a funding consumer (unused by any rule -- config
    = intent regardless of reachability), strategies declares a fear_greed
    consumer under 'unknown'. Passes tools/validate_config.py."""
    return {
        "regime_detector": {
            "mode": "threshold_rules",
            "components": [
                {"id": "funding_probe",
                 "class": "strategies.strategy_components.FundingRateMeanReversionComponent",
                 "params": {}},
            ],
            "rules": [],
            "default_regime": "unknown",
        },
        "strategies": {
            "warmup": 3,
            "regimes": {
                "unknown": {"components": [
                    {"id": "fg",
                     "class": "strategies.strategy_components.FearGreedContrarianComponent",
                     "weight": 1.0, "transforms": [{"op": "identity"}], "params": {}},
                ]},
                "trending": None, "mean_reversion": None, "chop": None,
            },
        },
    }


def test_advanced_strategy_required_feeds_merges_both_engines():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(_mixed_config(), f)
        tmp_path = f.name
    try:
        strat = AdvancedStrategy(config_path=tmp_path)
        assert strat.required_feeds == {
            "funding_rate": ("funding_probe",),
            "fear_greed": ("unknown.fg",),
        }
    finally:
        Path(tmp_path).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# V1 -- registration completeness at BacktestEngine.load_data
# ---------------------------------------------------------------------------

class _StubStrategy:
    """Stands in for AdvancedStrategy: only `.required_feeds` matters to V1."""

    def __init__(self, required):
        self._required = required

    @property
    def required_feeds(self):
        return self._required


class _RecordingDataManager:
    """Stands in for DataManager inside load_data(): serves one bar, records
    register_feed() calls, never touches the network."""

    def __init__(self):
        self.historical_data = {}
        self._aux_feeds = {}
        self._required_flags = {}

    def fetch_historical_data(self, symbol, start_date, end_date, exchange="binance"):
        return pd.DataFrame({"timestamp": [pd.Timestamp("2022-01-01")], "close": [1.0]})

    def register_feed(self, name, fetcher, window_seconds, agg, required=False, fill="none",
                      delay_seconds=0.0):
        self._aux_feeds[name] = fetcher
        self._required_flags[name] = required
        self._agg_fill = getattr(self, "_agg_fill", {})
        self._agg_fill[name] = (agg, fill)
        self._delay = getattr(self, "_delay", {})
        self._delay[name] = delay_seconds

    def initialize(self):
        pass


def test_v1_raises_when_required_feed_absent_from_extra_feeds():
    dm = _RecordingDataManager()
    strat = _StubStrategy({"fear_greed": ("unknown.fg",)})
    engine = BacktestEngine(data_manager=dm, strategy=strat, logger=TEST_LOGGER, symbols=["BTCUSD"])

    with pytest.raises(FeedRequirementError) as exc_info:
        engine.load_data(start_date="2022-01-01", end_date="2022-01-02", extra_feeds={})

    assert "fear_greed" in str(exc_info.value)
    assert "unknown.fg" in str(exc_info.value)


def test_v1_passes_when_required_feed_present_in_extra_feeds():
    dm = _RecordingDataManager()
    strat = _StubStrategy({"fear_greed": ("unknown.fg",)})
    engine = BacktestEngine(data_manager=dm, strategy=strat, logger=TEST_LOGGER, symbols=["BTCUSD"])

    def factory(symbols, start, end, data_dir, exchange="binance"):
        return object()

    engine.load_data(start_date="2022-01-01", end_date="2022-01-02",
                      extra_feeds={"fear_greed": factory})

    assert "fear_greed" in dm._aux_feeds


def test_v1_pass_wires_required_true_only_for_the_required_feed():
    """Step 3: BacktestEngine.load_data must pass required=True to
    register_feed for a feed the strategy declares required, and
    required=False for a feed it doesn't -- proves the register_feed loop's
    `feed_name in required_feeds` membership test runs correctly across
    iterations (the loop variable must not shadow the required_feeds dict)."""
    dm = _RecordingDataManager()
    strat = _StubStrategy({"fear_greed": ("unknown.fg",)})
    engine = BacktestEngine(data_manager=dm, strategy=strat, logger=TEST_LOGGER, symbols=["BTCUSD"])

    def factory(symbols, start, end, data_dir, exchange="binance"):
        return object()

    engine.load_data(start_date="2022-01-01", end_date="2022-01-02",
                      extra_feeds={"fear_greed": factory, "funding_rate": factory})

    assert dm._required_flags == {"fear_greed": True, "funding_rate": False}


# ---------------------------------------------------------------------------
# Drift tripwire: a class referencing a known feed column in real code must
# declare it in consumes_feeds. Static, fast, fails the suite on drift.
# ---------------------------------------------------------------------------

_KNOWN_FEEDS = set(FEED_REGISTRY.keys()) | set(WHALE_FOOTPRINT_FEEDS)


def _is_docstring(stmt) -> bool:
    return (
        isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant)
        and isinstance(stmt.value.value, str)
    )


def _referenced_known_feeds(cls) -> set:
    """Known feed names the class's real (non-docstring) source references,
    either as a string literal or as a Name resolving to one via a module-level
    constant (e.g. WHALE_LT_IMBALANCE_COLUMN)."""
    source = inspect.getsource(cls)
    class_node = ast.parse(source).body[0]
    assert isinstance(class_node, ast.ClassDef)
    body = class_node.body
    if body and _is_docstring(body[0]):
        body = body[1:]

    found = set()
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value in _KNOWN_FEEDS:
                    found.add(node.value)
            elif isinstance(node, ast.Name):
                val = getattr(sc_module, node.id, None)
                if isinstance(val, str) and val in _KNOWN_FEEDS:
                    found.add(val)
    return found


def test_no_undeclared_feed_reference_drift():
    for name, cls in vars(sc_module).items():
        if not inspect.isclass(cls):
            continue
        if cls.__module__ != sc_module.__name__:
            continue
        if not issubclass(cls, SubStrategyComponent):
            continue

        referenced = _referenced_known_feeds(cls)
        declared = set(cls.consumes_feeds)
        undeclared = referenced - declared
        assert not undeclared, (
            f"{name} references feed(s) {sorted(undeclared)} in its source but "
            f"does not declare them in consumes_feeds (declared: {sorted(declared)})"
        )


# ---------------------------------------------------------------------------
# Step 2/3: `drop_feeds` param on core.launcher.run_backtest + manifest
# "feeds" provenance block (reporting/run_artifact.py::write_manifest).
# Byte-identical at default: drop_feeds=None forwards the SAME FEED_REGISTRY
# object, and write_manifest(feeds=None) adds no new manifest.json key.
# ---------------------------------------------------------------------------

_NO_AUX_FEED_CONFIG = PROJECT_ROOT / "tests" / "fixtures" / "no_aux_feed_check_config.json"
_FEAR_GREED_CONFIG = PROJECT_ROOT / "tests" / "fixtures" / "warmup_prefetch_check_config.json"


class _RecordingRunBacktestEngine:
    """Stands in for BacktestEngine inside run_backtest(): records both
    construction kwargs and load_data()'s kwargs, touches no data, runs no
    strategy. Same shape as tests/test_exchange_selection.py's
    _RecordingRunBacktestEngine (Ticket 13), extended to also capture
    load_data's extra_feeds -- the thing drop_feeds actually changes."""

    init_kwargs: ClassVar[dict] = {}
    load_data_kwargs: ClassVar[dict] = {}

    def __init__(self, **kwargs):
        type(self).init_kwargs = kwargs
        self._last_run_dir = None
        self._symbols = kwargs.get("symbols") or ["BTCUSDT"]
        # run_backtest now refuses an empty fetch (a zero-bar run would write an
        # all-zero metrics.json the campaign runner reads as a real result), so
        # this stub models historical_data the way the real engine does rather
        # than omitting it.
        self.historical_data = {}

    def load_data(self, **kwargs):
        type(self).load_data_kwargs = kwargs
        self.historical_data[self._symbols[0]] = pd.DataFrame(
            {"timestamp": [pd.Timestamp("2024-04-01")], "close": [1.0]})

    def simulate_on_loaded_data(self):
        pass


def test_run_backtest_drop_feeds_none_forwards_identical_feed_registry(monkeypatch, tmp_path):
    """drop_feeds=None (the default) must forward the SAME FEED_REGISTRY object
    to engine.load_data -- byte-identical by construction, not merely by
    matching keys."""
    _RecordingRunBacktestEngine.load_data_kwargs = {}
    monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingRunBacktestEngine)

    launcher_mod.run_backtest(
        config_path=str(_NO_AUX_FEED_CONFIG),
        symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
        results_root=str(tmp_path / "results"),
        trades_log_file=str(tmp_path / "trades.json"),
    )

    assert _RecordingRunBacktestEngine.load_data_kwargs["extra_feeds"] is FEED_REGISTRY


def test_run_backtest_drop_feeds_empty_list_takes_non_none_path(monkeypatch, tmp_path):
    """drop_feeds=[] is non-None: validation is vacuous but the filter still
    produces a fresh mapping (equal by value, not identical by object), and
    the raw [] is forwarded to BacktestEngine for manifest provenance."""
    _RecordingRunBacktestEngine.load_data_kwargs = {}
    _RecordingRunBacktestEngine.init_kwargs = {}
    monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingRunBacktestEngine)

    launcher_mod.run_backtest(
        config_path=str(_NO_AUX_FEED_CONFIG),
        symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
        results_root=str(tmp_path / "results"),
        trades_log_file=str(tmp_path / "trades.json"),
        drop_feeds=[],
    )

    forwarded = _RecordingRunBacktestEngine.load_data_kwargs["extra_feeds"]
    assert forwarded is not FEED_REGISTRY
    assert forwarded == FEED_REGISTRY
    assert _RecordingRunBacktestEngine.init_kwargs["drop_feeds"] == []


def test_run_backtest_drop_feeds_unknown_name_raises_value_error(tmp_path):
    """An unknown drop_feeds name must raise before any Launcher/strategy/data
    work -- a typo'd drop must not be a silent no-op. config_path is a path
    that is never read: the raise happens before it would be opened."""
    with pytest.raises(ValueError) as exc_info:
        launcher_mod.run_backtest(
            config_path="/nonexistent/config_never_read.json",
            symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
            results_root=str(tmp_path / "results"),
            trades_log_file=str(tmp_path / "trades.json"),
            drop_feeds=["not_a_real_feed"],
        )
    assert "not_a_real_feed" in str(exc_info.value)


def test_run_backtest_drop_feeds_required_feed_raises_feed_requirement_error(block_network, monkeypatch, tmp_path):
    """Dropping a feed the loaded strategy actually requires must raise V1's
    FeedRequirementError -- the already-built Step 1 guard, exercised end to
    end through run_backtest(). V1 raises inside load_data right after the
    price fetch and before any aux-feed fetch; the price fetch is stubbed to a
    one-bar frame (same shape as _RecordingDataManager above) so the real
    engine + strategy + guard run without a live Binance fetch that would
    write the shared local_data/BTCUSDT_1h.csv cache on a cache-less tree
    (fork CI). block_network makes any socket use fail loud, proving the run
    is hermetic."""
    monkeypatch.setattr(
        DataManager, "fetch_historical_data",
        lambda self, symbol, start_date, end_date, exchange="binance": pd.DataFrame(
            {"timestamp": [pd.Timestamp("2024-01-01")], "close": [1.0]}),
    )
    with pytest.raises(FeedRequirementError) as exc_info:
        launcher_mod.run_backtest(
            config_path=str(_FEAR_GREED_CONFIG),
            symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
            results_root=str(tmp_path / "results"),
            trades_log_file=str(tmp_path / "trades.json"),
            drop_feeds=["fear_greed"],
        )
    assert "fear_greed" in str(exc_info.value)


def _manifest_fixture_df() -> pd.DataFrame:
    return pd.DataFrame({
        "timestamp": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "open": [1.0, 1.0], "high": [1.0, 1.0], "low": [1.0, 1.0],
        "close": [1.0, 1.0], "volume": [1.0, 1.0],
    })


def test_write_manifest_records_feeds_block_with_empty_dropped_list(tmp_path):
    """Direct unit test of the write_manifest change: a non-None feeds dict
    (including an empty "dropped" list) is recorded verbatim."""
    from reporting.run_artifact import write_manifest

    write_manifest(
        run_dir=tmp_path, config={"x": 1}, data_df=_manifest_fixture_df(),
        symbols=["BTCUSDT"], timeframe="3600s", git_sha="deadbeef",
        lookback=10, warmup=5,
        feeds={"registered": [], "dropped": [], "required": []},
    )
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    assert manifest["feeds"] == {"registered": [], "dropped": [], "required": []}


def test_write_manifest_omits_feeds_key_when_feeds_is_none(tmp_path):
    """feeds=None (the default) must add no "feeds" key at all -- byte-
    identical manifest.json to before this parameter existed."""
    from reporting.run_artifact import write_manifest

    write_manifest(
        run_dir=tmp_path, config={"x": 1}, data_df=_manifest_fixture_df(),
        symbols=["BTCUSDT"], timeframe="3600s", git_sha="deadbeef",
        lookback=10, warmup=5,
    )
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    assert "feeds" not in manifest


# ---------------------------------------------------------------------------
# Slow: run_backtest() end to end, real engine, real caches (same shape as
# T-12/T-13, tests/test_exchange_selection.py).
# ---------------------------------------------------------------------------

class _NoNetworkSocket:
    """Raises at construction -- no real connection is ever attempted. Same
    shape as tests/test_exchange_selection.py's block_network fixture (T-13)."""

    def __init__(self, *a, **kw):
        raise OSError("network access blocked in test (Step 2 drop_feeds slow fixture)")


@pytest.fixture
def block_network(monkeypatch):
    monkeypatch.setattr(socket, "socket", _NoNetworkSocket)


_DROP_FEEDS_WINDOW_START = "2022-01-01"
_DROP_FEEDS_WINDOW_END = "2022-01-05"
_DROP_FEEDS_CACHE_SKIP = cache_skip_reason(
    PROJECT_ROOT / "local_data", ("BTCUSDT_1h.csv",),
    _DROP_FEEDS_WINDOW_START, _DROP_FEEDS_WINDOW_END,
)


@pytest.mark.slow
@pytest.mark.skipif(_DROP_FEEDS_CACHE_SKIP is not None,
                     reason=_DROP_FEEDS_CACHE_SKIP or "local_data caches usable")
def test_run_backtest_drop_feeds_completes_and_records_feeds_block(block_network, tmp_path):
    """Dropping both default feeds on the aux-free config runs to completion
    (nothing is registered, so block_network proves zero network is touched)
    and the manifest records the feeds block."""
    run_dir = launcher_mod.run_backtest(
        config_path=str(_NO_AUX_FEED_CONFIG),
        symbol="BTCUSDT", start=_DROP_FEEDS_WINDOW_START, end=_DROP_FEEDS_WINDOW_END,
        results_root=str(tmp_path / "results"),
        trades_log_file=str(tmp_path / "trades.json"),
        drop_feeds=["funding_rate", "fear_greed"],
    )
    assert run_dir is not None
    manifest = json.loads((Path(run_dir) / "manifest.json").read_text())
    assert manifest["feeds"] == {
        "registered": [],
        "dropped": ["fear_greed", "funding_rate"],
        "required": [],
    }


@pytest.mark.slow
@pytest.mark.skipif(_DROP_FEEDS_CACHE_SKIP is not None,
                     reason=_DROP_FEEDS_CACHE_SKIP or "local_data caches usable")
def test_run_backtest_default_run_manifest_has_no_feeds_key(tmp_path):
    """Companion to the above: omitting drop_feeds (the default) must produce
    a manifest with no "feeds" key at all."""
    run_dir = launcher_mod.run_backtest(
        config_path=str(_NO_AUX_FEED_CONFIG),
        symbol="BTCUSDT", start=_DROP_FEEDS_WINDOW_START, end=_DROP_FEEDS_WINDOW_END,
        results_root=str(tmp_path / "results"),
        trades_log_file=str(tmp_path / "trades.json"),
    )
    assert run_dir is not None
    manifest = json.loads((Path(run_dir) / "manifest.json").read_text())
    assert "feeds" not in manifest
