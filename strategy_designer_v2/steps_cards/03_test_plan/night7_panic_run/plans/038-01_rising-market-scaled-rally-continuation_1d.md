---
idea: 038-01_rising-market-scaled-rally-continuation
brief: 038_scaled-rallies-continue-in-rising-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's 3-day return, in units of its 30-day daily-return std, in a rising market -> kept: the profile keeps "rising", and VolatilityScaledReturnComponent with period 3 and vol_period 30 measures the scaled rise; its constant sqrt(3) is cancelled by standardise.
- Comparison: larger scaled rises against smaller ones, with flat or down days getting no lift -> kept: the forecast grows with the scaled rise and is 0 when the 3-day return is not positive.
- Outcome: the coin keeps rising over the next 3 days -> kept: long positions, each bet held 3 bars.
- Verdict transfer: yes: inside rising markets, the test checks whether the next 3-day move above the coin's normal drift grows with the scaled 3-day rise, exactly as the idea claims.
Forecast: The forecast uses one component, the 3-day return divided by the coin's 30-day daily-return std (times sqrt(3)). Standardise sets its scale against its own last 60 values (min 20), and a clip at 0 keeps only rises. The forecast is 0 when the last 3 days were flat or down. It is positive after a 3-day rise and grows linearly with the scaled rise, about +10 for a usual-sized rise, capped at +20. It is never short. The profile code keeps it flat outside rising markets.
Config: 038-01_rising-market-scaled-rally-continuation_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The slope, and its t, of a least-squares fit of each bar's excess 3-bar forward return on its forecast. The excess return is close[t+3] / close[t] - 1 minus the coin's mean 3-bar return over all windows. The bars are those of the non-overlapping 3-bar grid of each window that lie inside the rising profile (regime not flat), forecast-0 bars included.
- Supporting check: The mean unusual move (strength) of the cases with forecast > 0 is positive, by the workflow's case definition.
- Confirm: The slope is positive with t >= 2, and the supporting check's mean unusual move is above 0.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope with |t| < 2, and a positive slope with t >= 2 whose mean unusual move is not above 0. The test needs at least 100 grid cases with forecast > 0, pooled over coins and windows; fewer is inconclusive.
