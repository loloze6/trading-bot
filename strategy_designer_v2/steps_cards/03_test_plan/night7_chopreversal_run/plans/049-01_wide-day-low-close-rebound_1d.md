---
idea: 049-01_wide-day-low-close-rebound
brief: 049_wide-day-close-location-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e8f4c1171351
---
Fidelity:
- Situation: a close low in the day's high-low range, on a day wide against usual -> kept: (high − close) / prior 30-day mean range, which is close location × range multiple.
- Comparison: the day's range against the usual daily range over the past 30 days -> kept: the mean of high − low over the 30 prior days.
- Outcome: a larger rise over the next day -> kept: next-day return, horizon 1 bar, long only.
- Verdict transfer: yes: the forecast is the idea's own graded product, and next-day gains that grow with it test exactly the claimed relation.
Forecast: The forecast uses one component, `BreakoutInMeanRangesComponent`, with period 1, base_period 30, side "below", high_current 1 and base_exclude_current 1. Its value is (high − close) / mean(high − low over the 30 prior days). This equals the close's depth from the day's high as a share of the range, times the day's range in usual ranges. It is standardised over its own past 60 values (min_periods 20). The forecast is never negative: it is 0 when the close is at the high. It grows as the close sits nearer the low and as the day gets wider than usual, so a low close on a wide day gives the largest long, up to the cap at 20. It is ungated, because the idea is a graded relation, not a condition.
Config: 049-01_wide-day-low-close-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the coin's next-day return, minus its mean daily return over all windows, on the bar's forecast. It uses every bar (the 1-bar grid), pooled over coins and windows, with the t of the slope taken with cases of one day summed together.
- Supporting check: The mean next-day return in excess of the coin's mean, on bars in the top fifth of the forecast, is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is −2 or less.
- Inconclusive: The slope's t is between −2 and 2, or it is 2 or more while the check fails. A verdict needs at least 1,000 bars with a forecast on at least 500 distinct days, and at least 200 bars in the top fifth.
