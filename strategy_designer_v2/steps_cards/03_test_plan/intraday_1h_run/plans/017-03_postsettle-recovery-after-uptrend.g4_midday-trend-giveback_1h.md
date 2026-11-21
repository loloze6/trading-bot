---
idea: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: the 3 hours from 11:00 UTC, and a coin's own 3-day return -> kept: a regime on the coming bar's hour (11, 12, 13), with the 72-bar return re-read at each hourly close.
- Comparison: the larger the 3-day return, the larger the move against it -> kept: the position is graded on the size of the 72-bar return.
- Outcome: over those 3 hours the price moves against the 3-day return -> kept: the position is held over the 3 bars starting 11:00, 12:00 and 13:00 UTC.
- Verdict transfer: yes: the test measures exactly the idea's 3-hour countermove and its size relation, and nothing else.
Forecast: The forecast is computed on each hourly bar whose next bar starts at 11:00, 12:00 or 13:00 UTC. There it is minus the coin's 72-bar (3-day) percent return, divided by the mean absolute size of that return over its previous 72 hourly values, times 10, capped at ±20. It is negative (short) after a 3-day rise and positive (long) after a 3-day fall. Its size grows in proportion to the 3-day move, and it is near 0 when the coin is flat over 3 days. On all other hours the forecast is 0 (flat), because the idea is itself a clock condition.
Config: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback_1h_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Take one case per day per coin and window: the bar stamped 10:00 UTC. Its outcome is the excess 3-hour return close[t+3]/close[t]-1 minus the coin's mean 3-bar return over all its windows. Regress this excess return on that bar's recorded forecast, pooled over coins and windows. The measure is the t of the slope.
- Supporting check: The mean before-cost gain of the position over the 11:00–13:00 bars must be above 0. The gain counted is the position times the bar return, minus the position times the coin's mean hourly return over all windows.
- Confirm: The idea is confirmed when the slope's t is 2 or more, with at least 500 cases, and the supporting check passes.
- Reject: The idea is rejected when the slope's t is -2 or less, with at least 500 cases.
- Inconclusive: The result is inconclusive when the t is between -2 and 2, or when the t is 2 or more but the supporting check fails. It is also inconclusive with fewer than 500 daily cases, whatever the t.
