---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3252 USD
---
## Findings
- **F1:** The next-day reversal after a vol-scaled daily move holds only when volatility is high: in the top tercile of each coin's 20-day volatility, the slope of next-day excess return on the day's vol-scaled return is -0.0055 (t -5.74, n 1757). The middle tercile shows nothing (slope -0.0004, t -0.49), and the bottom tercile turns positive, i.e. continuation (slope +0.0018, t +2.94, n 1755).
- **F2:** The pattern is graded and fits one model: regressing next-day excess return on z, the coin's volatility rank and their product gives z +0.0045 (t 4.85) and z×vol-rank -0.0118 (t -7.41), so the reversal strengthens steadily as volatility rises and flips to continuation at low volatility.
- **F3:** In the high-volatility tercile the effect runs through the vol-scaled quintiles: from the largest falls to the largest rises, next-day excess returns are +0.0114 (t 3.78), +0.0035, +0.0012, -0.0044 (t -1.78) and -0.0064 (t -2.83), each with about 350 bars.
- **F4:** The high-volatility reversal is not one period's or one coin's: its slope is negative in all 8 years (t below -2 in 2018, 2020, 2021, 2022 and 2025), and negative in both coins (BTC -0.0042, t -3.84; ETH -0.0072, t -4.41).
- **F5:** In the low-volatility tercile the bottom z quintile is followed by -0.0030 (t -1.62) and the top quintile by +0.0034 (t +1.96), with positive slopes in both coins (BTC t 2.22, ETH t 2.01), so the low-volatility side is weaker but has the same sign throughout.
- **F6:** The book's mixed use of regimes costs it money: its pre-fee position gain per bar is -0.0011 in the low-volatility tercile against +0.0016 in the high tercile. Overall the pre-fee gain is 0.00023 per bar against fees of 0.00036 per bar, at a mean turnover of 0.44 of the book per bar. This explains the negative Sharpe of -0.19 despite the confirmed forecast (t 2.28).

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal` (from F1, F2, F3, F4, F6): The higher a coin's 20-day daily volatility stands against its own past year, the more strongly its next 1 day reverses a vol-scaled 1-day move: the larger the day's fall in units of 20-day volatility, the more it rises over the next 1 day, and the larger the day's rise, the more it falls.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g2_calm-market-one-day-continuation` (from F1, F2, F5, F6): When a coin's 20-day daily volatility is low against its own past year, its vol-scaled 1-day return carries into the next 1 day: the larger the day's rise in units of 20-day volatility, the more it rises the next day, and the larger the fall, the more it falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
