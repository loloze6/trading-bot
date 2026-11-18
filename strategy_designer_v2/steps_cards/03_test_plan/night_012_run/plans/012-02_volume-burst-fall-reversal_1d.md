---
idea: 012-02_volume-burst-fall-reversal
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: a bar that falls sharply -> adapted: the threshold "sharply" is made graded as the bar's fall in usual moves, damped near zero by a graded dead zone.
- Comparison: the bar's volume against the coin's 30-day average volume -> kept: the volume divided by the mean of the last 30 daily volumes, which grows with the burst.
- Outcome: a larger price rise over the next 3 days -> kept: a long position, judged on the 3-bar forward return.
- Verdict transfer: yes: the forecast grows with exactly the fall times relative-volume reading the idea names, and it is judged on the 3-day rise that follows.
Forecast: The forecast uses VolumeWeightedScaledReturnComponent with vol_period 20 and volume_period 30. Its raw value is the bar's return in usual moves (the 20-day standard deviation of daily returns) times the bar's volume over its 30-day mean volume. The value is standardised over its past 60 values and then negated, so a heavy-volume fall reads positive. It is clipped at 0, so up bars and flat bars give a forecast of exactly 0, and there is no short side. Finally, signed_power with exponent 3 and pivot 20, the strongest graded dead zone the guide allows, keeps ordinary falls near 0. The forecast is positive only on down bars. It grows with the depth of the fall and with the volume burst, and it is largest on deep falls on extreme volume.
Config: 012-02_volume-burst-fall-reversal_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The sample is the bars with forecast > 0 on each window's non-overlapping 3-bar grid, pooled over coins and windows. Each bar's 3-bar forward return is compared with the coin's mean 3-bar return over all windows; the difference is the excess return. The measure is the OLS slope of that excess return on the forecast, with its t.
- Supporting check: On the same bars, regress the excess return on two regressors, both recomputed from the bars. The first is the volume ratio (volume over its 30-bar mean). The second, a control, is the fall size in usual moves. The volume ratio's coefficient must be above 0.
- Confirm: The idea is confirmed when the slope t is 2 or more and the volume-ratio coefficient in the supporting check is positive.
- Reject: The idea is rejected when the slope t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive, and so is a t of 2 or more with a volume-ratio coefficient that is not positive. The test needs at least 100 independent cases with forecast > 0 on the grid; fewer is inconclusive.
