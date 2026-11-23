---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return up to the close of the first hour after the 00:00 UTC funding settlement, the more its return over the next 24 hours runs the opposite way. The same 24-hour return measured at other times of day shows no such reversal.
Consequence: A trader would fade the prior day's run once a day, just after the midnight settlement, and more heavily the larger that run.
Why:
- F3: Fading the prior 24-hour return measured at the 00:00 bar's close is graded by its size. The quintiles of |24-hour return| give −0.007 % (t −0.10) for the smallest, then −0.150 %, +0.055 %, +0.260 % (t 3.04), and +0.427 % (t 3.72) for the largest. The same fade taken at the 12:00 bar gives −0.060 % (t −1.60, n 17120), so the prior day's run reverses after the midnight settlement only.
- F1: The 00:00 UTC hour's move is faded over the next 24 hours far more than any other hour's: the faded 24-hour return in excess of drift is +0.297 % (t 7.76, 17096 daily cases). No other hour reaches t 2.6: the largest is hour 22 at +0.093 % (t 2.54), and hour 3 goes the other way at −0.114 % (t −3.00). The effect is tied to the settlement clock, not to hourly moves in general.
- F6: The 00:00 reversal builds slowly over the day. The faded return is +0.093 % at 6 h (t 5.30), +0.170 % at 12 h (t 6.76) and +0.297 % at 24 h (t 7.76), so it gives back about 39 % of the hour's mean absolute move of 0.757 %.
