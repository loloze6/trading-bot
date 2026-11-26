---
idea: 065-03_falling-agitated-down-streak-rebound
brief: 065_agitated-downtrend-slide-depth-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a falling, agitated market with the coin on a run of consecutive lower closes -> kept: the profile is added by code, and the down-close streak length is measured directly.
- Comparison: more consecutive down days against fewer -> kept: the forecast is graded by the streak length.
- Outcome: a larger rise over the next day -> kept: long, held 1 bar.
- Verdict transfer: yes: the forecast is the down-streak length itself, held one day inside the named profile, so its slope on next-day returns answers the idea directly.
Forecast: One component, `UpCloseStreakLengthComponent` with side "down", base "none" and max_bars 30. It counts the consecutive lower closes ending today: 0 when today did not close down, and +1 for each further down day. It is standardised over the 60 values before today (min_periods 20), so a streak of usual size is about +10, capped at 20. The forecast is never below 0, so the strategy is long only. It is zero on any day that did not close lower, and it grows linearly with the streak's length. The code keeps the book flat outside the falling, agitated profile.
Config: 065-03_falling-agitated-down-streak-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Take the bars with forecast > 0. On those bars, regress the coin's next-day return (close[t+1]/close[t] - 1) minus the coin's mean daily return over all its windows on that bar's forecast. The measure is the slope and its t, with the deviations summed per day across coins.
- Supporting check: The mean next-day return minus the coin's mean daily return, over bars with forecast > 0, is above 0 (gains before costs beat holding the coin).
- Confirm: The slope is positive with t >= 2 and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope with |t| < 2, or t >= 2 when the supporting check fails, is inconclusive. The test also needs at least 100 distinct days with forecast > 0 across the coins; fewer is inconclusive.
