"""
strategy_designer_v2 components (operator, 2026-11-14): MovingAverageSlopeComponent, DistanceFromHighComponent and
VolatilityScaledReturnComponent (graded, forecast sources), VolumeRatioComponent (graded, 2026-11-17),
and three regime measures: MovingAverageAgeComponent, BarsSinceHighComponent, WeekdayComponent.

Each output is checked against an independent hand computation on synthetic bars that uses only rows up to and
including bar t (no lookahead), plus warmup, parameter validation, a real engine run for the graded one, and that
validate_config accepts each class where it is meant to be used (the graded one in a strategy, the regime measures in
the regime detector).
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
    BarsSinceHighComponent,
    DistanceFromHighComponent,
    VolatilityScaledReturnComponent,
    VolumeRatioComponent,
    MovingAverageAgeComponent,
    MovingAverageSlopeComponent,
    WeekdayComponent,
)
from strategies.strategy_engine import ConfigDrivenStrategyEngine  # noqa: E402
from tools.validate_config import validate  # noqa: E402

SC = "strategies.strategy_components."


def _bars(n: int, seed: int = 7, freq: str = "D") -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 0.02, n)))
    return pd.DataFrame({
        "timestamp": pd.date_range("2021-03-01", periods=n, freq=freq),
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
# MovingAverageSlopeComponent
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("t", [40, 77, 149])
def test_slope_sma_matches_the_hand_computation_using_rows_up_to_t(t):
    df = _bars(150)
    c = df["close"].to_numpy()[: t + 1]
    now, then = c[-10:].mean(), c[-15:-5].mean()
    got = _run(MovingAverageSlopeComponent(parameters={"period": 10, "lookback": 5}), df.iloc[: t + 1])
    assert got == pytest.approx((now - then) / then * 100.0, rel=1e-12)


def test_slope_ema_matches_the_hand_computation():
    df = _bars(150)
    e = _hand_ema(list(df["close"]), 10)
    got = _run(MovingAverageSlopeComponent(parameters={"period": 10, "lookback": 5, "average": "ema"}), df)
    assert got == pytest.approx((e[-1] - e[-6]) / e[-6] * 100.0, rel=1e-9)


def test_slope_sign_follows_the_average():
    up = pd.DataFrame({"timestamp": pd.date_range("2021-01-01", periods=60, freq="D"),
                       "close": np.linspace(100, 160, 60)})
    down = up.assign(close=up["close"][::-1].to_numpy())
    p = {"period": 10, "lookback": 5}
    assert _run(MovingAverageSlopeComponent(parameters=p), up) > 0
    assert _run(MovingAverageSlopeComponent(parameters=p), down) < 0


def test_slope_warmup_and_defaults():
    comp = MovingAverageSlopeComponent()
    assert (comp.period, comp.lookback, comp.average) == (200, 20, "sma")
    assert comp.get_required_periods() == 220
    small = MovingAverageSlopeComponent(parameters={"period": 10, "lookback": 5})
    assert _run(small, _bars(14)) == 0.0 and not small.is_ready()
    assert _run(small, _bars(15)) != 0.0


@pytest.mark.parametrize("params,match", [({"average": "wma"}, "average"), ({"period": 1}, "period"),
                                          ({"lookback": 0}, "lookback")])
def test_slope_bad_params_raise(params, match):
    with pytest.raises(ValueError, match=match):
        MovingAverageSlopeComponent(parameters=params)


# ---------------------------------------------------------------------------
# MovingAverageAgeComponent (regime measure)
# ---------------------------------------------------------------------------

def _hand_age(close, t, period, max_bars, fast=None):
    def side(i):
        slow = close[i - period + 1: i + 1].mean()
        x = close[i - fast + 1: i + 1].mean() if fast else close[i]
        return x > slow
    s, n = side(t), 0
    while n < max_bars and side(t - n) == s:
        n += 1
    return float(n if s else -n)


@pytest.mark.parametrize("t,fast", [(60, None), (99, None), (149, None), (149, 5), (120, 5)])
def test_age_matches_the_hand_computation_using_rows_up_to_t(t, fast):
    df = _bars(150)
    params = {"period": 20, "max_bars": 30, **({"fast_period": fast} if fast else {})}
    got = _run(MovingAverageAgeComponent(parameters=params), df.iloc[: t + 1])
    assert got == _hand_age(df["close"].to_numpy()[: t + 1], t, 20, 30, fast)


def test_age_is_capped_and_signed():
    rising = pd.DataFrame({"timestamp": pd.date_range("2021-01-01", periods=100, freq="D"),
                           "close": np.linspace(100, 200, 100)})
    assert _run(MovingAverageAgeComponent(parameters={"period": 10, "max_bars": 30}), rising) == 30.0
    falling = rising.assign(close=rising["close"][::-1].to_numpy())
    assert _run(MovingAverageAgeComponent(parameters={"period": 10, "max_bars": 30}), falling) == -30.0


@pytest.mark.parametrize("params", [{"period": 1}, {"max_bars": 0}, {"period": 20, "fast_period": 20}])
def test_age_bad_params_raise(params):
    with pytest.raises(ValueError):
        MovingAverageAgeComponent(parameters=params)


def test_age_warmup():
    comp = MovingAverageAgeComponent(parameters={"period": 20, "max_bars": 30})
    assert comp.get_required_periods() == 50
    assert _run(comp, _bars(49)) == 0.0 and not comp.is_ready()


# ---------------------------------------------------------------------------
# BarsSinceHighComponent (regime measure)
# ---------------------------------------------------------------------------

def _hand_bars_since_high(close, t, lookback, max_bars):
    for k in range(max_bars + 1):
        i = t - k
        if i - lookback >= 0 and close[i] > close[i - lookback: i].max():
            return float(max(0, max_bars - k))
    return 0.0


@pytest.mark.parametrize("t", range(41, 150, 7))
def test_bars_since_high_matches_the_hand_computation_using_rows_up_to_t(t):
    df = _bars(150, seed=3)
    got = _run(BarsSinceHighComponent(parameters={"lookback": 20, "max_bars": 20}), df.iloc[: t + 1])
    assert got == _hand_bars_since_high(df["close"].to_numpy()[: t + 1], t, 20, 20)


def test_bars_since_high_on_and_after_the_high():
    close = np.r_[np.full(45, 100.0), 110.0, np.full(25, 105.0)]   # warmup is lookback + max_bars + 1 = 41 bars
    df = pd.DataFrame({"timestamp": pd.date_range("2021-01-01", periods=len(close), freq="D"), "close": close})
    p = {"lookback": 20, "max_bars": 20}
    assert _run(BarsSinceHighComponent(parameters=p), df.iloc[:46]) == 20.0   # the day of the new high
    assert _run(BarsSinceHighComponent(parameters=p), df.iloc[:51]) == 15.0   # five bars later
    assert _run(BarsSinceHighComponent(parameters=p), df) == 0.0              # older than max_bars


@pytest.mark.parametrize("params", [{"lookback": 1}, {"max_bars": 0}])
def test_bars_since_high_bad_params_raise(params):
    with pytest.raises(ValueError):
        BarsSinceHighComponent(parameters=params)


# ---------------------------------------------------------------------------
# WeekdayComponent (regime measure)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("freq", ["D", "h"])
def test_weekday_is_the_coming_bars_weekday(freq):
    df = _bars(30, freq=freq)
    for t in range(1, 30):
        step = df["timestamp"].iloc[t] - df["timestamp"].iloc[t - 1]
        expected = (df["timestamp"].iloc[t] + step).weekday()
        assert _run(WeekdayComponent(), df.iloc[: t + 1]) == float(expected)


# ---------------------------------------------------------------------------
# Wiring: a real engine run for the graded one; the validator for each, where it is meant to be used
# ---------------------------------------------------------------------------

def _strategies(cls: str, params: dict) -> dict:
    return {"warmup": 5, "regimes": {
        "unknown": {"components": [{
            "id": "c", "class": SC + cls, "params": params, "weight": 1.0,
            "transforms": [{"op": "identity"}, {"op": "clip", "params": {"min": -20, "max": 20}}]}]},
        "trending": None, "mean_reversion": None, "chop": None}}


def test_engine_forecast_is_the_clipped_slope_once_warm():
    params = {"period": 10, "lookback": 5}
    eng = ConfigDrivenStrategyEngine(_strategies("MovingAverageSlopeComponent", params))
    df = _bars(120)
    nonzero = 0
    for i in range(2, len(df) + 1):
        eng.update(df.iloc[:i])
        if i >= 60:
            fc, dbg = eng.forecast(MarketRegime.UNKNOWN)
            assert "not_ready_component" not in dbg, (i, dbg)
            probe = _run(MovingAverageSlopeComponent(parameters=params), df.iloc[:i])
            assert fc == pytest.approx(float(np.clip(probe, -20, 20)), rel=1e-12)
            nonzero += fc != 0.0
    assert nonzero == len(df) - 59


def test_validator_accepts_the_slope_in_a_strategy():
    config = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                                  "default_regime": "unknown"},
              "strategies": {**_strategies("MovingAverageSlopeComponent", {"period": 50, "lookback": 10}), "warmup": 61}}
    assert validate(config) == []


@pytest.mark.parametrize("cls,params,op,value", [
    ("MovingAverageAgeComponent", {"period": 50, "max_bars": 60}, "gt", 10),
    ("BarsSinceHighComponent", {"lookback": 20, "max_bars": 20}, "gt", 0),
    ("WeekdayComponent", {}, "between", [4.5, 5.5]),
])
def test_validator_accepts_the_regime_measures_in_the_detector(cls, params, op, value):
    config = {"regime_detector": {"mode": "threshold_rules",
                                  "components": [{"id": "m", "class": SC + cls, "params": params}],
                                  "vetoes": [],
                                  "rules": [{"regime": "trending", "any_of": [[{"id": "m", "op": op, "value": value}]]}],
                                  "default_regime": "unknown"},
              "strategies": {**_strategies("MovingAverageSlopeComponent", {"period": 50, "lookback": 10}), "warmup": 61}}
    config["strategies"]["regimes"]["trending"] = config["strategies"]["regimes"].pop("unknown")
    config["strategies"]["regimes"]["unknown"] = None
    assert validate(config) == []


# ---------------------------------------------------------------------------
# DistanceFromHighComponent
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("t", [30, 77, 149])
def test_distance_from_high_matches_the_hand_computation_using_rows_up_to_t(t):
    df = _bars(150)
    c = df["close"].to_numpy()[: t + 1]
    high = c[-30:].max()
    got = _run(DistanceFromHighComponent(parameters={"period": 30}), df.iloc[: t + 1])
    assert got == pytest.approx((c[-1] - high) / high * 100.0, rel=1e-12)


def test_distance_from_high_is_zero_at_a_new_high_and_negative_below():
    close = np.r_[np.linspace(100, 120, 40), np.linspace(119, 90, 20)]
    df = pd.DataFrame({"timestamp": pd.date_range("2021-01-01", periods=len(close), freq="D"), "close": close})
    p = {"period": 30}
    assert _run(DistanceFromHighComponent(parameters=p), df.iloc[:40]) == 0.0
    assert _run(DistanceFromHighComponent(parameters=p), df) == pytest.approx((90 - 120) / 120 * 100.0)


def test_distance_from_high_warmup_nan_and_bad_params():
    comp = DistanceFromHighComponent(parameters={"period": 30})
    assert comp.get_required_periods() == 30
    assert _run(comp, _bars(29)) == 0.0 and not comp.is_ready()
    df = _bars(60)
    df.loc[45, "close"] = np.nan
    assert math.isnan(_run(DistanceFromHighComponent(parameters={"period": 30}), df))
    assert DistanceFromHighComponent().period == 60
    with pytest.raises(ValueError, match="period"):
        DistanceFromHighComponent(parameters={"period": 1})


def test_validator_accepts_the_distance_from_high_in_a_strategy():
    config = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                                  "default_regime": "unknown"},
              "strategies": {**_strategies("DistanceFromHighComponent", {"period": 60}), "warmup": 61}}
    assert validate(config) == []


# ---------------------------------------------------------------------------
# VolatilityScaledReturnComponent
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("t,period", [(40, 1), (77, 5), (149, 10)])
def test_scaled_return_matches_the_hand_computation_using_rows_up_to_t(t, period):
    df = _bars(150)
    c = df["close"].to_numpy()[: t + 1]
    r = c[1:] / c[:-1] - 1
    s = np.std(r[-20:], ddof=1)
    expected = (c[-1] / c[-1 - period] - 1) / (s * np.sqrt(period))
    got = _run(VolatilityScaledReturnComponent(parameters={"period": period, "vol_period": 20}), df.iloc[: t + 1])
    assert got == pytest.approx(expected, rel=1e-12)


def test_scaled_return_sign_warmup_flat_nan_and_bad_params():
    up = pd.DataFrame({"timestamp": pd.date_range("2021-01-01", periods=30, freq="D"),
                       "close": 100 * np.exp(np.cumsum(np.r_[0, np.full(28, 0.001), 0.05]))})
    assert _run(VolatilityScaledReturnComponent(), up) > 0
    assert _run(VolatilityScaledReturnComponent(), up.assign(close=1 / up["close"])) < 0
    comp = VolatilityScaledReturnComponent(parameters={"period": 5, "vol_period": 20})
    assert comp.get_required_periods() == 21 and _run(comp, _bars(20)) == 0.0
    flat = up.assign(close=100.0)
    assert _run(VolatilityScaledReturnComponent(), flat) == 0.0
    df = _bars(40)
    df.loc[30, "close"] = np.nan
    assert math.isnan(_run(VolatilityScaledReturnComponent(), df))
    for p in ({"period": 0}, {"vol_period": 1}):
        with pytest.raises(ValueError):
            VolatilityScaledReturnComponent(parameters=p)


def test_validator_accepts_the_scaled_return_in_a_strategy():
    config = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                                  "default_regime": "unknown"},
              "strategies": {**_strategies("VolatilityScaledReturnComponent", {"period": 1, "vol_period": 20}), "warmup": 61}}
    assert validate(config) == []


# ---------------------------------------------------------------------------
# VolumeRatioComponent
# ---------------------------------------------------------------------------

def _vol_bars(n: int, seed: int = 11) -> pd.DataFrame:
    df = _bars(n, seed)
    df["volume"] = np.random.default_rng(seed).lognormal(10.0, 0.5, n)
    return df


@pytest.mark.parametrize("t,period", [(29, 30), (77, 30), (149, 10)])
def test_volume_ratio_matches_the_hand_computation_using_rows_up_to_t(t, period):
    df = _vol_bars(150)
    v = df["volume"].to_numpy()[: t + 1]
    expected = v[-1] / (sum(v[-period:]) / period)
    got = _run(VolumeRatioComponent(parameters={"period": period}), df.iloc[: t + 1])
    assert got == pytest.approx(expected, rel=1e-12)


def test_volume_ratio_ignores_later_bars():
    df = _vol_bars(150)
    a = _run(VolumeRatioComponent(), df.iloc[:100])
    later = df.copy()
    later.loc[100:, "volume"] = 1e12
    assert _run(VolumeRatioComponent(), later.iloc[:100]) == a


def test_volume_ratio_is_one_at_average_and_grows_with_the_burst():
    df = _bars(40).assign(volume=100.0)
    assert _run(VolumeRatioComponent(parameters={"period": 10}), df) == pytest.approx(1.0)
    burst = df.copy()
    burst.loc[39, "volume"] = 300.0
    big = burst.copy()
    big.loc[39, "volume"] = 900.0
    r3 = _run(VolumeRatioComponent(parameters={"period": 10}), burst)
    r9 = _run(VolumeRatioComponent(parameters={"period": 10}), big)
    assert r3 == pytest.approx(300 / ((9 * 100 + 300) / 10)) and r9 > r3 > 1.0
    quiet = df.copy()
    quiet.loc[39, "volume"] = 10.0
    assert 0 < _run(VolumeRatioComponent(parameters={"period": 10}), quiet) < 1.0


def test_volume_ratio_warmup_nan_zero_and_bad_params():
    comp = VolumeRatioComponent(parameters={"period": 30})
    assert comp.get_required_periods() == 30
    assert _run(comp, _vol_bars(29)) == 0.0 and not comp.is_ready()
    df = _vol_bars(60)
    df.loc[45, "volume"] = np.nan
    assert math.isnan(_run(VolumeRatioComponent(parameters={"period": 30}), df))
    assert math.isnan(_run(VolumeRatioComponent(parameters={"period": 30}), _bars(40).assign(volume=0.0)))
    assert VolumeRatioComponent().period == 30
    with pytest.raises(ValueError, match="period"):
        VolumeRatioComponent(parameters={"period": 1})


def test_validator_accepts_the_volume_ratio_in_a_strategy_and_in_the_regime_detector():
    config = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                                  "default_regime": "unknown"},
              "strategies": {**_strategies("VolumeRatioComponent", {"period": 30}), "warmup": 61}}
    assert validate(config) == []
    config = {"regime_detector": {"mode": "threshold_rules",
                                  "components": [{"id": "vr", "class": SC + "VolumeRatioComponent",
                                                  "params": {"period": 30}}],
                                  "rules": [{"regime": "trending", "any_of": [[{"id": "vr", "op": "gt", "value": 1.5}]]}],
                                  "default_regime": "unknown"},
              "strategies": {**_strategies("DistanceFromHighComponent", {"period": 60}), "warmup": 61}}
    assert validate(config) == []


def test_engine_forecast_is_the_clipped_volume_ratio_once_warm():
    params = {"period": 20}
    eng = ConfigDrivenStrategyEngine(_strategies("VolumeRatioComponent", params))
    df = _vol_bars(120)
    for i in range(2, len(df) + 1):
        eng.update(df.iloc[:i])
        if i >= 40:
            fc, dbg = eng.forecast(MarketRegime.UNKNOWN)
            assert "not_ready_component" not in dbg, (i, dbg)
            probe = _run(VolumeRatioComponent(parameters=params), df.iloc[:i])
            assert fc == pytest.approx(float(np.clip(probe, -20, 20)), rel=1e-12) and fc > 0
