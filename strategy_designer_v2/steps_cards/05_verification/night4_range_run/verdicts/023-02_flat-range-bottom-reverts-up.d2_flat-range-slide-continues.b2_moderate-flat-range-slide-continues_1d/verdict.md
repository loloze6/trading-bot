---
plan: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 5-bar move: 0.0109337; t of the mean: 2.31835 (threshold: t >= 2 over at least 30 cases to confirm, t <= -2 to reject)
- Supporting check: larger-|forecast| half minus smaller half mean unusual move: -0.00768064, passed: False
- Counts: cases: 436
- Decided by: A confirming t with a supporting difference at or below 0.
- Reading: Situation recomputed per window from prices (NMR = |close[t]-close[t-30]| over the 30-bar high-low range, midpoint of the 30-bar high and low, veto = 10-day return over the mean absolute 10-day return of the last 60 bars including t), with the 10-day return sign from the recorded ret10 value; active bars whose situation cannot be computed inside the window are left out of the agreement; the coin's mean 5-bar return is over its non-overlapping grid returns of all windows; for the supporting check cases are sorted by absolute forecast and split into two halves of n//2 (the middle case left out when n is odd).
- Size: unusual move +0.71 % per case over 5 bars, 0.066 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +0.12 %; 802 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d`
Measure: `measure.py`
