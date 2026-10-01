"""
CUL-357: graded FundingRateComponent (-funding_rate x 10000, bps) and
FearGreedComponent (50 - index), the D-051 versions of the on/off originals.

The first attempt (held back from PR #282) passed unit tests on hand-filled
columns but could not work for real: a 1-bar history never forecast, and the
real feed merge left most 1h/4h bars NaN. Hence three levels here:
  * unit: formula, sign, None/NaN/missing column -> NaN, warmup 2;
  * the REAL DataManager merge with the production feed declarations
    (FEED_FILL carry_forward, FEED_DELAY_SECONDS) on sparse feeds;
  * the REAL ConfigDrivenStrategyEngine: the forecast follows the value on
    every bar once warm.
"""
import datetime
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import DataManager  # noqa: E402
from data.feed_registry import FEED_AGG, FEED_DELAY_SECONDS, FEED_FILL  # noqa: E402
from strategies.strategy_base import MarketRegime  # noqa: E402
from strategies.strategy_components import FearGreedComponent, FundingRateComponent  # noqa: E402
from strategies.strategy_engine import ConfigDrivenStrategyEngine  # noqa: E402
from tools.validate_config import validate  # noqa: E402

SC = "strategies.strategy_components."
START = pd.Timestamp("2021-03-01")
SYMBOL = "BTCUSDT"


def _df(n=3, **cols):
    df = pd.DataFrame({"timestamp": pd.date_range(START, periods=n, freq="h"), "close": 100.0})
    for k, v in cols.items():
        df[k] = v
    return df


def _raw(comp, df):
    comp.update(df)
    return comp.raw_value()


# ---------------------------------------------------------------------------
# unit
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rate,expected", [(0.0001, -1.0), (-0.00025, 2.5), (0.0, 0.0), (0.003, -30.0)])
def test_funding_is_minus_the_rate_in_bps(rate, expected):
    assert _raw(FundingRateComponent(), _df(funding_rate=[0.0005, 0.0005, rate])) == pytest.approx(expected)


@pytest.mark.parametrize("fg,expected", [(20.0, 30.0), (80.0, -30.0), (50.0, 0.0), (0.0, 50.0), (100.0, -50.0)])
def test_fear_greed_is_fifty_minus_the_index(fg, expected):
    assert _raw(FearGreedComponent(), _df(fear_greed=[50.0, 50.0, fg])) == pytest.approx(expected)


@pytest.mark.parametrize("cls,col", [(FundingRateComponent, "funding_rate"), (FearGreedComponent, "fear_greed")])
@pytest.mark.parametrize("last", [np.nan, None, "missing_column"])
def test_a_gap_is_nan_never_a_fabricated_reading(cls, col, last):
    df = _df() if last == "missing_column" else _df(**{col: pd.Series([1.0, 1.0, last], dtype=object)})
    assert math.isnan(_raw(cls(), df))


@pytest.mark.parametrize("cls", [FundingRateComponent, FearGreedComponent])
def test_warmup_is_two_bars(cls):
    comp = cls()
    assert comp.get_required_periods() == 2
    col = "funding_rate" if cls is FundingRateComponent else "fear_greed"
    assert _raw(comp, _df(n=1, **{col: [1.0]})) == 0.0 and not comp.is_ready()


def test_feed_declarations():
    assert FundingRateComponent.consumes_feeds == ("funding_rate",)
    assert FearGreedComponent.consumes_feeds == ("fear_greed",)


# ---------------------------------------------------------------------------
# the real DataManager merge, production declarations, sparse feeds
# ---------------------------------------------------------------------------

class _StubFetcher:
    exchange_id = "binance"

    def __init__(self, df):
        self._df = df

    def get_data(self, symbol=None):
        return self._df

    def cache_key(self, symbol):
        return "stub"


FUNDING = pd.DataFrame({"timestamp": pd.date_range(START + datetime.timedelta(days=1), periods=9, freq="8h"),
                        "funding_rate": [0.0001 * (i + 1) for i in range(9)]})
