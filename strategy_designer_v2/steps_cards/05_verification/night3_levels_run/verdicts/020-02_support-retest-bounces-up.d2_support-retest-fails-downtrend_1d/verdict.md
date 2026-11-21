---
plan: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend_1d
idea: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed (short) excess 5-bar return at grid bars where a short bet starts: 0.00598484; t of the mean: 1.1307 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: t <= -2; fewer than 30 cases inconclusive)
- Supporting check: mean signed excess fall, larger |forecast| half minus smaller half: -0.00947313, passed: False
- Counts: cases: 271, larger-forecast half: 135, smaller-forecast half: 136, active bars: 2299
- Decided by: The t of the mean signed excess fall lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are the bars at positions 0, 5, 10, ... of each window on which a short bet starts (a fall of the forecast of at least 2 points below its least-negative level since the last bet, reset at flat), the excess is against the coin's mean 5-bar grid return over all its windows, and the median split puts cases with |forecast| above the median in the larger half and the rest in the smaller.
- Size: unusual move +0.45 % per case over 5 bars, 0.045 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -0.13 %; 920 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend_1d`
Measure: `measure.py`
