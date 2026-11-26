---
line: 7.b inconclusive
backtest: 060-01.b1.d1.b1.b1_deep-slide-bounce-fades-overnight_1d
idea tested: 060-01.b1.d1.b1.b1_deep-slide-bounce-fades-overnight
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4190 USD
---
## Findings
- **F1:** The tested effect is on the predicted side but too noisy across days to clear the bar. In the visible folds B and C, the next-day gain of the short against the coin's mean averages +1.04 % per case (t 3.49 over 431 cases). Taken as one mean per day, it is +0.72 % with t 1.60 over 190 days. Step 5's weighted main measure gives t 1.58 over 535 days, and all of the 1d data in the four folds was already used, so no more data is available at this bar.
- **F2:** The plan's horizon is the right one. Per case, the gain is +1.04 % at 1 day (t 3.49), +0.79 % at 2 days (t 1.80), +0.57 % at 3 days (t 1.23) and +0.13 % at 5 days (t 0.24). The 1-day gain is positive in every year shown: 2018 +1.50 %, 2019 +0.71 %, 2020 +0.71 %, 2021 +1.11 %.
- **F3:** The largest bounces carry none of the effect. Next-day gain by terciles of the size of the up day, one mean per day:
- **F4:** The effect is graded at the shallow end of the 5-day fall and flat at the deep end. Next-day gain by terciles of the depth forecast, one mean per day:
- **F5:** The cases cluster on market-wide days, which is what makes the per-day t low. There are 2.26 cases per day on average, and 63 % of cases fall on days with 3 or more coins. Days with 4 or more coins average +1.54 % (t 1.60, 38 days), against +0.38 % (t 0.57, 109 days) for days with a single coin.

## Ideas
- `060-01.b1.d1.b1.b1.b1_small-bounce-deep-slide-fades` (from F1, F2, F3, F4): In a falling, agitated market, a coin's one-day rise that comes after a fall over its last 5 days is followed by a fall over the next day that grows with the depth of that 5-day fall and shrinks with the size of the rise itself, both measured against the standard deviation of its daily returns over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
