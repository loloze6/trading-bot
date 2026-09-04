"""
CUL-273 Task A. Three components explicitly coerced a missing/unmeasurable
required input into a fabricated numeric default rather than propagating
invalidity -- the shared base class's own nan_policy="propagate_invalid"
default, which this ticket makes explicit. Grepped for every explicit
pd.isna/np.isnan/fillna-style check in strategy_components.py (exactly 4
found): RSIPullbackComponent (coerced to 50.0 = "neutral"), FundingRate-
MeanReversionComponent and FearGreedContrarianComponent (returned early,
silently reusing the same _raw_value=0.0 a real "no event this bar" reading
produces) -- all three fixed here. The fourth, WhaleLongTermImbalance-
Component's np.isnan check, already does the right thing (self._abstain(...))
and needed no change -- not retested here, it isn't a regression risk.

A first version of this fix ALSO added a guard in
ConfigDrivenStrategyEngine.forecast() converting a NaN component value into
0.0 ("invalid_component", treated like the existing not_ready_component
short-circuit). That guard was wrong and was reverted: it broke
tests/test_whale_lt_imbalance_component.py, which locks in the OPPOSITE,
deliberate, pre-existing design -- a NaN component value must produce a NaN
FINAL forecast, because 0.0 asserts "balanced/no signal", which is a false
claim about a bar that measured nothing. AdvancedStrategy.generate_forecast()
returns ConfigDrivenStrategyEngine.forecast()'s value with zero NaN
sanitization ANYWHERE in the chain (checked: main_strategy.py,
core/trading_bot.py, execution/forecast_manager.py, none of them touch NaN) --
so a NaN forecast today already reaches target_allocation/allocation_change
completely unguarded, for the whale component, in production, right now.
That is a REAL, PRE-EXISTING gap, not introduced by this ticket -- but this
ticket's own scope (fixing 3 components that coerced NaN into a fabricated
default) is not the place to silently redesign the ensemble/allocation
layer's handling of an already-NaN forecast. Flagged as its own finding,
not fixed here.
"""
import math
import numpy as np
import pandas as pd
import pytest

from strategies.strategy_components import (
    RSIPullbackComponent,
    FundingRateMeanReversionComponent,
    FearGreedContrarianComponent,
)
from strategies.strategy_engine import ConfigDrivenStrategyEngine
from strategies.strategy_base import MarketRegime


def _bars(n, close_flat=True):
    close = [100.0] * n if close_flat else list(np.linspace(100.0, 110.0, n))
    return pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
        "open": close, "high": close, "low": close, "close": close, "volume": 1.0,
    })


def test_rsi_propagates_nan_on_zero_loss_instead_of_coercing_to_neutral():
    """A perfectly flat price series makes RSI's `loss` term 0 -> rs undefined
    -> NaN, before this fix silently coerced to 50.0 ('neutral'). That number
    was indistinguishable from a real, measured neutral reading -- propagate
    NaN instead."""
    comp = RSIPullbackComponent(parameters={"period": 5})
    df = _bars(20, close_flat=True)
    for i in range(2, len(df) + 1):
        comp.update(df.iloc[:i])
    assert comp.is_ready()
    assert math.isnan(comp.raw_value()), (
        "flat price -> RSI loss==0 -> NaN must propagate, not silently become 50.0"
    )
    assert comp.confidence == 0.0


def test_rsi_still_computes_a_real_value_on_varying_prices():
    """Byte-identity guard: the fix only changes the NaN branch. Real,
    non-degenerate data must still produce a real (non-NaN) value, exactly as
    before this ticket."""
    comp = RSIPullbackComponent(parameters={"period": 5})
    df = _bars(20, close_flat=False)
    for i in range(2, len(df) + 1):
        comp.update(df.iloc[:i])
    assert comp.is_ready()
    assert not math.isnan(comp.raw_value())


