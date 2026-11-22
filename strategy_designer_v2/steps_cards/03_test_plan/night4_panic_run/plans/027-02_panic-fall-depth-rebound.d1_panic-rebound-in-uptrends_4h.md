---
idea: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour stretch whose range is several times its 30-day average, with a 90-day return above zero -> kept: a regime fires when the mean bar range of the last 6 bars is at least 3 times its 180-bar mean, and the component is 0 unless the 540-bar return is above zero.
- Comparison: a deeper 24h fall and a larger 90-day rise give a higher return than shallower ones -> kept: the position grows with the 6-bar fall (in usual 24h moves) times the 540-bar rise.
- Outcome: a higher return over the next 14 days (84 bars), long -> kept: each bet is held 84 bars and judged against the coin's normal drift.
- Verdict transfer: yes: the test measures the panic, the fall, the 90-day rise and the 14-day return as the idea states them, so a confirm or reject carries over.
Forecast: The regime detector reads the ratio of the 180-bar mean bar range to the 6-bar mean bar range. When that ratio is 0.333 or less, the last 24 hours' bars are at least 3 times as wide as their 30-day average. That is a panic, and the regime is `mean_reversion`. On every other bar the forecast is 0. Inside a panic, the forecast uses MeanAbsScaledFallTimesRise, with fall_period 6, window 180 and rise_period 540. It multiplies two things: - the 24h fall, measured in usual 24h moves over 30 days; - the positive 90-day percent return. The forecast is 0 when the coin did not fall or its 90-day return is not positive. It grows with both the depth of the fall and the size of the rise. This value is standardised against its own past (window 500, min_periods 120). It then goes through signed_power with exponent 3 and pivot 10, the strongest graded dead zone, so small panics give near-zero positions and deep ones are amplified. The forecast is never negative (long only by construction), and it is capped at 20.
Config: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: The cases are long bets (forecast rises of at least 2 points), read once per 84-bar grid cell inside each window. For each case, take the coin's 84-bar return from the signal bar's close minus the coin's normal 84-bar drift over all windows. Compute the mean of these unusual returns and its t across cases.
- Supporting check: The cases whose forecast is above the cases' median have a higher mean unusual 84-bar return than those at or below it (difference, upper minus lower, greater than 0).
- Confirm: The mean unusual 84-bar return is positive with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual 84-bar return is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2. Also a confirming main measure whose supporting check fails, or fewer than 30 cases in total.
