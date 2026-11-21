---
idea: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a 2-hour move into each funding settlement while 24-hour volatility is high, larger against its usual size -> kept: on the bars closing at 00, 08 and 16 UTC, the regime fires when 24-bar volatility is at or above its 720-bar mean, and the size is the 2-bar return over the 720-bar mean volatility.
- Comparison: the 8-hour return after settlement runs opposite to the 2-hour return before it -> kept: the scaled 2-bar return is negated.
- Outcome: price moves back over the 8 hours after settlement, more when the move and the volatility are larger -> kept: each bet is held 8 bars from the settlement close.
- Verdict transfer: yes: the forecast bets against exactly the pre-settlement move, only in high volatility, sized by the move and the volatility, over the idea's 8-hour horizon.
Forecast: On the bar that closes at a funding settlement time (00:00, 08:00 or 16:00 UTC), the regime is active only if the coin's 24-bar return volatility is at or above its 720-bar average. It is flat on all other bars. - The forecast is minus the 2-bar return divided by the 720-bar mean of 24-bar volatility. This equals the pre-settlement move in usual moves, times the current-to-average volatility ratio. - That value is standardised against its own past 500 values (target 10, cap 20). - The forecast is positive after a fall into settlement and negative after a rise. Its size grows with the size of the move and with the volatility. - Each bet is held for the 8 bars that follow. The forecast is zero outside settlement bars in high volatility.
Config: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses_1h_config.json
Criterion:
- Horizon: 8 bars
- Main measure: Cases are the settlement bars with a non-zero forecast, each on its own 8-bar grid cell. For each case, take forecast/10 times the excess return: close[t+8]/close[t] - 1, minus the coin's mean 8-bar return over all windows. Report the ordinary t of the mean over all cases and coins.
- Supporting check: Split the cases at the median |forecast|. The mean unusual move in the forecast's direction must be higher in the larger half than in the smaller half (difference > 0).
- Confirm: The main-measure t is 2 or more and the larger-half minus smaller-half difference is above 0.
- Reject: The main-measure t is -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with the check failing is also inconclusive. Fewer than 500 cases over all coins and windows is inconclusive.
