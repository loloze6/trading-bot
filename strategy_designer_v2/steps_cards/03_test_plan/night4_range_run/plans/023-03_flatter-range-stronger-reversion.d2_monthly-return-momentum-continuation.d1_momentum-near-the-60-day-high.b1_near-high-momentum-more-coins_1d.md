---
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 10d8cbead801
---
Fidelity:
- Situation: a coin's 30-day return, larger is stronger -> kept
- Comparison: how close the close stands to its highest close of the past 60 days -> kept
- Outcome: a larger rise over the next 5 days, more so near the 60-day high -> kept
- Verdict transfer: yes: the forecast is the 30-day return weighted by nearness to the 60-day closing high, tested against the next 5 days' return.
Forecast: The forecast uses one indicator, HighProximityMomentumComponent with a 60-day window and a 30-day return, in its "convex" form at its default power of 2. It computes the 30-day percent return times (1 / (1 + D))^2, where D is the percent distance of the close below its highest close of the last 60 days. The weight is 1 at a new 60-day high and shrinks smoothly as the close falls further below it. The value is standardised against its own past 60 values, giving an average absolute size of about 10, capped at ±20. The forecast is: - positive (long) when the 30-day return is up; - negative (short) when it is down; - zero when the return is flat. Its size grows with the size of the monthly move and with nearness to the 2-month high. This means strength at the high gives the largest longs, and weakness far below the high gives only small shorts. There is no regime: the forecast is active on every bar.
Config: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the bars at positions 0, 5, 10, ... of each window, pooled over all coins and windows. For each case, the coin's 5-day return from that bar's close minus the coin's mean 5-day return over all its windows (non-overlapping) is regressed on the bar's forecast. The measure is the slope's t.
- Supporting check: The book's mean daily return before costs, minus its gain from the market's own rise (position × the coin's mean daily return), must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A slope with t ≥ 2 while the check is at or below 0 is also inconclusive. At least 200 grid cases with a non-zero forecast are required; fewer is inconclusive.