FG = pd.DataFrame({"timestamp": pd.date_range(START + datetime.timedelta(days=1), periods=3, freq="D"),
                   "fear_greed": [20.0, 40.0, 60.0]})


def _enriched_hourly(days=6):
    ts = pd.date_range(START, periods=days * 24, freq="h")
    price = pd.DataFrame({"timestamp": ts, "open": 100.0, "high": 100.0, "low": 100.0,
                          "close": 100.0, "volume": 1.0})
    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    for name, df in (("funding_rate", FUNDING), ("fear_greed", FG)):
        dm.register_feed(name, _StubFetcher(df), window_seconds=0, agg=FEED_AGG[name],
                         fill=FEED_FILL[name], delay_seconds=FEED_DELAY_SECONDS[name])
    dm.historical_data[SYMBOL] = price
    dm.initialize()
    return dm._attach_aux_columns(SYMBOL, price).sort_values("timestamp").reset_index(drop=True)


def test_funding_component_on_every_hourly_bar_of_the_real_merge():
    out = _enriched_hourly()
    comp = FundingRateComponent()
    for i in range(1, len(out)):
        bar = out.iloc[i]
        seen = FUNDING[FUNDING["timestamp"] < bar["timestamp"] + datetime.timedelta(hours=1)]
        got = _raw(comp, out.iloc[: i + 1])
        if seen.empty:
            assert math.isnan(got), bar["timestamp"]
        else:
            assert got == pytest.approx(-seen["funding_rate"].iloc[-1] * 10000), bar["timestamp"]


def test_fear_greed_component_sees_the_prior_days_value_on_every_bar():
    out = _enriched_hourly()
    comp = FearGreedComponent()
    for i in range(1, len(out)):
        bar = out.iloc[i]
        usable = FG[FG["timestamp"] + datetime.timedelta(days=1) <= bar["timestamp"]]   # one-day delay
        got = _raw(comp, out.iloc[: i + 1])
        if usable.empty:
            assert math.isnan(got), bar["timestamp"]
        else:
            assert got == pytest.approx(50.0 - usable["fear_greed"].iloc[-1]), bar["timestamp"]


# ---------------------------------------------------------------------------
# the real strategy engine: the forecast follows the value on every bar
# ---------------------------------------------------------------------------

def _strategies(cls):
    return {"warmup": 3, "regimes": {
        "unknown": {"components": [{
            "id": "c", "class": SC + cls, "params": {}, "weight": 1.0,
            "transforms": [{"op": "identity"}, {"op": "clip", "params": {"min": -20, "max": 20}}]}]},
        "trending": None, "mean_reversion": None, "chop": None}}


@pytest.mark.parametrize("cls,comp_cls", [("FundingRateComponent", FundingRateComponent),
                                          ("FearGreedComponent", FearGreedComponent)])
def test_engine_forecasts_on_every_bar_once_the_feed_has_started(cls, comp_cls):
    """The first attempt's blocker: a 1-bar history never forecast. Here the
    forecast equals the clipped value on every bar after the feed starts."""
    out = _enriched_hourly()
    eng = ConfigDrivenStrategyEngine(_strategies(cls))
    probe = comp_cls()
    checked = 0
    for i in range(2, len(out) + 1):
        window = out.iloc[:i]
        eng.update(window)
        value = _raw(probe, window)
        if i >= 72 and not math.isnan(value):               # well after both feeds started
            fc, dbg = eng.forecast(MarketRegime.UNKNOWN)
            assert "not_ready_component" not in dbg
            assert fc == pytest.approx(float(np.clip(value, -20, 20)))
            checked += 1
    assert checked > 50


@pytest.mark.parametrize("cls", ["FundingRateComponent", "FearGreedComponent"])
def test_validator_accepts_the_class(cls):
    cfg = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                               "default_regime": "unknown"},
           "strategies": {**_strategies(cls), "warmup": 51}}
    assert validate(cfg) == []
