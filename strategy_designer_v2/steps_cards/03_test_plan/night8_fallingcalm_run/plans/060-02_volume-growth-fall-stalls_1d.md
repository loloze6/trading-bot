---
idea: 060-02_volume-growth-fall-stalls
brief: 060_volume-dry-up-extends-downtrends
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ca7c09a81ba4
---
Fidelity:
- Situation: a falling market, with volume over the past 30 days grown against the 30 days before -> kept: the falling profile is added by code, and inside it the 30-day over prior-30-day volume ratio is graded.
- Comparison: the more volume has grown, against less growth or shrinkage -> kept: the forecast's size and sign follow the log of that ratio.
- Outcome: a smaller fall or a larger rise over the next 5 days, the larger the growth -> kept: the 5-day return should grow with the forecast.
- Verdict transfer: yes: a 5-day return that rises with the volume ratio inside falling markets is exactly the claim, and a return that falls with it contradicts it.
Forecast: One component, `VolumeRatioComponent` (period 30, short_period 30, exclude_current 30, form "log"). It reads ln(mean volume of bars t-29..t / mean volume of bars t-59..t-30), which is 0 when the two months traded the same. It is standardised over its last 60 values (min_periods 20). The forecast is positive (long) when recent volume has grown, negative (short) when it has shrunk, and zero at equal volume. Its size grows continuously with the log ratio. It is active only inside the falling profile, which step 3's code adds, and flat elsewhere.
Config: 060-02_volume-growth-fall-stalls_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The slope, with its t, of a least-squares fit of the coin's 5-bar forward return minus its normal 5-bar drift on the forecast. The fit uses cases on bars with a nonzero forecast, taken on each window's non-overlapping 5-bar grid. The normal drift is the coin's mean 5-bar return over all its windows.
- Supporting check: The mean excess 5-bar return of cases with a positive forecast, minus that of cases with a negative forecast, is above 0. This is the growing-volume against shrinking-volume difference.
- Confirm: The slope has t ≥ 2 and the supporting difference is above 0, with at least 100 cases.
- Reject: The slope has t ≤ -2, with at least 100 cases.
- Inconclusive: A slope t between -2 and 2, or a slope t ≥ 2 whose supporting difference is not above 0, or fewer than 100 grid cases with a nonzero forecast.
