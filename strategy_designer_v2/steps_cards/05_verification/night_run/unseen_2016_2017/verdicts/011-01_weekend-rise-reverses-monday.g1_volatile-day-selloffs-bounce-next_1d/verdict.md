---
plan: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
idea: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar excess return (vs coin's all-window mean daily return) on bars with forecast >= 5: 0.00530775; ordinary t of the mean (n=302): 1.36677 (threshold: confirm: mean > 0 with ordinary t >= 2 and high-vol minus low-vol > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean excess high-vol half minus low-vol half (split at pooled median 60-day std): 0.019687, passed: True
- Counts: cases with forecast >= 5: 302, high-volatility half cases: 77, low-volatility half cases: 77
- Decided by: t lies between -2 and 2 (inconclusive rule).
- Reading: Situation bars are those where the recorded vol-scaled 1-day return (price return where unrecorded) is below 0, long side; the 60-day std is recomputed within each window (60 returns, min 60, missing earlier), the high-volatility half is std > pooled median of cases with a std and the low half is std <= median, and the plan's minimum counts not reached give 'not observable'.
- Size: unusual move +0.10 % (t 0.21, the cases of one day together: 227 days) per case over 1 bars, 0.013 of the coin's usual move (7.81 %); normal drift in its direction +0.96 %, total +1.06 %; 386 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d.md`
Record: `steps_cards/04_backtest/night_run/unseen_2016_2017/backtests/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d`
Measure: `measure.py`
