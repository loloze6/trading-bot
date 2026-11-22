---
idea: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: cb945cd336ee
---
Fidelity:
- Situation: a 24-hour panic stretch (range several times usual, hard fall) that ended one day ago, after a deeply negative 90-day return -> adapted: the panic threshold is made graded (the fall in usual 24h moves times the range in usual 24h ranges, over the stretch ending 6 bars ago), and "after X" is made "while X".
- Comparison: higher than usual, only while the 90-day return before the stretch is deeply negative, and more so the deeper it is -> adapted: the 540-bar fall up to the stretch's start is a graded multiplier that is 0 when that return is not negative, and the case's move is judged against the coin's normal drift.
- Outcome: the return from one day after the stretch to 14 days after it is higher -> kept: each bet starts 6 bars after the stretch ends and is held 78 bars (13 days), long.
- Verdict transfer: yes: the forecast is exactly the idea's graded prior-fall times panic reading, read one day after the stretch and held for the 13 days the idea names.
Forecast: One component, PriorFallTimesScaledFallRangeMultipleComponent (period 6, lag 6, window 180, prior_period 540). It reads the 24h stretch that ended 24h ago. It multiplies three parts: the coin's 90-day fall up to that stretch's start, in percent; the stretch's fall in usual 24h moves over 30 days; and the stretch's 24h range in multiples of its 30-day mean. The value is standardised against its own past 500 values. Then signed_power with exponent 3 damps ordinary readings towards 0 and amplifies extreme ones. The forecast is 0 unless both the 90-day return and the stretch's return are negative. It is never negative, so the strategy is long only. It grows smoothly with the depth of the prior fall, the depth of the panic and the size of its range.
Config: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h_config.json
Criterion:
- Horizon: 78 bars
- Main measure: The unusual move per case, averaged over the cases with its ordinary t. A case is a long bet (a rise of the forecast of at least 2 points, read once per 78-bar grid cell of each window). Its unusual move is the coin's 78-bar return from the signal bar's close minus the coin's normal 78-bar drift, before costs.
- Supporting check: The forecast-weighted mean unusual move of the cases (weighted by the forecast on the signal bar) is above 0.
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2. Also a positive t of 2 or more when the weighted check fails. Fewer than 30 cases is inconclusive whatever the t.
