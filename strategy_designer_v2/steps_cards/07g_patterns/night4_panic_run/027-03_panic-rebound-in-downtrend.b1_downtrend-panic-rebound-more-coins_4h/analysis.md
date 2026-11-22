---
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h
idea tested: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4571 USD
---
## Findings
- **F1:** The ratio of a coin's 5-day to its 30-day volatility of 4h returns grades its 14-day return over its normal drift: the top quintile earns +4.99 % (t 3.64, 298 non-overlapping cases) and the bottom quintile −4.40 % (t −3.93, 298), rising steadily through −1.34 %, +0.34 % and +1.24 % in between. The per-coin Spearman correlation is positive in all 19 coins (mean 0.215, minimum 0.058), and top minus bottom is positive in 6 of 8 years (+0.13 to +0.23 in 2020, 2021, 2023, 2024 and 2025).
- **F2:** The F1 effect holds whatever the coin's prior trend. With a positive 30-day return, the 14-day excess goes from −3.99 % (t −2.68, 129) to +6.83 % (t 3.34, 147). With a negative one, it goes from −4.94 % (t −3.14, 177) to +3.68 % (t 2.05, 159). At 3 days the top quintile alone earns +1.72 % (t 4.99, 981) when the prior return is positive.
- **F3:** Large falls do bounce, but only briefly. The bottom quintile of the 24-hour return earns +0.43 % over the next day (t 6.00, 7335 cases). In volatility-scaled terms (the 24-hour return over 30-day volatility), the bottom quintile earns +1.87 % over the next 3 days (t 6.04, 935) when the prior 30-day return is positive, but only +0.42 % (t 1.44, 827) when it is negative. The 1-day bounce is positive in 7 of 8 years and strongest in 2018–2021 (+0.46 % to +1.22 %).
- **F4:** Over 14 days the same bottom 24-hour-return quintile loses −3.33 % against drift (t −4.19, 436). In coins with a negative 30-day return, mid-to-large 24-hour drops (the tested situation) lose −3.72 % over 7 days (t −6.41, 348) and −3.82 % over 14 days (t −2.46, 152). The bounce is spent before the tested horizon, which matches the rejected verdict (−2.35 % per case, t −5.29).
- **F5:** In the book, trades held over 40 days lost −6.18 % each on average (1203 trades). Trades held 21–40 days gained +17.71 % (860 trades), and trades held under 7 days gained +1.07 % (667 trades). The losses sit in long holdings in persistent downtrends.

## Ideas
- `027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.g1_volatility-expansion-precedes-gains` (from F1, F2): The more a coin's volatility over the last 5 days exceeds its volatility over the last 30 days, the higher its return over the next 14 days, both when its 30-day return was rising and when it was falling.
- `027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.g2_short-panic-rebound-in-uptrends` (from F3, F4): The deeper a coin's 24-hour fall, measured in units of its 30-day volatility, the higher its return over the next 3 days, and the larger that rebound when the coin's 30-day return before the fall was positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
