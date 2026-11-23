---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high against its 30-day volatility, its first-hour move after the 00:00 UTC settlement reverses more over the next 24 hours. The reversal grows with that volatility ratio.
Consequence: A trader would size the post-settlement fade up when short-term volatility is raised against its usual level, and keep it near nothing in calm periods.
Why:
- F4: The 00:00 fade grows with the coin's current volatility against its usual level. By quintile of 24-hour vol over 30-day vol it rises from +0.067 % (t 0.83) to +0.266 %, +0.240 %, +0.319 % and +0.448 % (t 4.22, n 3190 each). The quartiles of short-to-long mean absolute return give the same rise, from +0.115 % (t 1.63) to +0.471 % (t 5.03).
- F1: The 00:00 UTC hour's move is faded over the next 24 hours far more than any other hour's: the faded 24-hour return in excess of drift is +0.297 % (t 7.76, 17096 daily cases). No other hour reaches t 2.6: the largest is hour 22 at +0.093 % (t 2.54), and hour 3 goes the other way at −0.114 % (t −3.00). The effect is tied to the settlement clock, not to hourly moves in general.
- F5: The reversal is not convex in the hour's own move, which is why the supporting check failed. By |z| it is +0.161 % (≤0.5), +0.239 %, +0.547 % (1–1.5), +0.411 %, +0.672 % (2–3), and −0.012 % (t −0.04, n 364) beyond 3 usual moves.
