---
idea: 037-01_choppy-swing-scaled-fall-continues
brief: 037_choppy-market-multiday-falls-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: adf647c613f7
---
Fidelity:
- Situation: a coin's 5-day fall, measured in its own 20-day daily swings, in a choppy market -> kept: the 5-day return divided by the 20-day std of daily returns (the constant sqrt(5) cancels under standardise), short side only, inside the choppy profile.
- Comparison: the larger the fall in swing units, the larger the continuation -> kept: the short position grows with the fall's size in swing units.
- Outcome: the coin keeps falling over the next 5 days -> kept: a short held 5 daily bars.
- Verdict transfer: yes: the forecast is the idea's own measure, sized by it and held for its horizon, so a confirm or reject applies to the idea.
Forecast: One component, `VolatilityScaledReturnComponent` (period 5, vol_period 20): the 5-day return in usual daily moves of the last 20 days. It is standardised over 60 bars and clipped at a maximum of 0, so the forecast is negative (short) only after a 5-day fall, and 0 after a 5-day rise. The short grows linearly with the size of the fall in swing units. The choppy profile, added by code, keeps the book flat outside choppy markets.
Config: 037-01_choppy-swing-scaled-fall-continues_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Cases are the non-overlapping 5-bar grid bars of each window where the forecast is below 0. For each case, take the coin's 5-bar forward return minus its normal 5-bar drift (all windows), in the short direction. The measure is the mean of these unusual moves, with t computed from cases clustered by day.
- Supporting check: Split the cases at the median of |forecast|. The mean short-direction unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The main mean is above 0 with t ≥ 2, and the larger-half minus smaller-half difference is above 0.
- Reject: The main mean is below 0 with t ≤ -2: after choppy-market falls, prices rise more than the coin's drift.
- Inconclusive: A main t between -2 and 2, or a t ≥ 2 with the larger-half difference at or below 0. At least 30 cases on at least 30 distinct days are required; fewer is inconclusive.
