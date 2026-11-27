---
plan: 074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 1-day move per case: 0.00597685; t of the mean, cases of one day pooled: 1.73975 (threshold: mean > 0 with day-pooled t >= 2 confirms; mean < 0 with t <= -2 rejects)
- Supporting check: heavier-half minus lighter-half mean unusual move (split at median |forecast|): 0.00495002, passed: True
- Counts: cases: 1119, distinct days: 516
- Decided by: The t lies between -2 and 2 (or cannot be computed).
- Reading: Cases are the short bets (forecast rising >= 2 points on the short side from its lowest level since the last bet) with a next bar in the window; the coin's mean is its mean 1-day return over all its windows; the day-pooled t uses the per-day sums of deviations without small-sample correction; the heavier half is |forecast| strictly above the median; situation conditions not computable inside a window were taken from the record (heavy_volume raw > 0, regime 'mean_reversion') and the 60-bar evolution is read in percent.
- Size: unusual move +0.60 % (t 1.74, the cases of one day together: 516 days) per case over 1 bars, 0.116 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.44 %; 1119 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade_1d`
Measure: `measure.py`
