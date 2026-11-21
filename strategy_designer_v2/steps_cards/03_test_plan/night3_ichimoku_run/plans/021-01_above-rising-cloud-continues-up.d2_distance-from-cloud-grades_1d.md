---
idea: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: the daily close stands above or below the top of its Ichimoku cloud (9/26/52 midpoints, plotted 26 days ahead) -> kept
- Comparison: how far the close is from the cloud top, as a signed distance -> kept
- Outcome: the next 26 days' return is larger the farther above and smaller the farther below -> kept
- Verdict transfer: yes: the forecast is the signed percent distance of the close from the cloud top, and the test checks whether the 26-bar return rises with it.
Forecast: The forecast uses one indicator, IchimokuCloudPositionComponent with tenkan 9, kijun 26, senkou 52, displacement 26, edge "top" and base "edge". It is the percent distance of the close above the cloud top, which is the higher of the two leading spans plotted at today's bar. Standardise divides it by its mean absolute value over the prior 78 bars, which gives about ±10, capped at ±20. The forecast is positive and grows the farther the close sits above the cloud top. It is negative, giving a short, and grows in size the farther the close sits below the top. It is near zero at the top. There is no regime gate, so the position changes in steps of the distance.
Config: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: Use the bars at positions 0, 26, 52, ... of each window. For each, take the coin's 26-bar forward return minus its normal 26-bar drift (its mean over all its windows). Regress this pooled across coins on the forecast at that bar. The measure is the t of the slope.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2, on at least 100 non-overlapping cases.
- Reject: The slope is negative with t ≤ -2, on at least 100 non-overlapping cases.
- Inconclusive: The result is inconclusive if t is between -2 and 2, or if there are fewer than 100 non-overlapping cases (about 550 are expected).
