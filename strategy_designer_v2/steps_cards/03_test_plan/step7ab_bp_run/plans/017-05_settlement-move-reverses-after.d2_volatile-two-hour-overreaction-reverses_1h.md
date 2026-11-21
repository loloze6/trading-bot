---
idea: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a large 2-hour move made while 24-hour volatility is high -> adapted: the 2-hour move is graded; "volatility high" is a regime condition, 24-bar volatility above its 30-day average.
- Comparison: the 2-hour move against the coin's usual 2-hour move -> kept: the 2-bar return in units of the coin's average 24-bar volatility over 720 bars, scaled by sqrt(2).
- Outcome: an opposite move over the next 8 hours, larger after larger moves, at any hour -> kept: contrarian graded position held 8 bars, with no clock condition.
- Verdict transfer: yes: the test measures the stated move, the stated condition and the stated 8-hour reversal at every hour, so its verdict is the idea's.
Forecast: On bars where the 24-bar return volatility is at or above its own 720-bar average (the regime `mean_reversion`), the forecast takes the 2-bar return and divides it by the coin's usual 2-bar move. That usual move is the mean over 720 bars of the 24-bar one-bar-return standard deviation, times sqrt(2). The result is standardised over 500 past values, then negated, so a rise gives a short and a fall gives a long. A cubic dead zone (exponent 3, pivot 20) then keeps ordinary moves near zero and lets the position grow steeply as the move gets larger against the usual move. On all other bars the forecast is 0 (flat).
Config: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h_config.json
Criterion:
- Horizon: 8 bars
- Main measure: For each case (a bet, read once per 8-bar grid cell), take the coin's 8-bar return from the signal bar, minus the coin's normal 8-bar drift over all windows, signed in the forecast's direction. Report its mean and its t over the cases, pooled across coins and windows.
- Supporting check: The mean unusual move of cases with |forecast| above the cases' median is larger than that of cases below it (difference, larger minus smaller, above 0).
- Confirm: Mean unusual move > 0 with t >= 2, and the supporting check passes.
- Reject: Mean unusual move < 0 with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with a failed supporting check. A result is also inconclusive with fewer than 100 independent cases in total.
