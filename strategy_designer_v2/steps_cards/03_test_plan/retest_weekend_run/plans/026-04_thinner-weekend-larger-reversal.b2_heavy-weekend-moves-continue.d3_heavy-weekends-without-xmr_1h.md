---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a coin's Saturday-Sunday move, graded by its size -> kept: the 48-bar return to Sunday 23:00 UTC, read only on that bar, scaled by the usual 48-bar move.
- Comparison: weekend volume higher than its mean over the preceding five weekdays, the heavier the stronger -> kept: a regime rule requires the ratio of the 48 weekend bars' mean volume to the prior 120 weekday bars' mean to be above 1, and the forecast also grows with that ratio.
- Outcome: the price continues in the weekend move's direction over the next 48 hours -> kept: the bet is placed at Sunday's close and held 48 bars.
- Verdict transfer: yes: the test bets on exactly the heavy-volume weekend moves, in their own direction, sized by move and volume ratio, over Monday and Tuesday.
Forecast: The forecast is nonzero only on the bar stamped Sunday 23:00 UTC, and only when the weekend volume ratio is above 1. That ratio is the mean volume of the last 48 bars over the mean of the 120 bars before them, which are Monday 00:00 to Friday 23:00. On that bar the forecast is RecentToPriorVolumeScaledReturnComponent with period 48, base_period 120 and window 720: the 48-bar return in usual 48-bar moves over 30 days, times that volume ratio. It is standardised over its past 500 hourly values (min_periods 120). It is positive after a weekend rise and negative after a weekend fall. Its size grows with the move and with how much heavier the weekend was than the weekdays. On every other bar it is 0, and the bet made at Sunday's close is held for 48 bars.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The unusual move per case. A case is a bar with a nonzero forecast, one per qualifying weekend, so the 48-bar windows do not overlap. Each case's 48-bar forward return close[t+48]/close[t]-1 has the coin's normal 48-bar drift removed and is signed by the forecast's sign. The measure is the mean of these values over all coins and windows, with its t.
- Supporting check: The mean signed unusual move of cases with |forecast| above the median exceeds that of cases below the median (difference above 0).
- Confirm: The mean signed unusual move is positive with t >= 2 and the supporting check passes.
- Reject: The mean signed unusual move is negative with t <= -2, meaning heavy-volume weekend moves reverse early in the week.
- Inconclusive: Either of two results is inconclusive. The first is a t between -2 and 2. The second is t >= 2 with the size check failing. A minimum of 30 cases is required; fewer is inconclusive.
