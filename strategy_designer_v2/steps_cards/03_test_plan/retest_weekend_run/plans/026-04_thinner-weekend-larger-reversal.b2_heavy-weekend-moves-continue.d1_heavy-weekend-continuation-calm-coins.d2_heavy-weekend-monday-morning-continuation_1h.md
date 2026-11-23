---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a coin's Saturday-Sunday move, graded by its size and by weekend volume -> kept: the 48-bar return to Sunday's last close, in the coin's usual 48h moves, times weekend over weekday mean hourly volume.
- Comparison: weekend volume higher than its mean over the preceding five weekdays -> kept: a regime rule requires the 48h mean volume over the prior 120h mean to be at least 1.
- Outcome: the price continues in the weekend move's direction over Monday's first 12 hours -> kept: the position is opened at Sunday's close and held 12 bars.
- Verdict transfer: yes: the test bets only on heavy-volume weekends, in the move's direction, sized by move and volume, over Monday 00:00-12:00 UTC.
Forecast: The forecast is computed once a week, on the bar stamped Sunday 23:00 UTC, when the coming bar is Monday 00:00. It is non-zero only when the weekend's mean hourly volume (the last 48 bars) is at least the mean over the 120 weekday bars before them. On that bar it is `RecentToPriorVolumeScaledReturnComponent` (`period` 48, `base_period` 120, `window` 720). That is the weekend's 48h return in the coin's usual 48h moves, times the weekend over weekday volume ratio. It is standardised over its last 500 hourly values (`min_periods` 120). The forecast is positive after a weekend rise and negative after a weekend fall. It grows with the size of the move and with the heaviness of the weekend volume. On every other bar it is 0, and the bet is held 12 bars.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation_1h_config.json
Criterion:
- Horizon: 12 bars
- Main measure: Each case is a non-zero forecast on a Sunday 23:00 bar. Measure the coin's return from that close to 12 bars later, minus the coin's mean 12-bar return over all windows, signed by the forecast. Take the mean over all cases and coins, with its t.
- Supporting check: The cases in the upper half of |forecast| have a higher mean signed excess return than those in the lower half (difference above 0).
- Confirm: The mean signed excess 12-bar return is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean signed excess 12-bar return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with the check failing is also inconclusive. Fewer than 200 cases over all coins and windows is inconclusive whatever the t.
