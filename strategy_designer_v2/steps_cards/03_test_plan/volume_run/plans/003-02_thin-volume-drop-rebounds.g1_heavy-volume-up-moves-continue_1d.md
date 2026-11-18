---
idea: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a sharp one-day rise against the coin's 20-day volatility, on heavy volume against its 30-day average -> adapted: the "sharp" threshold becomes a graded one-bar scaled return times the volume ratio, with a cubic dead zone and the long side only.
- Comparison: a larger scaled rise and heavier volume give a larger further gain -> kept: the forecast grows with both factors through their product.
- Outcome: the price keeps rising over the next 5 days -> adapted: the 5-day hold is dropped, so the position follows each bar's reading and the 5-bar forward return is measured from the record.
- Verdict transfer: yes: the forecast is the idea's own product of the scaled rise and the volume ratio, judged on the 5-day return that follows it.
Forecast: The forecast uses one component, VolumeWeightedScaledReturnComponent (vol_period 20, volume_period 30). Its raw value is today's return divided by the 20-day standard deviation of returns, times today's volume over its 30-day mean. Standardise (window 60, min_periods 20) puts it on the scale of its own past size. A clip at 0 keeps only up days, because the idea is about rises. A signed_power with exponent 3 and pivot 20 is the strongest dead zone the guide allows, so ordinary days stay near 0. The forecast is zero on down days and small on ordinary up days. It grows steeply, up to +20, when a large volatility-scaled rise comes on heavy volume.
Config: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the bars at positions 0, 5, 10, … of each window where the forecast is at least 2. For each case, take the 5-bar forward return close[t+5]/close[t]-1 inside the window. Subtract the coin's mean 5-bar return over all windows on the same grid. Report the mean of this excess and its t.
- Supporting check: Among the cases, the cases with forecast above their median minus those below it should give a positive difference in mean excess return.
- Confirm: The idea is confirmed only if both of these hold: - the mean excess 5-bar return has t ≥ 2; - the supporting difference is above 0.
- Reject: The idea is rejected if the mean excess 5-bar return has t ≤ -2, meaning large heavy-volume rises are given back.
- Inconclusive: The result is inconclusive in either of these cases: - t lies between -2 and 2, whatever the supporting check shows; - t ≥ 2 but the supporting difference is not above 0. The test needs at least 30 cases across all coins and windows; with fewer it is inconclusive.
