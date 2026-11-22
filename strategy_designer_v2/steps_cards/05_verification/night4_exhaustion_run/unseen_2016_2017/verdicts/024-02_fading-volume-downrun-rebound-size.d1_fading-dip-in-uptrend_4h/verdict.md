---
plan: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h
idea: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 18-bar excess return over normal drift, per bet, pooled: 0.0107908; t of the weighted mean: 1.57598 (threshold: positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 over at least 30 cases to reject)
- Supporting check: timing gain: mean daily book return minus position x coin mean daily return: 0.000310169, passed: True
- Counts: cases: 462
- Decided by: t between -2 and 2 (or sign and t disagree) over at least 30 cases.
- Reading: The down-streak is the run of consecutive closes below the previous close (capped at 180 bars) with the volume slope fitted on those falling bars, the first bet in each 18-bar grid cell is the case, the t of the forecast-weighted mean uses the weighted standard error sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w), and the daily position for the market part is the mean allocation held over the bars of that day.
- Size: unusual move +0.54 % per case over 18 bars, 0.069 of the coin's usual move (13.56 %); normal drift in its direction +3.14 %, total +3.68 %; 462 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/unseen_2016_2017/backtests/024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h`
Measure: `measure.py`
