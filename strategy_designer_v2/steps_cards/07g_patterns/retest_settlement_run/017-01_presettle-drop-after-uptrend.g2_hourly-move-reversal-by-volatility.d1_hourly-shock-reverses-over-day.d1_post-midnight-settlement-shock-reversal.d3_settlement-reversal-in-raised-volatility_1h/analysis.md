---
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4586 USD
---
## Findings
- **F1:** Apart from the tested 00:00 UTC hour itself (24-hour slope on the hour's volatility-scaled return −26.1 bp per unit, t −7.8, 17086 cases), the coin's prior 24-hour return in 24h-volatility units reverses over the next 24 hours when read at the close of the early-UTC hours. The slope is −21.1 bp at hour 0 (t −5.2), −21.7 at hour 1 (t −5.3), −19.2 at hour 2 (t −4.7), −18.2 at 3 (t −4.4), −18.0 at 4 (t −4.3) and −15.3 at 5 (t −3.6), about 17000 cases each. It fades to −3.1 (t −0.7) by hour 7 and turns positive at hours 12–15 (hour 14: +16.7, t +4.1).
- **F2:** At hour 0 the prior trend adds to the settlement-hour return rather than repeating it. In a joint fit, the hour's return keeps −26.2 bp (t −7.8) and the 23-hour trend before it adds −13.4 bp (t −3.2). That trend slope is negative in 2018–2023 (−47 to −15 bp) but near zero in 2024 (+2.0, t 0.2) and reversed in 2025 (+34.1, t +3.0), so it is not stable over time.
- **F3:** A coin's 1-hour return in 24h-volatility units reverses over the next 4 hours at many hours of the day, not only after settlement. Hour 11 gives −10.8 bp per unit (t −5.8), hour 18 −7.6 (t −5.0), hour 23 −6.3 (t −4.0) and hour 5 −6.7 (t −3.9). Pooled over hours 5, 11, 18 and 23 the slope is negative in every year (t below −2.5 in 6 of 8 years, about 8600 cases a year).
- **F4:** That 4-hour reversal, on the non-overlapping 4-hour grid, scales with how volatile and thin the coin is. ZEC gives −7.7 bp per unit (t −4.0), XRP −5.6 (t −3.4), XMR −5.2 (t −3.4) and LTC −3.2 (t −2.1), against BTC −0.9 (t −0.8) and ETH −0.1 (t −0.1), about 17000 cases each.
- **F5:** The settlement-hour reversal is larger on weekends: −37.9 bp per unit (t −6.8, 4833 cases) against −22.5 (t −5.5, 12111) on weekdays, with Saturday the strongest (−49.1, t −5.8). It is also larger when that hour's volume is low against its week: −34.3 (t −4.9) in the lowest volume tercile against −21.6 (t −4.4) in the highest. The weekend gap is about t 2.2, which is marginal after this many angles.
- **F6:** The volatility-ratio grading holds across quintiles at hour 0: the slope runs from −5.8 bp (t −0.8) at a ratio of 0.52 to −44.3 bp (t −4.5) at 1.59. Hours 6, 12 and 18 show no such grading (|t| ≤ 1.3).
- **F7:** The book is mostly uncorrelated with the coins (correlation of daily returns from −0.29 to +0.16 by year). It earns most on days after large coin moves: its mean daily return is 0.20 % in the top quintile of the previous day's absolute coin move, against 0.01–0.07 % in the others. It is weak in 2023 (Sharpe −0.20) and 2024 (0.14), while holding the coins gave 1.18 and 1.61; 5 of 24 windows lose, the worst w12 with Sharpe −3.1.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility.g1_early-utc-daily-trend-reversal` (from F1, F2): The larger a coin's 24-hour return relative to its 24-hour volatility at the close of the early UTC hours (00:00 to 05:00), the more its return over the next 24 hours runs the opposite way.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility.g2_hourly-shock-four-hour-fade` (from F3, F4): The larger a coin's 1-hour return relative to its 24-hour volatility, the more its return over the next 4 hours runs the opposite way, and more so the higher the coin's 24-hour volatility stands.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility.g3_weekend-settlement-shock-fade` (from F5, F6): The larger a coin's 1-hour return relative to its 24-hour volatility in the first hour after the 00:00 UTC settlement on Saturdays and Sundays, the more its return over the next 24 hours runs the opposite way.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
