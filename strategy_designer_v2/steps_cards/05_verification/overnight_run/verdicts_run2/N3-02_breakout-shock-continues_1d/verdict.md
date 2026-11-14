---
plan: N3-02_breakout-shock-continues_1d
idea: N3-02_breakout-shock-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return after shock-up new highs (forecast >= 10): 0.0100951; one-sample t: 2.00262 (threshold: confirm: positive with t >= 2; reject: negative with t <= -2)
- Supporting check: new-high mean excess minus inside-range shock mean excess: 0.00737079, passed: True
- Counts: non-overlapping cases pooled across coins: 684, inside-range cases: 1112
- Decided by: Mean excess 5-bar return is positive with t >= 2 and exceeds the inside-range shock mean.
- Reading: New high = close >= max of the current and prior 20 closes inside the window (falling back to regime=='trending' on the first 20 bars), up day = raw shock value (else price return) > 0; the coin mean is over all bars' overlapping 5-bar returns pooled across its windows; signals are merged when less than 5 bars after the last kept case, which keeps its return; the inside-range standardised return is 10 x r / rolling mean |r| (60 bars incl. current, min 20, inside the window), with the same merging; t is the ordinary one-sample t of the pooled mean.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N3-02_breakout-shock-continues_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N3-02_breakout-shock-continues_1d`
Measure: `measure.py`
