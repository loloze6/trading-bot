---
idea: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 9111077ea370
---
Fidelity:
- Situation: the coin has just fallen in an unbroken streak of 4h bars, with volume declining across the streak -> kept: the streak and its volume slope are a regime condition, the idea's own condition.
- Comparison: the streak's loss against the typical 4h move over 30 days, and 5-day volatility against 30-day volatility -> kept: loss in mean absolute 4h moves over 180 bars, plus 30-bar volatility over its 180-bar average, both graded.
- Outcome: the price rises over the next three days, more for larger loss and higher volatility ratio -> kept: long, held 18 bars, sized by both measures.
- Verdict transfer: yes: the test measures the streak, the volume fade, both size drivers and the 3-day rise as the idea states them.
Forecast: The forecast is active only while the current bar closes a down-streak of at least 2 bars whose volume slope is falling (`DownStreakVolumeFadeComponent` > 0). Otherwise it is flat. While it is active, it is the equal-weight mean of two standardised parts: - the streak's loss in usual one-bar moves over 180 bars (`DownStreakLossInUsualMovesComponent`); - the 30-bar volatility over its 180-bar average (`VolatilityRatioToAverageComponent`). Both parts are never negative, so the forecast is long or zero. It grows as the streak loss grows and as recent volatility rises above its 30-day level. It returns to 0 when the streak breaks or volume stops fading.
Config: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are bets (forecast rises of at least 2 on the long side), read once per cell of a non-overlapping 18-bar grid in each window. For each case, take the coin's 18-bar return from the signal bar minus the coin's normal 18-bar drift over all windows. Measure the mean of these excess returns and its t.
- Supporting check: Split the cases at the median of their forecast. The mean excess return of the upper half minus that of the lower half must be above 0.
- Confirm: The mean excess return is positive with t >= 2, and the supporting check passes.
- Reject: The mean excess return is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 when the supporting check fails, and so is any result from fewer than 30 cases.
