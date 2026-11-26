---
idea: 035-01_falling-agitated-scaled-fall-rebound
brief: 035_falling-agitated-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a one-day fall, in a falling, agitated market -> kept: the profile is added by code, and the fall is the bar's return below zero.
- Comparison: the fall relative to the coin's 30-day daily swing -> kept: the one-day return divided by the 30-day std of daily returns.
- Outcome: the larger the fall, the larger the rise over the next day -> kept: a long position graded by the scaled fall, held 1 bar.
- Verdict transfer: yes: the forecast is the idea's scaled fall inside its profile, judged on the next-day return.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 1 and vol_period 30, which gives the day's return in units of the 30-day daily standard deviation. It is standardised over its past 60 values, then negated, then clipped at 0. On a down day it is positive and grows linearly with the size of the fall in usual moves, up to the cap of 20. It is 0 on up days and flat days, and it is never negative. Code keeps the book flat outside the falling, agitated profile.
Config: 035-01_falling-agitated-scaled-fall-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next-day return on the forecast, over bars with forecast > 0. The next-day return is close[t+1]/close[t]-1 minus the coin's mean daily return over all windows, so the market's own drift is not credited. The t of the slope is computed with cases on the same day taken together.
- Supporting check: Over the bars in the top third of the positive forecasts, the mean of the same excess next-day return is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive, as is a positive t of 2 or more whose top-third check fails. The test needs at least 30 bars with forecast > 0, on at least 20 distinct days; fewer is inconclusive.
