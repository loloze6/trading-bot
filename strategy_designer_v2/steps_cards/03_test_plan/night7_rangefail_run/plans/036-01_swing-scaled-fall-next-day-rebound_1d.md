---
idea: 036-01_swing-scaled-fall-next-day-rebound
brief: 036_sharp-fall-next-day-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: adf647c613f7
---
Fidelity:
- Situation: a one-day fall, measured in the coin's own 20-day daily-return standard deviations -> kept
- Comparison: the fall against the coin's own recent daily swings -> kept
- Outcome: the coin rises over the next day, more the larger the fall in swing units -> kept
- Verdict transfer: yes: the forecast is that fall in swing units, held one day, so the test's answer is the idea's answer.
Forecast: The forecast uses `VolatilityScaledReturnComponent` with `period` 1 and `vol_period` 20. Its raw value is the day's return divided by the standard deviation of the last 20 daily returns, today's included. `standardise` (window 60, min_periods 20) puts that value on the forecast scale against its own past absolute size. `negate` then makes a fall read positive, and `clip` with `min` 0 removes up days. The result is long only. It is 0 on up days and flat days. It is positive after a down day and grows linearly with the number of swings the fall spans: a fall of usual size gives about +10, and the cap is +20. It is active in every market, with no regime.
Config: 036-01_swing-scaled-fall-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bars
- Main measure: The least-squares slope of the coin's next-day return minus its mean daily return over all windows, against the bar's `forecast`. It uses every bar of every coin and window (horizon 1, so all bars are non-overlapping), before costs. Its t counts the cases of one day together.
- Supporting check: On bars with forecast above 0, the mean next-day return minus the coin's mean daily return is above 0.
- Confirm: The idea is confirmed when the slope's t is 2 or more and the supporting check's mean excess return is above 0.
- Reject: The idea is rejected when the slope's t is -2 or less, meaning larger falls in swing units are followed by lower next-day returns than usual.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. A slope t of 2 or more with a supporting mean at or below 0 is also inconclusive. The test needs at least 300 bars with forecast above 0, spread over at least 200 distinct days.
