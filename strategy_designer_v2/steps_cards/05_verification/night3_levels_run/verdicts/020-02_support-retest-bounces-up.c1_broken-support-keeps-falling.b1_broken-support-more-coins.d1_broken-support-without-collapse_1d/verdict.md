---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean of |forecast|-weighted unusual 10-bar falls on short grid cases: 0.156346; t of the mean: 3.68999 (threshold: confirm if t >= 2 over at least 30 cases (and supporting check passes); reject if t <= -2 over at least 30 cases)
- Supporting check: mean unusual fall, top third |forecast| minus bottom third: 0.00858032, passed: True
- Counts: cases: 2251, cases per third: 750
- Decided by: The main t is 2 or more over at least 30 cases and the top third shows a larger unusual fall than the bottom third.
- Reading: Situation taken as raw support_above > 0 on bars whose regime is mean_reversion (the recorded decision of the 90-bar return >= -50 % rule) with a negative forecast; the coin's mean 10-bar return is taken over the non-overlapping grid of all its windows; thirds are floor(n/3) cases each by |forecast| (unweighted unusual fall); fewer than 30 cases is reported as not observable.
- Size: unusual move +0.48 % per case over 10 bars, 0.030 of the coin's usual move (16.53 %); normal drift in its direction -1.38 %, total -0.90 %; 2430 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse_1d`
Measure: `measure.py`
