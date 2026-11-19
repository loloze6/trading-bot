---
idea: 016-02_down-grind-price-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: the coin has fallen over the past 3 days (72 bars) -> kept: the sign of the 72-bar net return, with the short side kept by clip max 0.
- Comparison: share of the fall made by many small hourly losses rather than by its few biggest hours -> kept: 1 minus the share of the window's losses carried by its 3 largest loss hours.
- Outcome: the coin keeps falling over the next 3 days (72 bars), downward -> kept: a short position, judged on the 72-bar forward return.
- Verdict transfer: yes: the forecast is short only after a 3-day fall and grows with how much of that fall was a grind, which is exactly the idea's claim.
Forecast: LossShareBeyondLargestComponent (period 72, k 3) gives, over the last 72 hourly bars, the share of the summed hourly losses not carried by the 3 largest losses. It is signed by the 72-bar net return, so it is negative after a net fall. Standardise (window 72, min_periods 20) puts it on the forecast scale, and clip max 0 keeps only net falls. The forecast is 0 when the coin did not fall over 3 days. After a fall it is negative (short), and it grows more negative as more of the fall comes from many small losses rather than a few big hours. It goes down to about -20 for a fall spread almost entirely over many small hours. It is never positive.
Config: 016-02_down-grind-price-continuation_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The sample is the bars of a non-overlapping 72-bar grid in each window where the forecast is below 0, pooled over coins and windows. On each such bar, the case gain is (forecast / 10) x (the coin's 72-bar forward return minus that coin's mean 72-bar return over all windows). The measure is the mean of this gain and its t.
- Supporting check: Among the same grid bars, take the excess 72-bar forward return of bars with forecast below the median forecast (larger grind) minus that of bars above it. The point estimate must be below 0 (Welch t reported).
- Confirm: The main measure's mean gain is above 0 with t >= 2, and the supporting check's difference is below 0.
- Reject: The main measure's mean gain is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main t >= 2 with a supporting difference of 0 or above is also inconclusive. Fewer than 300 grid bars with a negative forecast is inconclusive whatever the t.
