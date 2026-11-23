---
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4355 USD
---
## Findings
- **F1:** Saturday's volatility-scaled return predicts the volatility-scaled return over Monday and Tuesday in the same direction (slope 0.211, t 6.27, 2103 Mondays), and this holds in both halves of the period (2018–2021 t 4.77, 2022–2025 t 3.97). On the other start days, the return from two days back predicts nothing comparable (t between −1.18 and 2.11).
- **F2:** The book's condition that the 7-day return agree with Saturday is not what carries the effect, and calm markets are where it is largest.
- **F3:** The 7-day return at Friday 00:00 UTC predicts the volatility-scaled return over Friday and Saturday in the same direction.
- **F4:** Saturday's own return is positive on average, in both halves and for every coin.
- **F5:** Sunday's volatility-scaled return is partly reversed on Monday, but only in turbulent markets and mostly in the earlier years, so this is the weakest finding.
- **F6:** The book's gain comes from its strongest forecasts and is uneven across years.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend.g1_calm-saturday-continuation-unfiltered` (from F1, F2): A coin's 24-hour return over Saturday is followed over Monday and Tuesday by a move in the same direction that grows with the size of Saturday's move scaled by the coin's 30-day volatility of hourly returns, while that volatility is low against its own past year, whichever way the coin's 7-day return points.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend.g2_weekly-momentum-into-weekend` (from F3, F4): A coin's 7-day return, read at the start of Friday, is followed over Friday and Saturday by a move in the same direction that grows with the size of the 7-day return scaled by its 30-day volatility of hourly returns, the more so the lower that volatility is against its own past year.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend.g3_turbulent-sunday-reverses-monday` (from F5): A coin's 24-hour return over Sunday is followed on Monday by a move in the opposite direction that grows with the size of Sunday's move scaled by its 30-day volatility of hourly returns, while that volatility is high against its own past year.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
