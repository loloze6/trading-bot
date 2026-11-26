---
plan: 031-01.g1.g2_monthly-trend-carries-into-saturday_1d
idea: 031-01.g1.g2_monthly-trend-carries-into-saturday
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the daily-summed forecast/10 x excess next-bar return on Friday-close trending cases: 0.0324785; t of the mean across days: 3.02483 (threshold: t of 2 or more confirms (with top-minus-bottom above 0); t of -2 or less rejects; at least 200 distinct Friday days)
- Supporting check: Saturday excess return, top third minus bottom third of forecast (Welch t 4.951): 0.0100706, passed: True
- Counts: distinct Friday days with cases: 414, coin-cases: 2478, cases per third: 826
- Decided by: The main measure's t is 2 or more and the top-minus-bottom difference is above 0.
- Reading: Cases are all Friday-start bars with regime 'trending' and a next bar in the same window (forecast 0 included), the coin's mean is its mean next-bar return over all windows, the thirds are the lowest and highest floor(n/3) cases pooled across coins by forecast (stable sort), and only the 200-day minimum is applied as a hard count since the 2,000 coin-cases is stated as 'about'.
- Size: unusual move +0.30 % (t 2.10, the cases of one day together: 413 days) per case over 1 bars, 0.060 of the coin's usual move (4.78 %); normal drift in its direction -0.01 %, total +0.29 %; 2150 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g2_monthly-trend-carries-into-saturday_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g2_monthly-trend-carries-into-saturday_1d`
Measure: `measure.py`
