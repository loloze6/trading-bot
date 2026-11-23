---
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6200 USD
---
## Findings
- **F1:** Across all regimes, a large hourly move reverses over the next 24 hours, and the reversal grows with the move's size. The pooled slope of the unusual 24-hour return on the hour's return in 24-hour volatility units is negative (t -4.18, 17102 non-overlapping cases). By quartile of |z| (mean |z| 0.15, 0.46, 0.86, 1.81), the reversal strength rises 0.015, 0.027, 0.036, 0.059, with t 0.93, 1.65, 2.67, 3.77. The top quartile's unusual move is 0.30 % per case, against a 0.19 % trade cost.
- **F2:** The 24-hour reversal sits in the regime the tested idea excluded and is absent where the idea looked. In the highest quintile of the 24h/720h volatility ratio the slope t is -3.02 (2604 cases); in the lowest it is +0.62 (2558 cases). With the ratio at or above its 60th percentile, t is -2.60 (5171 cases); below it, t is -0.24 (7755 cases). This is why the quiet-market continuation idea was rejected (t -2.30).
- **F3:** The 24-hour reversal is fading over time. The all-regime slope t by year is -0.77, -3.04, -0.77, -3.23, -3.60, -1.98, -0.15, +1.85 for 2018–2025. In the high-ratio subset only 2018 (t -2.49) and 2019 (t -2.88) pass 2. ZEC (t -2.34) and XRP (t -1.67) carry most of it, and BTC and ETH show none (t -0.12, +0.10).
- **F4:** At the 13:00 UTC close, the return over the next 1 and 3 hours runs against the coin's 24-hour return, graded by its size. The slope t is -11.6 for 1 hour and -10.96 for 3 hours (17263 cases, one per coin-day). In the top quartile of |24h trend z|, the trend-signed 3-hour unusual move is -0.20 % (t -4.45). The 3-hour slope is negative in 7 of 8 years (t ≤ -2 in 2018 and 2021–2025) and in 5 of 6 coins (XMR t -9.7, ZEC -6.7, LTC -4.2, BTC -3.7, ETH -2.9; XRP +0.15).
- **F5:** At the 23:00 UTC close, the hour before the 00:00 funding settlement, the next 1 and 3 hours continue the coin's 24-hour return, graded by its size. This is the opposite of the brief's pre-settlement lean. The slope t is +10.1 for 1 hour (17215 cases) and +7.75 for 3 hours (17073 cases). By |trend z| quartile, the trend-signed 3-hour unusual move rises 0.02 %, 0.05 %, 0.06 %, 0.17 %, with t 0.87, 2.02, 2.51, 4.05. The 3-hour slope is positive in all 6 coins (BTC t 5.6), but it is concentrated in 2018–2020 (t 3.4, 3.3, 8.6); 2021–2025 range from t -1.7 to 1.6.
- **F6:** The bar opening at 21:00 UTC has a positive unusual return (t 5.98, about 17400 cases), with t ≥ 1.99 in every coin. It is not stable across years: 2022 t -2.39 and 2023 t -2.18. The 14:00 bar is negative (t -4.46), driven by 2018, 2020 and 2021. Neither is graded, so they support no idea.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation.g1_13-utc-trend-fade` (from F4): At the 13:00 UTC close, the larger a coin's 24-hour return, the more its return over the next 3 hours runs in the opposite direction.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation.g2_agitated-market-hourly-shock-reversal` (from F1, F2, F3): When a coin's 24-hour volatility is high relative to its 30-day volatility, the larger its 1-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs in the opposite direction.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation.g3_pre-midnight-trend-continuation` (from F5): At the 23:00 UTC close, the larger a coin's 24-hour return, the more its return over the next 3 hours continues in the same direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
