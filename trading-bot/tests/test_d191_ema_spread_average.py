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


# ---------------------------------------------------------------------------
# Extended coverage (dispatch PR-9 tests).
#
# "Before D-191" (c0ec04d8, strategy_components.py): EMASpreadComponent read
# fast_period/slow_period/scaling_factor from `parameters`, is_ready() was
# `data is not None and len(data) >= slow_period`, get_required_periods() was
# `slow_period` (no max() with fast_period), update() did nothing before ready
# (so `_raw_value` was never assigned and debug_info stayed {}), and once ready
# it set raw = ((fast_ewm - slow_ewm) / slow_ewm * 100) * scaling_factor with
# close.ewm(span=..., adjust=False).mean().iloc[-1] and debug_info
# {fast_ema, slow_ema, spread_pct}. The tests below pin exactly that.
# ---------------------------------------------------------------------------

from strategies.strategy_engine import ConfigDrivenStrategyEngine  # noqa: E402
from tools.validate_config import validate  # noqa: E402

_BYTE_IDENTITY_PARAMS = [
    pytest.param({}, id="defaults_9_21_5.0"),
    pytest.param({"fast_period": 50, "slow_period": 200, "scaling_factor": 1.0}, id="fast50_slow200"),
    pytest.param({"fast_period": 9, "slow_period": 21, "scaling_factor": -3.0}, id="negative_scaling_factor"),
    pytest.param({"fast_period": 30, "slow_period": 10, "scaling_factor": 2.5}, id="fast_gt_slow"),
]


@pytest.mark.parametrize("average_kw", [None, "ema"], ids=["key_absent", "explicit_ema"])
@pytest.mark.parametrize("params", _BYTE_IDENTITY_PARAMS)
def test_ema_default_is_identical_to_independent_ewm_on_every_ready_bar(params, average_kw):
    p = dict(params)
    if average_kw is not None:
        p["average"] = average_kw
    fast, slow = p.get("fast_period", 9), p.get("slow_period", 21)
    sf = p.get("scaling_factor", 5.0)
    data = _bars(420, seed=5)
    comp = EMASpreadComponent(parameters=p)
    assert comp.average == "ema"
    # pre-change: required periods is slow_period alone, even when fast > slow
    assert comp.get_required_periods() == slow
    n_ready = 0
    for t in range(1, len(data) + 1):
        window = data.iloc[:t]
        comp.update(window)
        assert comp.is_ready() == (t >= slow)
        if t >= slow:
            raw, debug = _expected_ema(window, fast, slow, sf)
            # == on purpose: the "ema" branch is the untouched pre-change code path
            assert comp.raw_value() == raw
            assert comp.debug_info == debug
            assert "average" not in comp.debug_info
            n_ready += 1
    assert n_ready == len(data) - slow + 1


def test_sma_formula_on_a_hand_computable_series():
    # fast 2 / slow 4, scaling 0.5, closes chosen so the t=5 SMAs are exact
    # binary floats (19.0 and 16.0): that bar is asserted with ==. t=4 has a
    # non-terminating spread (2.5/13.5), so it uses a 1e-12 relative tolerance,
    # which is far tighter than any formula error (a wrong window or a dropped
    # x100 moves the value by whole percents).
    closes = [10.0, 12.0, 14.0, 18.0, 20.0]
    data = pd.DataFrame({"close": closes})
    comp = EMASpreadComponent(parameters={"fast_period": 2, "slow_period": 4,
                                          "scaling_factor": 0.5, "average": "sma"})
    comp.update(data.iloc[:4])
    # SMA2 = (14+18)/2 = 16, SMA4 = (10+12+14+18)/4 = 13.5
    assert comp.debug_info["fast_sma"] == 16.0
    assert comp.debug_info["slow_sma"] == 13.5
    assert comp.raw_value() == pytest.approx((16.0 - 13.5) / 13.5 * 100.0 * 0.5, rel=1e-12)
    comp.update(data)
    # SMA2 includes the current close: (18+20)/2 = 19; SMA4 = (12+14+18+20)/4 = 16
    assert comp.debug_info["fast_sma"] == 19.0
    assert comp.debug_info["slow_sma"] == 16.0
    assert comp.debug_info["spread_pct"] == 18.75
    assert comp.raw_value() == 9.375


