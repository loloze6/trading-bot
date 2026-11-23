---
idea: 030-04_heavy-flat-low-close-reverses
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: volume far above its 20-day average, close little changed from open, close near the day's low -> kept: two regime rules (volume ≥ 2× prior 20-day mean, body ≤ 1/3 of range) and a graded close location in the range.
- Comparison: the effect is larger the heavier that day's volume -> kept: the close location is multiplied by the day's volume over its prior 20-day mean.
- Outcome: the coin rises over the next 5 days, more the nearer the close is to the low -> kept: the position is held 5 daily bars and judged against the coin's normal 5-day drift.
- Verdict transfer: yes: the test bets on exactly these days, graded by close location and volume, over the idea's 5 days.
Forecast: The forecast is active only on a day whose volume is at least 2 times the mean of the prior 20 days (VolumeRatioComponent, period 20, prior days only) and whose body |close − open| is at most one third of its high-low range (BarBodySizeComponent, relative to the range). On every other day it is 0. On an active day it is the signed close location in the bar, 2×(close−low)/(high−low) − 1, multiplied by the day's volume over its prior 20-day mean (VolumeWeightedCloseLocationComponent, "signed", exclude_current 1). It is then negated and standardised over the prior 60 days (min 20). - It is positive (long) when the close is in the lower half of the range and negative when it is in the upper half. - It is 0 at mid-range. - Its size grows as the close nears the low (or high) and as volume gets heavier. - It is capped at ±20.
Config: 030-04_heavy-flat-low-close-reverses_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Each case is a bet: a rise of at least 2 points in the forecast on its own side, read once per 5-bar grid cell. Per case, compute (forecast / 10) × (the coin's 5-bar return from the case's close − the coin's mean 5-bar return over all its windows). Report the t of that mean over the cases.
- Supporting check: none
- Confirm: The forecast-weighted excess 5-bar return is positive with t ≥ 2, over at least 30 cases.
- Reject: The forecast-weighted excess 5-bar return is negative with t ≤ −2, over at least 30 cases.
- Inconclusive: Any t between −2 and 2 is inconclusive. So is any result with fewer than 30 cases, whatever its t.
