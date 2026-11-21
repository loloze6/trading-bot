---
line: 7.b inconclusive
backtest: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d
idea tested: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3739 USD
---
## Findings
- **F1:** The mean unusual move after an upward cloud cross comes from a few extreme cases, not from the typical case. Over 129 recomputed 40-day cases the mean is +9.3 % (t 1.72) but the median is −2.1 %. Without the 5 largest cases (the top one is ZEC in 2025 at +518 %) the mean is +0.13 % (t 0.05). The mean of log moves is +1.1 % (t 0.36). The +18.95 % mean of step 5's supporting check is therefore not a typical move.
- **F2:** The grading by the forecast (the standardised 60-day return) is absent rather than weak. The 40-day unusual move by forecast quartile is −9.2 %, +36.2 %, −6.5 % and +36.0 %, with no order. The rank correlation is 0.06 (p 0.47) on 129 cases and 0.13 (p 0.26) on the 77 cases with a positive forecast. This matches step 5's slope t of 0.14 and makes it a zero result, not one short of the bar.
- **F3:** Other horizons do not rescue the 60-day grading. The forecast slope's t is 1.16 at 10 days, 1.81 at 20 days, 0.88 at 40 days and −0.70 at 60 days. The 20-day value is the highest but still short of 2, on 170 cases.
- **F4:** The effect depends on the market's period more than on the cross. The mean 40-day unusual move is −36.5 % in 2018 (0 of 11 cases up) and −4.9 % in 2022 (33 % up), against +23.9 % in 2020 (74 % up). On XRP only 32 % of 28 cases end above the drift (median −6.0 %), yet its mean is +10.1 % because of two cases of +283 % and +221 %.
- **F5:** The one variable that grades the move after the cross is the coin's own past volatility, in the opposite direction to a "bigger breakout" reading. Over 81 cases, the lower the 30-day volatility of daily returns at the cross, the larger the 40-day unusual move: rank correlation −0.32 (p 0.003) on simple moves and OLS t −2.73 on log moves. A rising leading cloud line over the past 5 days points the other way, with rank correlation +0.32 (p 0.044), but on only 39 cases.
- **F6:** The 60-day return can only be recomputed inside a window for 35 of 129 cases, because windows hold about 122 daily bars. The forecast built with warm-up history correlates 0.70 with it, so the tested grading is close to the idea's own but sits on a short history per window.
- **F7:** Size is not the problem. The measured unusual move is 98 times the 0.19 % cost of a buy and a sell, and the total move 123 times. The book still fails on mean daily return (0.033 % against 0.05 %) and on trades per day (0.007): it trades too rarely, not too thinly.

## Ideas
- `021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold.b1_calm-market-cloud-breakout` (from F5, F2, F1, F4): After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises more than usual over the next 40 days, and the lower the volatility of the coin's daily returns over the past 30 days, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
