---
idea: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 2a96c3272007
---
Fidelity:
- Situation: a Saturday-Sunday move that is large in the coin's usual 48-hour moves, read on Sunday's close -> kept: the 48-bar return over its 720-bar mean absolute 48-bar return, read only on the bar closing Sunday 24:00 UTC.
- Comparison: weekend volume against the preceding five weekdays' volume -> kept: the mean volume of bars t-168..t-49 over the mean volume of bars t-47..t.
- Outcome: the weekend move is reversed over Monday and Tuesday, more so as move × thinness grows, and only for large moves -> adapted: the large-move threshold becomes a graded cubic dead zone on move × thinness, and the bet is held 48 bars.
- Verdict transfer: yes: the forecast is the negated product of move size and thinness, set at Sunday's close and held over Monday and Tuesday, so its result is the idea's.
Forecast: The forecast is computed only on the bar whose close is Sunday 24:00 UTC. The detector selects that bar when the coming bar is Monday, hour 0. It is flat on every other bar, and the holding period carries the bet through Monday and Tuesday. On that bar the forecast is `ThinVolumeScaledReturnComponent` with `period` 48, `window` 720, `volume_period` 48, `base_near` 49 and `base_far` 168. This is the weekend's 48-bar return counted in usual 48-hour moves (720-bar mean), times the five weekdays' mean volume over the weekend's mean volume. It is standardised over its own past 500 values and negated, so it bets against the move: short after a weekend rise, long after a weekend fall. It then passes through `signed_power` with exponent 3. Small or normal-volume moves give a position near zero; the position grows with the cube of move × thinness, so only the largest thin weekend moves carry real size. It is zero when the weekend was flat.
Config: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: Each Sunday-close case with a non-zero forecast gives one value: the coin's return over the next 48 bars, minus the coin's normal 48-bar drift over all windows. Regress that value on the case's forecast, using one case per coin-week (cases are 168 bars apart, so they do not overlap). The measure is the slope and its t.
- Supporting check: The 20 % of cases with the largest |forecast| must show a mean signed unusual move (the drift-removed return in the forecast's direction) above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2: larger thin-weekend moves continue rather than reverse.
- Inconclusive: Any slope with -2 < t < 2, or t ≥ 2 with a failed supporting check. The test also needs at least 300 cases with a non-zero forecast across all coins; fewer is inconclusive.
