---
plan: 069-02.d3_below-high-up-day-two-day-fade_1d
idea: 069-02.d3_below-high-up-day-two-day-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction excess 2-bar return of the cases: 0.00251686; t of the mean, cases of one day taken together: 1.48813 (threshold: above 0 with t >= 2 (confirm); below 0 with t <= -2 (reject))
- Supporting check: slope of short excess return on |forecast|: 0.000656051, passed: True
- Counts: cases: 4528, distinct days: 1594
- Decided by: t lies between -2 and 2, so the plan calls it inconclusive.
- Reading: Up day = close above the previous close inside the window, with window-first bars left out of the situation check; depth below the high = raw depth < 0 (else close below the 20-bar max high); a bet is a short-side rise in |forecast| of >= 2 points from its lowest level since the last bet (reset at flat or side change); one case per 2-bar grid cell (the first bet in the cell), return from that bet's close; drift = mean of the coin's non-overlapping 2-bar grid returns over all windows; day-clustered t with D/(D-1) correction; the plan's minimum counts lead to 'not observable' when not reached.
- Size: unusual move +0.25 % (t 1.49, the cases of one day together: 1594 days) per case over 2 bars, 0.037 of the coin's usual move (6.58 %); normal drift in its direction -0.24 %, total +0.02 %; 4528 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/069-02.d3_below-high-up-day-two-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02.d3_below-high-up-day-two-day-fade_1d`
Measure: `measure.py`
