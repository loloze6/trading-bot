---
plan: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar unusual move of long cases (return minus coin drift): 0.00636572; t of the mean: 2.89041 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2; at least 100 cases)
- Supporting check: wider-minus-narrower half mean unusual move (Welch t > 0): 0.00842836, passed: True
- Counts: independent cases: 2556, wider half cases: 1278, narrower half cases: 1278, active bars checked: 3577
- Decided by: Mean unusual move positive with t >= 2 and wider-minus-narrower Welch t > 0: confirm rule met.
- Reading: Situation recomputed per window as close below the min low of the 12 prior bars and close/close[t-180]-1 > 0, agreement taken over active bars where both can be computed inside the window (1057 active bars without 180 bars of in-window history left out); cases are long bets (forecast rise >= 2 points from its low since the last bet), the first per 18-bar grid cell of each window, with an in-window 18-bar return; drift is the coin's mean non-overlapping 18-bar return over all its windows; the wider half is cases with entry forecast above the pooled median, the narrower half those at or below it; fewer than 100 cases gives 'not observable'.
- Size: unusual move +0.64 % per case over 18 bars, 0.059 of the coin's usual move (9.29 %); normal drift in its direction +0.52 %, total +1.16 %; 2556 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h`
Measure: `measure.py`
