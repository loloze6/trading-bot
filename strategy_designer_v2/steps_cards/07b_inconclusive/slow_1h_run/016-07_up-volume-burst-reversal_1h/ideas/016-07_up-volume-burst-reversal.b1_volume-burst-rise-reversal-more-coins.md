---
brief: 016_grind-versus-jump-moves
source-idea: 016-07_up-volume-burst-reversal
line: 7.b inconclusive
backtest: 016-07_up-volume-burst-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of that period's volume traded in its few busiest hours, the more of the rise the coin gives back over the next 3 days.
Consequence: Up moves made with a burst of volume are forced flow that overshoots, so they partly reverse.
Why:
- F1: The test's main result points the way the idea predicts but falls short of the bar: top-third minus bottom-third excess 72-bar return was -0.0044 (Welch t -1.10, 972 grid samples per third). The concentrated third's own mean was +0.0007, so the supporting check failed.
- F2: Every way of measuring concentration gives the same weak negative sign over 72 hours. The raw top-3 volume share gives -0.0005 vs +0.0041 (t -1.15, 2,865 samples). Thirds ranked within each coin give -0.0017 vs +0.0042 (t -1.46, 958 per third). After controlling for the size of the rise, the share's OLS slope is -0.030 (t -1.69). Overall the effect is small against the noise: Spearman rho is -0.007 (p 0.72).
- F3: The effect is mixed across coins and years. Only ZEC reaches significance (top -0.0150 vs bottom +0.0126, t -2.18, n 474). XMR, BTC and ETH lean the other way (t +0.96, +0.34, +0.17). By year the t-statistics run from -0.85 to +1.01 with no stable sign.
