---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-02_breakout-shock-continues
line: 7.g patterns
backtest: N3-02_breakout-shock-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a large down day relative to the coin's own recent day sizes, especially one that closes at a new 21-day closing low, the coin rises over the next five days by more than its average five-day move. Late sellers capitulate and the selling then runs out.
Consequence: A trader should refuse to open shorts after a shock-down new low, and may treat it as a setup for a short-term long rebound.
Why:
- F1: A large down day that closes at a new 21-day closing low (standardised one-day return ≤ -10) is followed by a mean excess 5-bar return of +1.28% (t = 2.40, 485 merged non-overlapping cases); the 466 cases below the 50-bar average give +1.37% (t = 2.47); new lows without a large down day give -0.25% (t = -0.38, n = 321); and the excess is positive in all six coins, from +0.39% in XMR to +2.48% in ZEC, though no single coin reaches t = 2.
- F2: Large down days still help when they are not at a new low: those cases give +0.71% excess over 5 bars (t = 2.22, n = 1060). On all non-overlapping bars, days with z ≤ -20 give +0.96% (t = 1.56, n = 168). The large down move itself, more than the new low, seems to come before the rebound.
