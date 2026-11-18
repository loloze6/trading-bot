---
idea: 003-02_thin-volume-drop-rebounds
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: a coin falls sharply over one day on volume well below its average -> adapted: a regime selects down days on below-average volume, and "sharply" and "well below" become graded sizes.
- Comparison: the day's volume against its own 30-day average daily volume -> kept: volume[t] over the mean of the prior 30 days' volumes.
- Outcome: the price wins back part of the fall over the next 5 days, more for a larger fall on thinner volume -> kept: long, 5 bars, size grows with fall and thinness.
- Verdict transfer: yes: the forecast is long only on thin-volume down days, sized by the fall and the thinness, and it is judged on the 5-day rebound.
Forecast: Each day the config checks whether the close fell and the day's volume was below its prior 30-day mean. On all other days the forecast is 0 (flat). On those days it averages two parts with equal weight: - the fall: the one-day percent return, standardised (60/20), negated and clipped at 0; - the thinness: minus the log of volume over its prior 30-day mean, standardised (60/20), negated and clipped at 0. Each part goes through signed_power (exponent 3, pivot 20), the strongest graded dead zone, so small falls or slightly thin volume give almost nothing. Both parts are near 0 at the edge of the regime, so the position does not jump from none to some. The forecast is never negative and grows with both the size of the fall and the thinness of the volume.
Config: 003-02_thin-volume-drop-rebounds_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The excess 5-bar return is close[t+5]/close[t]-1 minus the coin's mean 5-bar return over all its windows. The measure is the mean of forecast/10 × excess 5-bar return. It uses the non-overlapping 5-bar grid of each window, on grid bars with forecast > 0, pooled over coins, with the t of that mean.
- Supporting check: On those same cases, the mean excess 5-bar return of cases above the median positive forecast, minus that of cases below it, is > 0.
- Confirm: The main measure's t is ≥ 2 and the supporting check's difference is > 0.
- Reject: The main measure's t is ≤ -2.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with the check's difference ≤ 0; at least 30 grid cases with forecast > 0 are needed, otherwise inconclusive.
