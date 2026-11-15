---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3948 USD
---
## Findings
- **F1:** The main measure's positive result comes from a handful of extreme blocks, not from a steady drift. The block mean is 0.126 with t 1.73 over 811 blocks, but removing the 5 largest blocks drops it to 0.005 with t 0.11 (806 blocks). Winsorising at 1% gives 0.056 with t 1.21.
- **F2:** On a typical bar above the average, the coin lags holding it. On the 399 non-overlapping 20-day grid bars with forecast > 0, the median excess return is -0.036, only 40.6% beat holding, and the skew is 7.4. The mean of +0.005 (t 0.32) is a right tail on a losing middle.
- **F3:** Being above the 200-day SMA adds nothing measurable over being below it at any horizon. Above-minus-below excess return is 0.0019 at 5 days (Welch t 0.50), 0.0053 at 20 days (t 0.27), -0.016 at 40 days (t -0.35) and 0.059 at 60 days (t 0.66).
- **F4:** The grading the idea relies on does not appear. The Spearman correlation between forecast and the next 20-day excess return is 0.043 (p 0.39). The 20-day excess return by percent distance above the average is not monotone across its quartiles (0.005, -0.019, 0.031, 0.004).
- **F5:** The result flips sign across periods. Block means are -0.150 (t -3.02) in 2018 and -0.036 (t -1.96) in 2022, against 0.461 (t 2.03) in 2020. It also differs across coins, from XMR at -0.096 (t -1.00) to ZEC at 0.370 (t 1.27).
- **F6:** Recent strength gives no reliable split either. Above-average bars after a rising 20 days returned 0.033 against -0.028 after a falling 20 days (Welch t 1.63). That drops to t 1.29 when winsorised, and the Spearman correlation of past 20-day return with the next 20-day excess return is 0.010 (p 0.85).
- **F7:** The book's gain is mostly the market's own rise rather than timing. The market part is 0.000344 a day and timing is 0.000237 a day, out of 0.000581.

## Ideas
- No ideas: The trend effect is not there. Being above the 200-day average gives no excess over being below it (F3), grading by distance shows nothing (F4), a typical bar above the average underperforms holding (F2), and the near-significant t rests on five outlier blocks (F1) in a sign that flips between years (F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
