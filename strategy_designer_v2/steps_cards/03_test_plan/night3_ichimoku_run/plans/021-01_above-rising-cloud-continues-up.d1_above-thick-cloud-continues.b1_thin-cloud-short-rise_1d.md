---
idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: the coin closes above its Ichimoku cloud and the cloud is rising -> kept: a regime rule needs the close above the cloud top and a positive cloud slope over 26 bars.
- Comparison: a thinner cloud (the gap between the spans as a share of price) against a thicker one -> kept: the cloud width as a percent of the close, read as 1 / (1 + width), which grows as the cloud thins.
- Outcome: the return over the next 5 days is larger, upward, the thinner the cloud -> kept: the 5-day return is measured against the forecast's size.
- Verdict transfer: yes: the regime is exactly the above-rising-cloud situation, and the size grows only with cloud thinness, so the gradient of 5-day returns on size is the idea's claim.
Forecast: The forecast is zero unless the close is above the cloud top (Ichimoku 9/26/52, displacement 26) and the cloud's mid level rose over the last 26 bars. Inside that regime the forecast is long. Its size is the cloud's thinness, 1 / (1 + |spanA − spanB| / close × 100), standardised against its own past 78 values. It sits about +10 at a usual thinness, rises toward +20 as the cloud thins, and falls toward 0 as it thickens. It is never negative.
Config: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take the bars on each window's non-overlapping 5-bar grid where the forecast is above 0, pooled over coins. Regress each case's 5-day return, minus that coin's normal 5-day drift over all windows, on the case's forecast. The measure is the t of the slope.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2: excess 5-day returns grow with cloud thinness inside the above-rising-cloud regime.
- Reject: The slope is negative with t ≤ -2: thinner clouds are followed by smaller excess returns.
- Inconclusive: A slope t between -2 and 2 is inconclusive. Fewer than 50 grid cases with a forecast above 0 is also inconclusive, whatever the t.
