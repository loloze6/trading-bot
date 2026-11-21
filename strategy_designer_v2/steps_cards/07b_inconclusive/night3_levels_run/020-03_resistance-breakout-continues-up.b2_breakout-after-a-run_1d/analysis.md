---
line: 7.b inconclusive
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3506 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but stops short of the bar. Over 1,292 grid cases at 5 days, the mean unusual move is +0.57 % with t 1.81 and a strength of 0.048. The same cases measured at other horizons give t 2.58 at 3 days (+0.60 %, 1,313 cases), t 1.85 at 10 days (+0.93 %) and t 2.30 at 20 days (+2.05 %, 1,154 cases). The effect is positive at every horizon from 1 to 20 days.
- **F2:** A heavy right tail of large rises carries the mean, and it inflates the spread that the t divides by. The median 5-day unusual move is −0.80 %, only 46 % of cases are positive, and the skew is 1.43. The top 5 % of cases sum to +19.6 against +7.4 for all cases. Clipped at the 5th and 95th percentiles, the mean is +0.31 % against a standard deviation of 11.3 %.
- **F3:** The effect changes sign with the market's longer trend.
- **F4:** Breaks taken while the coin's 60-day return is positive carry the effect, and the others carry almost none. With a positive 60-day return, the 5-day unusual move is +1.68 % (t 2.99, 422 cases). Otherwise it is +0.37 % (t 0.59, 214 cases). By 60-day-return tercile, the move is +0.33 %, +1.67 % (t 2.34) and +1.70 % (t 1.98).
- **F5:** The run-up that matters is the last 10 days, not the plan's 20.
- **F6:** The effect differs across coins.
- **F7:** The move is large enough to pay, so the open question is whether it is real, not whether it covers costs. The total move is +1.13 % per case, 5.8 times the 0.19 % round-trip cost, and the unusual move alone is 2.8 times it. The book passed every check (Sharpe 0.89, 0.34 above holding), consistent with run finding F11.
- **F8:** More data is available than the test used. It ran on 6 coins, while 13 more coins have daily bars in folds A and D and in part of B and C. At the measured spread, about 1.3 times the cases would lift t from 1.75 past 2 if the mean holds. Run finding F7 warns, though, that falls the coins share, as in 2018 and 2022, do not shrink with more coins.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins` (from F1, F2, F7, F8): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, and the larger its 20-day return before the break and the more times the level held, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend` (from F3, F4, F5, F7): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return is positive, and the larger its 10-day return before the break, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
