---
idea: 028-02_volume-surge-down-continuation
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour that falls far more than its typical 30-day hourly move, on volume several times its 30-day average -> adapted: the two thresholds become one graded product, the fall in 720-bar return standard deviations times volume over its 720-bar mean, kept on the fall side only.
- Comparison: the larger that hour's volume relative to its usual volume, the larger the further fall -> kept: the volume ratio scales the forecast's size directly.
- Outcome: the price keeps falling over the next two to six hours -> kept: each short bet is held 6 bars, the upper end of the stated span.
- Verdict transfer: yes: the forecast is short exactly when the hour fell on heavy volume, and larger as the fall and the volume ratio grow, so its gains test the idea both ways.
Forecast: The forecast uses one indicator, `VolumeWeightedScaledReturnComponent`. It takes the last hour's return in 720-bar (30-day) return standard deviations and multiplies it by that hour's volume over its 720-bar mean volume. This is standardised against its own past 500 values and clipped at 0 from above, so only falls count. It then goes through `signed_power` with exponent 3, so ordinary hours stay near zero and only large falls on heavy volume give a sizeable short. The forecast is negative (short) after a down hour, larger as the fall and the volume ratio grow, and zero after an up hour. It is never positive.
Config: 028-02_volume-surge-down-continuation_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: A case is a short bet: a fall of the forecast of at least 2 points, read once per 6-bar grid cell of each window. For each case, take the coin's 6-bar return from the signal bar's close, minus the coin's normal 6-bar drift over all windows, with the sign flipped so a further fall counts positive. Measure the mean of this over the cases and its t.
- Supporting check: Across the cases, the rank correlation between the signal hour's volume ratio (from `last_history_value`, or recomputed from volume over its 720-bar mean) and the case's unusual move is above 0.
- Confirm: The mean unusual fall is above 0 with t ≥ 2, over at least 30 cases pooled over BTC and ETH, and the supporting rank correlation is positive.
- Reject: The mean unusual move is a rise, with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with a rank correlation of 0 or below, or fewer than 30 cases.
