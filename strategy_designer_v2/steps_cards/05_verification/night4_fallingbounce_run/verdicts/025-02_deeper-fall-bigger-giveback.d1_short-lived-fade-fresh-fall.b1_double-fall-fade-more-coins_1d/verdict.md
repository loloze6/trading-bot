---
plan: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins_1d
idea: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 2-bar return in excess of the coin's drift per short bet: 0.00511341; t of the mean: 3.33504 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: excess return of larger-|forecast| half minus smaller half: -0.00474604, passed: False
- Counts: cases: 1883, larger half cases: 942, smaller half cases: 941
- Decided by: The main t is >= 2 but the supporting check fails (difference not above 0).
- Reading: The 90- and 30-bar price changes are recomputed from closes inside each window where 90/30 prior bars exist, falling back to the recorded regime elsewhere, and the rise is the bounce raw value > 0; a case is a short bet (forecast's short size rising >= 2 points above its lowest short level since the last bet, from 0 after flat), taking the first bet bar of each non-overlapping 2-bar grid cell with its full 2-bar return inside the window; drift is the mean of each coin's non-overlapping 2-bar returns over all its windows; the supporting split puts |forecast| >= median in the larger half and < median in the smaller half.
- Size: unusual move +0.51 % per case over 2 bars, 0.063 of the coin's usual move (7.48 %); normal drift in its direction -0.29 %, total +0.22 %; 1883 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins_1d`
Measure: `measure.py`
