---
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 10d8cbead801
---
Fidelity:
- Situation: the coin's 30-day return, larger meaning stronger -> kept: 30-bar percent return on daily bars.
- Comparison: the closer the close stands to its highest close of the past 60 days, the more so -> kept: the return is weighted by (1/(1+D))^2, D being the percent distance below the 60-bar closing high.
- Outcome: a larger rise over the next 5 days -> kept: 5-bar forward return, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's own product of monthly return and nearness to the 2-month high, judged on the 5-day move it claims.
Forecast: One component, HighProximityMomentumComponent (period 60, return_period 30, power 2, proximity "convex"). It computes the 30-day percent return times a nearness weight to the 60-day closing high. The weight is 1 at a new high and shrinks smoothly as the close falls further below that high. The result is standardised against its own past 60 values. The forecast is positive after a monthly rise and negative after a monthly fall, and zero only when the 30-day return is zero. Its size grows with the size of the return and with how close the coin is to its 60-day high. So strength at the high gives the largest long, and weakness far from the high gives only a small short. It is ungated and signed.
Config: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On each window's non-overlapping 5-bar grid, the coin's 5-bar forward return minus its normal 5-bar drift. The drift is the mean over all windows of that coin. This excess return is regressed on the bar's forecast (post_pipeline_value), pooled over coins and windows. The measure is the slope's t.
- Supporting check: The book's mean daily timing gain must be above 0. The timing gain is the book's daily return minus position held x the coin's mean daily return.
- Confirm: The slope t is +2.0 or more, and the timing gain is above 0.
- Reject: The slope t is -2.0 or less.
- Inconclusive: A slope t between -2.0 and +2.0 is inconclusive. A slope t of +2.0 or more with a timing gain of 0 or less is also inconclusive. At least 300 grid cases with a non-zero forecast are needed; fewer is inconclusive whatever the t.
