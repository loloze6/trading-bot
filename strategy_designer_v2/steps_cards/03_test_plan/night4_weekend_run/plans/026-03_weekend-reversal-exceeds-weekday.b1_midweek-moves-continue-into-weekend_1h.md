---
idea: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a coin's 48-hour return over Wednesday and Thursday -> kept: the 48-bar return read at Thursday's last hourly close, which is the only bar the regime is active.
- Comparison: the larger the Wednesday-Thursday move, the larger the move that follows -> kept: the position is graded by the size of the standardised 48-bar return.
- Outcome: a same-direction move over Friday and Saturday (next 48 hours) -> kept: the bet is held 48 bars, from Thursday's last close to Saturday's last close.
- Verdict transfer: yes: the test bets the exact Wednesday-Thursday move, at its size, over exactly Friday and Saturday.
Forecast: The forecast is computed only on the bar whose coming bar starts Friday 00:00 UTC, which is Thursday's 23:00 bar. That bar is selected by the weekday rule (4) and the hour rule (0). On that bar the forecast is the 48-bar percent return, from Tuesday's last close to Thursday's last close, standardised against its own last 60 hourly values (min_periods 20). It is positive after a midweek rise and negative after a midweek fall, and its size grows with the move, capped at ±20. On every other bar the forecast is 0. The 48-bar holding period keeps that bet through Friday and Saturday.
Config: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: Each case is a Thursday-23:00 bar, one per coin per week, with a non-zero forecast; these cases do not overlap. The main measure is the slope, with its t, of a least-squares fit across these cases. The dependent variable is the coin's 48-bar return from that close minus the coin's normal 48-bar drift over all windows. The regressor is the forecast.
- Supporting check: The mean of that drift-removed 48-bar return, taken in the forecast's direction, is above 0 over all cases.
- Confirm: The slope is positive with t ≥ 2, and the supporting mean is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: The result is inconclusive when the slope's t is between -2 and 2. It is also inconclusive when t ≥ 2 but the supporting mean is not above 0. A verdict needs at least 300 cases across coins and windows; fewer is inconclusive.
