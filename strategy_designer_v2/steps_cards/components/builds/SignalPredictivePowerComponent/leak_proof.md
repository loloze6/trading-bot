# No-lookahead proof: SignalPredictivePowerComponent (night3_learned_run, 2026-11-21; added by the session, beside the standard checks)

Asked by the night's brief: the value at bar t must be unchanged when every bar after t is removed or altered.
Method: on real 1d Kraken bars, the value on every bar computed the engine's way (from the rows up to that bar),
on the real data, on a copy whose bars after a random cut t are a random walk, and on a copy cut at t.
Pass: values at every bar <= t identical in the three cases; values after t change (the test can see a change).
First 4 coins, 4 signals: 16 cases, 0 differences, 12904 values. (A first run used the default warm-up for every signal and misaligned the arrays: 12 false differences; fixed to the warm-up of each setting.)

## Output
```
AAVEUSD {'signal': 'momentum'} cut-bar#1883: bars<=t identical=True (1491 values); after t changed=True
AAVEUSD {'signal': 'reversal'} cut-bar#1883: bars<=t identical=True (1518 values); after t changed=True
AAVEUSD {'signal': 'high'} cut-bar#1883: bars<=t identical=True (1430 values); after t changed=True
AAVEUSD {'signal': 'volatility'} cut-bar#1883: bars<=t identical=True (1489 values); after t changed=True
ADAUSD {'signal': 'momentum'} cut-bar#2025: bars<=t identical=True (1633 values); after t changed=True
ADAUSD {'signal': 'reversal'} cut-bar#2025: bars<=t identical=True (1660 values); after t changed=True
ADAUSD {'signal': 'high'} cut-bar#2025: bars<=t identical=True (1572 values); after t changed=True
ADAUSD {'signal': 'volatility'} cut-bar#2025: bars<=t identical=True (1631 values); after t changed=True
AVAXUSD {'signal': 'momentum'} cut-bar#466: bars<=t identical=True (74 values); after t changed=True
AVAXUSD {'signal': 'reversal'} cut-bar#466: bars<=t identical=True (101 values); after t changed=True
AVAXUSD {'signal': 'high'} cut-bar#466: bars<=t identical=True (13 values); after t changed=True
AVAXUSD {'signal': 'volatility'} cut-bar#466: bars<=t identical=True (72 values); after t changed=True
BTCUSD {'signal': 'momentum'} cut-bar#456: bars<=t identical=True (64 values); after t changed=True
BTCUSD {'signal': 'reversal'} cut-bar#456: bars<=t identical=True (91 values); after t changed=True
BTCUSD {'signal': 'high'} cut-bar#456: bars<=t identical=True (3 values); after t changed=True
BTCUSD {'signal': 'volatility'} cut-bar#456: bars<=t identical=True (62 values); after t changed=True
TOTAL values compared 12904; settings-coins with a difference: 0
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
from strategies.strategy_components import SignalPredictivePowerComponent as C
rng = np.random.default_rng(0)
settings = [{"signal": s} for s in ("momentum","reversal","high","volatility")]
tot = bad = 0
for coin, df in list(real_data("1d").items())[:4]:
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
