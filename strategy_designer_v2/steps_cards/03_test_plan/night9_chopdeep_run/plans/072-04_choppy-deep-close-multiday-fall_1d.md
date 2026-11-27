---
idea: 072-04_choppy-deep-close-multiday-fall
brief: 072_choppy-deep-below-high-falls
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a choppy market, close below its 20-day high, in 20-day daily-return std units -> kept: the profile is added by code; the depth is graded by `VolatilityScaledDistanceFromHighComponent` (20, 20).
- Comparison: deeper closes against shallower ones ("the further ... the larger") -> kept: the short position grows with the depth.
- Outcome: the price falls over the next three days, more after deeper closes -> kept: each bet is held 3 bars, on the short side only.
- Verdict transfer: yes: a 3-day fall that grows with the depth would confirm the idea, and a 3-day rise that grows with the depth would reject it.
Forecast: The forecast uses one component, the distance of the close below its 20-day high, (close − highest high of the last 20 bars, today included) / that high / the std of the last 20 daily returns. It is 0 at the high and more negative the deeper the close sits below it, in usual daily moves. It is standardised over its own past 60 values (min 20), so it averages about −10 and is capped at −20. A clip at max 0 keeps it short only. The forecast is never positive. It is 0 when the close is at the 20-day high, and the short grows linearly with the depth. The code keeps the book flat outside the choppy profile.
Config: 072-04_choppy-deep-close-multiday-fall_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The slope of the coin's 3-bar forward return minus its normal 3-bar drift (its mean over all windows) on the bar's forecast. It uses the non-overlapping 3-bar grid of each window and bars with a nonzero forecast, pooled over coins, with t clustered by day.
- Supporting check: The deepest third of the forecasts (most negative) has a mean excess 3-bar return below 0.
- Confirm: The slope is positive with t ≥ 2: deeper shorts are followed by larger excess falls. The supporting check must also pass.
- Reject: The slope is negative with t ≤ −2: deeper closes are followed by larger excess rises.
- Inconclusive: Any slope with |t| < 2 is inconclusive. So is a positive slope with t ≥ 2 where the deepest third's mean excess return is not below 0. A result needs at least 100 non-overlapping cases on at least 60 distinct days, else it is inconclusive.
