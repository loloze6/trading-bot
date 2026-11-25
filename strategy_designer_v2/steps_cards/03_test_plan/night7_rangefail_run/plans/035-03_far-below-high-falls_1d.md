---
idea: 035-03_far-below-high-falls
brief: 035_nearness-to-high-drift-any-market
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: f090b5ff5633
---
Fidelity:
- Situation: a daily close many daily swings below its 20-day high -> adapted: a regime of closes at least 2 daily swings below the prior 20-day closing high (convention), graded inside by the depth.
- Comparison: depth measured in the coin's own daily swings -> kept: distance from the prior 20-day high over the std of the last 20 daily returns.
- Outcome: a fall over the next 5 days, larger the deeper below the high -> kept: a short held 5 bars, sized by the depth.
- Verdict transfer: yes: the book is short only on deep-below-high closes, sized by depth, and held for the idea's 5 days.
Forecast: VolatilityScaledDistanceFromHighComponent (period 20, vol_period 20) gives the close's distance from the highest close of the prior 20 days, in daily swings. The regime detector selects `trending` only when that distance is -2 or lower. Elsewhere the forecast is 0. Inside the regime the forecast is the distance standardised over its last 60 values, clipped at 0 above. It is negative (short) and grows in size the more swings the close sits below the high.
Config: 035-03_far-below-high-falls_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The mean unusual move over 5 bars on the cases. A case is a short bet, one per 5-bar grid cell. The unusual move is the coin's 5-bar return minus its normal 5-bar drift, taken in the short direction. Its t is computed with cases clustered by day, before costs.
- Supporting check: Split the cases at the median depth (`last_history_value`). The deeper half must show a mean unusual move larger than the shallower half (difference deeper minus shallower above 0).
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t ≤ -2.
- Inconclusive: Any other result is inconclusive, including t between -2 and 2, or t ≥ 2 with a failed supporting check. Fewer than 30 distinct case days is also inconclusive.
