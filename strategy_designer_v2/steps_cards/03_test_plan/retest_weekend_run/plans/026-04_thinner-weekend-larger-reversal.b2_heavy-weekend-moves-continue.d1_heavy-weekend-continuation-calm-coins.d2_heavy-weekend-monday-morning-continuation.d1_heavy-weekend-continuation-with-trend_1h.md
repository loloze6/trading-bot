---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a Saturday-Sunday move on weekend volume above the mean of the five preceding weekdays -> adapted: the move is graded, as the 48-bar return in usual 48-bar moves times the ratio of weekend volume to weekday volume; "volume higher than its mean" stays a regime condition (ratio > 1), read on the bar that closes Sunday 23:59 UTC.
- Comparison: the weekend move goes the same way as the 30-day return -> kept: the regime fires only when the 48-bar and 720-bar returns have the same sign.
- Outcome: the price continues in the weekend move's direction over Monday's first 12 hours, more so for larger moves on heavier volume -> kept: the position is entered at Sunday's close, held 12 bars and sized by the graded move times volume.
- Verdict transfer: yes: the test bets exactly the gated Monday-morning continuation, sized as the idea says, over its 12-hour horizon.
Forecast: The forecast is nonzero on one bar a week, the hourly bar whose close ends Sunday (the coming bar is Monday 00:00 UTC). On that bar, three conditions must all hold: - the 48-bar weekend return and the 720-bar (30-day) return have the same sign; - the mean volume of the 48 weekend bars is above the mean volume of the 120 weekday bars before them. When they hold, the forecast is RecentToPriorVolumeScaledReturnComponent (period 48, window 720, base_period 120), standardised (window 500, min_periods 120). That value is the weekend return in usual 48-bar moves times the weekend-to-weekday volume ratio. It is positive after an up weekend and negative after a down weekend. Its size grows with the move and with the volume ratio. On every other bar, and on Monday bars that fail the conditions, the forecast is 0 (flat). The 12-bar holding period keeps the bet through Monday 00:00 to 11:59.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend_1h_config.json
Criterion:
- Horizon: 12 bars
- Main measure: The cases are the bars where the forecast is nonzero, at most one per coin per week, so they are independent. For each case: - take the coin's 12-bar return from that bar's close, inside its window; - subtract the coin's normal 12-bar drift (its mean 12-bar return over all windows, on non-overlapping stretches); - multiply by the forecast's sign. The measure is the mean of this unusual move over all cases, with its t-statistic.
- Supporting check: Split the cases at the median of |forecast|. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: Mean unusual move > 0 with t ≥ 2, and the supporting check passes.
- Reject: Mean unusual move < 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main measure with t ≥ 2 whose supporting check fails is also inconclusive. So is any result from fewer than 100 cases over all coins and windows.
