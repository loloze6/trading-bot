---
line: 7.b inconclusive
backtest: 054-04.b1_reclaimed-low-after-rise_1d
idea tested: 054-04.b1_reclaimed-low-after-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2209 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but rests on few cases: step 5's mean unusual 10-day short move is +3.72 % per case (strength 0.220 of a usual 14.49 % move) with t 1.48 over only 39 cases on 31 days, and the supporting check passed (+12.3 % larger-forecast half minus smaller half). It is short of the t ≥ 2 bar because the cases are few, not because the effect is small.
- **F2:** In folds B and C, the grading the idea claims is clear among agitated reclaim days. The Spearman correlation between the prior 60-day return and the next 10-day unusual return is -0.50 over 45 cases. Reclaims after a 60-day rise moved -18.2 % unusual over 10 days (t -4.39, 10 cases). Those after a 60-day fall moved +0.3 % (t 0.13, 48 cases).
- **F3:** The book's own short bets in agitated markets (forecast ≤ -2) were followed by -13.5 % unusual over 10 days (t -3.10, 13 cases) and -22.9 % over 20 days (t -3.56). Agitated reclaims without a bet moved +0.2 % (t 0.08, 45 cases). The effect sits in the strongest cases, and the test had few of them.
- **F4:** Taken together, agitated reclaims show no clear move: -2.9 % over 10 days (t -1.17, 58 cases). By year they flip sign: +2.7 % in 2018 and +4.5 % in 2021, against -10.3 % in 2019 and -9.6 % in 2020. Only the prior-rise grading carries the result.
- **F5:** The same grading shows across all reclaim days in every profile. By quartile of the prior 60-day return, the 10-day unusual move goes +1.8 % (t 0.50), -4.3 % (t -1.34), -9.8 % (t -3.67), -11.0 % (t -4.54), with 27 to 31 cases each. Calm reclaims after a rise moved -9.5 % (t -6.14, 8 cases).
- **F6:** More data is available than the test used. The test ran on 6 coins, while folds A and D hold up to 19 coins, so the tested idea can gather more of its rare strong cases unchanged.

## Ideas
- `054-04.b1.b1_reclaimed-low-after-rise` (from F1, F2, F3, F6): In an agitated market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it falls over the next 10 days, and the fall is larger the higher the coin's 60-day return before that day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
