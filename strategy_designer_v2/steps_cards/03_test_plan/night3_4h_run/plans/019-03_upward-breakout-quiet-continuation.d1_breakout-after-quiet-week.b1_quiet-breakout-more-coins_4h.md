---
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 0974d5467d9f
---
Fidelity:
- Situation: a 4h close above the highest high of the preceding two-day stretch -> adapted: the on/off break becomes graded by the size of the break above the prior 12-bar high.
- Comparison: stretch range narrow against the 30-day average 4h range, and 7-day average range quiet against the 60-day average -> kept: the component multiplies by B/S (180-bar mean bar range over the 12-bar stretch range) and by L/Q (360-bar over 42-bar mean bar range).
- Outcome: the coin rises over the next three days -> kept: each bet is held 18 bars, long only.
- Verdict transfer: yes: the forecast is the idea's breakout, weighted by its two stated quietness ratios, held for its three-day horizon.
Forecast: The forecast uses NarrowRangeBreakoutRangeRatioComponent with period 12 (two days), base_period 180 (30 days), ratio_long_period 360 (60 days) and ratio_short_period 42 (7 days). Its raw value is the percent break of the close above the prior 12-bar high, times the 30-day mean bar range over the stretch's range, times the 60-day over the 7-day mean bar range. It is 0 when there is no break. It grows with the size of the break, with how narrow the stretch was, and with how quiet the past week was. It is standardised against its own past 360 values (min_periods 90), so a typical non-zero reading is on the forecast scale. The forecast is never negative: it is positive on upward breakouts and 0 otherwise, and it is ungated.
Config: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Take each case (a bet: a forecast rise of at least 2 points, once per 18-bar grid cell). Measure the coin's 18-bar return from the signal's close minus the coin's normal 18-bar drift over all windows. Take the mean of that unusual move weighted by the forecast at the case, with its t over all coins and windows.
- Supporting check: The mean unusual move of the top third of cases by forecast minus that of the bottom third must be above 0.
- Confirm: The forecast-weighted mean unusual move is positive with t >= 2, and the top-minus-bottom-third difference is above 0.
- Reject: The forecast-weighted mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 with the top-minus-bottom difference at or below 0. At least 100 cases are required in total, else inconclusive.
