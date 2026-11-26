---
line: 7.g patterns
backtest: 032-02.b1.e1_quiet-breakouts-continue-longer_1d
idea tested: 032-02.b1.e1_quiet-breakouts-continue-longer
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4826 USD
---
## Findings
- **F1:** Across all coins and bars, the next day's unusual return rises step by step with the size of a down day measured against the coin's 20-day daily volatility: +1.51 % (t 3.58, 220 cases) after a fall of more than 2 standard deviations, +0.65 % (t 2.90, 675) after a fall of 1 to 2, and +0.14 % (t 1.40, 2632) after a fall of 0 to 1.
- **F2:** After an up day of 1 to 2 standard deviations, the unusual move over the next 5 days is +3.03 % (t 2.39, 107 non-overlapping cases). After an up day of more than 2, it is +4.97 % (t 2.36, 47). After up days of 0 to 1 it is only +0.39 % (t 0.68, 469). Large up days are followed by more rise, not by a give-back.
- **F3:** The tested signal's unusual move arrives early and then stops growing. Over 164 first-per-cell cases it is +2.90 % by day 3 (t 3.13), +3.31 % by day 5 (t 3.04), +6.17 % by day 10 (t 3.23) and +5.83 % by day 20 (t 2.75).
- **F4:** The idea's grading by the breaking day's gain is absent. The unusual 10-day move is +6.6 % (t 2.25), +5.0 % (t 2.09) and +6.7 % (t 1.53) across the low, mid and high gain terciles. The book's trades by entry-forecast tercile show the same lack of order: +14.6 %, +6.7 % and +15.0 % net, 73 trades each.
- **F5:** The book's 219 trades earned a mean of +12.1 % net (median +5.5 %, 70 % positive) and were held a mean of 18.5 days, well past the plan's 10, with a maximum of 122 days. The 5 best trades carry 28 % of the summed net profit.
- **F6:** The signal's gain is uneven across coins. ETH shows +10.6 % (t 3.37, 28 cases), while BTC shows −0.2 % (t −0.09, 25) and ZEC −0.2 % (t −0.09, 33).
- **F7:** Downside breaks of the 60-day low in coins with the lowest efficiency ratio continue rather than fail: −9.5 % unusual over 10 days (t −2.71, 26 cases). This is not graded across the quartiles (+6.3 %, −3.8 %, +3.0 %), so I read it as not distinguishable from chance given the many angles examined.

## Ideas
- `032-02.b1.e1.g1_next-day-rebound-after-shocks` (from F1): The larger a coin's fall over the past day relative to its usual daily move over the past 20 days, the larger its rise over the next day.
- `032-02.b1.e1.g2_big-up-days-keep-rising` (from F2, F4): The larger a coin's rise over the past day relative to its usual daily move over the past 20 days, the larger its further rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
