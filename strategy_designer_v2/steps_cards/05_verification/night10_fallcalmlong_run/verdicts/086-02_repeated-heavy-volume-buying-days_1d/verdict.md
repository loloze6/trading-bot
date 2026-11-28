---
plan: 086-02_repeated-heavy-volume-buying-days_1d
idea: 086-02_repeated-heavy-volume-buying-days
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 5-day return of forecast>0 grid bars: -0.0100191; t of the weighted mean, cases of one day grouped: -0.942332 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2; fewer than 30 cases inconclusive)
- Supporting check: mean excess 5-day return, upper minus lower half at median forecast: 0.0114067, passed: True
- Counts: cases: 118, days: 75, active bars: 595
- Decided by: The t of the weighted mean excess return lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -0.942 (below 1), 118 cases (30 needed).
- Reading: Heavy volume is the mean of bars t-2..t over the mean of bars t-22..t-3 recomputed from the window's volumes (the recorded regime where fewer bars exist), the rise is close[t]/close[t-3]-1>0, and the falling-calm profile (60-bar fall, 365-bar volatility percentile) is read from the regime being 'trending' since it cannot be rebuilt from the recorded bars; the median split puts cases above the median forecast in the upper half and the rest in the lower half, halves compared unweighted; the t is the forecast-weighted mean over its day-clustered standard error.
- Size: unusual move -0.03 % (t -0.05, the cases of one day together: 231 days) per case over 5 bars, -0.002 of the coin's usual move (11.31 %); normal drift in its direction +0.61 %, total +0.58 %; 285 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.942 (below 1), 118 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/086-02_repeated-heavy-volume-buying-days_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-02_repeated-heavy-volume-buying-days_1d`
Measure: `measure.py`
