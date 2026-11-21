# No-lookahead proof: ExcessPredictivePowerZComponent (night3_learned_run, 2026-11-21; added by the session, beside the standard checks)

Same method as the other two learned-weight components (see their leak_proof.md): values computed the engine's way on real 1d bars, on a copy whose bars after a random cut t are a random walk, and on a copy cut at t. First 3 coins, default settings: 3 cases, 2991 values, 0 differences; values after t changed in every case.

## Output
```
AAVEUSD default cut-bar#1946: bars<=t identical=True (1128 values); after t changed=True
ADAUSD default cut-bar#2180: bars<=t identical=True (1362 values); after t changed=True
AVAXUSD default cut-bar#1319: bars<=t identical=True (501 values); after t changed=True
TOTAL values compared 2991; settings-coins with a difference: 0
```

## Script
```python
# No-lookahead proof for PastPredictivePowerWeightedCompositeComponent, on every cached 1d Kraken coin.
# For each coin and setting: values on every bar (each from the rows up to that bar, the engine's way) on the real data,
# then on a copy whose bars after a cut t are replaced by a random walk (and on a copy cut at t: bars after t removed).
# The values at every bar <= t must be identical in the three cases.
import sys, numpy as np
sys.path.insert(0, "/home/user/trading-bot/trading-bot"); sys.path.insert(0, "/home/user/trading-bot/trading-bot/tests")
from component_harness import real_data, values_on
from strategies.strategy_components import ExcessPredictivePowerZComponent as C
rng = np.random.default_rng(0)
settings = [{}]
tot = bad = 0
for coin, df in list(real_data("1d").items())[:3]:
    n = len(df); need = C().get_required_periods()
    if n < need + 30: print(coin, "too short", n); continue
    t = int(rng.integers(need + 5, n - 20))
    alt = df.copy(); k = n - t - 1
    walk = df["close"].iloc[t] * np.exp(np.cumsum(rng.normal(0, .1, k)))
    for col in ("open", "high", "low", "close"): alt.loc[t + 1:, col] = walk
    cut = df.iloc[:t + 1]
    for p in settings:
        need = C(parameters=p).get_required_periods()
        a, b, c = values_on(C, p, df), values_on(C, p, alt), values_on(C, p, cut)
        m = t - (need - 1) + 1          # values at bars need-1 .. t
        same = np.array_equal(a[:m], b[:m], equal_nan=True) and np.array_equal(a[:m], c, equal_nan=True)
        moved = not np.allclose(a[m:], b[m:], equal_nan=True)  # the future does change values after t
        tot += m; bad += (not same)
        print(f"{coin} {p or 'default'} cut-bar#{t}: bars<=t identical={same} ({m} values); after t changed={moved}")
print(f"TOTAL values compared {tot}; settings-coins with a difference: {bad}")
```
