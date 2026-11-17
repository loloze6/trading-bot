---
line: 7.b inconclusive
backtest: 010-03_rsi-above-streak-continuation_1d
idea tested: 010-03_rsi-above-streak-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 1
cost: 0.1578 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar: the pooled 14-day slope t is 1.48 on 384 grid cases (199 with a forecast above 0); bars with a forecast above 0 average +0.0063 excess 14-day return against −0.0068 when flat, a gap whose Welch t is only 0.80.
- **F2:** Noise drowns the effect: the excess 14-day return's standard deviation is about 0.16 in every forecast bin, against a spread of about 0.05 between the bins' means (−0.024 to +0.027).
- **F3:** The effect is clearer at shorter horizons on the same bars. At 3 days the slope t is 2.14 on 1,907 non-overlapping cases (on-minus-off Welch t 2.67). At 7 days it is 1.92 on 815 cases (Welch t 2.59). At 21 and 28 days it is 0.94 and 1.73.
- **F4:** The gradient by stretch length is not monotone. Runs of 0–5 days average −0.0087 excess 14-day return (n 64), 5–15 days +0.0092 (n 53), 15–30 days +0.0237 (n 44) and 30–60 days +0.0076 (n 38), so the effect mostly appears in the middle of a stretch.
- **F5:** The effect is uneven. BTC has slope t 1.85 and ETH 0.42, on 192 cases each. Yearly slopes are positive in 2018–2020 and 2025 and negative in 2021–2024, all with |t| < 1.3 on 48 cases each. When the coin's 60-day return is positive the slope t is 1.55 (n 106), and −0.53 (n 86) when it is negative.
- **F6:** The test ran on only two coins, BTC and ETH, over 24 windows each; BNB was not run. The default data offers six coins (BTC, ETH, LTC, XMR, XRP, ZEC) over all four folds, so roughly three times the cases are available for a result that is on the predicted side but short of the bar.

## Ideas
- `010-03_rsi-above-streak-continuation.b1_rsi-above-streak-six-coins` (from F1, F2, F6): The longer a coin's 14-day RSI has stayed above 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days.
- `010-03_rsi-above-streak-continuation.b2_rsi-above-streak-one-week-continuation` (from F3, F2): The longer a coin's 14-day RSI has stayed above 50 without a break, measured in days up to the current close, the higher the coin's return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
