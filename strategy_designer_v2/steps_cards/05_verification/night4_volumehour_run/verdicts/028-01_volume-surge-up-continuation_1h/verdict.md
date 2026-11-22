---
plan: 028-01_volume-surge-up-continuation_1h
idea: 028-01_volume-surge-up-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 6-bar return over long-bet cases: 3.55825e-05; t of the mean: 0.143296 (threshold: t >= 2 confirms, t <= -2 rejects, with at least 100 cases)
- Supporting check: OLS slope of excess return on volume ratio (cases at bar >= 720): 8.21829e-05, passed: True
- Counts: cases: 8827, cases at or after bar 720: 6539
- Decided by: Inconclusive rule: the main t lies between -2 and 2.
- Reading: A bet is a forecast rise of at least 2 from its lowest positive level since the last bet (reset to 0 when flat), each 6-bar grid cell counts once at its first bet, the reject rule is checked before the confirm rule, and fewer than 100 cases is reported as not observable per the workflow's minimum-count rule.
- Size: unusual move +0.00 % per case over 6 bars, 0.000 of the coin's usual move (1.98 %); normal drift in its direction +0.03 %, total +0.04 %; 8827 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-01_volume-surge-up-continuation_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-01_volume-surge-up-continuation_1h`
Measure: `measure.py`
