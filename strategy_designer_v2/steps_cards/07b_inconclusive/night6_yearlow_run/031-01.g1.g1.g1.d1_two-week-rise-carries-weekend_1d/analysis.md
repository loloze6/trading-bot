---
line: 7.b inconclusive
backtest: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend_1d
idea tested: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3255 USD
---
## Findings
- **F1:** Step 5's slope is on the side the idea predicts but short of the bar (slope 0.00044, clustered t 1.29, 1215 cases on 319 Fridays), while the level of the effect is clear: Friday cases with a forecast above 0 earn +0.91 % above the coin's 2-day drift (t 3.37 over 291 days, strength 0.136), and Fridays after a 14-day fall earn −0.31 % (t −1.04, 1041 cases).
- **F2:** Over all Fridays, the raw volatility-scaled 14-day rise predicts the weekend's excess return, with a day-clustered slope t of 2.96 (2046 cases, 341 days). The quintiles climb from −0.38 % and −0.49 % through +0.31 % and +0.43 % to +1.57 % (t 3.79), so the grading spans the whole range of the rise.
- **F3:** The test kept only forecasts above 0, which cuts the range in half, and inside that half the gradient is noisy. The clustered slope t is 1.86 on the forecast and 1.61 on the raw rise (1005 cases, 265 days). The forecast quartiles give +0.56 %, +0.34 %, +1.06 % and +1.71 %, so the gradient mostly lives in the top half.
- **F4:** The effect is spread across the data, not confined to one part of it, so it is too thin for six coins rather than mixed. Among cases with a forecast above 0, the weekend excess is positive in all 6 coins (+0.21 % for BTC up to +1.37 % for XRP). It is positive in 7 of 8 years (2022: −0.19 %). On all Fridays, the per-coin slope on the raw rise is positive for all 6 coins (t from 0.79 for XMR to 3.01 for ETH).
- **F5:** The link is not unique to Friday. On a 2-day grid, the clustered slope on the 14-day rise is t 2.49 on Thursdays and 1.71 on Fridays. On Monday to Wednesday it is near 0 (t −0.08 to 0.50), and on Saturday and Sunday it is 0 or negative (t −0.02 and −0.85).

## Ideas
- `031-01.g1.g1.g1.d1.b1_two-week-rise-carries-weekend` (from F1, F3, F4): The higher a coin's 14-day rise, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following Saturday and Sunday together.
- `031-01.g1.g1.g1.d1.b2_two-week-rise-carries-week-end` (from F2, F5): The higher a coin's 14-day return, measured in its usual daily moves at Thursday's or Friday's close (UTC), the more it rises over the following two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
