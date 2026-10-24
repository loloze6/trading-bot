"""
D-191: EMASpreadComponent gains `average` ("ema" default, or "sma").

Builder's minimal proof (to be extended):
  (a) default and explicit "ema" give output and debug_info equal (==, not approx)
      to an independent pandas ewm computation of the pre-change formula, on every
      bar of a fixed synthetic series -- the "ema" path is unchanged;
  (b) "sma" equals the hand formula (SMA_fast - SMA_slow) / SMA_slow x 100 x sf,
      SMAs over the last fast/slow closes including the current one;
  (c) an unknown `average` raises when the component is built.
Plus the "sma" readiness rule and NaN behaviour.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from strategies.strategy_components import EMASpreadComponent  # noqa: E402


def _bars(n: int, seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 0.01, n)))
    return pd.DataFrame({
        "timestamp": pd.date_range("2021-03-01", periods=n, freq="h"),
        "open": close, "high": close * 1.001, "low": close * 0.999, "close": close, "volume": 1.0,
    })


def _expected_ema(data: pd.DataFrame, fast: int, slow: int, sf: float):
    """The pre-D-191 EMASpreadComponent formula, written out independently."""
    close = data["close"]
    fast_ema = close.ewm(span=fast, adjust=False).mean().iloc[-1]
    slow_ema = close.ewm(span=slow, adjust=False).mean().iloc[-1]
    spread_pct = ((fast_ema - slow_ema) / slow_ema) * 100.0
    debug = {"fast_ema": float(fast_ema), "slow_ema": float(slow_ema), "spread_pct": float(spread_pct)}
    return float(spread_pct * sf), debug


@pytest.mark.parametrize("params", [
    {},                                                   # class defaults 9 / 21 / 5.0
    {"fast_period": 50, "slow_period": 200, "scaling_factor": 1.0},
    {"fast_period": 50, "slow_period": 200, "scaling_factor": 1.0, "average": "ema"},
])
def test_ema_path_is_bit_identical_to_the_pre_change_formula(params):
    data = _bars(260)
    comp = EMASpreadComponent(parameters=dict(params))
    fast, slow = params.get("fast_period", 9), params.get("slow_period", 21)
    sf = params.get("scaling_factor", 5.0)
    assert comp.get_required_periods() == slow
    for t in range(1, len(data) + 1):
        window = data.iloc[:t]
        comp.update(window)
        assert comp.is_ready() == (t >= slow)
        if t >= slow:
            raw, debug = _expected_ema(window, fast, slow, sf)
            assert comp.raw_value() == raw
            assert comp.debug_info == debug


def test_default_and_explicit_ema_agree_exactly():
    data = _bars(120)
    a = EMASpreadComponent(parameters={"fast_period": 9, "slow_period": 21})
    b = EMASpreadComponent(parameters={"fast_period": 9, "slow_period": 21, "average": "ema"})
    for t in range(21, len(data) + 1):
        a.update(data.iloc[:t])
        b.update(data.iloc[:t])
        assert a.raw_value() == b.raw_value()
        assert a.debug_info == b.debug_info


def test_sma_equals_the_hand_formula():
    data = _bars(260)
    fast, slow, sf = 50, 200, 2.0
    comp = EMASpreadComponent(parameters={"fast_period": fast, "slow_period": slow,
                                          "scaling_factor": sf, "average": "sma"})
    closes = data["close"].tolist()
    for t in range(slow, len(data) + 1):
        comp.update(data.iloc[:t])
        sma_fast = sum(closes[t - fast:t]) / fast
        sma_slow = sum(closes[t - slow:t]) / slow
        expected = (sma_fast - sma_slow) / sma_slow * 100.0 * sf
        assert comp.raw_value() == pytest.approx(expected, rel=1e-9, abs=1e-12)
        assert comp.debug_info["fast_sma"] == pytest.approx(sma_fast, rel=1e-12)
        assert comp.debug_info["slow_sma"] == pytest.approx(sma_slow, rel=1e-12)
        assert comp.debug_info["average"] == "sma"


def test_sma_readiness_is_the_longer_window():
    comp = EMASpreadComponent(parameters={"fast_period": 5, "slow_period": 10, "average": "sma"})
    assert comp.get_required_periods() == 10
    comp.update(_bars(9))
    assert not comp.is_ready()
    comp.update(_bars(10))
    assert comp.is_ready()
    # no fast < slow check (unchanged); "sma" then waits for the longer window
    inverted = EMASpreadComponent(parameters={"fast_period": 12, "slow_period": 10, "average": "sma"})
    assert inverted.get_required_periods() == 12


def test_sma_nan_close_in_window_gives_nan():
    data = _bars(40)
    comp = EMASpreadComponent(parameters={"fast_period": 5, "slow_period": 10, "average": "sma"})
    inside = data.copy()
    inside.loc[35, "close"] = np.nan          # inside the last 10 closes
    comp.update(inside)
    assert math.isnan(comp.raw_value())
    outside = data.copy()
    outside.loc[5, "close"] = np.nan          # before both windows
    comp.update(outside)
    assert math.isfinite(comp.raw_value())


def test_unknown_average_raises():
    with pytest.raises(ValueError, match="average must be one of"):
        EMASpreadComponent(parameters={"average": "wma"})
