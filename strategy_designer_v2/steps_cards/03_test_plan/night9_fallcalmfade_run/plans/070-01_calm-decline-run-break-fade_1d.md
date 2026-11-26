---
idea: 070-01_calm-decline-run-break-fade
brief: 070_falling-calm-run-break-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a falling, calm market, a day closing up after an unbroken run of down days -> kept: a regime rule on the prior down-run length on an up close (at least 1); the profile is added by code.
- Comparison: longer down runs against shorter ones -> adapted: graded, so the short grows with the run's length.
- Outcome: a fall over the next day, larger after longer runs -> kept: a 1-bar short held for the next day.
- Verdict transfer: yes: the book is short only on run-break days in the profile, sized by run length, and judged on the next day's move.
Forecast: The regime detector reads PriorDownRunOnUpCloseComponent (max_bars 30). It is the length of the down run that the current up close breaks, and 0 on every other bar. Bars where it is 1 or more go to `mean_reversion`; every other bar is flat. Inside that regime the forecast is the same run length, standardised and then negated. It is negative (short) only on run-break days, and its size grows with the number of down days in the run. It is 0 on every other bar, and never positive. The history holds mostly zeros, so its past mean absolute value is small, about 0.4 to 0.5. The `standardise` target is therefore set to 2 so the forecast stays graded rather than stuck at the cap. With that target, a 1-day run gives about -4 to -5, a 3-day run about -13, and runs of 5 days or more reach the -20 cap.
Config: 070-01_calm-decline-run-break-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On each case bar (forecast below 0), the coin's next-day return minus its mean daily return over all windows, taken in the short direction. Its mean over cases, with a t-statistic from cases summed per day.
- Supporting check: The same unusual move on cases with a run of 3 or more days, minus the cases with a run of 1 to 2 days (Welch t).
- Confirm: The main mean unusual move is positive with t >= 2. The check passes when the long-run minus short-run difference is positive with t >= 2.
- Reject: The main mean unusual move is negative with t <= -2, so up days after runs are followed by rises. The idea is also rejected if the long-run minus short-run difference has t <= -2.
- Inconclusive: Any other result, including either t between -2 and 2. At least 100 case-days in total and 20 in each run group are needed; with fewer, the test is inconclusive.
