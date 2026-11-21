---
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 28-day return, larger or smaller -> kept: PriceEvolutionComponent with period 28 on daily closes.
- Comparison: larger 28-day returns against smaller ones -> kept: the forecast grows with the size of the return.
- Outcome: a larger return over the next 5 days, in the same direction -> kept: each bet is held 5 bars and judged on the 5-bar forward return.
- Verdict transfer: yes: the forecast is the 28-day return itself, scaled, and the test measures whether it predicts the next 5 days' return.
Forecast: The forecast is the coin's 28-day percent return (PriceEvolutionComponent, period 28), standardised against the mean absolute value of its previous 60 readings (window 60, min_periods 20). Standardise scales the value but does not centre it, so the sign is the sign of the 28-day return. The forecast is positive after a 4-week rise and negative after a 4-week fall. It is 0 only when the 28-day return is 0. Its size grows in proportion to the size of the return, at about 10 for a typical move and capped at ±20. There is no regime, and the forecast is active on every bar.
Config: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the bars at positions 0, 5, 10, ... of each window, for every coin. On those cases, regress the coin's 5-bar forward return close[t+5]/close[t]-1, minus that coin's mean 5-bar return over all its windows, on the bar's forecast. The slope is pooled across coins and windows, and its t-statistic is the main measure.
- Supporting check: The book's timing gain must be above 0. This is the book's mean daily return before costs, minus its gain from the market's own rise.
- Confirm: The slope is positive with t ≥ 2, and the timing gain is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive. A positive slope with t ≥ 2 whose timing gain is 0 or below is also inconclusive. At least 500 non-overlapping cases are required.
