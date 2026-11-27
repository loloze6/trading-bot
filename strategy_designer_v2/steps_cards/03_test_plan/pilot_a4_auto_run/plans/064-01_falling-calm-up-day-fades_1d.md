---
idea: 064-01_falling-calm-up-day-fades
brief: 064_falling-calm-scaled-rallies-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: a coin's one-day rise in a falling, calm market -> kept (the profile is added by code; the rise is clipped to up days)
- Comparison: the rise in units of its own 30-day standard deviation of daily returns -> kept
- Outcome: the close falls over the next 3 days, more the larger the scaled rise -> kept
- Verdict transfer: yes: the forecast is short in proportion to the scaled rise, and the test checks both the fall and its growth with size.
Forecast: The forecast uses VolatilityScaledReturnComponent (period 1, vol_period 30). This is the day's return divided by the standard deviation of the last 30 daily returns. It is standardised over its past 60 values (min_periods 20), then clipped at 0 so only up days count, then negated. The forecast is 0 on down and flat days. On up days it is negative (short), and its size grows linearly with the rise in 30-day swing units. Code adds the falling-calm profile, so the forecast is 0 outside that profile.
Config: 064-01_falling-calm-up-day-fades_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping 3-bar grid of each window and keep the bars with forecast < 0. On each, take the coin's 3-bar forward return minus the coin's mean 3-bar return over all windows (holding the coin). Regress this excess return on the forecast and take the OLS slope and its t.
- Supporting check: On the same cases, the mean unusual move in the signal's direction (short) must be positive, with t ≥ 2, cases on the same day taken together.
- Confirm: The slope is positive with t ≥ 2, so larger rises are followed by larger excess falls, and the supporting check passes.
- Reject: The slope's t is ≤ -2, or the unusual move in the short direction has t ≤ -2 (scaled rises are followed by excess rises).
- Inconclusive: Anything else is inconclusive, including slope or mean-move t values between -2 and 2. The test also needs at least 100 grid cases with forecast < 0 over at least 60 distinct days; below that it is inconclusive.
