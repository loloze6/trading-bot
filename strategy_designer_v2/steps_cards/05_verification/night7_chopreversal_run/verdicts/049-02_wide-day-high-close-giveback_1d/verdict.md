---
plan: 049-02_wide-day-high-close-giveback_1d
idea: 049-02_wide-day-high-close-giveback
fit: adapted
status: inconclusive
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (pooled, day-clustered): 0.000412399; day-clustered t: 1.73258 (threshold: slope > 0 with t >= 2 (confirm); slope < 0 with t <= -2 (reject))
- Supporting check: mean sign(forecast) x excess return, top fifth of |forecast| minus bottom two fifths: 0.000265814, passed: True
- Counts: distinct days with a forecast: 2877, bars in regression: 17380
- Decided by: The slope's t lies between -2 and 2.
- Reading: Situation read as standardised width minus standardised distance under the high (rebuilt from raw values, short when positive); regression uses all bars with a next close in the window with an intercept and CR1 day-clustered errors; fifths of |forecast| are taken over those same bars (top fifth >= 80th percentile, bottom two fifths <= 40th percentile); a 'distinct day with a forecast' is a UTC day with a non-zero forecast on any coin among those bars.
- Size: unusual move +0.16 % (t 1.62, the cases of one day together: 2249 days) per case over 1 bars, 0.038 of the coin's usual move (4.78 %); normal drift in its direction -0.01 %, total +0.15 %; 6107 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/049-02_wide-day-high-close-giveback_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/049-02_wide-day-high-close-giveback_1d`
Measure: `measure.py`
