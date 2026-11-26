---
line: 7.g patterns
backtest: 061-01.g1.d1.d2.g3_calm-only-large-rises-continue_1d
idea tested: 061-01.g1.d1.d2.g3_calm-only-large-rises-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3997 USD
---
## Findings
- **F1:** In calm markets the 3-day return measured in 30-day daily swings is graded against the unusual 5-day move that follows: slope +0.0201 per swing unit, t 2.85, over 744 cases on 187 days. In agitated markets the same slope is +0.0048, t 0.55, over 551 cases on 165 days.
- **F2:** The calm-market grading holds on both sides over 5 days. Cases whose 3-day return is at least one swing up have an unusual move of +3.28 % (t 2.05, 96 cases, 46 days). Cases at least one swing down have −4.17 % (t −1.91, 78 cases, 35 days). The middle cases have +0.31 % (t 0.48, 570 cases). The agitated equivalents are +1.98 % (t 0.93) and −1.19 % (t −0.47).
- **F3:** A 3-day or 5-day return carries the calm-market grading better than the tested 1-day rise. Over 5 days the 1-day z gives slope t 2.53, the 3-day z gives t 2.85 and the 5-day z gives t 2.75. Over 3 days the 1-day z gives t −0.07 while the 3-day z gives t 2.05 and the 5-day z gives t 2.47. Over 10 days the 3-day z gives t 2.18 and the 5-day z gives t 2.05.
- **F4:** The calm-market slope of the 3-day z on the 5-day unusual move is positive in every trend and on every coin. By trend it is choppy +0.045 (t 2.49), falling +0.026 (t 2.24) and rising +0.025 (t 2.14). By coin it runs from +0.020 (BTC, t 1.66) to +0.048 (XRP, t 1.89). By window it is positive in 9 of 12, with w8 at −0.012 and w12 and w15 near 0.
- **F5:** The tested signal is weak because the strongest calm-market evidence sits in cases the long-only book ignores. In calm markets, days below −2 swings are followed by −3.39 % (17 cases), and 3-day falls below −2 swings by −8.98 % (t −1.83, 22 cases, 9 days). The tested idea's own size is only +0.39 % (t 0.87, 517 days).
- **F6:** Against a trade cost of 0.19 %, the calm 3-day-move cases are large. Those at least one swing up move +3.28 % unusual. Those at least one swing down move 4.17 % unusual on the short side, and about 3.5 % total after the coin's +0.64 % normal 5-day drift works against the short. So the falling side's move per case is many times the cost.

## Ideas
- `061-01.g1.d1.d2.g3.g1_calm-three-day-move-continues` (from F1, F2, F3, F4, F6): In a calm market, the larger a coin's 3-day return against the standard deviation of its daily returns over the past 30 days, the further the coin keeps moving the same way over the next 5 days. This holds for rises and for falls.
- `061-01.g1.d1.d2.g3.g2_calm-three-day-fall-continues` (from F2, F5, F6): In a calm market, the larger a coin's 3-day fall against the standard deviation of its daily returns over the past 30 days, the further the coin keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
