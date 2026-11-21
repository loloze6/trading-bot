---
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3723 USD
---
## Findings
- **F1:** The tested result is on the predicted side but small and short of the bar. The mean 18-bar unusual move is +0.20 % (t 1.29, 3109 cases), a strength of 0.023 against a usual move of 8.17 %. That is under half the 0.05 typical of real ideas, and only 1.1 times the 0.19 % round-trip cost. Other horizons are no clearer: t 0.39 at 1 day, 0.68 at 2 days and 1.18 at 6 days.
- **F2:** The breakout's direction depends on the coin's recent path. Breakouts made while the coin's 5-day return was positive were followed by +0.74 % unusual moves over 3 days (t 3.72, 2149 cases). Breakouts after a falling 5 days were followed by −1.16 % (t −4.50, 792 cases). The two signs cancel in the tested pool.
- **F3:** The same split holds on the 10-day return. Breakouts after a rising 10 days gave +0.54 % (t 2.52, 1816 cases) and those after a falling 10 days gave −0.42 % (t −1.68, 995 cases), a difference of +0.96 % (Welch t 2.92). Only the lowest 10-day-return quintile is negative (−1.01 % at 3 days, t −2.64; −1.85 % at 6 days, t −4.17). The other four quintiles all sit at +0.36 to +0.62 % over 3 days.
- **F4:** Inside rising stretches the effect is spread rather than held by one coin. After a rising 10 days, BTC gave +0.53 %, ETH +0.59 %, XRP +2.10 % (t 2.54) and ZEC +0.77 %, while LTC (−0.50 %) and XMR (−0.02 %) did not.
- **F5:** The effect is uneven over time. It is concentrated in 2020 (+1.54 %, t 3.85) and 2021 (+0.94 %); 2019 (−0.82 %, t −2.20) and 2022 (−0.72 %, t −1.95) go the other way. It is also uneven across windows, ranging from t −2.82 to +3.18.
- **F6:** The quietness grading is weak and not monotone.
- **F7:** With 3109 cases, a dispersion of 8.8 % per case and a mean of +0.20 %, this data cannot show the pooled effect clearly. Thirteen more coins are available in folds A and D, and some of them in B and C, which would roughly double or triple the case count.

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week.b1_quiet-week-breakout-more-coins` (from F1, F7): When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days. The rise is larger the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week.b2_breakout-after-rising-week` (from F2, F3, F4, F6): When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days, only while its 5-day return is positive. The rise is larger the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
