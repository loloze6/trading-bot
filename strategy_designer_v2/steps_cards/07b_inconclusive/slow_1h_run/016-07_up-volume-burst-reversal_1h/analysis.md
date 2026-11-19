---
line: 7.b inconclusive
backtest: 016-07_up-volume-burst-reversal_1h
idea tested: 016-07_up-volume-burst-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3047 USD
---
## Findings
- **F1:** The test's main result points the way the idea predicts but falls short of the bar: top-third minus bottom-third excess 72-bar return was -0.0044 (Welch t -1.10, 972 grid samples per third). The concentrated third's own mean was +0.0007, so the supporting check failed.
- **F2:** Every way of measuring concentration gives the same weak negative sign over 72 hours. The raw top-3 volume share gives -0.0005 vs +0.0041 (t -1.15, 2,865 samples). Thirds ranked within each coin give -0.0017 vs +0.0042 (t -1.46, 958 per third). After controlling for the size of the rise, the share's OLS slope is -0.030 (t -1.69). Overall the effect is small against the noise: Spearman rho is -0.007 (p 0.72).
- **F3:** The effect is mixed across coins and years. Only ZEC reaches significance (top -0.0150 vs bottom +0.0126, t -2.18, n 474). XMR, BTC and ETH lean the other way (t +0.96, +0.34, +0.17). By year the t-statistics run from -0.85 to +1.01 with no stable sign.
- **F4:** The give-back shows mainly after the smallest rises. In the bottom third of 3-day rise size, the concentrated minus even difference is -0.0079 vs +0.0029 (t -1.72, n 950). It is near zero after mid rises (t -0.28) and big rises (t -0.12), where the market's continuation of the rise dominates: the past-rise OLS slope is +0.065 (t 2.74).
- **F5:** The mirror effect after 3-day falls is clearer. Falls with the most concentrated volume did better than evenly traded falls by +0.0028 vs -0.0027 over the next 24 hours (t 2.20, 2,732 samples), and by +0.0010 vs -0.0085 over 144 hours (t 1.65). This fits the brief's claim that jump-made moves partly reverse.

## Ideas
- `016-07_up-volume-burst-reversal.b1_volume-burst-rise-reversal-more-coins` (from F1, F2, F3): When a coin has risen over the past 3 days, the larger the share of that period's volume traded in its few busiest hours, the more of the rise the coin gives back over the next 3 days.
- `016-07_up-volume-burst-reversal.b2_volume-burst-fall-rebound` (from F5): When a coin has fallen over the past 3 days, the larger the share of that period's volume traded in its 3 busiest hours, the more of the fall the coin recovers over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
