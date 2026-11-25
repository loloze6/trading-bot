---
idea: 039-01_scaled-fall-next-day-rebound
brief: 039_scaled-one-day-falls-rebound-next-day
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a down day, sized as the fall in units of the 30-day daily-return std -> kept: the 1-day return over a 30-day std, zero on up days
- Comparison: the fall against the coin's own 30-day daily swing -> kept
- Outcome: the coin rises over the next day, more after larger scaled falls -> kept: long held one bar, sized by the scaled fall
- Verdict transfer: yes: the forecast is the idea's scaled fall, held for the idea's next day, so the test's verdict is the idea's verdict
Forecast: The forecast uses `VolatilityScaledReturnComponent` with `period` 1 and `vol_period` 30. Its raw value is the day's return divided by the std of the last 30 daily returns. It is standardised over 60 past values (min 20), so a usual-sized move is about 10. The value is then negated and clipped at 0. The forecast is 0 on up and flat days. On down days it is positive and grows linearly with the fall in usual moves: about 10 at a typical down move and 20 (the cap) at about twice that. It is long only and is held for one day.
Config: 039-01_scaled-fall-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bars
- Main measure: On bars with forecast > 0, regress the next-day return minus the coin's mean daily return over all windows on the forecast. Report the slope and its t, with cases of one day summed across coins.
- Supporting check: The mean next-day excess return is above 0 on the down days in the top fifth of forecast (by coin).
- Confirm: The slope's t is 2 or more and the top-fifth mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a confirming slope whose top-fifth mean is not above 0. The test needs at least 300 down-day cases on at least 200 distinct days; with fewer it is inconclusive.
