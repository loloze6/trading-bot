---
idea: 032-02_low-range-decline-continues-more
brief: 032_calm-decline-keeps-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 051b3422f169
---
Fidelity:
- Situation: the coin has fallen over the past 28 days -> kept: a regime holds only when the 28-day return is below 0, and the book is flat elsewhere.
- Comparison: daily high-low ranges over those 28 days against the coin's own usual ranges -> kept: the mean daily range over 365 days divided by the mean over the last 28, graded (the calmer, the larger).
- Outcome: a further fall over the next 5 days, larger the calmer the decline -> kept: a short whose size grows with calmness, held 5 bars.
- Verdict transfer: yes: the test measures the same condition, the same graded comparison and the same 5-day fall, so a confirm or a reject carries over to the idea.
Forecast: The detector reads the 28-day percent return (`PriceEvolutionOnPeriodComponent`, 28). When it is below 0 the bar is "trending". Every other bar is "unknown" and flat. Inside the regime the forecast is minus the standardised calmness ratio. The ratio is the mean high-low range over the last 365 bars divided by the mean over the last 28 bars (`MeanBarRangeRatioComponent`). It is 1 when the decline's ranges are usual and above 1 when they are quieter. Standardise uses a 365-bar window with min_periods 91, and negate turns it into a short. At a usual calmness the short is about -10. It grows towards -20 as the 28-day ranges shrink against their yearly norm, and falls towards 0 as they widen. The forecast is never positive.
Config: 032-02_low-range-decline-continues-more_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the "trending" bars on the non-overlapping 5-bar grid of each window. For each, take the coin's 5-bar forward return minus that coin's mean 5-bar return over all windows. Regress it on the size of the short (abs forecast, from `post_pipeline_value` of "calm"). Report the slope's t and the number of cases.
- Supporting check: Over the same cases, the mean drift-adjusted 5-bar return weighted by abs forecast is below 0.
- Confirm: The slope is negative with t ≤ -2 (larger shorts are followed by larger falls than usual), and the supporting check passes.
- Reject: The slope is positive with t ≥ +2 (calmer declines are followed by smaller falls or rises).
- Inconclusive: A slope t between -2 and +2, or a confirming slope whose supporting check fails. At least 200 grid cases in the regime are required; with fewer the result is inconclusive.
