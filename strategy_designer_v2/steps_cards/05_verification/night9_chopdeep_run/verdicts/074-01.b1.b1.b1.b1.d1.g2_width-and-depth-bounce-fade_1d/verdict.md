---
plan: 074-01.b1.b1.b1.b1.d1.g2_width-and-depth-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.d1.g2_width-and-depth-bounce-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move in the short direction over forecast < 0 bars: 0.00260147; t of the mean, cases of one day taken together: 1.88468 (threshold: mean unusual move positive with day-clustered t >= 2 confirms; negative with t <= -2 rejects)
- Supporting check: larger-half minus smaller-half mean unusual move (split at median abs(forecast)): 0.00181807, passed: True
- Counts: cases: 6519, distinct days: 1426
- Decided by: The t lies between -2 and 2.
- Reading: Falling market = 60-bar close return below -10 % and up day = close above prior close, from the window's prices, using the recorded regime where the window lacks the past prices; cases are all bars with forecast < 0 and a next close in the window; the larger half is abs(forecast) above the cases' median, the smaller half at or below it; the day-clustered t uses the per-day summed deviations with a G/(G-1) correction.
- Size: unusual move +0.32 % (t 1.93, the cases of one day together: 1160 days) per case over 1 bars, 0.062 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.17 %; 4222 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.g2_width-and-depth-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.d1.g2_width-and-depth-bounce-fade_1d`
Measure: `measure.py`
