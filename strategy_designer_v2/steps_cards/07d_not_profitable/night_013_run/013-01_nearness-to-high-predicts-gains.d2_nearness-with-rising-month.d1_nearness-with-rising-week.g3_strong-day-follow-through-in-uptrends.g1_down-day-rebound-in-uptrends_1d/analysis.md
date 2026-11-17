---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3690 USD
---
## Findings
- **F1:** The book's deepest fall, 24.0% over 380 days from w20 to w23, came while holding the coins gained: the book summed -0.263 in daily returns while holding summed +0.861, and in w20–w24 the position's gain before costs averaged -0.000155 per bar against +0.000523 in w1–w19, while the coin itself rose 0.002529 per bar against 0.000836.
- **F2:** In w20–w24 the active bars' rebound came after the 1-day horizon: next-1-day return 0.000369, next-3-day 0.009113 and next-5-day 0.020980 (n=815), against 0.002961, 0.005315 and 0.005711 in w1–w19 (n=3054); positions were held about 2.0 days on average.
- **F3:** On the active bars as a whole, the forward return keeps building past one day, with 0.0024 at 1 day (t 3.09, n 3839), 0.0061 at 3 days (t 4.33) and 0.0089 at 5 days (t 4.82); with non-overlapping samples on down days inside a rising month, the fall-size slope is t 2.64 at 1 day (n 2961) and t 2.06 at 3 days (n 959).
- **F4:** The rebound grows with the strength of the 30-day rise, with next-1-day return -0.0016 (t -1.12), 0.0010, 0.0040 (t 2.33), 0.0053 (t 2.89) and 0.0050 across 30-day-return quintiles (n≈592 each); the non-overlapping 3-day return runs -0.0015, 0.0022, 0.0077 and 0.0203 across quartiles (n≈240 each).
- **F5:** The mean daily return is held down by small, fee-heavy exposure: the book is long on only 23% of bars, with a mean allocation of 0.094; fees take 42% of the gross gain (0.000160 of 0.000381 per bar); in the two weakest forecast quintiles, fees (0.000143, 0.000233) match or exceed the gain (0.000115, 0.000234).
- **F6:** The gain is concentrated in the largest falls, with a next-1-day return of 0.0070 and gain 0.0057 per bar in the top forecast quintile, against 0.0014 and 0.0001 in the bottom one.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends.d1_down-day-rebound-over-three-days` (from F1, F2, F3): While a coin's 30-day return is positive, the larger its latest one-day fall relative to its 30-day daily volatility, the higher its return over the next 3 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends.d2_rebound-scaled-by-month-strength` (from F4, F5, F6): While a coin's 30-day return is positive, the larger its latest one-day fall relative to its 30-day daily volatility, the higher its return over the next 1 day, and the larger that coin's 30-day return, the larger this rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
