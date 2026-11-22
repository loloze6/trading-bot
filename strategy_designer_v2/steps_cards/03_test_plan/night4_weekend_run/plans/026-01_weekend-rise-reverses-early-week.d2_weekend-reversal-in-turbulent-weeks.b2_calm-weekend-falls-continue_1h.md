---
idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2a96c3272007
---
Fidelity:
- Situation: the price falls from Saturday 00:00 UTC to Monday 00:00 UTC -> kept: the 48-bar return read at the bar closing at Monday 00:00, short side only, graded by the size of the fall.
- Comparison: 30-day hourly volatility is low against its own last 6 months -> kept: a regime rule on the rank of 720-bar volatility within 4380 bars, at or below the median.
- Outcome: the price keeps falling over Monday and Tuesday, more after a larger fall -> kept: a short sized by the fall, held 48 bars.
- Verdict transfer: yes: the test measures this exact fall, this condition and this window, so its result is the idea's result.
Forecast: The forecast is computed on one bar a week only: the bar whose close is Monday 00:00 UTC, when the coin's volatility rank is at or below 0.5. The volatility is the 720-bar standard deviation of returns, ranked within 4380 bars, with the default smoothing of 5. On that bar, the forecast is the coin's 48-bar return, which runs from Saturday 00:00 to Monday 00:00. It is standardised over 60 bars and clipped at 0 from above. The forecast is negative (short) after a weekend fall, and its size grows with the fall, up to -20. It is 0 after a weekend rise, on every other bar, and in high-volatility weeks. The holding period keeps the short for the 48 bars of Monday and Tuesday.
Config: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: For each case, take the coin's 48-bar return from the close of the signal bar (Monday 00:00), minus the coin's normal 48-bar drift over all windows, in the short direction. A case is a short bet on a Monday signal bar. Measure the mean of this move over all cases and its t.
- Supporting check: Cases whose forecast size is at or above the median size have a larger mean short-direction move than cases below the median (difference > 0).
- Confirm: The mean short-direction move has t >= 2 over at least 100 cases, and the supporting check passes.
- Reject: The mean short-direction move has t <= -2 over at least 100 cases, meaning weekend falls are followed by rises beyond the coin's drift.
- Inconclusive: Any t between -2 and 2; or t >= 2 with the supporting check failing; or fewer than 100 cases.
