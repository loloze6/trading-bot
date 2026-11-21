# No-lookahead proof: PastPredictivePowerWeightedCompositeComponent (night3_learned_run, 2026-11-21; added by the session, beside the standard checks)

Asked by the night's brief: the value at bar t must be unchanged when every bar after t is removed or altered.
Method: on real 1d Kraken bars, the value on every bar computed the engine's way (from the rows up to that bar),
on the real data, on a copy whose bars after a random cut t are a random walk, and on a copy cut at t.
Pass: values at every bar <= t identical in the three cases; values after t change (the test can see a change).
Ran 25 min (its time limit) on the first 9 coins, 7 settings: 60 cases, 60 identical, 60 changed after t. (The weightings share one warm-up, 455 bars.)

## Output
```
AAVEUSD default cut-bar#1892: bars<=t identical=True (1439 values); after t changed=True
AAVEUSD {'weighting': 'regression'} cut-bar#1892: bars<=t identical=True (1439 values); after t changed=True
AAVEUSD {'weighting': 'best'} cut-bar#1892: bars<=t identical=True (1439 values); after t changed=True
AAVEUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#1892: bars<=t identical=True (1439 values); after t changed=True
AAVEUSD {'weighting': 'single', 'signal': 'reversal'} cut-bar#1892: bars<=t identical=True (1439 values); after t changed=True
AAVEUSD {'weighting': 'single', 'signal': 'high'} cut-bar#1892: bars<=t identical=True (1439 values); after t changed=True
AAVEUSD {'weighting': 'single', 'signal': 'volatility'} cut-bar#1892: bars<=t identical=True (1439 values); after t changed=True
ADAUSD default cut-bar#2047: bars<=t identical=True (1594 values); after t changed=True
ADAUSD {'weighting': 'regression'} cut-bar#2047: bars<=t identical=True (1594 values); after t changed=True
ADAUSD {'weighting': 'best'} cut-bar#2047: bars<=t identical=True (1594 values); after t changed=True
ADAUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#2047: bars<=t identical=True (1594 values); after t changed=True
ADAUSD {'weighting': 'single', 'signal': 'reversal'} cut-bar#2047: bars<=t identical=True (1594 values); after t changed=True
ADAUSD {'weighting': 'single', 'signal': 'high'} cut-bar#2047: bars<=t identical=True (1594 values); after t changed=True
ADAUSD {'weighting': 'single', 'signal': 'volatility'} cut-bar#2047: bars<=t identical=True (1594 values); after t changed=True
AVAXUSD default cut-bar#876: bars<=t identical=True (423 values); after t changed=True
AVAXUSD {'weighting': 'regression'} cut-bar#876: bars<=t identical=True (423 values); after t changed=True
AVAXUSD {'weighting': 'best'} cut-bar#876: bars<=t identical=True (423 values); after t changed=True
AVAXUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#876: bars<=t identical=True (423 values); after t changed=True
AVAXUSD {'weighting': 'single', 'signal': 'reversal'} cut-bar#876: bars<=t identical=True (423 values); after t changed=True
AVAXUSD {'weighting': 'single', 'signal': 'high'} cut-bar#876: bars<=t identical=True (423 values); after t changed=True
AVAXUSD {'weighting': 'single', 'signal': 'volatility'} cut-bar#876: bars<=t identical=True (423 values); after t changed=True
BTCUSD default cut-bar#3222: bars<=t identical=True (2769 values); after t changed=True
BTCUSD {'weighting': 'regression'} cut-bar#3222: bars<=t identical=True (2769 values); after t changed=True
BTCUSD {'weighting': 'best'} cut-bar#3222: bars<=t identical=True (2769 values); after t changed=True
BTCUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#3222: bars<=t identical=True (2769 values); after t changed=True
BTCUSD {'weighting': 'single', 'signal': 'reversal'} cut-bar#3222: bars<=t identical=True (2769 values); after t changed=True
BTCUSD {'weighting': 'single', 'signal': 'high'} cut-bar#3222: bars<=t identical=True (2769 values); after t changed=True
BTCUSD {'weighting': 'single', 'signal': 'volatility'} cut-bar#3222: bars<=t identical=True (2769 values); after t changed=True
DOGEUSD default cut-bar#1995: bars<=t identical=True (1542 values); after t changed=True
DOGEUSD {'weighting': 'regression'} cut-bar#1995: bars<=t identical=True (1542 values); after t changed=True
DOGEUSD {'weighting': 'best'} cut-bar#1995: bars<=t identical=True (1542 values); after t changed=True
DOGEUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#1995: bars<=t identical=True (1542 values); after t changed=True
DOGEUSD {'weighting': 'single', 'signal': 'reversal'} cut-bar#1995: bars<=t identical=True (1542 values); after t changed=True
DOGEUSD {'weighting': 'single', 'signal': 'high'} cut-bar#1995: bars<=t identical=True (1542 values); after t changed=True
DOGEUSD {'weighting': 'single', 'signal': 'volatility'} cut-bar#1995: bars<=t identical=True (1542 values); after t changed=True
ETHUSD default cut-bar#1570: bars<=t identical=True (1117 values); after t changed=True
ETHUSD {'weighting': 'regression'} cut-bar#1570: bars<=t identical=True (1117 values); after t changed=True
ETHUSD {'weighting': 'best'} cut-bar#1570: bars<=t identical=True (1117 values); after t changed=True
ETHUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#1570: bars<=t identical=True (1117 values); after t changed=True
ETHUSD {'weighting': 'single', 'signal': 'reversal'} cut-bar#1570: bars<=t identical=True (1117 values); after t changed=True
ETHUSD {'weighting': 'single', 'signal': 'high'} cut-bar#1570: bars<=t identical=True (1117 values); after t changed=True
ETHUSD {'weighting': 'single', 'signal': 'volatility'} cut-bar#1570: bars<=t identical=True (1117 values); after t changed=True
INJUSD default cut-bar#1266: bars<=t identical=True (813 values); after t changed=True
INJUSD {'weighting': 'regression'} cut-bar#1266: bars<=t identical=True (813 values); after t changed=True
INJUSD {'weighting': 'best'} cut-bar#1266: bars<=t identical=True (813 values); after t changed=True
INJUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#1266: bars<=t identical=True (813 values); after t changed=True
INJUSD {'weighting': 'single', 'signal': 'reversal'} cut-bar#1266: bars<=t identical=True (813 values); after t changed=True
INJUSD {'weighting': 'single', 'signal': 'high'} cut-bar#1266: bars<=t identical=True (813 values); after t changed=True
INJUSD {'weighting': 'single', 'signal': 'volatility'} cut-bar#1266: bars<=t identical=True (813 values); after t changed=True
LINKUSD default cut-bar#574: bars<=t identical=True (121 values); after t changed=True
LINKUSD {'weighting': 'regression'} cut-bar#574: bars<=t identical=True (121 values); after t changed=True
LINKUSD {'weighting': 'best'} cut-bar#574: bars<=t identical=True (121 values); after t changed=True
LINKUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#574: bars<=t identical=True (121 values); after t changed=True
LINKUSD {'weighting': 'single', 'signal': 'reversal'} cut-bar#574: bars<=t identical=True (121 values); after t changed=True
LINKUSD {'weighting': 'single', 'signal': 'high'} cut-bar#574: bars<=t identical=True (121 values); after t changed=True
LINKUSD {'weighting': 'single', 'signal': 'volatility'} cut-bar#574: bars<=t identical=True (121 values); after t changed=True
LTCUSD default cut-bar#1095: bars<=t identical=True (642 values); after t changed=True
LTCUSD {'weighting': 'regression'} cut-bar#1095: bars<=t identical=True (642 values); after t changed=True
LTCUSD {'weighting': 'best'} cut-bar#1095: bars<=t identical=True (642 values); after t changed=True
LTCUSD {'weighting': 'single', 'signal': 'momentum'} cut-bar#1095: bars<=t identical=True (642 values); after t changed=True
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
from strategies.strategy_components import PastPredictivePowerWeightedCompositeComponent as C
rng = np.random.default_rng(0)
settings = [{}, {"weighting": "regression"}, {"weighting": "best"}] + [{"weighting": "single", "signal": s} for s in C._SIGNALS]
tot = bad = 0
for coin, df in real_data("1d").items():
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
