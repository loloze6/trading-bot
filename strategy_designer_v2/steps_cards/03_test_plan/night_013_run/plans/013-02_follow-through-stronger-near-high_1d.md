---
idea: 013-02_follow-through-stronger-near-high
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: the coin's past 30-day return, while it closes near its 52-week high -> kept: the 30-bar return is weighted by convex proximity to the 365-bar closing high.
- Comparison: near the high against far below it -> adapted: the near/far split is made graded, so the weight shrinks smoothly with depth below the high.
- Outcome: the past return carries on over the next 30 days, in its own direction -> kept: the forward 30-bar return is read in the forecast's sign.
- Verdict transfer: yes: the forecast is exactly the past return weighted by nearness to the high, and the check compares carry-on near the high against carry-on far below it.
Forecast: One component, `HighProximityMomentumComponent` with `period` 365, `return_period` 30, `proximity` "convex" and `power` 2.0. - It computes the 30-bar return times (1/(1+D))², where D is the percent depth below the highest close of the last 365 bars. - `standardise` uses window 365 and min_periods 91. - The forecast is positive after a 30-day rise and negative after a fall, and zero when there was no move. - Its size grows with the past move and with nearness to the 52-week high. Far below the high it shrinks towards zero. - It runs on every bar, with no regime.
Config: 013-02_follow-through-stronger-near-high_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: The slope of the coin's forward 30-bar return, minus that coin's mean 30-bar return over all windows, regressed on forecast/10. It is pooled over the non-overlapping grid (positions 0, 30, 60, 90 of each window), with its t-statistic.
- Supporting check: The comparison between near and far below the high: - At grid positions 30, 60 and 90, take the plain past 30-bar return from the recorded closes. - Take the proximity weight W = `hpm.last_history_value` / past return. - Regress the excess forward return on the past return, separately in the cases above the median W and below it. - The slope in the above-median half minus the slope in the below-median half must be greater than 0.
- Confirm: The main slope's t is at least +2, and the near-minus-far slope difference is greater than 0.
- Reject: The main slope's t is at most -2.
- Inconclusive: - Any main t between -2 and +2 is inconclusive. - A main t of at least +2 with a near-minus-far difference of 0 or less is also inconclusive. - At least 300 independent grid cases are needed across the coins and windows; with fewer, nothing is decided.
