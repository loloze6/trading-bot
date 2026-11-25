---
plan: 032-02.b2.g2_volatile-close-near-low-rebound_1d
idea: 032-02.b2.g2_volatile-close-near-low-rebound
fit: adapted
status: confirmed
---
Situation check: 96 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on low_close forecast, regime bars: 0.000429026; t of OLS slope, SE clustered by day: 2.45411 (threshold: confirm: slope > 0 with t >= 2 and top-minus-bottom third > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean excess next-day return, top third minus bottom third of forecasts: 0.00589702, passed: True
- Counts: regime bars: 7697, distinct days: 2128
- Decided by: The slope is positive with t >= 2 and the top-minus-bottom-third difference is above 0.
- Reading: The detector's MeanBarRangeRatio is recomputed from prices as the 90-bar mean of (high-low)/close over its 30-bar mean, inside each window, and where fewer than 90 bars of the window exist the recorded regime stands in for it; the close sits low when (high-close)/(high-low) > 0; the coin's mean daily return is the mean of all its 1-bar returns over all windows; the slope's t is the OLS slope with standard errors clustered by UTC day; regime bars are those with regime 'mean_reversion' and a next-day return in the window; thirds are cut by forecast rank.
- Size: unusual move +0.23 % (t 1.43, the cases of one day together: 1348 days) per case over 1 bars, 0.053 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.35 %; 3328 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +9.485e-05 on the check folds against +0.000429 on every fold
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g2_volatile-close-near-low-rebound_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g2_volatile-close-near-low-rebound_1d`
Measure: `measure.py`
