---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
idea tested: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5490 USD
---
## Findings
- **F1:** The tested idea is real but far too small to pay for a trade. Its unusual move is +0.12 % per case over 5 days, a strength of 0.004, about a tenth of the usual 0.05 (findings F10). Its total move is +0.07 %, which is 0.4 times the 0.19 % cost of a round trip. The book earns 0.044 % a day against the 0.05 % required, with a Calmar of 0.26.
- **F2:** A coin's 14-day return predicts its next 7 days in the same direction, and the effect is graded. The slope of strength on the coin's own rank is +0.31 (t 3.97, 1916 non-overlapping cases), positive in 6 of 6 coins. The top 20 % of 14-day returns are followed by an unusual move of +2.6 % (strength 0.20) and a total move of +3.8 %, about 20 times the cost of a round trip.
- **F3:** This continuation is carried mostly by the later windows, so it may not be stable.
- **F4:** The continuation fades as the past period and the horizon lengthen.
- **F5:** The 28-day return scaled by 30-day volatility predicts the next 7 days. Its slope is +0.25 (t 3.12, 1779 cases), positive in 6 of 6 coins, with t 3.40 in w13–w24 against 0.58 in w1–w12.
- **F6:** The tested book takes none of this momentum. Its position has a correlation of -0.04 with the 28-day return, and its forecast -0.09.
- **F7:** Weekday effects look large but are not stable across years, and they are not graded, so they support no idea.
- **F8:** The other quintile tables are not monotone and read as chance given about 40 angles examined. These include the last day's return (2nd quintile t -3.65, extremes both positive), the range against its 30-day mean (2nd quintile t -3.14), volatility and nearness to the 60-day high.

## Ideas
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.g1_two-week-return-continues-weekly` (from F2, F3, F4, F1): For a coin, the higher its 14-day return, the higher its return over the next 7 days.
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.g2_volatility-scaled-monthly-trend-continues` (from F5, F3, F4, F1): For a coin, the larger its 28-day return measured against its 30-day volatility, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
