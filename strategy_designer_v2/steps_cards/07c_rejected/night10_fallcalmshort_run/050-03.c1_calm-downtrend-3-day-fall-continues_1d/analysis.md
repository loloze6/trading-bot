---
line: 7.c no effect
backtest: 050-03.c1_calm-downtrend-3-day-fall-continues_1d
idea tested: 050-03.c1_calm-downtrend-3-day-fall-continues
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4040 USD
---
## Findings
- **F1:** In the explore half's falling calm bars (BTC, XMR, XRP), a 3-day fall carries on only weakly: the short-side unusual move is +0.09 % over 2 days (t 0.17, 121 cases on 90 days), +1.23 % over 3 days (t 1.64, 84 cases, 63 days), +2.29 % over 5 days (t 1.81, 45 cases, 32 days) and +1.61 % over 7 days (t 0.64, 29 cases). The full test's +0.19 % over 3 days (t 0.58, 659 cases on 415 days) is the weakest of these readings, and the carry-on is largest at 5 days.
- **F2:** The size of the scaled fall barely grades the carry-on at the plan's horizon. Its rank correlation with the unusual move is 0.005 over 3 days and -0.10 over 7 days. The 3-day terciles give big +1.59 % (t 0.92), mid +1.40 % (t 1.49) and small +0.81 % (t 0.77); over 2 days the big tercile is -0.30 %. This matches the verdict's supporting check of -0.11 %.
- **F3:** The grade shows only at 5 days. The forecast's standardised value has a rank correlation of 0.21 with the 5-day unusual move (0.03 at 3 days), and the biggest tercile of 3-day falls gives +4.92 % over 5 days (t 1.78, 14 cases) against +0.26 % (mid) and +1.88 % (small).
- **F4:** The most extreme scaled falls reverse while moderate ones carry on. Over 3 days, falls beyond -1.5 usual swings give -2.63 % (t -0.87, 10 cases), and forecasts below -2 give -6.97 % (4 cases). Falls of -1.5 to -0.75 swings give +4.41 % (t 2.90, 14 cases). This hump is what flattens the linear grade.
- **F5:** Across all scaled 3-day moves in the profile, the next move follows the move's sign. The rank correlation with the forward return is +0.19 over 3 days (p 0.02) and +0.23 over 5 days (p 0.035). Part of this comes from rises being followed by further rises: the short-side unusual move after a rise is -3.32 % on XRP (t -1.68), -0.75 % on XMR and -0.27 % on BTC. That is long-side continuation, outside this research's box.
- **F6:** The 3-day carry-on after falls points the same way on every explore coin and year, but is sure on one coin only. XRP gives +1.78 % (t 2.33, 29 cases), BTC +0.98 % (t 0.89) and XMR +0.90 % (t 0.59). The years from 2018 to 2021 give +0.60 % to +1.74 %, each with t below 1.3.
- **F7:** Against the 0.29 % cost of a trade, the full test's 3-day total move of -0.09 % cannot pay. In the explore half, the short-side total move after falls is +0.42 % over 3 days and +0.92 % over 5 days, about 3 times the cost. This is the only horizon where the move could cover a trade.
- **F8:** The depth of the 60-day downtrend does not grade the carry-on. Over 3 days, a 60-day return below -30 % gives +1.98 % (t 2.02, 11 cases), -30 % to -20 % gives +0.11 % (t 0.07), and -20 % to -10 % gives +2.37 % (t 1.73).

## Ideas
- `050-03.c1.c1_calm-downtrend-fall-continues-5-days` (from F1, F3, F7): In a falling, calm market, a coin that has fallen over the last 3 days keeps falling over the next 5 days, and falls further the larger its 3-day fall is in units of its 30-day daily swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
