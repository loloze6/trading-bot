---
plan: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
idea: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar excess return (vs coin's all-window mean daily return) on bars with forecast >= 5: 0.00293698; ordinary t of the mean (n=2552): 2.44495 (threshold: confirm: mean > 0 with ordinary t >= 2 and high-vol minus low-vol > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean excess high-vol half minus low-vol half (split at pooled median 60-day std): 0.00914909, passed: True
- Counts: cases with forecast >= 5: 2552, high-volatility half cases: 634, low-volatility half cases: 635
- Decided by: Mean excess > 0 with t >= 2 and high-vol minus low-vol difference > 0 (confirm rule).
- Reading: Situation bars are those where the recorded vol-scaled 1-day return (price return where unrecorded) is below 0, long side; the 60-day std is recomputed within each window (60 returns, min 60, missing earlier), the high-volatility half is std > pooled median of cases with a std and the low half is std <= median, and the plan's minimum counts not reached give 'not observable'.
- Size: unusual move +0.19 % (t 0.79, the cases of one day together: 925 days) per case over 1 bars, 0.024 of the coin's usual move (5.55 %); normal drift in its direction +0.17 %, total +0.36 %; 3285 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003274 on the check folds against +0.002937 on every fold
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d.md`
Record: `steps_cards/04_backtest/night_run/unseen_coins/backtests/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d`
Measure: `measure.py`
