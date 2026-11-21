---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4659 USD
---
## Findings
- **F1:** The tested weekly momentum's edge sits only in its top forecast quintile. Over 3 days (18 bars), strength is +0.096 (t 4.0, 2433 cases, unusual move +0.90 %) in the top quintile, against −0.013 to −0.037 in the other four. Its size per case (+0.18 %) is 0.8 times the 0.22 % cost of a round trip, so the book pays little. Year by year the momentum fades: +0.07 to +0.09 in 2018, 2019 and 2021, and −0.021 in 2025 (2261 cases).
- **F2:** A sharp one-day fall is followed by a rebound much larger than a trade's cost. The bottom decile of the past day's return over 30-day volatility (mean −1.78) is followed by a 3-day strength of +0.193 (t 6.3, 1003 non-overlapping cases), an unusual move of +1.80 % per case, about 8 times the 0.22 % round-trip cost. Over 1 day the same decile gives +0.089 (t 4.2, 3082 cases, +0.45 %). The effect is graded: the second decile gives +0.049, the third −0.047, and among all falls corr(size of fall, strength) is 0.091 over 4950 cases (t about 6.4). It holds broadly: 18 of 19 coins and 16 of 24 windows are positive, and 6 of 8 years.
- **F3:** The rebound after a sharp one-day fall is much stronger when the coin's longer trend is up. In the top tercile of the 7-day scaled return, the bottom one-day quintile gives a 3-day strength of +0.360 (391 cases), against +0.052 in the bottom tercile (1090). When the 30-day return is positive it gives +0.228 (790 cases), against +0.052 when negative (1215).
- **F4:** Quiet stretches do not precede larger moves, against the brief. The quietest quintile of 7-day volatility over 30-day volatility is followed by a 3-day absolute move of 0.630 usual moves, against 0.747 in the most volatile quintile. The narrowest 7-day range quintile gives 0.637, against 0.725 for the widest. Inside the quietest 30 % of ranges, a close at the top of the range is followed by +0.011 strength (602 cases, t 0.3), not by continuation.
- **F5:** Weekday patterns did not stand out against the number of angles looked at. Thursday's 3-day strength is +0.102 and Sunday's −0.129 (about 1700 cases each), but Thursday is positive in only 6 of 8 years and Sunday negative in 5 of 8.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation.g1_sharp-daily-fall-rebound` (from F2): The larger a coin's fall over the past day, measured against its 30-day volatility, the more the coin rises over the next three days, by more than its normal drift.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation.g2_dip-within-weekly-rise` (from F1, F2, F3): When a coin has risen over the past 7 days, the larger its fall over the past day, measured against its 30-day volatility, the more the coin rises over the next three days, by more than its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
