"""
D-051 graded components: MovingAverageDistanceComponent (percent distance from
an SMA or EMA) and MacdHistogramComponent (the MACD histogram as a percent of
the close, graded version of MacdHistogramCrossoverComponent).

Each output is checked against an independent hand computation on synthetic
bars that uses only rows up to and including bar t (no lookahead), plus sign,
NaN handling, warmup, parameter validation, a real engine run (the forecast is
non-zero once warm), and that validate_config accepts the class.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from strategies.strategy_base import MarketRegime  # noqa: E402
from strategies.strategy_components import (  # noqa: E402
    MacdHistogramComponent,
    MacroTrendFilterComponent,
    MovingAverageDistanceComponent,
)
from strategies.strategy_engine import ConfigDrivenStrategyEngine  # noqa: E402
from tools.validate_config import validate  # noqa: E402

SC = "strategies.strategy_components."


def _bars(n: int, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 0.01, n)))
    return pd.DataFrame({
        "timestamp": pd.date_range("2021-03-01", periods=n, freq="h"),
        "open": close, "high": close * 1.001, "low": close * 0.999, "close": close, "volume": 1.0,
    })


def _run(comp, df: pd.DataFrame) -> float:
    comp.update(df)
    return comp.raw_value()


def _hand_ema(xs, span):
    alpha, out = 2.0 / (span + 1.0), []
    for x in xs:
        out.append(x if not out else alpha * x + (1 - alpha) * out[-1])
    return out


# ---------------------------------------------------------------------------
# MovingAverageDistanceComponent
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("t", [50, 51, 120, 300])
def test_sma_distance_matches_the_hand_computation_using_rows_up_to_t(t):
    df = _bars(300)
    closes = [float(c) for c in df["close"].iloc[:t]]
    sma = sum(closes[-50:]) / 50                      # includes bar t's own close: no lag
    expected = (closes[-1] - sma) / sma * 100.0
    assert _run(MovingAverageDistanceComponent(), df.iloc[:t]) == pytest.approx(expected, rel=1e-12)


def test_ema_distance_matches_the_hand_computation():
    df = _bars(200)
    closes = [float(c) for c in df["close"]]
    ema = _hand_ema(closes, 30)[-1]
    comp = MovingAverageDistanceComponent(parameters={"period": 30, "average": "ema"})
    assert _run(comp, df) == pytest.approx((closes[-1] - ema) / ema * 100.0, rel=1e-12)


@pytest.mark.parametrize("period", [20, 100, 200])
def test_ema_distance_equals_macro_trend_filter_at_scaling_factor_one(period):
    df = _bars(400)
    new = MovingAverageDistanceComponent(parameters={"period": period, "average": "ema"})
    old = MacroTrendFilterComponent(parameters={"period": period, "scaling_factor": 1.0})
    assert _run(new, df) == pytest.approx(_run(old, df), rel=1e-12)


def test_sma_and_ema_differ():
    df = _bars(200)
    sma = _run(MovingAverageDistanceComponent(parameters={"period": 50}), df)
    ema = _run(MovingAverageDistanceComponent(parameters={"period": 50, "average": "ema"}), df)
    assert sma != pytest.approx(ema)


@pytest.mark.parametrize("average", ["sma", "ema"])
def test_distance_sign(average):
    up = pd.DataFrame({"close": np.r_[np.full(60, 100.0), np.full(5, 110.0)]})
    down = pd.DataFrame({"close": np.r_[np.full(60, 100.0), np.full(5, 90.0)]})
    params = {"period": 50, "average": average}
    assert _run(MovingAverageDistanceComponent(parameters=params), up) > 0
    assert _run(MovingAverageDistanceComponent(parameters=params), down) < 0


def test_distance_defaults_and_warmup():
    comp = MovingAverageDistanceComponent()
    assert (comp.period, comp.average, comp.get_required_periods()) == (50, "sma", 50)
    assert _run(comp, _bars(49)) == 0.0 and not comp.is_ready()
    _run(comp, _bars(50))
    assert comp.is_ready()


@pytest.mark.parametrize("params,match", [({"average": "wma"}, "average must be one of"),
                                          ({"period": 1}, "period must be >= 2")])
def test_distance_bad_params_raise(params, match):
    with pytest.raises(ValueError, match=match):
        MovingAverageDistanceComponent(parameters=params)


def test_sma_window_holding_a_nan_close_gives_nan():
    df = _bars(80)
    df.loc[df.index[-10], "close"] = np.nan
    assert math.isnan(_run(MovingAverageDistanceComponent(), df))
    # outside the 50-bar window it no longer matters
    assert not math.isnan(_run(MovingAverageDistanceComponent(parameters={"period": 5}), df))


@pytest.mark.parametrize("average", ["sma", "ema"])
def test_nan_latest_close_gives_nan(average):
    df = _bars(80)
    df.loc[df.index[-1], "close"] = np.nan
    assert math.isnan(_run(MovingAverageDistanceComponent(parameters={"average": average}), df))


# ---------------------------------------------------------------------------
# MacdHistogramComponent: (MACD - signal) / close x 100
# ---------------------------------------------------------------------------

def _hand_macd_pct(close: pd.Series, fast=12, slow=26, signal=9) -> float:
    values = [float(c) for c in close]
    macd = [f - s for f, s in zip(_hand_ema(values, fast), _hand_ema(values, slow))]
    sig = _hand_ema(macd, signal)
    return (macd[-1] - sig[-1]) / values[-1] * 100.0


@pytest.mark.parametrize("t", [35, 60, 199])
def test_macd_matches_the_hand_computation_using_rows_up_to_t(t):
    df = _bars(200)
    assert _run(MacdHistogramComponent(), df.iloc[:t]) == pytest.approx(
        _hand_macd_pct(df["close"].iloc[:t]), rel=1e-12, abs=1e-12)


def test_macd_params_are_used():
    df = _bars(120)
    comp = MacdHistogramComponent(parameters={"fast_period": 5, "slow_period": 20, "signal_period": 4})
    assert comp.get_required_periods() == 24
    assert _run(comp, df) == pytest.approx(_hand_macd_pct(df["close"], 5, 20, 4), rel=1e-12)


def test_macd_sign_follows_the_histogram():
    up = pd.DataFrame({"close": np.r_[np.full(40, 100.0), np.linspace(100, 130, 20)]})
    down = pd.DataFrame({"close": np.r_[np.full(40, 100.0), np.linspace(100, 70, 20)]})
    assert _run(MacdHistogramComponent(), up) > 0
    assert _run(MacdHistogramComponent(), down) < 0


def test_macd_is_stateless():
    df = _bars(150)
    fresh = _run(MacdHistogramComponent(), df)
    used = MacdHistogramComponent()
    for t in (40, 90, 60):
        used.update(df.iloc[:t])
    assert _run(used, df) == fresh


def test_macd_is_scale_free():
    df = _bars(100)
    scaled = df.assign(close=df["close"] * 1000.0)
    assert _run(MacdHistogramComponent(), scaled) == pytest.approx(_run(MacdHistogramComponent(), df), rel=1e-9)


def test_macd_warmup():
    comp = MacdHistogramComponent()
    assert comp.get_required_periods() == 35
    assert _run(comp, _bars(34)) == 0.0 and not comp.is_ready()
    _run(comp, _bars(35))
    assert comp.is_ready()


def test_macd_nan_latest_close_is_nan():
    df = _bars(60)
    df.loc[df.index[-1], "close"] = np.nan
    assert math.isnan(_run(MacdHistogramComponent(), df))


# ---------------------------------------------------------------------------
# Wiring: a real engine run, and the validator
# ---------------------------------------------------------------------------

def _strategies(cls: str, params: dict) -> dict:
    return {"warmup": 5, "regimes": {
        "unknown": {"components": [{
            "id": "c", "class": SC + cls, "params": params, "weight": 1.0,
            "transforms": [{"op": "identity"}, {"op": "clip", "params": {"min": -20, "max": 20}}]}]},
        "trending": None, "mean_reversion": None, "chop": None}}


@pytest.mark.parametrize("cls,params", [("MovingAverageDistanceComponent", {"period": 20}),
                                        ("MovingAverageDistanceComponent", {"period": 20, "average": "ema"}),
                                        ("MacdHistogramComponent", {})])
def test_engine_forecast_is_the_clipped_raw_value_once_warm(cls, params):
    """Through ConfigDrivenStrategyEngine: after warmup the forecast is the
    component's current value (identity + clip, one component), non-zero --
    i.e. the component really drives a position, bar after bar."""
    eng = ConfigDrivenStrategyEngine(_strategies(cls, params))
    df = _bars(120)
    probe = MovingAverageDistanceComponent(parameters=params) if cls.startswith("Moving") \
        else MacdHistogramComponent(parameters=params)
    nonzero = 0
    for i in range(2, len(df) + 1):
        eng.update(df.iloc[:i])
        if i >= 60:
            fc, dbg = eng.forecast(MarketRegime.UNKNOWN)
            assert "not_ready_component" not in dbg, (i, dbg)
            assert fc == pytest.approx(float(np.clip(_run(probe, df.iloc[:i]), -20, 20)), rel=1e-12)
            nonzero += fc != 0.0
    assert nonzero == len(df) - 59


def _config(cls: str, params: dict) -> dict:
    return {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                                "default_regime": "unknown"},
            "strategies": {**_strategies(cls, params), "warmup": 51}}


@pytest.mark.parametrize("cls,params", [("MovingAverageDistanceComponent", {"period": 100, "average": "sma"}),
                                        ("MacdHistogramComponent", {})])
def test_validator_accepts_the_class(cls, params):
    assert validate(_config(cls, params)) == []
