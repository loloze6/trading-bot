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
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.backtester import BacktestEngine, FeedRequirementError  # noqa: E402
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

    def fetch_historical_data(self, symbol, start_date, end_date, exchange="binance"):
        return pd.DataFrame({"timestamp": [pd.Timestamp("2022-01-01")], "close": [1.0]})

    def register_feed(self, name, fetcher, window_seconds, agg):
        self._aux_feeds[name] = fetcher

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
