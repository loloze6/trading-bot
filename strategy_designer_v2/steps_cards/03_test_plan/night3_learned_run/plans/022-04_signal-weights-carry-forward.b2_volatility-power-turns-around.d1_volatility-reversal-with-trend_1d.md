---
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d1_volatility-reversal-with-trend
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the 30-day volatility signal's predictive power for 5-day returns over the past 365 days is high -> kept: `SignalPredictivePowerComponent` (signal "volatility", vol_period 30, corr_lookback 365, horizon 5) computes it.
- Comparison: the same signal's power over the following 90 days, lower the higher its past power, more so when its side agrees with the 28-day return -> replaced: no component bets on the signal against its usual power, and no component makes that bet larger as it agrees with the 28-day return.
- Outcome: the volatility signal's 5-day calls work less, or in reverse, over the next 90 days -> adapted: while the past power is high, take a graded reversed-volatility bet, held 5 bars.
- Verdict transfer: no: the only bet the catalogue allows, -w x z (`PastPredictivePowerWeightedCompositeComponent` single "volatility", negated), tests a reversal to below zero rather than "lower than usual", and it cannot grow with agreement with the 28-day trend.
Reason: All the inputs come from the coin's own closes. A weighted sum of catalogue components cannot form (w - wbar) x z for the volatility signal, because no component gives wbar x z or z alone. It also cannot multiply the reversed bet by its agreement with the 28-day return; a regime would only switch it on or off, not grade it.
