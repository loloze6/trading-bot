---
idea: 035-01_wide-low-close-rebounds
brief: 035_wide-day-low-close-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a day's high-to-low range is wide, and its close sits near the day's low -> kept: (high − close) / (mean prior range) equals the range multiple times the close's nearness to the low, which is the idea's product, graded.
- Comparison: the coin's average daily range over the past 14 days -> kept: the mean of high − low over the 14 days before the day.
- Outcome: the coin rises over the next day, more so the larger the product -> kept: the next-day return, against the coin's normal drift.
- Verdict transfer: yes: the forecast is exactly the idea's graded product, held for one day, so a confirm or reject on its next-day returns transfers to the idea.
Forecast: The forecast uses one indicator, `BreakoutInMeanRangesComponent` with period 1, base_period 14, side "below", high_current 1 and base_exclude_current 1. It reads (high − close) of today divided by the mean daily range of the prior 14 days. That equals today's range in multiples of its 14-day average times how near the close sits to the low. It is 0 when the close is at the day's high. It grows as the day widens and as the close nears its low. It is standardised against its own last 60 values, so a usual reading is about +10, capped at 20. It is never negative, which keeps the book long only. It is ungated: the idea is a steady graded relation, not a named situation.
Config: 035-01_wide-low-close-rebounds_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the coin's next-day return, minus its mean daily return over all windows, on the bar's forecast (post_pipeline_value). It is pooled over every coin and every bar, one bar per case (non-overlapping at h = 1). Its t is computed with the cases of one day taken together.
- Supporting check: The mean next-day excess return of the bars in the top fifth of forecast values (per coin) must be above 0.
- Confirm: The slope's t is 2 or more, and the top-fifth mean next-day excess return is positive.
- Reject: The slope's t is −2 or less: wider, lower-closing days are followed by smaller or more negative next-day returns.
- Inconclusive: The slope's t lies between −2 and 2, or the t is 2 or more while the top-fifth mean is at or below 0. At least 500 distinct days with a recorded forecast are required, else the result is inconclusive.
