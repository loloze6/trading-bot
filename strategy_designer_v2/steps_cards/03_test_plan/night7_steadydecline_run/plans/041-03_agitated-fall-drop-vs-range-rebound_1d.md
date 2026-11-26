---
idea: 041-03_agitated-fall-drop-vs-range-rebound
brief: 041_falling-agitated-daily-moves-reverse
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8ae04f0765bb
---
Fidelity:
- Situation: a one-day fall, in a falling, agitated market -> kept: the close-to-close fall is measured on each bar, and the profile is added by code.
- Comparison: the fall against the coin's 30-day average daily range -> kept: the fall is divided by the mean (high − low) of the prior 30 days.
- Outcome: a larger rise over the next day, growing with the fall -> kept: a long position graded by the scaled fall, held 1 bar.
- Verdict transfer: yes: the forecast is exactly the scaled one-day fall inside the profile, so its next-day result decides the idea.
Forecast: One component, BreakoutInMeanRangesComponent (period 1, base_period 30, side "below", high_current 0, base_exclude_current 1, source "close"). It computes max(0, close[t-1] − close[t]) / the mean daily range of the prior 30 days, which is the day's fall in average daily ranges. It is standardised over its past 60 values (min_periods 20). The forecast is 0 on up days and flat days. It is positive on down days and grows linearly with the scaled fall, up to the cap of 20. It is never negative (long only). The book holds nothing outside the falling-agitated profile, which code adds.
Config: 041-03_agitated-fall-drop-vs-range-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars with forecast > 0 inside the profile; with a 1-bar horizon every bar is its own non-overlapping case. On those bars, take the forecast-weighted mean of the next-day return minus the coin's mean daily return over all windows. Its t has cases of the same day summed together.
- Supporting check: The slope of next-day excess return on forecast across those cases is positive, meaning larger scaled falls are followed by larger excess rises.
- Confirm: The forecast-weighted mean excess next-day return is above 0 with t ≥ 2, and the supporting slope is positive.
- Reject: The forecast-weighted mean excess next-day return is below 0 with t ≤ −2.
- Inconclusive: Anything with t between −2 and 2, or a confirming mean with a non-positive slope. At least 100 cases on at least 60 distinct days are needed; with fewer, the result is inconclusive.
