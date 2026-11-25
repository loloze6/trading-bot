---
idea: 041-02_agitated-fall-rise-vs-range-giveback
brief: 041_falling-agitated-daily-moves-reverse
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8ae04f0765bb
---
Fidelity:
- Situation: a one-day rise against the coin's 30-day average daily range, in a falling, agitated market -> kept: the close-to-close rise in prior 30-day mean daily ranges, 0 on down days; the profile is added by code.
- Comparison: the rise's size against the 30-day average daily range -> kept: the divisor is the mean high-low range of the prior 30 days.
- Outcome: a larger fall over the next day, growing with the rise -> kept: a short whose size grows with the scaled rise, held 1 bar.
- Verdict transfer: yes: the forecast is the idea's scaled rise turned into a graded short over the idea's one-day horizon, inside the idea's profile.
Forecast: The forecast is built from BreakoutInMeanRangesComponent with period 1, source "close", side "above", high_current 0, base_period 30 and base_exclude_current 1. It reads max(0, close[t] − close[t−1]) divided by the mean daily high-low range of the prior 30 days, so it is today's rise in usual daily ranges. It is standardised over 60 bars (min_periods 20) and negated. The forecast is 0 on days that did not rise. It is negative (short) on up-days, and the short grows linearly with the size of the rise against the 30-day range, capped at −20. It is never positive. The book is flat outside the falling agitated profile, which code adds.
Config: 041-02_agitated-fall-rise-vs-range-giveback_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars with a forecast below 0 (up-days in the profile). Regress each bar's next-day return, minus the coin's mean daily return over all windows, on that bar's forecast (post_pipeline_value). Take the slope and its t, with the cases of one day pooled.
- Supporting check: On those bars, the mean next-day unusual move in the short direction (minus the coin's normal drift) is above 0.
- Confirm: The slope is positive with t ≥ 2: a more negative forecast (a larger rise) is followed by a lower next-day excess return. The supporting check must also pass.
- Reject: The slope is negative with t ≤ −2: larger rises are followed by larger next-day gains.
- Inconclusive: A slope t between −2 and 2, or a confirming slope with the supporting check failing. At least 30 independent days with a negative forecast are required; with fewer, the result is inconclusive.
