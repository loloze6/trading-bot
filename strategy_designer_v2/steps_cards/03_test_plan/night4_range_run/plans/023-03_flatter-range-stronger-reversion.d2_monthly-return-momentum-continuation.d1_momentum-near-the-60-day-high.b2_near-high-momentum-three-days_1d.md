---
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 10d8cbead801
---
Fidelity:
- Situation: the coin's 30-day return, larger meaning stronger -> kept
- Comparison: how close the close stands to its highest close of the past 60 days, which strengthens the link -> kept
- Outcome: a larger rise over the next 3 days, a week being too long -> kept
- Verdict transfer: yes: the forecast is the 30-day return weighted by nearness to the 60-day closing high, held 3 days, which is the idea's own relation.
Forecast: The forecast uses HighProximityMomentumComponent with `period` 60, `return_period` 30, `proximity` "convex" and the catalogue's default `power` 2. It computes the 30-day percent return times (1/(1+D))², where D is the percent distance of the close below its highest close of the last 60 days. It is then standardised against its own past 60 values. The forecast is positive after a monthly rise and negative after a monthly fall. Its size grows with the size of the 30-day move and shrinks as the close sits further below the 60-day high. Monthly weakness far from the high therefore gives only a small short. The forecast is zero only when the 30-day return is zero.
Config: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: On each window's non-overlapping 3-bar grid, take the coin's next-3-bar return minus that coin's mean 3-bar return over all windows. Regress this excess return on the recorded forecast, pooled over coins and windows, and read the slope's t.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2.0, on at least 300 grid cases with a nonzero forecast.
- Reject: The slope is negative with t ≤ -2.0, on at least 300 grid cases with a nonzero forecast.
- Inconclusive: Any t between -2.0 and 2.0 is inconclusive. Fewer than 300 grid cases with a nonzero forecast is also inconclusive, whatever the t.
