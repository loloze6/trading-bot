---
idea: 050-03_falling-calm-range-scaled-week-fall
brief: 050_calm-downtrend-scaled-weeks-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling, calm market, a coin that has fallen over the last 7 days -> kept: the profile is added by code, and the 7-day fall is a regime (7-day return below 0).
- Comparison: the 7-day fall in units of the 30-day average daily high-low range -> kept: the 7-day return over the 30-day mean (high-low)/close, graded.
- Outcome: keeps falling over the next 3 days, further the larger the scaled fall -> kept: a short position, held 3 bars, that grows with the scaled fall.
- Verdict transfer: yes: the test measures this situation, this scaling, this side and this horizon.
Forecast: On bars where the 7-day return (PriceEvolutionComponent, period 7) is below 0, the forecast comes from MeanAbsScaledReturnComponent (period 7, window 30, base "mean_relative_range", form "ratio"). That component is the 7-day return divided by the 30-day mean daily range as a share of the close. It is standardised over its past 60 values (min_periods 20), then clipped at max 0. The forecast is negative (short) and grows in size with the scaled fall. It is 0 at no fall, and it is 0 on bars that did not fall over 7 days (null regime). It is never positive. The profile (falling calm) is added by code.
Config: 050-03_falling-calm-range-scaled-week-fall_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The sample is the cases: bars where the forecast falls by at least 2 points on the short side, read once per 3-bar grid cell in each window. For each case, the unusual move is the coin's 3-bar return minus its normal 3-bar drift (from all its windows), taken in the short direction. The measure is the mean of that unusual move, with its t. Cases from the same day are summed into one deviation.
- Supporting check: Split the cases at the median of |forecast|. The larger-forecast half must have a higher mean unusual move than the smaller half (difference larger minus smaller > 0).
- Confirm: The mean unusual move is > 0 with t >= 2, over at least 30 distinct case days, and the supporting check passes.
- Reject: The mean unusual move is < 0 with t <= -2 over at least 30 distinct case days, which is a reversal against the short.
- Inconclusive: Any t between -2 and 2. Also a confirm-level main measure whose supporting check fails. Also fewer than 30 distinct case days.
