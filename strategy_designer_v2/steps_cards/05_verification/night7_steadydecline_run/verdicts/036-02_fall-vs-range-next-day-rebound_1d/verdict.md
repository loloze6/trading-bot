---
plan: 036-02_fall-vs-range-next-day-rebound_1d
idea: 036-02_fall-vs-range-next-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return (close[t+1]/close[t]-1 minus coin's mean daily return) on case bars, same-day cases summed: 0.0172916; t of the mean (over per-day summed cases): 1.9338 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: t <= -2)
- Supporting check: Spearman correlation of raw ratio (fall.last_history_value) vs next-day excess return across cases: 0.0615476, passed: True
- Counts: case days: 365, case bars: 936, active bars: 946
- Decided by: Inconclusive rule met: the t of the mean next-day excess return lies between -2 and 2.
- Reading: Cases on the same UTC day are summed into one value and the mean and ordinary t are taken over these day sums, the Spearman correlation is taken over individual case bars, the coin's mean daily return is the mean of all its 1-bar returns inside all windows, and the plan's 'fewer than 100 case days' is reported as not observable.
- Size: unusual move +0.46 % (t 1.29, the cases of one day together: 349 days) per case over 1 bars, 0.089 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.58 %; 861 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/036-02_fall-vs-range-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/036-02_fall-vs-range-next-day-rebound_1d`
Measure: `measure.py`
