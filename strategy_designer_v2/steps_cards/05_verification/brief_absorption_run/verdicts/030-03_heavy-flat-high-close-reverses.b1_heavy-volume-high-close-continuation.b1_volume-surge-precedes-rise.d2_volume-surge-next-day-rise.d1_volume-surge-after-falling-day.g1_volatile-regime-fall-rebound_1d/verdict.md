---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day excess return on forecast (forecast > 0): 0.000452113; OLS t of slope: 5.4331 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; |t| < 2 inconclusive)
- Supporting check: mean next-day excess return over top third of positive forecasts > 0: 0.00498507, passed: True
- Counts: bars with forecast > 0: 8514, top-third bars: 2838
- Decided by: The slope is positive with t >= 2 and the top-third mean excess return is above 0.
- Reading: Coin mean daily return is the mean of close[t+1]/close[t]-1 over every bar of all the coin's windows; the slope's t is the ordinary OLS t; the top third is the pooled positive-forecast bars with forecast at or above the pooled 2/3 quantile; the 300-bar minimum counts positive-forecast bars with a next-day return and, as a minimum count, gives 'not observable'.
- Size: unusual move +0.20 % per case over 1 bars, 0.042 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.32 %; 5581 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d`
Measure: `measure.py`
