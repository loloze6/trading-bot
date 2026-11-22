---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following days. The deeper the re-entry close sits below the old high, in units of the coin's 20-day daily volatility, and the smaller the coin's 10-day return before the failure, the larger the fall over the next 8 days.
Consequence: A trader would refuse to short failed breakouts that come right after a strong 10-day run-up, which keep rising, and short those that follow a flat or falling stretch.
Why:
- F1: Measured from the signal bar, the short earns nothing in total: across 349 cases its gain is +0.05 % over 8 days (t 0.07), −0.30 % over 5 days and +0.12 % over 12 days. The confirmed +1.18 % "unusual move" exists only because the coins' normal 8-day drift is up 1.06 %. So the total move, +0.12 %, is 0.6 times the 0.19 % cost, and the book's mean daily return is 0.0164 % against 0.118 % for holding.
- F5: A strong run-up before the failure removes the effect. Cases in the top quartile of 10-day return (median +17.7 %) lose −1.02 % over 8 days, while the other three quartiles gain +0.22 % to +1.23 %. Likewise, the top quartile of 60-day return (median +51 %) loses −1.98 %.
- F7: The trades lose before fees, not through fees. Across 878 trades the mean is −1.81 % gross and −1.91 % net, with 35 % winners. Trades held under 4 days lose −3.1 % to −4.6 % gross (299 trades), and shallow-entry trades (|forecast| 2–6) lose −3.27 % gross over about 14 days (248 trades).
