---
idea: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: a daily close that crosses up from below the coin's Ichimoku cloud to above it -> kept: the cross bar is read by `IchimokuCloudCrossAgeComponent` at age 1 (standard 9/26/52/26 cloud).
- Comparison: the more the coin fell over the past 26 days before the cross -> kept: the 26-bar return ending at the cross bar, negated, sizes the long; a cross after a run-up gets zero.
- Outcome: the coin rises over the next 26 days, more after a larger fall -> kept: each bet is held 26 daily bars, long only.
- Verdict transfer: yes: the test bets only at the cross, sizes the bet by the prior 26-day fall and holds it for 26 days, as the idea states.
Forecast: The regime is active only on the bar whose close is the first one above the cloud after the coin was last outside the cloud below it. On every other bar the forecast is 0. On that bar the forecast is the coin's 26-bar percent return, standardised against its own past 60 values (target 10, cap 20), negated and clipped at 0. It is positive and grows with the size of the fall over the 26 days ending at the cross. It is 0 when those 26 days rose. It is never negative. The bet is then held for 26 bars.
Config: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: The cases are the bets (forecast of 2 or more on a cross bar), counted once per 26-bar grid cell of each window, and only those with a full 26 bars left in their window. For each case, take the coin's 26-bar return from the cross close minus the coin's normal 26-bar drift over all windows. The measure is the ordinary t of the mean of these unusual moves.
- Supporting check: Split the cases at the median `forecast` on the cross bar. The mean unusual move of the larger-forecast half minus that of the smaller half must be above 0.
- Confirm: The mean unusual move is positive with t >= 2, and the supporting check passes (larger-fall half minus smaller-fall half > 0).
- Reject: The mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 whose supporting check fails is also inconclusive. Fewer than 20 independent cases over all coins and windows is inconclusive whatever the t.
