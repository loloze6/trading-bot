---
plan: 061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade_1d
idea: 061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 10-bar move per case (return minus normal drift, sign flipped): 0.029998; t of the mean, same-day cases pooled: 3.15752 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: larger-|forecast| half minus smaller half, mean short-side unusual move: -4.15174e-05, passed: False
- Counts: cases: 225, distinct days: 176
- Decided by: t >= 2 but the supporting check failed, which the plan calls inconclusive.
- Reading: Situation recomputed from prices (close location, 1-bar return over 20-bar std of daily returns, 10% tolerance on the upper gain bound) with the profile taken as regime not 'chop'; a bet is a rise of |forecast| on the short side of at least 2 points from its lowest level since the last bet, the first bet of each 10-bar grid cell is the case; the split puts cases with |forecast| >= median in the larger half and < median in the smaller; same-day cases pooled by summing deviations per day.
- Size: unusual move +3.00 % (t 3.16, the cases of one day together: 176 days) per case over 10 bars, 0.182 of the coin's usual move (15.92 %); normal drift in its direction -1.31 %, total +1.69 %; 225 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade_1d`
Measure: `measure.py`
