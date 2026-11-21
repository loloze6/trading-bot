---
idea: 021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: a daily close that crosses down from above the coin's Ichimoku cloud to below it -> kept: the cloud cross age is -1 on exactly that close, which is the regime rule.
- Comparison: only while the 26-day return is already a fall, and the deeper that fall at the cross, the larger the bet -> kept: a regime rule requires the 26-day return below 0, and the short is sized by that return's depth on the cross bar.
- Outcome: the coin falls over the next 26 days -> kept: each bet is held 26 daily bars, short.
- Verdict transfer: yes: the test bets only at the stated cross, sizes the bet by the stated 26-day fall, and holds it for the stated 26 days.
Forecast: The forecast is 0 on every bar except a cross bar. A cross bar is a close below the default Ichimoku cloud (9/26/52, displacement 26) where the last close outside the cloud before it was above the cloud, and where the 26-bar return is negative. On such a bar the forecast is the 26-bar price change, standardised against its own past 60 values (about -10 for a usual-sized fall) and clipped at 0. It is therefore a short that grows with the depth of the 26-day fall, up to -20. It is never positive. The holding period keeps each such bet for 26 bars.
Config: 021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: Each case is a short bet on a cross bar. Measure the coin's 26-bar return from that bar's close, minus the coin's normal 26-bar drift over all windows, taken in the short direction (the unusual move). Take its mean over the cases, with the t of the mean.
- Supporting check: Regress the cases' unusual move on the absolute forecast at the cross. The slope must be positive: deeper prior falls are followed by larger falls.
- Confirm: The mean unusual move is positive with t ≥ 2, and the supporting slope is above 0.
- Reject: The mean unusual move is negative with t ≤ -2, meaning the coin rises more than its drift after these breaks.
- Inconclusive: Any t between -2 and 2, or a positive main result with a slope at or below 0, is inconclusive. Fewer than 30 cases across all coins and windows is also inconclusive, whatever the t.
