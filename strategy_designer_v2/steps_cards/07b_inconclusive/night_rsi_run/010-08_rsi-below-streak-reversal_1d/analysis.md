---
line: 7.b inconclusive
backtest: 010-08_rsi-below-streak-reversal_1d
idea tested: 010-08_rsi-below-streak-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2787 USD
---
## Findings
- **F1:** The tested effect points the way the idea predicts but is too small for 185 cases: the slope of the 14-day excess return on the forecast is +0.00186 (t 1.08); it is positive in both coins that ran (BTC t 0.82, n 89; ETH t 0.72, n 96); and the forecast thirds rise in order (-0.025, -0.005, +0.010 mean excess).
- **F2:** The data is too noisy for a gap that size: the 14-day excess returns have a standard deviation of about 0.14–0.19 in every run-length bin, while the bin means differ by only about 0.05; and only BTC and ETH ran (BNB is missing), giving 185 grid bars.
- **F3:** The gain sits in the longest runs. Runs of 30 days or more below 50 average +0.031 excess (n 32), against -0.015 for shorter runs (n 153; Welch t 1.28). With the longest runs left out, the slope's t falls to 0.17.
- **F4:** The effect shows only after deep falls. Among grid bars in the bottom third of 30-day return (mean -30.5%, n 38), the slope's t is 2.28. In the middle third it is -0.47 and in the top third -0.12 (n 37 and 38).
- **F5:** The effect varies across years. The slope's t is 2.56 in 2018 (n 37) but -1.23 in 2025 (n 22). The longest runs average +0.081 excess in 2018 (n 12) but -0.006 in 2022 (n 11).
- **F6:** The plan's 14-day horizon is not where a stronger effect hides. The slope's t is 0.94 at 7 days (n 406) and -0.38 at 28 days (n 95).

## Ideas
- `010-08_rsi-below-streak-reversal.b1_rsi-below-streak-reversal-more-coins` (from F1, F2): The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days.
- `010-08_rsi-below-streak-reversal.b2_long-slide-exhaustion-rebound` (from F3, F4): The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days, and the more so the further the coin has fallen over its past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
