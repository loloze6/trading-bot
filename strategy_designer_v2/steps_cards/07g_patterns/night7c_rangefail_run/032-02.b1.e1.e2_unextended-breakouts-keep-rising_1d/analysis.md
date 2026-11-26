---
line: 7.g patterns
backtest: 032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d
idea tested: 032-02.b1.e1.e2_unextended-breakouts-keep-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3889 USD
---
## Findings
- **F1:** Over the next 5 days, a coin's excess return (in usual moves) rises with where its close sits in its 60-day closing range: from -0.13 in the bottom quintile to +0.24 in the top quintile (t 3.30, 169 cases; Spearman rho 0.159, p < 0.0001, 846 non-overlapping cases); the same holds over 10 days (top quintile +0.29, t 2.97; rho 0.167, p 0.0006, 414 cases) and over 20 days (top quintile +0.50, t 2.75; rho 0.170, p 0.017, 198 cases).
- **F2:** In raw returns, 5-day cases with the close in the top fifth of the 60-day range (position at least 0.8) beat the coin's normal drift by +3.39 %, against -0.70 % for the middle of the range (Welch t 3.75, 192 against 354 cases), which is about 18 times the 0.19 % cost of a trade.
- **F3:** The range-position effect over 10 days points the same way in all six coins (rho from 0.086 for LTC to 0.252 for ETH; top-quintile excess from +1.2 % to +18.9 %) and in 2019, 2020 and 2021 (rho 0.36, 0.12, 0.04), but it reverses in 2018 (rho -0.34, top-quintile excess -16.3 %, 102 cases).
- **F4:** The distance of the close below its prior 60-day high gives the same picture: the 5-day excess is +0.26 in the quintile nearest the high (t 3.60) against -0.22 two quintiles lower (t -3.18), with rho 0.120 (p 0.0005, 846 cases); over 20 days it is +0.50 (t 3.42) against -0.34 (t -2.18), rho 0.179 (p 0.012, 198 cases).
- **F5:** The tested grading by prior 20-day run-up adds nothing: the 20-day excess by prior 20-day return quintile moves without order (rho 0.050, p 0.36, 342 cases), and the book's trades do not improve with the entry forecast (mean net P&L 9.3 %, 12.7 % and 7.5 % by forecast tercile). This matches step 5's unusual move of -1.83 % (t -0.60).
- **F6:** Daily coin returns are higher on Fridays (+0.545 %, t 3.75) and Saturdays (+0.584 %, t 4.24) than on other days. The gap is clear in 2018 (t 3.37) and 2019 (t 5.82), weaker in 2020 (t 1.88), and gone in 2021 (t -0.08), so it is not stable enough to carry an idea.
- **F7:** The book barely follows the coins window by window: its mean daily return is between -0.019 % and +0.094 % in every window, while the coins' mean daily return ranges from -0.473 % to +1.256 %. The book is in a position on only 18 % of coin-days.

## Ideas
- `032-02.b1.e1.e2.g1_top-of-range-closes-keep-rising` (from F1, F2, F3, F4): The higher a coin's daily close sits within its range of closes over the past 60 days, the larger its rise over the next 10 days, beyond its normal drift.
- `032-02.b1.e1.e2.g2_nearness-to-high-predicts-gains` (from F1, F4, F5): The closer a coin's daily close is to its highest close of the past 60 days, the larger its rise over the next 20 days, beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
