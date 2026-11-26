---
idea: 062-01_choppy-calm-fall-continues
brief: 062_choppy-calm-falls-keep-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a more negative 5-day return, measured against the 30-day daily swing, in a choppy calm market -> adapted: the 5-day return in units of the 30-day daily standard deviation, short side only, graded by size; the profile is added by code.
- Comparison: the fall judged against the coin's own 30-day daily swing -> kept
- Outcome: the price falls further over the next 5 days, more after larger scaled falls -> kept
- Verdict transfer: yes: the forecast is the idea's own scaled fall, inside its profile, held for its 5-day horizon.
Forecast: The forecast uses one component, `VolatilityScaledReturnComponent` with `period` 5 and `vol_period` 30. It is the 5-day return divided by the standard deviation of the last 30 daily returns, times sqrt(5); that constant cancels under `standardise`. It is standardised over 60 bars with min_periods 20, then clipped at a maximum of 0. The forecast is negative (short) after a 5-day fall, and its size grows linearly with the fall in swing units. It is 0 after a 5-day rise or a flat stretch. It runs on every bar, and the code keeps the book flat outside the choppy calm profile.
Config: 062-01_choppy-calm-fall-continues_1d_config.json
Profile: choppy calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the bars of each window's 5-bar grid (positions 0, 5, 10, ...) where the forecast is below 0. On each, take the coin's 5-day return from the close minus its normal 5-day drift (the mean over all windows), signed in the short direction. Its mean, with t computed with each day's cases summed together.
- Supporting check: Split those cases at the median of |forecast|. The mean short-direction excess return of the larger half minus that of the smaller half must be above 0.
- Confirm: The mean short-direction excess return has t ≥ 2, and the larger-half minus smaller-half difference is above 0.
- Reject: The mean short-direction excess return has t ≤ -2: scaled falls are followed by rebounds relative to the coin's drift.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with a size difference at or below 0. Fewer than 30 distinct days holding cases is also inconclusive.
