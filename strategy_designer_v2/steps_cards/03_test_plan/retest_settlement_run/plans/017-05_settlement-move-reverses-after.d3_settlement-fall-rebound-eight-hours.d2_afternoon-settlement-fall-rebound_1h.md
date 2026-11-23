---
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a fall over the 2 hours before the 16:00 UTC funding settlement -> kept: the 2-bar return ending at the 16:00 close, read only on that bar, through a clock regime.
- Comparison: the fall against the coin's usual 2-hour move -> kept: the fall is divided by the coin's mean absolute 2-hour return over the last 720 bars.
- Outcome: the return over the 8 hours after the settlement rises, more for a larger fall -> kept: an 8-bar hold from the 16:00 close, sized by the scaled fall.
- Verdict transfer: yes: the test bets on exactly the post-settlement 8h return, sized by the scaled pre-settlement fall, so its result is the idea's.
Forecast: A clock regime is active only on the bar whose close is the 16:00 UTC settlement (HourOfDay of the coming bar = 16). On every other bar the forecast is 0. On that bar the forecast is the 2-hour return divided by the coin's mean absolute 2-hour return over 720 bars. It is standardised over its own past 500 values, negated, and clipped at 0. It is positive only after a 2-hour fall, and grows linearly with the fall's size in usual 2-hour moves, up to the cap of 20. After a 2-hour rise it is 0. The bet is then held for 8 bars.
Config: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h_config.json
Criterion:
- Horizon: 8 bars
- Main measure: Over the cases (16:00 settlement bars with forecast > 0), take the coin's 8-bar return from the signal bar's close. Subtract the coin's normal 8-bar drift, the mean over non-overlapping 8-bar stretches of all its windows. Multiply that by the forecast. The measure is the mean of this product, with its ordinary t, pooled over coins and windows.
- Supporting check: The mean drift-removed 8-bar return of the cases with forecast above the cases' median must exceed that of the cases below the median (difference > 0).
- Confirm: The main-measure mean is > 0 with t >= 2, and the supporting check passes.
- Reject: The main-measure mean is < 0 with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the supporting check failing, is inconclusive. Fewer than 300 cases is also inconclusive. The cases are one per coin per day, and are independent because 8 bars is less than the daily spacing.
