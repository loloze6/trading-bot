---
plan: 017-02_presettle-rise-after-downtrend_1h
idea: 017-02_presettle-rise-after-downtrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of excess 2-bar return on forecast, pooled pre-settlement episodes: 1.29763; OLS t of slope: 1.29763 (threshold: confirm: slope t >= 2 and mean excess t >= 2; reject: slope t <= -2 or mean excess t <= -2)
- Supporting check: mean excess 2-bar return over cases (t >= 2 and > 0); value is its t: 0.356876, passed: False
- Counts: cases pooled: 25569, cases BTCUSD: 4178, cases ETHUSD: 4199, cases LTCUSD: 4321, cases XMRUSD: 4063, cases XRPUSD: 4593, cases ZECUSD: 4215
- Decided by: Neither the confirm rule (both t >= 2) nor the reject rule (either t <= -2) is met.
- Reading: Situation = bars whose close is 1 or 2 hours before a 00/08/16 UTC settlement (bars stamped 05/06, 13/14, 21/22, holding through 06/07, 14/15, 22/23) with a negative 72-bar price change, long side; a case is such a bar with HoursToSettlement = 2 (stamped 05, 13, 21), regime trending and forecast > 0; the coin's mean 2-bar return uses positions 0,2,4,... of every window pooled; the per-coin minimum applies to every coin in the record; unmet minimums give 'not observable'.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-02_presettle-rise-after-downtrend_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-02_presettle-rise-after-downtrend_1h`
Measure: `measure.py`
