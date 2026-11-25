---
idea: 043-01_falling-market-narrow-day-rise
brief: 043_quiet-days-mark-downtrend-exhaustion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: in a falling market, a day whose high-low range is narrow against its 30-day daily-return swing -> kept: the brief's falling profile, plus RangeInReturnStdComponent (vol_period 30), graded so a narrower day gives a larger long.
- Comparison: the day's range in units of the coin's 30-day return swing, narrower than usual -> kept: the 30-day std is the component's divisor, and the offset centres it at its usual size.
- Outcome: the coin rises over the next 3 days, more the narrower the day -> kept: held 3 bars, position grows as the range shrinks.
- Verdict transfer: yes: the test measures whether 3-day returns in falling markets grow as the range-to-swing ratio shrinks, which is the idea's claim.
Forecast: Inside the falling profile, which code adds, the forecast reads the day's high-low range divided by the close and by the std of the last 30 daily returns (RangeInReturnStdComponent, vol_period 30). That ratio is standardised against its past 60 values (about +10 at its usual size) and negated. A constant of +10 is added at equal weight, so the forecast is (10 − x)/2. It is positive when the day is narrower than usual and grows to about +5 for a day with almost no range. It is 0 at the usual width and negative, down to −5, on unusually wide days. The size changes smoothly with the ratio and has no threshold.
Config: 043-01_falling-market-narrow-day-rise_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping 3-bar grid in each window, on bars with a nonzero forecast (inside the falling profile). Regress the coin's 3-day forward return, minus its normal 3-day drift over all windows, on the forecast; report the slope's t.
- Supporting check: On grid bars with forecast > 0, the mean 3-day return minus the coin's normal drift is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is −2 or less.
- Inconclusive: Any t between −2 and 2 is inconclusive, as is a t of 2 or more when the supporting check fails, or fewer than 100 non-overlapping cases.
