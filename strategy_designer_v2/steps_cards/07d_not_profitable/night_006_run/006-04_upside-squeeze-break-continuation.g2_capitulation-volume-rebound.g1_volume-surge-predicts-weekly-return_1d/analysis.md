---
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
idea tested: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3285 USD
---
## Findings
- **F1:** The book is short on 58% of bars (10,285 short against 7,063 long) while every coin rose on average (0.0007 to 0.0016 a day), so its gain from the market's own rise is negative for every coin (-0.00005 to -0.00014 a bar). Shorts lose 0.000581 a bar to drift and net only 0.000082 a bar, while longs earn 0.001624 a bar.
- **F2:** This is why the book trails holding: its mean daily return is 0.000434 against holding's 0.00118, its Sharpe is 0.45 against 0.55, and it loses 0.000347 a day on the days the coins rise (n=1551).
- **F3:** The book's deepest fall is -53.4% over 556 days spanning several windows, while holding summed only -2.6% over the same days, so the fall comes from positioning against a flat-to-rising market, not from a crash.
- **F4:** The forecast's information is concentrated where the coin's 30-day return is high. In the top 30-day-return tercile, the slope of 7-day excess return on the forecast is 0.001378 (t=2.52, n=575), against 0.000464 (t=1.01) and 0.000155 (t=0.37) in the lower two terciles. Across all samples, the forecast × z(30-day return) interaction has t=2.02.
- **F5:** At bar level, longs in the top 30-day-return tercile earn 0.003218 a bar (n=2,144), while shorts there earn 0.000024 a bar even though the coin rose 0.0011 a bar. Shorts earn only 0.000208 even in the bottom tercile.
- **F6:** The coin's own 30-day return predicts its 7-day excess return by itself (beta 0.0074 per standard deviation, t=2.34, about 1,723 non-overlapping cases). Positive forecasts after a 5-day rise lead to an excess return of +0.0136 (n=559), against -0.0053 after a 5-day fall (n=388).
- **F7:** Fees take 0.00023 a bar out of a gross gain of 0.000708 a bar, about a third, at 0.57 trades per bar.

## Ideas
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return.d1_volume-surge-within-uptrend` (from F1, F4, F5): For a coin, the higher its 5-day average volume against its 30-day average, the higher its return over the next 7 days, whatever the direction of its last 5 days, and the more so the higher its 30-day return.
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return.d2_monthly-momentum-weekly-continuation` (from F4, F6): For a coin, the higher its 30-day return, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
