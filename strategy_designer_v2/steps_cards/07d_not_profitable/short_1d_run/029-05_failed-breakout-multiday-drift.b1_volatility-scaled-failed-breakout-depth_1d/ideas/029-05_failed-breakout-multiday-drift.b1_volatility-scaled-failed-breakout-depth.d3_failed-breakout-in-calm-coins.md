---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following days. The deeper the re-entry close sits below the old high, in units of the coin's 20-day daily volatility, and the lower that 20-day volatility, the larger the fall over the next 8 days.
Consequence: A trader would short deep failed breakouts in calm coins and refuse them in highly volatile ones, where the failure is followed by rebounds.
Why:
- F1: Measured from the signal bar, the short earns nothing in total: across 349 cases its gain is +0.05 % over 8 days (t 0.07), −0.30 % over 5 days and +0.12 % over 12 days. The confirmed +1.18 % "unusual move" exists only because the coins' normal 8-day drift is up 1.06 %. So the total move, +0.12 %, is 0.6 times the 0.19 % cost, and the book's mean daily return is 0.0164 % against 0.118 % for holding.
- F6: Calm coins carry the effect and volatile ones do not. Cases in the lowest quartile of 20-day volatility (median 2.1 % a day) gain +1.12 % in total over 8 days, against −0.75 % in the highest quartile (median 6.1 %).
