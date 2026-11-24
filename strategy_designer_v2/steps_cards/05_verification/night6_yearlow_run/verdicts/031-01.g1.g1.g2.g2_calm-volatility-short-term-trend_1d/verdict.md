---
plan: 031-01.g1.g1.g2.g2_calm-volatility-short-term-trend_1d
idea: 031-01.g1.g1.g2.g2_calm-volatility-short-term-trend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: calm-regime slope of demeaned 2-day forward return on the forecast: 0.000325119; OLS slope t: 3.52507 (threshold: confirm if t >= 2 (with the check passing and >= 300 calm cases); reject if t <= -2)
- Supporting check: calm minus non-calm slope difference (t >= 2, positive): 0.000178152, passed: False
- Counts: calm grid cases: 4872, non-calm grid cases: 3323
- Decided by: Inconclusive rule: neither the confirm nor the reject rule is met (calm slope |t| < 2, or a positive calm slope whose difference from the non-calm slope has t between -2 and 2).
- Reading: Calm bars are those whose recorded regime is 'trending' (the detector's vr<1 decision, its component not being recorded) and the expected side is the sign of the raw 14-day return; the grid is positions 0,2,4,... of each window, the coin's mean 2-day return is the mean over all its windows' grid returns, slopes are pooled OLS with intercept over all coins, the non-calm standardised 14-day return is rebuilt from in-window closes (missing early bars dropped), the slope-difference t is (b1-b2)/sqrt(se1^2+se2^2), and the plan's 'fewer than 300 cases' minimums are reported as not observable.
- Size: unusual move +0.35 % (t 2.15, the cases of one day together: 1383 days) per case over 2 bars, 0.053 of the coin's usual move (6.58 %); normal drift in its direction -0.01 %, total +0.35 %; 2811 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g2_calm-volatility-short-term-trend_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g2.g2_calm-volatility-short-term-trend_1d`
Measure: `measure.py`
