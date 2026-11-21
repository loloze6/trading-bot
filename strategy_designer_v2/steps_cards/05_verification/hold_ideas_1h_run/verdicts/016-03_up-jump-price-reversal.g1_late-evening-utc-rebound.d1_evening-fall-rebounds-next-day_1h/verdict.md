---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-24-bar excess return on fall24 post_pipeline_value at 20:00 UTC bars: 0.000150032; OLS slope t: 2.69808 (threshold: slope t >= +2 confirms (with supporting check); t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean next-24-bar excess return on 20:00 bars with forecast > 0: 0.000520844, passed: True
- Counts: bars at 20:00 with forecast > 0: 8538, bars at 20:00 in regression: 17196
- Decided by: The slope's t is +2 or more and the mean excess return on forecast > 0 bars is positive.
- Reading: The 20:00 UTC bar is the bar stamped 19:00; the coin's mean 24-bar return is the mean of the non-overlapping 24-bar returns (positions 0, 24, 48, ... of each window) pooled over all its windows; the slope's t is the ordinary OLS t with an intercept; the 300-bar minimum counts 20:00 bars with forecast > 0 and a next-24-bar return inside the window, and a shortfall is reported as not observable.
- Size: unusual move +0.09 % per case over 24 bars, 0.019 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.23 %; 7307 cases
Plan: `steps_cards/03_test_plan/hold_ideas_1h_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h.md`
Record: `steps_cards/04_backtest/hold_ideas_1h_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h`
Measure: `measure.py`
