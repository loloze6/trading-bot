---
idea: 010-08_rsi-below-streak-reversal
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: days the 14-day RSI has stayed below 50 without a break, up to the current close -> replaced: no catalogue component counts that run; RSIPullbackComponent gives only the RSI level, a different quantity.
- Comparison: longer runs below 50 against shorter ones -> kept: a graded count makes the position larger as the run lengthens.
- Outcome: the coin's return over the next 14 days is higher, upward -> kept: 14 bars on daily bars, long side.
- Verdict transfer: no: a test on the RSI level or a smoothed RSI would judge how far RSI is below 50, not how long it has stayed there.
Reason: The run length of RSI(14) below 50 can be computed from one coin's own closes, and a graded count fits the config's logic, as MovingAverageAgeComponent shows for an SMA. But no catalogue component counts consecutive bars of RSI below 50. Vetoes with `consecutive_bars` only give a few fixed levels across at most four regimes, and smoothing RSIPullbackComponent measures depth, not duration.
