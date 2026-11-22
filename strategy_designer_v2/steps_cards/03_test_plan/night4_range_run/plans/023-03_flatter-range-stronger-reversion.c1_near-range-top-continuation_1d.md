---
idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the daily close's position within its 30-day closing range, nearer the top -> kept
- Comparison: none
- Outcome: the coin rises over the next 10 days, more the closer it is to the top -> kept
- Verdict transfer: yes: the forecast grows with the close's position in its 30-day closing range, and is judged on the 10-day return.
Forecast: The forecast is the 30-bar Donchian range position, computed on closes (the default source, so no `source` key is set). It is +20 raw at the highest close of the last 30 bars, -20 at the lowest, and 0 at the middle. It is standardised over 60 bars (min_periods 20), so its average absolute value is about 10. It is positive and grows as the close nears the top of the range. It is negative and grows in size as the close nears the bottom. It is 0 at the middle. It runs ungated on every bar.
Config: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On a non-overlapping 10-bar grid per window, the slope (and its t) of the coin's 10-bar forward return, minus the coin's mean 10-bar return over all its windows, on the bar's forecast. Coins and windows are pooled, before costs.
- Supporting check: the book's timing gain is above 0. This is its mean daily return before costs minus its gain from the market's own rise.
- Confirm: The slope is positive with t >= 2 over at least 200 grid cases, and the timing gain is above 0.
- Reject: The slope is negative with t <= -2 over at least 200 grid cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 when the timing gain is at or below 0. So is any result with fewer than 200 grid cases.
