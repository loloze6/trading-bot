---
idea: 038-02_agitated-fall-vs-swing-rebound
brief: 038_agitated-decline-big-falls-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 00d5d6f5c07b
---
Fidelity:
- Situation: a coin's one-day fall against the standard deviation of its daily returns over the last 30 days -> kept: the 1-bar return over the 30-bar return std, fall side only, and the falling agitated profile is added by code.
- Comparison: larger falls against smaller ones, the next day -> kept: the forecast grows with the size of the fall.
- Outcome: the coin rises over the next day, more after larger falls -> kept: horizon of 1 bar, long only.
- Verdict transfer: yes: the forecast is the idea's own scaled fall, inside its profile, judged on the next day's return.
Forecast: One component, `VolatilityScaledReturnComponent` with `period` 1, `vol_period` 30, `lag` 0 and `vol_lookback` 1. It gives the day's return divided by the standard deviation of the last 30 daily returns. This is the day's move in usual moves. The value is standardised over 60 bars (min_periods 20), then negated and clipped at 0. The forecast is positive only on down days and grows linearly with the fall's size in usual moves, up to the cap of 20. It is 0 on up days and flat days, and never negative (long only). Code adds the falling agitated profile, so the book is flat outside that profile.
Config: 038-02_agitated-fall-vs-swing-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars with forecast > 0, every bar being a non-overlapping 1-bar case. Regress the coin's next-day return, minus that coin's mean daily return over all windows, on the forecast. Report the slope's t.
- Supporting check: On the same bars, the mean next-day excess return (minus the coin's mean daily return) is above 0.
- Confirm: The slope's t is 2 or more, the supporting check passes, and there are at least 100 cases.
- Reject: The slope's t is -2 or less with at least 100 cases. A mean next-day excess return on those bars with a t of -2 or less also rejects (large falls followed by further declines).
- Inconclusive: A slope t between -2 and 2. A slope t of 2 or more with a mean excess return of 0 or less. Fewer than 100 cases with forecast > 0.
