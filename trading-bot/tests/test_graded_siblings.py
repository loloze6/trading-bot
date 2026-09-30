"""
D-051 graded siblings: FundingRateGradedComponent, FearGreedGradedComponent,
MacdHistogramGradedComponent (the on/off originals are unchanged).

Each output is checked against an independent hand computation on synthetic
bars, using only rows up to and including bar t (no lookahead), plus its sign,
NaN handling (a gap gives NaN, never a fabricated 0.0), warmup, and that the
validator (V12) and the feed machinery accept the class.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from strategies.strategy_components import (  # noqa: E402
    FearGreedGradedComponent,
    FundingRateGradedComponent,
    MacdHistogramGradedComponent,
)
from tools.validate_config import validate  # noqa: E402

SC = "strategies.strategy_components."


def _bars(n: int, **cols) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 0.01, n)))
    df = pd.DataFrame({
        "timestamp": pd.date_range("2021-03-01 01:00:00", periods=n, freq="h"),
        "close": close,
    })
    for k, v in cols.items():
        df[k] = v
    return df


def _run(comp, df: pd.DataFrame) -> float:
    comp.update(df)
    return comp.raw_value()


# ---------------------------------------------------------------------------
# FundingRateGradedComponent: -funding_rate x 10000, every bar
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rate,expected", [(0.0001, -1.0), (-0.00025, 2.5), (0.0, 0.0), (0.003, -30.0)])
def test_funding_is_minus_the_rate_in_bps(rate, expected):
    assert _run(FundingRateGradedComponent(), _bars(3, funding_rate=[0.0005, 0.0005, rate])) == \
        pytest.approx(expected)


def test_funding_is_graded_on_every_bar_not_only_at_settlement():
    """The original fires only at UTC hour 0/8/16; the graded one reads the
    latest print on every bar (bar 01:00 here is not a settlement hour)."""
    df = _bars(1, funding_rate=[0.0002])
    assert pd.Timestamp(df["timestamp"].iloc[-1]).hour % 8 != 0
    assert _run(FundingRateGradedComponent(), df) == pytest.approx(-2.0)


def test_funding_uses_only_the_latest_row():
    df = _bars(5, funding_rate=[0.01, -0.01, 0.02, 0.0, 0.0004])
    assert _run(FundingRateGradedComponent(), df) == pytest.approx(-4.0)
    assert _run(FundingRateGradedComponent(), df.iloc[:3]) == pytest.approx(-200.0)


@pytest.mark.parametrize("df", [_bars(2, funding_rate=[0.0001, np.nan]), _bars(2)],
                         ids=["nan_print", "missing_column"])
def test_funding_gap_is_nan_not_zero(df):
    assert math.isnan(_run(FundingRateGradedComponent(), df))


# ---------------------------------------------------------------------------
# FearGreedGradedComponent: 50 - index, every bar
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("fg,expected", [(20.0, 30.0), (80.0, -30.0), (50.0, 0.0), (0.0, 50.0), (100.0, -50.0)])
def test_fear_greed_is_fifty_minus_the_index(fg, expected):
    assert _run(FearGreedGradedComponent(), _bars(2, fear_greed=[50.0, fg])) == pytest.approx(expected)


def test_fear_greed_is_graded_on_every_bar_not_only_at_midnight():
    df = _bars(1, fear_greed=[40.0])
    assert pd.Timestamp(df["timestamp"].iloc[-1]).hour != 0
    assert _run(FearGreedGradedComponent(), df) == pytest.approx(10.0)


@pytest.mark.parametrize("df", [_bars(2, fear_greed=[40.0, np.nan]), _bars(2)],
                         ids=["nan_value", "missing_column"])
def test_fear_greed_gap_is_nan_not_zero(df):
    assert math.isnan(_run(FearGreedGradedComponent(), df))


# ---------------------------------------------------------------------------
# MacdHistogramGradedComponent: (MACD - signal) / close x 100
# ---------------------------------------------------------------------------

def _hand_macd_pct(close: pd.Series, fast=12, slow=26, signal=9) -> float:
    """Independent computation, written out step by step."""
    values = [float(c) for c in close]

    def ema(xs, span):
        alpha, out = 2.0 / (span + 1.0), []
        for x in xs:
            out.append(x if not out else alpha * x + (1 - alpha) * out[-1])
        return out

    macd = [f - s for f, s in zip(ema(values, fast), ema(values, slow))]
    sig = ema(macd, signal)
    return (macd[-1] - sig[-1]) / values[-1] * 100.0


@pytest.mark.parametrize("t", [35, 60, 199])
def test_macd_matches_the_hand_computation_using_rows_up_to_t(t):
    df = _bars(200)
    got = _run(MacdHistogramGradedComponent(), df.iloc[:t])
    assert got == pytest.approx(_hand_macd_pct(df["close"].iloc[:t]), rel=1e-12, abs=1e-12)


def test_macd_params_are_used():
    df = _bars(120)
    comp = MacdHistogramGradedComponent(parameters={"fast_period": 5, "slow_period": 20, "signal_period": 4})
    assert comp.get_required_periods() == 24
    assert _run(comp, df) == pytest.approx(_hand_macd_pct(df["close"], 5, 20, 4), rel=1e-12)


def test_macd_sign_follows_the_histogram():
    up = pd.DataFrame({"close": np.r_[np.full(40, 100.0), np.linspace(100, 130, 20)]})
    down = pd.DataFrame({"close": np.r_[np.full(40, 100.0), np.linspace(100, 70, 20)]})
    assert _run(MacdHistogramGradedComponent(), up) > 0
    assert _run(MacdHistogramGradedComponent(), down) < 0


def test_macd_is_stateless():
    """Same window, same value, whatever the component saw before (the
    crossover original remembers the previous bar's sign; this one must not)."""
    df = _bars(150)
    fresh = _run(MacdHistogramGradedComponent(), df)
    used = MacdHistogramGradedComponent()
    for t in (40, 90, 60):
        used.update(df.iloc[:t])
    assert _run(used, df) == fresh


def test_macd_is_scale_free():
    df = _bars(100)
    scaled = df.assign(close=df["close"] * 1000.0)
    assert _run(MacdHistogramGradedComponent(), scaled) == pytest.approx(
        _run(MacdHistogramGradedComponent(), df), rel=1e-9)


def test_macd_warmup():
    comp = MacdHistogramGradedComponent()
    assert comp.get_required_periods() == 35
    assert _run(comp, _bars(34)) == 0.0 and not comp.is_ready()
    _run(comp, _bars(35))
    assert comp.is_ready()


def test_macd_nan_latest_close_is_nan():
    df = _bars(60)
    df.loc[df.index[-1], "close"] = np.nan
    assert math.isnan(_run(MacdHistogramGradedComponent(), df))


# ---------------------------------------------------------------------------
# Wiring: validator, feeds
# ---------------------------------------------------------------------------

def _config(cls: str) -> dict:
    return {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                            "default_regime": "unknown"},
        "strategies": {"warmup": 51, "regimes": {"unknown": {"components": [
            {"id": "c", "class": SC + cls, "weight": 1.0,
             "transforms": [{"op": "identity"}, {"op": "clip", "params": {"min": -20, "max": 20}}]}]},
            "trending": None, "mean_reversion": None, "chop": None}},
    }


@pytest.mark.parametrize("cls", ["FundingRateGradedComponent", "FearGreedGradedComponent",
                                 "MacdHistogramGradedComponent"])
def test_validator_accepts_the_class(cls):
    assert validate(_config(cls)) == []


def test_feed_declarations():
    assert FundingRateGradedComponent.consumes_feeds == ("funding_rate",)
    assert FearGreedGradedComponent.consumes_feeds == ("fear_greed",)
    assert MacdHistogramGradedComponent.consumes_feeds == ()
