---
idea: 062-02_choppy-calm-below-high-falls
brief: 062_choppy-calm-falls-keep-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: the close sits below its highest close of the past 5 days, measured in 30-day daily swings -> kept
- Comparison: the drop is scaled by the coin's own 30-day daily swing; a deeper drop is compared with a shallower one -> kept
- Outcome: the coin falls further over the next 5 days, and falls more the deeper the drop -> kept
- Verdict transfer: yes: the forecast is exactly the swing-scaled drop below the 5-day high, short and graded, held 5 days inside the brief's profile.
Forecast: The forecast uses one indicator, VolatilityScaledDistanceFromHighComponent with period 5, vol_period 30, source close, bar t included and base level. Its value is (close − highest close of the last 5 days) / that high / std of the last 30 daily returns. It is 0 at the 5-day high and more negative the deeper the close sits below it in usual daily moves. The value is standardised over its past 60 values, which keeps its sign. The forecast is therefore never positive: it is 0 at the high and a short that grows with the swing-scaled drop, about −10 at a usual drop and capped at −20. There is no regime of its own; step 3's code adds the choppy calm profile and keeps the book flat outside it.
Config: 062-02_choppy-calm-below-high-falls_1d_config.json
Profile: choppy calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Take the non-overlapping 5-bar grid bars of each window where the forecast is not 0. On those bars, measure the slope of the coin's 5-bar forward return, minus its mean 5-bar return over all windows, against the bar's forecast. Bars on the same day are pooled into one case, and the t is computed on those day cases.
- Supporting check: On grid bars with forecast ≤ −10 (a drop of a usual size or deeper), the mean excess 5-bar return is below 0.
- Confirm: The slope is positive with t ≥ 2 (a deeper drop is followed by a larger fall beyond drift), and the supporting check passes.
- Reject: The slope is negative with t ≤ −2: deeper drops are followed by rebounds beyond drift.
- Inconclusive: Any slope with |t| < 2, or a confirming slope whose check fails. At least 50 distinct days of grid cases with a non-zero forecast are needed, else the result is inconclusive.
