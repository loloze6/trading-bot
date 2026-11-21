---
idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a31b77de3651
---
Fidelity:
- Situation: close above the Ichimoku cloud while the cloud is rising -> kept: a regime rule on cloud position (close above the top, as a percent of the top) above 0 and the 26-bar cloud mid-level slope above 0.
- Comparison: larger the thicker the cloud (span gap as a share of price), not the faster it rose -> kept: the forecast grows with cloud width as a percent of the close, and the check pits width against the slope.
- Outcome: the 26-day return is positive, and larger with thickness -> kept: every bet is held 26 bars and judged on the 26-bar forward return.
- Verdict transfer: yes: the regime selects exactly the above-rising-cloud bars, and the position inside it grows only with thickness.
Forecast: The regime is active only when two things hold: the close is above the cloud top (IchimokuCloudPositionComponent at 9/26/52/26, edge "top"), and the cloud's mid level is higher than 26 bars ago (IchimokuCloudSlopeComponent, lookback 26). Inside that regime the forecast is the cloud width (IchimokuCloudWidthComponent at 9/26/52/26, the gap between the spans as a percent of the close). The width is standardised against its own past 78 values, so it is about +10 for a cloud of usual thickness, above 10 for a thicker one (capped at 20) and near 0 for a very thin one. The forecast is always long and graded by thickness. Outside the regime it is 0 (flat).
Config: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: Take the in-regime bars on the non-overlapping 26-bar grid of each window. For each, compute the coin's 26-bar forward return minus its mean 26-bar return over all windows (holding the coin). Regress this excess return on the recorded forecast, pooled over coins, and read the slope's t.
- Supporting check: On the same cases, regress the excess return jointly on the standardised cloud width and the standardised 26-bar cloud slope (the slope is recomputed from prices). The width coefficient must exceed the slope coefficient.
- Confirm: The forecast slope is positive with t >= 2 on at least 30 independent cases, and the supporting check passes.
- Reject: The forecast slope is negative with t <= -2 on at least 30 independent cases.
- Inconclusive: A t between -2 and 2 is inconclusive. A confirming slope whose width coefficient does not exceed the slope coefficient is also inconclusive. Any result on fewer than 30 independent in-regime cases is inconclusive.
