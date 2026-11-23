---
idea: 030-02_absorption-close-low-falls
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day with volume far above its 20-day average and a close little changed from its open -> kept: a regime rule on volume over the prior 20-day mean (at least 2, by convention) and on the open-to-close change (at most 1 percent, by convention).
- Comparison: the closer the close sits to the day's low, and the heavier the volume, the larger the effect -> kept: (high - close) / range times volume over its prior 20-day mean, graded.
- Outcome: the coin falls over the next 5 days -> kept: a graded short, held 5 daily bars.
- Verdict transfer: yes: the test measures the stated situation, its grading and the 5-day fall.
Forecast: The forecast is zero on every day except heavy, flat days: volume at least 2 times its prior 20-day mean, and the close within 1 percent of the open. On those days it is short. Its size is the close's distance from the day's high as a share of the day's range, times the volume over its prior 20-day mean (`VolumeWeightedCloseLocationComponent`, reference "high", volume_period 20, exclude_current 1), standardised over 60 bars and negated. A close at the high gives 0. The short grows as the close nears the low and as the volume gets heavier.
Config: 030-02_absorption-close-low-falls_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the forecast's short bets, one per 5-bar grid cell of each window. For each case, take the coin's 5-day return from the signal bar's close, minus the coin's mean 5-day return over all its windows (holding the coin), with the sign flipped so that a fall counts positive. The measure is the mean of this value over the cases, with its t.
- Supporting check: Over the cases, the slope of that excess fall on the size of the forecast (abs(forecast)) is above 0.
- Confirm: The mean excess fall has t ≥ 2 and the supporting check passes, with at least 30 cases.
- Reject: The mean excess fall has t ≤ -2 (the coin rises more than its drift after these days), with at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is a positive mean whose slope is not above 0. Fewer than 30 cases in total is also inconclusive.
