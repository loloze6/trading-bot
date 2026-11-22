---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following days, only while the coin closes below its 50-day average. The deeper the re-entry close sits below the old high, in units of the coin's 20-day daily volatility, and the further the close sits below its 50-day average, the larger the fall over the next 8 days.
Consequence: A trader would short deep failed breakouts only when the coin is already below its 50-day average, and refuse them in an uptrend, where they are followed by further rises.
Why:
- F1: Measured from the signal bar, the short earns nothing in total: across 349 cases its gain is +0.05 % over 8 days (t 0.07), −0.30 % over 5 days and +0.12 % over 12 days. The confirmed +1.18 % "unusual move" exists only because the coins' normal 8-day drift is up 1.06 %. So the total move, +0.12 %, is 0.6 times the 0.19 % cost, and the book's mean daily return is 0.0164 % against 0.118 % for holding.
- F2: The book makes its money when the coin closes below its 50-day mean and loses it when the coin closes above. Below, it gains +0.117 % a day (5285 coin-days, the coin at −0.62 % a day). Above, it loses −0.099 % a day (5183 coin-days, the coin at +0.86 % a day). This uptrend loss is the source of the poor gain against holding and of the low Calmar: deepest fall −25.8 %, Calmar 0.19.
- F3: In the cases the same split holds, graded by distance from the 50-day mean. Cases furthest above it (median +22.7 %) lose −2.94 % over 8 days (t −1.38, 49 cases). Cases below it (median −5.2 %) gain +0.73 %. Deep (capped) failures below the 50-day mean gain +2.30 % (t 1.19, 23 cases), while shallow ones above it lose −1.92 % (t −1.45, 105 cases).
