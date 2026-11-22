---
plan: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends_1d
idea: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar unusual move over cases (before costs): -0.00157716; t of the mean: -0.26544 (threshold: confirm t >= 2 over at least 30 cases; reject t <= -2 over at least 30 cases)
- Supporting check: upper-half minus lower-half mean unusual move (median forecast split): 0.0284224, passed: True
- Counts: cases: 930, upper half cases: 465, lower half cases: 465
- Decided by: t between -2 and 2 over at least 30 cases (inconclusive rule).
- Reading: Regime ret90>0 recomputed from closes where the window holds 90 prior bars, else the recorded regime=='trending'; the rise is last_history_value>0 (day's return>0 if missing); cases are long bets per the holding rule (forecast rise >=2 from its lowest level since the last bet, from 0 after a flat), the first per 10-bar grid cell from each window's first row; drift is the coin's mean 10-bar grid return over all windows; the median split puts cases above the median in the upper half and at or below it in the lower half.
- Size: unusual move -0.16 % per case over 10 bars, -0.016 of the coin's usual move (14.49 %); normal drift in its direction +1.17 %, total +1.01 %; 930 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends_1d`
Measure: `measure.py`
