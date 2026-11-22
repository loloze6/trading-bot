---
idea: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 3503e22a3698
---
Fidelity:
- Situation: a coin's 24-hour fall, deeper is stronger -> kept: the 6-bar return, sign flipped and clipped at 0.
- Comparison: against the coin's usual 24-hour move -> kept: divided by the mean absolute 6-bar return over 180 bars (30 days, by convention).
- Outcome: return above normal drift over the next 14 days, higher the deeper the fall -> kept: held 84 bars and judged against holding the coin.
- Verdict transfer: yes: the forecast is the scaled fall depth itself, held for the idea's 14 days, so a confirm or a reject carries over to the idea.
Forecast: The forecast uses MeanAbsScaledReturnComponent with period 6 and window 180. Its raw value is the 24-hour return counted in usual 24-hour moves of the last 30 days. It is standardised over its past 180 values, then negated, so a fall reads positive. It is then clipped at 0. The forecast is 0 when the last 24 hours rose or were flat, and long otherwise. The long position grows linearly with the depth of the fall in usual moves, up to the cap of 20. It is never short.
Config: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: Use the bars at positions 0, 84, 168, … of each window. On each, take the coin's 84-bar forward return minus its normal drift (its mean 84-bar return over all windows). Regress that excess return on the forecast at the bar, pooled over coins, and read the slope's t.
- Supporting check: Take the cases with forecast above 0. Their mean unusual move (the 84-bar return minus the normal drift) must be above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes, with at least 200 cases.
- Reject: The slope's t is -2 or less, with at least 200 cases.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a slope t of 2 or more when the cases' mean unusual move is not above 0. So is any result with fewer than 200 cases.
