---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a coin's Saturday-Sunday move -> kept: the 48-bar return at Sunday 23:00's close, scored only on that bar.
- Comparison: weekend volume higher than its mean over the preceding five weekdays -> kept: the weekend's mean volume over Monday-to-Friday's (bars t-167..t-48) must be above 1, and the ratio also grades the size.
- Outcome: the move continues the same way over the next 48 hours, more so the larger the move and the heavier the volume -> kept: the position is the move's sign, sized by move times volume ratio, held 48 bars.
- Verdict transfer: yes: the config bets on continuation only on heavy-volume weekends, sized as the idea says, over its 48-hour horizon.
Forecast: The forecast is computed once a week, on the bar whose next bar starts Monday 00:00 UTC, and only when the weekend's mean hourly volume is above the mean over the five weekdays before it. Two regime rules on weekday and hour set the timing, and one rule sets the volume ratio above 1. The value is RecentToPriorVolumeScaledReturnComponent with period 48, base_period 120 and window 720. It is the 48-hour weekend return in usual 48-hour moves, times the weekend's mean volume over the weekdays' mean volume. It is standardised with window 500 and min_periods 120. It is positive after a weekend rise and negative after a weekend fall, and it grows with both the move and the volume ratio. It is 0 on every other bar. The holding period keeps each bet for 48 bars, which covers Monday and Tuesday.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: A case is a signal bar (regime "trending" with a nonzero forecast). For each case, take the coin's return over the next 48 bars minus its normal 48-bar drift (holding the coin), times sign(forecast). The measure is the mean of this over all cases, with its t. Cases are weekly, so they do not overlap.
- Supporting check: Split the cases at the median |forecast|. The top half's mean directional excess return minus the bottom half's must be above 0.
- Confirm: The main mean's t is +2 or more and the supporting check passes (top half minus bottom half above 0).
- Reject: The main mean's t is -2 or less: heavy-volume weekend moves are reversed rather than continued.
- Inconclusive: A t between -2 and +2, or a t of +2 or more with a failed check. At least 100 cases are needed across coins and windows; fewer is inconclusive.