@pytest.mark.parametrize("average", ["ema", "sma"])
def test_not_ready_update_changes_nothing_and_forecast_reports_not_ready(average):
    # The pre-change "ema" convention before ready: update() stores data but never
    # assigns _raw_value or debug_info, and generate_forecast() reports not_ready.
    # "sma" must follow the same convention.
    comp = EMASpreadComponent(parameters={"fast_period": 5, "slow_period": 10, "average": average})
    for n in range(1, 10):
        comp.update(_bars(n))
        assert not comp.is_ready()
        assert not hasattr(comp, "_raw_value")
        assert comp.debug_info == {}
        out = comp.generate_forecast()
        assert out.debug_info == {"error": "not_ready"}
    comp.update(_bars(10))
    assert comp.is_ready()
    assert math.isfinite(comp.raw_value())
    assert comp.debug_info != {}


def test_sma_ready_at_exactly_max_of_fast_and_slow():
    for fast, slow in [(5, 10), (12, 10), (7, 7)]:
        need = max(fast, slow)
        comp = EMASpreadComponent(parameters={"fast_period": fast, "slow_period": slow, "average": "sma"})
        assert comp.get_required_periods() == need
        comp.update(_bars(need - 1))
        assert not comp.is_ready(), (fast, slow)
        comp.update(_bars(need))
        assert comp.is_ready(), (fast, slow)
    # the "ema" requirement is unchanged: slow_period, not max(fast, slow)
    ema = EMASpreadComponent(parameters={"fast_period": 12, "slow_period": 10})
    assert ema.get_required_periods() == 10
    ema.update(_bars(10))
    assert ema.is_ready()


@pytest.mark.parametrize("fast,slow", [(3, 10), (10, 3)], ids=["slow_longer", "fast_longer"])
def test_sma_nan_close_poisons_output_until_it_leaves_both_windows(fast, slow):
    n, nan_at = 30, 10
    data = _bars(n)
    data.loc[nan_at, "close"] = np.nan
    longer = max(fast, slow)
    comp = EMASpreadComponent(parameters={"fast_period": fast, "slow_period": slow, "average": "sma"})
    seen_nan_fast_only = seen_nan_slow_only = seen_recovery = False
    for t in range(longer, n + 1):
        comp.update(data.iloc[:t])
        # bar index nan_at is in the last `w` closes of a t-bar frame iff t - w <= nan_at < t
        in_fast = t - fast <= nan_at < t
        in_slow = t - slow <= nan_at < t
        if in_fast or in_slow:
            assert math.isnan(comp.raw_value()), t
            # the NaN is confined to the average whose window holds it
            assert math.isnan(comp.debug_info["fast_sma"]) == in_fast
            assert math.isnan(comp.debug_info["slow_sma"]) == in_slow
            seen_nan_fast_only |= in_fast and not in_slow
            seen_nan_slow_only |= in_slow and not in_fast
        else:
            assert math.isfinite(comp.raw_value()), t
            seen_recovery |= t > nan_at
    assert seen_recovery
    # the shorter window's NaN-only phase exists in exactly one orientation
    assert seen_nan_fast_only or seen_nan_slow_only


@pytest.mark.parametrize("bad", ["SMA", "Ema", "", " sma", 1, None, ["sma"], "wma"])
def test_unknown_average_raises_at_construction(bad):
    with pytest.raises(ValueError, match="average must be one of"):
        EMASpreadComponent(parameters={"average": bad})


def test_default_average_is_ema_when_key_absent():
    assert EMASpreadComponent().average == "ema"
    assert EMASpreadComponent(parameters={"fast_period": 5}).average == "ema"
    assert EMASpreadComponent(parameters={"average": "sma"}).average == "sma"


def _engine_config(params: dict) -> dict:
    comp = {
        "id": "ema_spread",
        "class": "strategies.strategy_components.EMASpreadComponent",
        "weight": 1.0,
        "transforms": [{"op": "identity"}],
        "params": params,
    }
    regimes = {"trending": None, "mean_reversion": None, "chop": None, "unknown": {"components": [comp]}}
    return {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                            "default_regime": "unknown"},
        "strategies": {"warmup": 25, "regimes": regimes},
    }


