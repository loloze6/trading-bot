---
line: 7.b inconclusive
backtest: 010-01_rsi-above-share-continuation_1d
idea tested: 010-01_rsi-above-share-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2757 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar: the slope t is +1.65 on 384 independent 14-day samples, positive-forecast samples beat negative-forecast samples by +0.029 in mean excess 14-day return (+0.013 against −0.016), and both coins point the same way (BTC t +1.28, ETH t +1.10, 192 samples each), yet only BTC and ETH ran because BNB is absent from the record.
- **F2:** The slope has the same positive sign at every horizon, and its t follows the number of cases: +2.31 with 1,907 samples at 3 days, +1.85 with 815 at 7 days, +1.65 with 384 at 14 days and +1.26 with 192 at 28 days, so the 14-day test is short of cases rather than wrong in sign.
- **F3:** The pooled slope comes from differences between windows, not within them, so the effect is mixed across periods: the between-window t is +9.26 over 48 coin-windows, the within-year t is −0.16, the within-window t is −2.54, only 35% of the 48 windows have a positive slope, and only 2 of 8 years (2019 t +1.56, 2025 t +1.74) have a positive slope.
- **F4:** The effect is not graded evenly across forecast quintiles: the top quintile (forecast +15.5) earns +0.032 excess over 14 days, but the second-lowest quintile earns −0.051 while the lowest earns +0.008, so the gain sits at the extremes and is noisy with 77 samples per quintile.
- **F5:** The book earns from timing, not from the market's rise: Sharpe 0.83 (0.19 above holding), mean daily gain 0.00102, of which 0.00099 is timing and 0.00003 is market rise, but it failed on Calmar 0.58.

## Ideas
- `010-01_rsi-above-share-continuation.b1_rsi-share-more-coins` (from F1, F2, F3): The larger the share of the past 30 days that a coin's 14-day RSI has spent above its midpoint of 50, the higher the coin's return over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
