---
plan: 013-04_heavy-volume-below-high-breakout_1d
idea: 013-04_heavy-volume-below-high-breakout
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Welch t of mean 30-bar excess return, top half of forecast minus bottom half (breakout events): 0.273124; Welch t: 1.98702 (threshold: confirm if Welch t >= 2.0 with top minus bottom positive; reject if Welch t <= -2.0 with top minus bottom negative; at least 30 events)
- Supporting check: none
- Counts: de-duplicated breakout events: 50, top half events: 25, bottom half events: 25
- Decided by: Welch t = 1.99 lies between -2.0 and 2.0 over 50 events (inconclusive rule).
- Reading: The breakout situation is taken as regime 'trending' (the detector's recorded close-above-prior-365-bar-high decision) together with close above every earlier high in the window, since 365 bars of history are not in the record; events are chosen greedily from each window's first trending bar, the coin mean 30-bar return uses the non-overlapping grid 0, 30, 60, ... of each window pooled over all windows, and the halves are the lower and upper floor(n/2) events after sorting all events by forecast (middle one dropped when n is odd).
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-04_heavy-volume-below-high-breakout_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-04_heavy-volume-below-high-breakout_1d`
Measure: `measure.py`
