---
idea: 031-01_near-yearly-low-keeps-falling
brief: 031_yearly-low-capitulation-or-exhaustion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: daily close near its lowest close of the past 365 days -> kept: `DistanceFromHighComponent` proximity to the 365-bar closing low, graded from 0 (far) to 1 (at the low)
- Comparison: closer to the low against farther from it -> kept: the short is sized by proximity, so cases far from the low carry almost no position
- Outcome: the coin falls more over the next 20 days the closer it was -> kept: short, held 20 daily bars, gains measured against the coin's drift
- Verdict transfer: yes: the test measures whether the 20-bar fall grows with closeness to the yearly low, which is exactly the idea's claim.
Forecast: The proximity of the close to its lowest close of the last 365 daily closes is 1 / (1 + D), where D is the percent distance above that low. It equals 1 at the low and falls fast toward 0 as the close moves away, so the signal is concentrated near the low. It is standardised against its own past 365 values (bar t left out) and negated. The forecast is therefore always short or near flat. It is about -10 at the usual proximity, near 0 when the coin sits far above its yearly low, and down to the -20 cap when the close is at or near the low. There is no long side.
Config: 031-01_near-yearly-low-keeps-falling_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The sample is the non-overlapping 20-bar grid of each window (positions 0, 20, 40, ...). For each case, the short gain is minus (the coin's 20-bar forward return minus its mean 20-bar return over all windows). The measure is the least-squares slope of that short gain on the size of the forecast, |forecast|, at the case's bar, with its t.
- Supporting check: Take the cases in the top fifth of |forecast|, the ones nearest the yearly low. Their mean short gain, net of the coin's drift, must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the top-fifth mean short gain is above 0. Together these say the short gains grow the closer the close is to its yearly low.
- Reject: The slope is negative with t ≤ -2. That means gains fall as proximity rises, so declines near the low reverse rather than continue.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A confirming slope whose top-fifth check fails is also inconclusive. At least 100 non-overlapping cases are needed across all coins and windows (about 860 are expected); with fewer the result is inconclusive.
