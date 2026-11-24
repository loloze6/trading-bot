---
idea: 025-01_falling-market-day-jump-fades
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 051b3422f169
---
Fidelity:
- Situation: a coin's one-day rise in a falling market -> kept: the falling market is the brief's profile, which code adds; the rise is the day's return, and the forecast is zero on days that did not rise
- Comparison: the rise measured in usual daily moves, the standard deviation of daily returns over the past 30 days -> kept
- Outcome: the larger the rise, the more the coin falls over the next 5 days -> kept: a short position that grows with the scaled rise and is held 5 bars
- Verdict transfer: yes: the test bets short in proportion to the scaled one-day rise, only in falling markets, over the idea's 5 days, so its result is the idea's result.
Forecast: The forecast uses one component: the day's return divided by the standard deviation of the last 30 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 30). It is standardised against its own past 60 values, clipped at 0 to keep only up days, then negated. On a down or flat day the forecast is 0. On an up day it is negative (short), and its size grows linearly with the rise counted in usual daily moves, up to -20. The code adds the falling-market profile, so the book is flat outside it.
Config: 025-01_falling-market-day-jump-fades_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case. A case is a short bet on the forecast, read once per 5-bar grid cell. Its unusual move is the coin's 5-bar return from the signal bar's close, minus the coin's mean 5-bar return over all windows, in the short direction. The measure is the mean over cases and its t, with the cases of one day taken together.
- Supporting check: Split the cases at the median absolute forecast. The mean unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The mean unusual move is above 0 with t >= 2, and the larger half's mean exceeds the smaller half's.
- Reject: The mean unusual move is below 0 with t <= -2: the coin rises more than its drift after up days in falling markets.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 whose larger half does not beat the smaller half is also inconclusive. So is any result with fewer than 30 cases or fewer than 30 distinct days.
