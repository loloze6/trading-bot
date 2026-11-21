---
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5657 USD
---
## Findings
- **F1:** The book's gain is too small because it stays long for long stretches after its signal has faded. 51 % of bars carry a forecast of 0, yet the book still holds about 0.14 of its value on them; those bars lose 0.32 of the book's total gain (timing −0.24 bps per bar) and pay 28 % of its fees. Its trades last 159 hours on average against a 48-hour horizon.
- **F2:** The gain sits almost entirely in the strongest drops. Bars with a forecast of 8 to 20 are 2.0 % of bars but carry 65 % of the gain, with timing of +6.8 bps per bar. Bars with a forecast of 0 to 0.5 earn only +0.13 bps of timing.
- **F3:** The rebound after a drop depends on the coin's 30-day return, which sets the failing mean return and Calmar. Over the 1,372 entries, when the 30-day return is above +6.8 % (top two quintiles) the next 48 hours rise +1.80 % (t 4.1) and +1.72 % (t 1.9). When it is below −3.5 % (bottom two quintiles) they move −0.09 % and −0.08 % (t −0.2), which is less than a 0.22 % round trip.
- **F4:** On the non-overlapping 48-hour grid the dip rebound holds in both 30-day states, but it is larger in rising ones. With a forecast of 2 to 20, the next 48 hours return +1.30 % (t 3.2, 301 cases) when the 30-day return is positive. They return +1.00 % (t 2.8, 657 cases) when it is negative. Grid cells with no drop return −0.30 % (t −2.5, 3,140) in falling 30-day states.
- **F5:** The 7-day return grades the rebound the same way. Entries in the top 7-day quintile rise +2.54 % over 48 hours (t 3.6) and the fourth quintile +1.45 % (t 3.0). The middle quintile rises only +0.004 %.
- **F6:** The book's deepest fall is 39 %, running over 305 days from window 1 to window 3, all falling-market windows (holding's summed daily returns −0.33, −0.41, −0.21). In window 2 alone the book lost −0.24 of summed daily return, while it bought drops that kept falling.
- **F7:** The book lags holding mainly because it is barely in the market, not because its rebounds fail. Its mean allocation when long is 0.22, and its mean daily return is 0.033 % against holding's 0.139 %. It trails holding by the most in rising windows: w11 earned 0.28 against 2.29, w6 0.16 against 0.76.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins.d1_plunge-rebound-in-uptrends` (from F2, F3, F4, F6): When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift, and the larger the 24-hour drop in those multiples, the larger the rise, only while the coin's 30-day return is positive, and the higher that 30-day return, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins.d2_plunge-rebound-after-rising-week` (from F2, F5, F6): When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift, and the larger the 24-hour drop in those multiples, the larger the rise, only while the coin's 7-day return is positive, and the higher that 7-day return, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins.d3_plunge-rebound-fades-after-two-days` (from F1, F2, F7): The 2-day rise that follows a coin's 24-hour drop of a large multiple of its 30-day average absolute daily return is spent within those 2 days, and the larger the drop, the larger the rise inside the 2 days compared with the days after.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
