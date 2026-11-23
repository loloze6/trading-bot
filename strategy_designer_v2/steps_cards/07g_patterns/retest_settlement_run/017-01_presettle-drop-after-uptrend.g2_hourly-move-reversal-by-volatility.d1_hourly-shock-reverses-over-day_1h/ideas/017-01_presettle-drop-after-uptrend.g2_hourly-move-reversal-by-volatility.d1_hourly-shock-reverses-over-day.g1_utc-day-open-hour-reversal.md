---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's return over the first hour of the UTC day (00:00 to 01:00), relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would take a day-long position against the coin's first-hour move of the UTC day, larger as that move is larger in usual hourly moves, and ignore the same-sized moves at other hours.
Why:
- F1: The tested reversal sits almost entirely in one clock hour. For the bar opening at 00:00 UTC (the first hour of the UTC day), the slope of the 24-hour excess return on the volatility-scaled hourly return z1 is -0.261 % per unit (t -7.83, about 17,086 cases). No other hour's t goes beyond ±2.8. The other 23 hours alternate in sign, and pooled outside hour 0 the per-year slopes range from -0.059 to +0.065 %. With 24 hours examined, only hour 0 stands clear of chance.
- F2: The first-hour reversal is graded and larger than a trade's cost. Over the next 24 hours, the move against that hour's return rises with |z1| quintile: +0.05 %, +0.23 %, +0.30 %, +0.43 %, +0.47 % (t 0.7 to 5.1, about 3,417 cases each). The total move is the same, since the drift is about 0, and the top quintile is 2.4 times the 0.19 % cost. The tested idea as a whole moved +0.12 % per case, 0.6 times that cost.
- F3: The hour-0 reversal holds across all 8 years and all 6 coins. The slope is negative in every year (-0.111 to -0.384 %, with t below -2 in 7 of 8 years) and in every coin (-0.144 % on BTC, t -2.5, to -0.416 % on ZEC, t -4.1).
- F5: The brief's funding clock does not carry the effect. At the other settlement hours, the slope is +0.006 % at the 08:00 bar (t 0.16) and -0.075 % at the 16:00 bar (t -2.3), against -0.261 % at 00:00. The hour before each of these is also weak (07:00 t 1.6, 15:00 t 1.3, 23:00 t -2.3). The effect belongs to the daily boundary at 00:00 UTC, not to settlement times as such.
