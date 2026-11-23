---
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5944 USD
---
## Findings
- **F1:** The book did not trade the signal. Its position had the forecast's sign on only 49.6 % of bars, and its correlation with the forecast was 0.026. It changed sign 0.009 times a day and its trades lasted 1330 to 2068 hours on average, against the idea's 24-hour horizon. Its 1352 short trades lost 41.6 % on average and its 797 long trades gained 29.7 %. So the failing Calmar (-0.099, a yearly return of -9.6 %) and the gap to holding's Sharpe (-0.37) come from months-long directional positions, not from the hourly-shock reversal.
- **F2:** The idea traded as it is stated is too small for the cost. A graded position held 24 hours from the step-5 grid gains 0.087 % per case before costs (t 4.5, 16958 cases) and only 0.013 % after a full 0.19 % turn. Its measured size, 0.12 % per case, is 0.6 times the cost of a trade.
- **F3:** The whole effect sits in the bar that opens at 00:00 UTC, the first hour after the daily settlement.
- **F4:** The reversal is graded only in the first hour after a settlement (bars opening at 00, 08 and 16 UTC).
- **F5:** In those settlement-closing bars with |z|>1, the long side earned 0.241 % in total and the short side -0.252 % (t -2.2), with unusual moves of +0.119 % and -0.131 %. Holding the coin over the whole period gained, and the book lost most against holding in the rising years 2020 (-0.047 % against +0.423 % a day) and 2021 (-0.155 % against +0.409 %).
- **F6:** The reversal is fading. The step-5 grid's 24-hour reversal was 0.469 % in 2021 (t 3.2) and 0.388 % in 2022 (t 4.0), then 0.001 % in 2024 and -0.118 % in 2025 (t -1.1).

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal` (from F1, F2, F3, F4): The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d2_post-settlement-hour-shock-reversal` (from F2, F4): The larger a coin's 1-hour return in the first hour after any funding settlement (00:00, 08:00 or 16:00 UTC) relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
