---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a coin's Saturday-Sunday fall, larger is stronger -> kept: the 48-bar return ending at Sunday 23:00's close, shorts only on a fall.
- Comparison: weekend volume heavier than its mean over the preceding five weekdays -> kept: a rule requires the ratio of the two means above 1, and the ratio scales the size.
- Outcome: the fall continues downward over Monday's first 12 hours -> kept: the short is opened at Sunday's last close and held 12 bars.
- Verdict transfer: yes: the test measures this fall, on this volume, over this Monday window and in this direction, so its verdict is the idea's.
Forecast: The regime is active only on the bar whose coming bar is Monday 00:00 UTC, and only when weekend volume is above the weekday base. That base is the mean volume of the last 48 bars against the mean of the 120 bars before them (Monday to Friday). On that bar the forecast is `RecentToPriorVolumeScaledReturnComponent` (period 48, window 720, base_period 120). This is the weekend return, counted in usual 48-hour moves, times the weekend-to-weekday volume ratio. It is standardised over its last 500 values and clipped at a maximum of 0, so it is short only. It is negative after a weekend fall and grows in size with the depth of the fall and the heaviness of the volume. It is 0 after a weekend rise and on every other bar. The 12-bar holding period keeps the short through Monday 00:00 to 11:00.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue_1h_config.json
Criterion:
- Horizon: 12 bars
- Main measure: The cases are the signal bars, where the forecast is -2 or below (Sunday 23:00 closes), one per coin-week. For each case, take the coin's 12-bar return from that close, in the short direction (negated), minus the coin's mean 12-bar return over all its windows on non-overlapping stretches. The measure is the ordinary t of the mean of these values, before costs.
- Supporting check: The least-squares slope of that short-direction excess return on the size of the forecast, across the cases, is positive.
- Confirm: The mean short-direction excess return is positive with t >= 2, and the slope on the forecast's size is above 0.
- Reject: The mean short-direction excess return has t <= -2, which means Monday's first 12 hours rise beyond the coin's drift after heavy-volume weekend falls.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 with a slope at or below 0. Fewer than 30 cases over all coins and windows is also inconclusive.
