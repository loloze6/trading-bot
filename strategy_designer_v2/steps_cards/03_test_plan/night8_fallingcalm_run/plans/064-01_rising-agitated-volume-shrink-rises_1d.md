---
idea: 064-01_rising-agitated-volume-shrink-rises
brief: 064_rising-agitated-volume-dry-up-rises
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6002f52a0948
---
Fidelity:
- Situation: a rising, agitated market where the coin's 30-day volume has shrunk against the 30 days before -> adapted: the profile comes from the header, and the shrinkage is graded as max(0, -ln(last-30-day mean volume / prior-30-day mean volume)).
- Comparison: the last 30 days' volume against the 30 days before -> kept
- Outcome: a larger rise over the next 5 days, the more volume shrank -> kept
- Verdict transfer: yes: a forecast graded by the shrinkage, inside the rising agitated profile and held 5 days, tests exactly whether a larger shrinkage brings a larger 5-day rise.
Forecast: The forecast uses one indicator, VolumeRatioComponent with period 30, exclude_current 30, short_period 30, statistic mean and form "log". It gives ln(mean volume of the last 30 days / mean volume of the 30 days before them). With equal window lengths, this is the ratio of the two 30-day totals. The value is standardised over its last 60 values, then negated, so shrinking volume reads positive. It is then clipped at 0, which keeps the book long only. The forecast is positive and grows with the shrinkage. It is 0 when volume grew or held. Code adds the rising agitated profile, so the book is flat outside it.
Config: 064-01_rising-agitated-volume-shrink-rises_1d_config.json
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the bars inside the profile, on a grid of non-overlapping 5-bar steps in each window. On these bars, regress the coin's 5-day forward return, minus the coin's mean 5-day return over all windows, on the forecast. The measure is the t of the slope.
- Supporting check: The mean of the same excess 5-day return, on grid bars with forecast > 0, is above 0.
- Confirm: The slope's t is +2 or more, and the supporting check's mean is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and +2 is inconclusive. A t of +2 or more with a check mean at or below 0 is also inconclusive. So is a sample under 30 non-overlapping grid cases with forecast > 0, or under 100 profile grid bars in total.
