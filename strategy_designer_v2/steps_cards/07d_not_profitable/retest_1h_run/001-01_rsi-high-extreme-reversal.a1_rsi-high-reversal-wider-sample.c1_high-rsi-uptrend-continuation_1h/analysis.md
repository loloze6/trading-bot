---
line: 7.d not profitable
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h
idea tested: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3064 USD
---
## Findings
- **F1:** Fees, not a missing effect, are what sink the book: across all bars the position earned 0.000647 a day before costs but paid 0.002097 a day in fees, so the book's daily mean is -0.001452 (sd 0.0212, 17,381 coin-days) while holding the coins returned +0.001190 a day.
- **F2:** The book trades far faster than the 10-day horizon it forecasts: turnover is 0.081 of the book per bar, the forecast moves by 1.74 points per bar on average, and 98,367 trades lasted a mean of only 14.2 hours.
- **F3:** The forecast follows RSI only loosely (correlation 0.75 on trending bars) because it is re-standardised against its own last 336 values, so most of its hour-to-hour churn is noise that the fees pay for.
- **F4:** The short side does not pay at all: short bars earned -0.000004 per bar gross against 0.000201 per bar in fees. Long bars earned 0.000078 gross against 0.000142 in fees.
- **F5:** On trending bars with RSI between 45 and 50, the most common short zone (68,893 bars), the book earned 0.000007 per bar gross against 0.000210 in fees, the highest fee of any RSI bin.
- **F6:** The gain sits where RSI is clearly above its midpoint, and there fees are low. On trending bars it was 0.000180 per bar gross against 0.000073 fees at RSI 55–60, and 0.000321 against 0.000057 at RSI 60–65. On the 240-bar grid, the excess 10-day return was +0.035 at RSI 55–60 (128 cases) and +0.014 at RSI 50–55 (364 cases).

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.d1_smoothed-rsi-uptrend-continuation` (from F1, F2, F3, F6): While a coin's 60-day return is positive, the higher its 14-day RSI averaged over its past 3 days, the more the coin rises over the next 10 days, by more than its usual 10-day move; the information lies in the RSI's slow level, not in its hour-to-hour changes.
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.d2_upper-rsi-uptrend-continuation` (from F1, F4, F5, F6): While a coin's 60-day return is positive, the higher its 14-day RSI, the more the coin rises over the next 10 days, by more than its usual 10-day move, only while its 14-day RSI is above its midpoint, and the more so the further above it the RSI sits.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
