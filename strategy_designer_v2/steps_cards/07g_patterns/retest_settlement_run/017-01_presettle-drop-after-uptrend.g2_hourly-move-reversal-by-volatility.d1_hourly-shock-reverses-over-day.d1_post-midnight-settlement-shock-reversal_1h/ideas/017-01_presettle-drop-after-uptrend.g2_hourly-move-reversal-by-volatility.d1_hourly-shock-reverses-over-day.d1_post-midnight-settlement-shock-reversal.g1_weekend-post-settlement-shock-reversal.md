---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement on a Saturday or Sunday, relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way. This weekend reversal is larger than the weekday one.
Consequence: A trader would favour fading the post-midnight hour's move on weekend days, where the captured move (about 0.8 %) is over four times the cost of a trade, and refuse it on weekdays when it is small.
Why:
- F2: The hour-0 reversal is about twice as large on Saturday and Sunday. Weekend days give +0.82 % (t 6.76, 1572 cases) against +0.38 % (t 4.52, 4190 cases) on Monday to Friday, a Welch t of 2.98. Saturday alone gives +0.94 % (t 4.98) and Tuesday gives -0.06 % (t -0.29).
- F3: The weekend lift holds in every volatility tercile, and it is largest when the coin's 24-hour volatility is high against its 30-day volatility. Weekend hour-0 moves give +0.60 % (t 3.59) in low volatility, +0.42 % (t 1.81) in mid and +1.32 % (t 4.24) in high. On weekdays the same terciles give +0.005 % (t 0.03), +0.28 % and +0.39 %.
- F1: The 24-hour reversal after a volatility-scaled hourly move is specific to the hour starting 00:00 UTC. At that hour the slope t is 7.84 and moves of at least one usual hourly move give +0.50 % signed (t 7.19, 5762 cases). Pooled over all other hours, the slope t is 0.59 and the signed mean is +0.014 % (t 0.89, 101012 cases). No other hour reaches a signed mean above 0.29 %.
