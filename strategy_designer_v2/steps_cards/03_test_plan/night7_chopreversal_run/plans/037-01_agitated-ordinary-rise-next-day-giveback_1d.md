---
idea: 037-01_agitated-ordinary-rise-next-day-giveback
brief: 037_agitated-ordinary-rise-next-day-giveback
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in an agitated market, a one-day rise that stays within the 30-day daily swing -> kept: the profile line adds agitation, and a regime holds only bars whose rise is 0 to 1 times the 30-day daily return std.
- Comparison: larger rise relative to the 30-day daily swing gives a larger fall -> kept: the short is graded by the rise divided by the 30-day std, judged against the coin's normal drift.
- Outcome: the coin falls over the next day -> kept: short, held 1 bar.
- Verdict transfer: yes: the test measures the idea's own rise, swing and next-day move on the bars the idea names.
Forecast: Take the day's return divided by the standard deviation of the last 30 daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 30). The regime detector computes the same quantity and selects `mean_reversion` only when it is between 0 and 1, that is, a rise within the usual swing. On every other bar the forecast is 0 (flat). The code-added agitated profile also keeps the book flat outside agitated markets. Inside the regime, the forecast is that scaled rise, standardised against its own past 60 values and negated. It is a short that grows from 0 at a flat day to its largest size at a rise of one usual swing. It is never positive.
Config: 037-01_agitated-ordinary-rise-next-day-giveback_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: For each case, take the coin's next-day return from the signal bar's close and subtract the coin's mean daily return over all windows. Read it in the short direction (sign flipped). The measure is its mean, with its t computed with cases of the same day taken together.
- Supporting check: Across the cases, regress the next-day excess return on the raw scaled rise (`last_history_value` of `rise`). The slope must be negative.
- Confirm: The main measure's mean is positive with t ≥ 2, and the supporting slope is below 0.
- Reject: The main measure's mean is negative with t ≤ -2, meaning ordinary rises continue the next day more than the drift.
- Inconclusive: Any other result is inconclusive, including a main t between -2 and 2, or a main t ≥ 2 with a slope at or above 0. At least 200 cases on at least 150 distinct days are needed; fewer is inconclusive.
