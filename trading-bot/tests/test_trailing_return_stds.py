"""Topic 33 (2026-11-20): the four components that average many rolling stds give, bar by bar, exactly the values of
their former loops (kept below as the reference), on real hourly closes, with a NaN close and a restart."""
import os

import numpy as np
import pandas as pd
import pytest

from strategies.strategy_components import (
    RankWeightedScaledMoveComponent, VolatilityRankedFallComponent, VolatilityRatioToAverageComponent,
    VolatilityScaledReturnComponent)

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(os.path.dirname(HERE), "local_data", "kraken_BTCUSD_1h.csv")


def _old_scaled(c, period, vp, lag, L):
    e = len(c) - 1 - lag
    ret = c[e] / c[e - period] - 1.0
    sds = []
    for k in range(L):
        i = e - k
        w = c[i - vp:i + 1]
        r = w[1:] / w[:-1] - 1.0
        sds.append(float(np.std(r, ddof=1)))
    return sds


def _old_ratio(c, vp, L):
    r = c[1:] / c[:-1] - 1.0
    m = len(r)
    return [float(np.std(r[m - k - vp:m - k], ddof=1)) for k in range(L)]


def _old_ranked(c, vp, L):
    r = c[1:] / c[:-1] - 1.0
    return [float(np.std(r[k:vp + k], ddof=1)) for k in range(L)]


def _old_rankw(c, vp, L):
    r = c[1:] / c[:-1] - 1.0
    last = len(r) - 1
    return [float(np.std(r[last - k - vp + 1:last - k + 1], ddof=1)) for k in range(L)]


def _closes(n):
    if not os.path.exists(CSV):
        pytest.skip("no local BTC 1h file")
    c = pd.read_csv(CSV, usecols=["close"], nrows=20000 + n)["close"].to_numpy(dtype=float)[20000:]
    c = c.copy()
    c[n // 2] = np.nan        # a NaN close: the memo must not carry over wrongly
    return c


CASES = [
    (VolatilityScaledReturnComponent, {"period": 24, "vol_period": 40, "lag": 0, "vol_lookback": 60},
     lambda c, p: _old_scaled(c, 24, 40, 0, 60), "mean_std", lambda s: float(np.mean(s))),
    (VolatilityScaledReturnComponent, {"period": 3, "vol_period": 20, "lag": 2, "vol_lookback": 30},
     lambda c, p: _old_scaled(c, 3, 20, 2, 30), "mean_std", lambda s: float(np.mean(s))),
    (VolatilityRatioToAverageComponent, {"vol_period": 30, "vol_lookback": 50},
     lambda c, p: _old_ratio(c[-80:], 30, 50), "mean_std", lambda s: float(np.mean(s))),
    (VolatilityRankedFallComponent, {"vol_period": 20, "lookback": 40},
     lambda c, p: _old_ranked(c[-60:], 20, 40), "std", lambda s: s[-1]),
    (RankWeightedScaledMoveComponent, {"abs_period": 90, "vol_period": 20, "lookback": 50},
     lambda c, p: _old_rankw(c[-91:], 20, 50), "std_t", lambda s: s[0]),
]


@pytest.mark.parametrize("cls,params,old,key,expect", CASES)
def test_same_values_every_bar(cls, params, old, key, expect):
    closes = _closes(600)
    comp = cls(parameters=params)
    need = comp.get_required_periods()
    checked = 0
    for t in range(1, len(closes) + 1):
        if t == 400:
            comp = cls(parameters=params)          # a restart (a new component, as after a large gap)
        window = closes[max(0, t - 300):t]
        comp.update(pd.DataFrame({"close": window}))
        if len(window) < need or np.isnan(window[-need:]).any():
            continue
        assert comp.debug_info[key] == expect(old(window, params)), t   # bit for bit
        checked += 1
    assert checked > 300