def test_funding_rate_component_propagates_nan_on_missing_settlement_print():
    """A genuinely missing funding_rate value AT a real settlement boundary
    (UTC hour % 8 == 0) is a data-quality gap, not 'no event fired'."""
    comp = FundingRateMeanReversionComponent(parameters={"threshold": 0.001})
    n = 9  # ends exactly on hour 8 (0-indexed bar 8), a real settlement boundary
    df = _bars(n)
    df["timestamp"] = pd.date_range("2024-01-01 00:00", periods=n, freq="h")
    df["funding_rate"] = [float("nan")] * n
    for i in range(1, n + 1):
        comp.update(df.iloc[:i])
    assert df["timestamp"].iloc[-1].hour % 8 == 0, "test setup must actually land on a settlement bar"
    assert math.isnan(comp.raw_value()), (
        "missing funding_rate at a real settlement bar must propagate NaN, "
        "not silently reuse the same 0.0 a below-threshold reading produces"
    )


def test_funding_rate_component_still_returns_zero_on_legitimate_non_event():
    """Byte-identity guard: a non-settlement bar (real, present funding_rate,
    just not a settlement hour) is a genuine 'nothing to report' -- must stay
    0.0, not become NaN. This is the case the fix must NOT touch."""
    comp = FundingRateMeanReversionComponent(parameters={"threshold": 0.001})
    n = 10
    df = _bars(n)
    df["timestamp"] = pd.date_range("2024-01-01 01:00", periods=n, freq="h")  # never hour%8==0
    df["funding_rate"] = [0.0005] * n
    for i in range(1, n + 1):
        comp.update(df.iloc[:i])
    assert comp.raw_value() == 0.0
    assert not math.isnan(comp.raw_value())


def test_fear_greed_component_propagates_nan_on_missing_daily_print():
    comp = FearGreedContrarianComponent()
    n = 2  # needs get_required_periods()==2; final bar lands on the daily boundary
    df = _bars(n)
    df["timestamp"] = pd.date_range("2024-01-01 23:00", periods=n, freq="h")  # -> [23:00, 00:00]
    df["fear_greed"] = [float("nan")] * n
    for i in range(1, n + 1):
        comp.update(df.iloc[:i])
    assert df["timestamp"].iloc[-1].hour == 0, "test setup must actually land on the daily boundary bar"
    assert math.isnan(comp.raw_value())


def test_fear_greed_component_still_returns_zero_on_legitimate_non_event():
    comp = FearGreedContrarianComponent()
    n = 10
    df = _bars(n)
    df["timestamp"] = pd.date_range("2024-01-01 01:00", periods=n, freq="h")  # never hour==0
    df["fear_greed"] = [50.0] * n
    for i in range(1, n + 1):
        comp.update(df.iloc[:i])
    assert comp.raw_value() == 0.0


def test_engine_forecast_propagates_a_nan_component_value_as_a_nan_forecast():
    """CORRECTED expectation (see module docstring): ConfigDrivenStrategyEngine
    .forecast() has NO NaN guard, deliberately -- it must propagate a NaN
    component value through to the returned forecast, exactly the behavior
    tests/test_whale_lt_imbalance_component.py already locks in for the whale
    component. This is not this ticket's design choice to make; it is
    confirming the newly-NaN-capable RSI component behaves consistently with
    the component that already had this property."""
    cfg = {
        "regimes": {
            "trending": {"components": [{
                "id": "rsi", "class": "strategies.strategy_components.RSIPullbackComponent",
                "params": {"period": 5}, "weight": 1.0,
                "transforms": [{"op": "identity"}],
            }]},
            "mean_reversion": None, "chop": None, "unknown": None,
        },
    }
    eng = ConfigDrivenStrategyEngine(cfg)
    df = _bars(20, close_flat=True)   # flat -> RSI's own NaN branch fires every bar
    for i in range(2, len(df) + 1):
        eng.update(df.iloc[:i])
    # Force is_ready regardless of warmup bar count -- this test is about NaN
    # propagation through forecast(), not warmup timing.
    eng.set_warmup(0)
    forecast, debug = eng.forecast(MarketRegime.TRENDING)
    assert math.isnan(forecast), (
        "a NaN component value must propagate to a NaN forecast -- coercing it "
        "to 0.0 would falsely assert 'neutral/balanced', the exact bug class "
        "test_whale_lt_imbalance_component.py exists to prevent"
    )
