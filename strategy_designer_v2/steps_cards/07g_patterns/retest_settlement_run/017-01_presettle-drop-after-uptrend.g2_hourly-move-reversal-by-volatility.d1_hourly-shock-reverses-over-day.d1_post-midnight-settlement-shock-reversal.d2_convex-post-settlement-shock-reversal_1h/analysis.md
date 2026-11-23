---
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4379 USD
---
## Findings
- **F1:** The 00:00 UTC hour's move is faded over the next 24 hours far more than any other hour's: the faded 24-hour return in excess of drift is +0.297 % (t 7.76, 17096 daily cases). No other hour reaches t 2.6: the largest is hour 22 at +0.093 % (t 2.54), and hour 3 goes the other way at −0.114 % (t −3.00). The effect is tied to the settlement clock, not to hourly moves in general.
- **F2:** At 00:00 the reversal is graded by how far that hour extends the prior 24-hour run in the same direction. By quintile of (sign of the hour's move × prior 24-hour return), the top quintile fades +0.772 % (t 7.27, n 3391) against +0.104 % (t 1.06) in the bottom quintile. Hours moving with the prior day fade +0.403 % (t 7.48, n 9308) against +0.170 % (t 3.15, n 7788) for hours against it.
- **F3:** Fading the prior 24-hour return measured at the 00:00 bar's close is graded by its size. The quintiles of |24-hour return| give −0.007 % (t −0.10) for the smallest, then −0.150 %, +0.055 %, +0.260 % (t 3.04), and +0.427 % (t 3.72) for the largest. The same fade taken at the 12:00 bar gives −0.060 % (t −1.60, n 17120), so the prior day's run reverses after the midnight settlement only.
- **F4:** The 00:00 fade grows with the coin's current volatility against its usual level. By quintile of 24-hour vol over 30-day vol it rises from +0.067 % (t 0.83) to +0.266 %, +0.240 %, +0.319 % and +0.448 % (t 4.22, n 3190 each). The quartiles of short-to-long mean absolute return give the same rise, from +0.115 % (t 1.63) to +0.471 % (t 5.03).
- **F5:** The reversal is not convex in the hour's own move, which is why the supporting check failed. By |z| it is +0.161 % (≤0.5), +0.239 %, +0.547 % (1–1.5), +0.411 %, +0.672 % (2–3), and −0.012 % (t −0.04, n 364) beyond 3 usual moves.
- **F6:** The 00:00 reversal builds slowly over the day. The faded return is +0.093 % at 6 h (t 5.30), +0.170 % at 12 h (t 6.76) and +0.297 % at 24 h (t 7.76), so it gives back about 39 % of the hour's mean absolute move of 0.757 %.
- **F7:** The 00:00 fade holds across groupings:
- **F8:** The book's worst 1 % of days fall on days when the coin moves 14.3 % in absolute terms on average (mean +4.2 %), against 3.2 % on all days. Its losses, and the Calmar failure, come from fading moves on violent trending days.
- **F9:** The 20:00 and 21:00 bars are followed by a next-hour rise of +0.055 % (t 6.75) and +0.044 % (t 5.66), but the sign flips in 2022 (t −2.31) and 2023 (t −2.15). This is about a quarter of one trade's cost and changes sign across years, so it supports no idea.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal.g1_midnight-fade-of-daily-run` (from F3, F1, F6): The larger a coin's 24-hour return up to the close of the first hour after the 00:00 UTC funding settlement, the more its return over the next 24 hours runs the opposite way. The same 24-hour return measured at other times of day shows no such reversal.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal.g2_settlement-extension-of-crowded-run` (from F2, F1): The more a coin's first hour after the 00:00 UTC settlement extends its prior 24-hour run in the same direction, measured as that hour's move times the prior 24-hour return, the more its next 24 hours run against both.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal.g3_volatility-scaled-settlement-reversal` (from F4, F1, F5): When a coin's 24-hour volatility is high against its 30-day volatility, its first-hour move after the 00:00 UTC settlement reverses more over the next 24 hours. The reversal grows with that volatility ratio.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
