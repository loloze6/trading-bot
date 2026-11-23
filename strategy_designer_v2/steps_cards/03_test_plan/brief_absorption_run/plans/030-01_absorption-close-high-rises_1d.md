---
idea: 030-01_absorption-close-high-rises
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day with volume far above its 20-day average and a close little changed from its open -> kept: a regime rule, volume ≥ 2x the prior 20-day mean and body ≤ 30% of the day's range.
- Comparison: the effect is larger the heavier that day's volume -> kept: the forecast is the close location times the day's volume ratio.
- Outcome: the closer the close is to the high, the more the coin rises over the next 5 days -> kept: a signed close location, held 5 daily bars.
- Verdict transfer: yes: the config bets on exactly these days, in proportion to close location times volume, over 5 days.
Forecast: On ordinary days the forecast is 0 (flat). On an absorption day it is non-zero. An absorption day has volume at least 2x the mean of the 20 prior days, and an open-to-close body of at most 30% of the day's high-low range. On those days the forecast is the signed close location times the volume ratio. The close location runs from -1 at the low to +1 at the high, and the volume ratio is the day's volume over its prior 20-day mean. The product is standardised against its own last 60 values (the window of 60 values, a minimum of 20 past values). It is positive (long) when the close is in the upper half of the range and negative (short) when it is in the lower half. Its size grows as the close nears an end of the range and as volume gets heavier, up to the cap of ±20.
Config: 030-01_absorption-close-high-rises_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope (with its t) of a regression across cases of the unusual move on the forecast at the signal bar. A case is a bet (a forecast rise of at least 2 points on its side), read once per 5-bar grid cell. The unusual move is the coin's 5-bar return from the signal bar's close minus the coin's mean 5-bar return over all its windows.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2, on at least 30 cases.
- Reject: The slope is negative with t ≤ -2, on at least 30 cases.
- Inconclusive: Any t between -2 and 2, or fewer than 30 cases, is neither a confirm nor a reject.
