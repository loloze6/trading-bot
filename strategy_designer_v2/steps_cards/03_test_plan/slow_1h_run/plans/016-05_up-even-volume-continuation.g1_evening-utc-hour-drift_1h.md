---
idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the two hours after 20:00 UTC, with the coin's realised hourly volatility over the past 7 days -> kept
- Comparison: the coin's rise in its other hours -> kept
- Outcome: the price rises over 20:00–22:00 UTC, more the higher the 7-day volatility (long) -> kept
- Verdict transfer: yes: the forecast holds a long only through the 20:00 and 21:00 bars and sizes it by the 7-day hourly volatility, as the idea states.
Forecast: A regime rule on `HourOfDayComponent` selects the bars whose coming bar starts at 20:00 or 21:00 UTC. The rule is `between` 19.5 and 21.5. A long is therefore held from the 20:00 close to the 22:00 close. All other hours are flat (null regime). In the selected regime the forecast is the 7-day realised hourly volatility: `VolatilityFromStdDevComponent` with `vol_period` 169, so the std of 168 hourly returns. It is standardised against its own past 169 values (min_periods 42). The forecast is always positive and graded: about +10 at its usual level, rising toward +20 when volatility is above it, and falling toward 0 when it is below.
Config: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The case is one per day per coin and window: the coin's 2-bar return from the close of the 19:00 bar to the close of the 21:00 bar. It is compared with the coin's 2-bar returns over the other hours of the day, taken on a non-overlapping grid aligned on even UTC hours and excluding the 20:00–22:00 block. The test is Welch's t on the 20:00–22:00 returns minus the other-hour returns, pooled over coins and windows.
- Supporting check: Regress the 20:00–22:00 return on the 7-day volatility, `vol7d` `last_history_value` at the 19:00 bar, pooled over coins and windows. The slope must have t ≥ 2.
- Confirm: The main difference is positive with Welch t ≥ 2, and the supporting check passes (slope t ≥ 2).
- Reject: The main difference has Welch t ≤ -2, or the volatility slope has t ≤ -2.
- Inconclusive: Any other result is inconclusive. This includes a main t between -2 and 2, and a positive main t with a slope t between -2 and 2. The test needs at least 500 daily 20:00–22:00 cases in total and at least 1500 other-hour cases.
