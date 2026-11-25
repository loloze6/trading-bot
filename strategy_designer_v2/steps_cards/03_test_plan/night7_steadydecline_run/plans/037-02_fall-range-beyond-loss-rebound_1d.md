---
idea: 037-02_fall-range-beyond-loss-rebound
brief: 037_wide-range-separates-forced-falls
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8ae04f0765bb
---
Fidelity:
- Situation: a one-day fall whose high-to-low range stretches beyond the closing loss, the two taken together -> kept: `FallTimesRangeExcessComponent` gives the fall times the range in excess of the loss, and is 0 on up days.
- Comparison: the day's range against the size of the closing loss itself -> kept: the excess term E is the range minus the closing loss.
- Outcome: a larger rise over the next day, growing with the product -> kept: the horizon is 1 bar on 1d bars, with long positions sized by the product.
- Verdict transfer: yes: the forecast is the idea's own product, held for one day, so a graded next-day rise confirms the idea and a graded next-day fall rejects it.
Forecast: The forecast is `FallTimesRangeExcessComponent`, which is the day's closing fall in percent times the day's range beyond that fall in percent. It is standardised against its own last 60 daily values, with at least 20 past values. The forecast is 0 on up days, flat days, and days whose range does not exceed the loss. On a falling day it is positive, and it grows with both the depth of the fall and the extra intraday travel, capped at 20. It is never negative, so the book is long only.
Config: 037-02_fall-range-beyond-loss-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars with forecast > 0, on every coin and window. Take each bar's next-bar return minus the coin's mean daily return over all windows, and regress it on the forecast. Report the t of the slope, with the cases of one day pooled (day-clustered standard errors).
- Supporting check: The mean unusual move over all cases (next-day return minus normal drift) is above 0.
- Confirm: The slope t is 2 or more, and the mean unusual move of the cases is above 0.
- Reject: The slope t is -2 or less, or the mean unusual move of the cases has a t of -2 or less (larger wide-range falls followed by further decline).
- Inconclusive: Any slope t between -2 and 2, or a positive slope t of 2 or more with a mean unusual move at or below 0 (t above -2), is inconclusive. A verdict needs at least 150 case bars on at least 100 distinct days; fewer cases is inconclusive.
