---
plan: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d
idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move (short direction), next 1 bar, on bars with forecast <= -2: 0.00269979; ordinary t of the mean: 3.26826 (threshold: confirm: mean > 0 with t >= 2 and larger-|forecast| half ahead; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger |forecast| half minus smaller half: -0.00203684, passed: False
- Counts: cases: 3535, larger half: 1767, smaller half: 1768
- Decided by: t >= 2 with a positive mean, but the larger half is not ahead of the smaller half.
- Reading: The 90-bar return is recomputed from closes where 90 prior bars exist in the window and taken from the recorded regime otherwise, the rise is the raw bounce value > 0, and the median split puts cases with |forecast| strictly above the median in the larger half and the rest in the smaller half.
- Size: unusual move +0.33 % per case over 1 bars, 0.059 of the coin's usual move (5.31 %); normal drift in its direction -0.14 %, total +0.19 %; 3119 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d`
Measure: `measure.py`
