---
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
idea tested: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4044 USD
---
## Findings
- **F1:** Measured from the signal bar, the short earns nothing in total: across 349 cases its gain is +0.05 % over 8 days (t 0.07), −0.30 % over 5 days and +0.12 % over 12 days. The confirmed +1.18 % "unusual move" exists only because the coins' normal 8-day drift is up 1.06 %. So the total move, +0.12 %, is 0.6 times the 0.19 % cost, and the book's mean daily return is 0.0164 % against 0.118 % for holding.
- **F2:** The book makes its money when the coin closes below its 50-day mean and loses it when the coin closes above. Below, it gains +0.117 % a day (5285 coin-days, the coin at −0.62 % a day). Above, it loses −0.099 % a day (5183 coin-days, the coin at +0.86 % a day). This uptrend loss is the source of the poor gain against holding and of the low Calmar: deepest fall −25.8 %, Calmar 0.19.
- **F3:** In the cases the same split holds, graded by distance from the 50-day mean. Cases furthest above it (median +22.7 %) lose −2.94 % over 8 days (t −1.38, 49 cases). Cases below it (median −5.2 %) gain +0.73 %. Deep (capped) failures below the 50-day mean gain +2.30 % (t 1.19, 23 cases), while shallow ones above it lose −1.92 % (t −1.45, 105 cases).
- **F4:** The 2-day lag enters after a bounce. From the failure bar's close, the coin rises 0.66 % the next day (short gain −0.66 %, t −2.76) and 1.12 % over 2 days (t −3.10, 349 cases). The short is therefore placed after an adverse move, with no follow-through left.
- **F5:** A strong run-up before the failure removes the effect. Cases in the top quartile of 10-day return (median +17.7 %) lose −1.02 % over 8 days, while the other three quartiles gain +0.22 % to +1.23 %. Likewise, the top quartile of 60-day return (median +51 %) loses −1.98 %.
- **F6:** Calm coins carry the effect and volatile ones do not. Cases in the lowest quartile of 20-day volatility (median 2.1 % a day) gain +1.12 % in total over 8 days, against −0.75 % in the highest quartile (median 6.1 %).
- **F7:** The trades lose before fees, not through fees. Across 878 trades the mean is −1.81 % gross and −1.91 % net, with 35 % winners. Trades held under 4 days lose −3.1 % to −4.6 % gross (299 trades), and shallow-entry trades (|forecast| 2–6) lose −3.27 % gross over about 14 days (248 trades).

## Ideas
- `029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth.d1_failed-breakout-in-downtrend` (from F1, F2, F3): After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following days, only while the coin closes below its 50-day average. The deeper the re-entry close sits below the old high, in units of the coin's 20-day daily volatility, and the further the close sits below its 50-day average, the larger the fall over the next 8 days.
- `029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth.d2_failure-without-prior-run-up` (from F1, F5, F7): After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following days. The deeper the re-entry close sits below the old high, in units of the coin's 20-day daily volatility, and the smaller the coin's 10-day return before the failure, the larger the fall over the next 8 days.
- `029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth.d3_failed-breakout-in-calm-coins` (from F1, F6): After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following days. The deeper the re-entry close sits below the old high, in units of the coin's 20-day daily volatility, and the lower that 20-day volatility, the larger the fall over the next 8 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
