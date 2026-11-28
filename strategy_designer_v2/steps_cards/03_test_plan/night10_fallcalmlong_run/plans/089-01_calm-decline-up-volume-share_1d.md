---
idea: 089-01_calm-decline-up-volume-share
brief: 089_falling-calm-up-volume-lean
data-instruments: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: b5764dedf919
---
Fidelity:
- Situation: a coin's last 20 days' volume leans to up days, in a falling calm market -> adapted: the up-day share of 20-day volume, graded above one half (long only); the falling calm profile is added by code.
- Comparison: a larger share against a smaller share -> kept: the position grows with the share above one half.
- Outcome: the coin rises more over the next 5 days -> kept: the 5-day forward return, judged against the coin's normal drift.
- Verdict transfer: yes: the forecast is the idea's share, inside the idea's profile, judged on the idea's 5-day horizon.
Forecast: One component, the share of the last 20 daily bars' volume traded on up-close days minus 0.5 (`UpDayVolumeShareComponent`, period 20, form "centred"). It is standardised against its own past 60 values and then clipped at 0, so the brief's long-only rule holds. The forecast is positive and grows linearly as more than half the recent volume falls on up days. It is zero when half or less does. Code keeps it flat outside the falling calm profile.
Config: 089-01_calm-decline-up-volume-share_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the 5-bar forward return on the forecast. The return is close[t+5]/close[t]-1 minus the coin's mean 5-bar return over all its windows. The sample is the bars of a non-overlapping 5-bar grid in each window, taken only where the bar is inside the profile, with the forecast at 0 included. The measure is the OLS t of that slope.
- Supporting check: Over the cases (forecast rises of at least 2 points, one per grid cell), the mean unusual 5-bar move must be above 0, with cases from the same day taken together.
- Confirm: The slope t is 2 or more, and the supporting check's mean unusual move is above 0.
- Reject: The slope t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a slope t of 2 or more when the cases' mean unusual move is 0 or below. The test needs at least 150 in-profile grid bars, of which at least 60 have a forecast above 0; with fewer, the result is inconclusive.
