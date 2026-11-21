---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4003 USD
---
## Findings
- **F1:** The pattern that stands out most is a rebound after a downward break out of wide ranges. When a 4h close falls below the prior two days' lowest low and those two days' bars were wide (top fifth of mean bar range against the 30-day average range), the coin rises over the next three days by 1.80 % more than its drift (t 4.43, 520 cases, about 9 times the 0.19 % cost). After the narrowest fifth, by contrast, the same break continues down by 1.07 % (t 2.73), and the three middle fifths sit near zero (0.13 % to 0.23 %).
- **F2:** That rebound is graded and broad. It grows with the size of the break (terciles: 1.25 %, 1.82 %, 2.33 %, t 1.97 to 2.87), it is positive on 6 of 6 coins (0.44 % to 3.17 %) and in 7 of 8 years, and it builds with time (1.05 % over 1 day, 1.80 % over 3 days, 2.03 % over 6 days).
- **F3:** Upward breaks during a falling week are followed by falls, which is what the tested idea's regime filter excludes. Over the next three days they fall 0.69 % against drift (t -2.76, 861 cases), and the deeper the 7-day fall, the larger the drop (deepest quartile -1.82 %, t -3.37; next quartile -0.79 %; upper two quartiles near zero). The fall shows on 6 of 6 coins and in 5 of 8 years.
- **F4:** The tested idea's gain sits only in its largest breaks. In rising weeks the top eighth of breaks gains 2.45 % (t 2.68) and the next eighth 0.92 %, while the other six eighths range from -0.42 % to +0.34 %. This step shape, not a straight line, explains why the median-split check failed. The top quarter is also concentrated on XRP (5.11 % of the coin's move, against -0.27 % to 2.03 % for the others).
- **F5:** The brief's premise that narrow ranges precede larger moves is not seen. The mean absolute 3-day move, in units of the coin's usual move, is 0.676 after the narrowest third of 2-day ranges and 0.734 after the widest.
- **F6:** The 4h bar opening at 16:00 UTC gains 0.099 % on average (t 6.6) and Friday bars gain 0.101 % (t 6.2). The 16:00 gain is positive in all 8 years and on all 6 coins, but both are about half a 0.19 % round trip.
- **F7:** The book lags holding the coins in rising years and leads in falling ones. Its mean daily return was 0.183 % against 0.409 % for holding in 2021 and 0.117 % against 0.244 % in 2024. It led in 2018 (0.038 % against -0.347 %) and in 2022 (-0.060 % against -0.180 %).

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.g1_wide-range-breakdown-rebound` (from F1, F2): When a 4h bar closes below the lowest low of the coin's preceding two days, after two days whose bars were wide compared with the coin's 30-day average 4h range, the coin rises over the next three days. The wider those two days' bars and the farther the close sits below the two-day low, measured in that average range, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.g2_failed-breakout-after-falling-week` (from F3): When a 4h bar closes above the highest high of the coin's preceding two days while the coin's 7-day return is negative, the coin falls over the next three days, and the deeper the 7-day fall, the larger the drop.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