def test_strategy_engine_builds_an_sma_spread_component_from_config():
    params = {"fast_period": 3, "slow_period": 10, "scaling_factor": 1.0, "average": "sma"}
    config = _engine_config(params)
    engine = ConfigDrivenStrategyEngine(config["strategies"])
    comp = engine._components["unknown"]["ema_spread"]
    assert isinstance(comp, EMASpreadComponent)
    assert comp.average == "sma"
    assert comp.get_required_periods() == 10

    data = _bars(40)
    closes = data["close"].tolist()
    for t in range(1, len(data) + 1):
        engine.update(data.iloc[:t])
    hist = engine._history["unknown"]["ema_spread"]
    assert len(hist) == hist.maxlen  # bounded history: filled once ready for >= maxlen bars
    expected = (sum(closes[-3:]) / 3 - sum(closes[-10:]) / 10) / (sum(closes[-10:]) / 10) * 100.0
    assert hist[-1] == pytest.approx(expected, rel=1e-9)

    # the same config without `average` builds the default EMA component
    legacy = _engine_config({k: v for k, v in params.items() if k != "average"})
    legacy_comp = ConfigDrivenStrategyEngine(legacy["strategies"])._components["unknown"]["ema_spread"]
    assert legacy_comp.average == "ema"
    assert legacy_comp.get_required_periods() == 10


def test_strategy_engine_rejects_an_unknown_average_in_config():
    config = _engine_config({"average": "wma"})
    with pytest.raises(ValueError, match="average must be one of"):
        ConfigDrivenStrategyEngine(config["strategies"])


@pytest.mark.parametrize("average", ["sma", "ema"])
def test_validate_config_accepts_the_average_param(average):
    config = _engine_config({"fast_period": 50, "slow_period": 200, "scaling_factor": 1.0,
                             "average": average})
    assert validate(config) == []


def test_sma_50_minus_200_sign_matches_output_sign_on_every_ready_bar():
    # D-187's finding: the "SMA50 vs SMA200" reading. Rising then falling series so
    # both signs of (SMA50 - SMA200) occur, with the cross inside the ready range.
    fast, slow = 50, 200
    up = np.linspace(100.0, 300.0, 300)
    down = np.linspace(300.0, 90.0, 300)[1:]
    close = np.concatenate([up, down])
    data = pd.DataFrame({"close": close})
    sma_fast = data["close"].rolling(fast).mean()
    sma_slow = data["close"].rolling(slow).mean()
    comp = EMASpreadComponent(parameters={"fast_period": fast, "slow_period": slow, "average": "sma"})
    signs = set()
    for t in range(slow, len(data) + 1):
        comp.update(data.iloc[:t])
        diff = float(sma_fast.iloc[t - 1] - sma_slow.iloc[t - 1])
        assert diff != 0.0
        assert np.sign(comp.raw_value()) == np.sign(diff), t
        signs.add(np.sign(diff))
    assert signs == {1.0, -1.0}


# Safety review (PR #542 fix round): on "sma" a period must be an integer >= 1.
# Integral floats are accepted and stored as int; bools are refused. "ema" is
# not checked at all (unchanged behaviour for existing configs).
_BAD_SMA_PERIODS = [0, -5, 9.7, 0.0, -1.0, True, False, float("nan"), float("inf"), "50", None]


@pytest.mark.parametrize("key", ["fast_period", "slow_period"])
@pytest.mark.parametrize("bad", _BAD_SMA_PERIODS)
def test_sma_refuses_a_period_that_is_not_an_integer_ge_1(key, bad):
    params = {"fast_period": 9, "slow_period": 21, "average": "sma", key: bad}
    with pytest.raises(ValueError, match=f"{key} must be an integer >= 1"):
        EMASpreadComponent(parameters=params)


def test_sma_accepts_integral_float_periods_as_ints():
    comp = EMASpreadComponent(parameters={"fast_period": 50.0, "slow_period": np.float64(200.0),
                                          "average": "sma"})
    assert comp.fast_period == 50 and isinstance(comp.fast_period, int)
    assert comp.slow_period == 200 and isinstance(comp.slow_period, int)
    assert comp.get_required_periods() == 200


def test_sma_accepts_numpy_ints_and_period_one():
    comp = EMASpreadComponent(parameters={"fast_period": np.int64(1), "slow_period": 3,
                                          "average": "sma"})
    assert comp.fast_period == 1 and comp.slow_period == 3


@pytest.mark.parametrize("odd", [0, -5, 9.7, 50.0, True])
@pytest.mark.parametrize("key", ["fast_period", "slow_period"])
@pytest.mark.parametrize("average_kw", [{}, {"average": "ema"}])
def test_ema_does_not_check_periods_at_construction(key, odd, average_kw):
    comp = EMASpreadComponent(parameters={key: odd, **average_kw})
    assert comp.average == "ema"
    # stored exactly as given: no cast, no check on the ema path
    assert getattr(comp, key) is odd
