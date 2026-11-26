---
idea: 054-02_strong-close-reclaim-rebound
brief: 054_reclaimed-monthly-low-in-falling-agitated
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a falling, agitated market, the day trades below its prior 30-day low but closes back above it -> kept: the profile is added by code, and the pierce-and-reclaim of the prior 30-day low is a regime rule.
- Comparison: the close's height above that low, against the day's range -> kept: (close − low30) / (high − low), from `PriorLowReclaimInRangeComponent`, sets the size of the position.
- Outcome: the coin rises over the next 5 days, more after a higher reclaim -> kept: the book is long for 5 daily bars, sized by the reclaim.
- Verdict transfer: yes: the book is long only on reclaim days in the profile, sized by the idea's own measure, so its 5-day result is the idea's result.
Forecast: A regime rule makes the book active only on bars where `ReclaimedPriorLowPierceDepthComponent` (period 30) is above 0. That means the day's low went below the lowest low of the prior 30 days and the close ended at or above that low. On every other bar the forecast is 0. The profile is added by code, so outside falling agitated bars it is also 0. On an active bar the forecast is `PriorLowReclaimInRangeComponent` (period 30, form "reclaim"): (close − prior 30-day low) / (day's high − day's low). This is near 0 for a close just above the low and nears 1 for a close at the day's high. It is standardised against its own past 60 values (window 60, min_periods 20, capped at 20). The forecast is therefore always zero or positive (long only) and grows linearly with how high the close reclaims within the day's range.
Config: 054-02_strong-close-reclaim-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: For each case (a rise of the forecast of at least 2 points, read once per 5-bar grid cell of each window), take the coin's 5-bar return from the signal bar's close. Subtract the coin's mean 5-bar return on falling agitated bars, measured on the non-overlapping 5-bar grid of all its windows. Measure the mean of that excess and its t, with cases on the same day counted together.
- Supporting check: Split the cases at the median forecast. The mean excess 5-bar return of the upper half minus that of the lower half must be above 0.
- Confirm: The mean excess return is positive with t ≥ 2, and the upper half beats the lower half (difference > 0). At least 30 cases are needed.
- Reject: The mean excess return is negative with t ≤ −2, with at least 30 cases.
- Inconclusive: Any t between −2 and 2, or t ≥ 2 with the upper half not beating the lower half, or fewer than 30 cases over all coins and windows.
