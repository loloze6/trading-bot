---
plan: 021-04_thin-cloud-downward-breakdown_1d
idea: 021-04_thin-cloud-downward-breakdown
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 26-bar unusual move in the short direction: -0.00188273; ordinary t of the mean: -0.101087 (threshold: confirm: positive with t >= 2; reject: t <= -2)
- Supporting check: thin-minus-thick unusual move, Welch t: -0.360632, passed: False
- Counts: cases: 198, thin-cloud half: 99, thick-cloud half: 99
- Decided by: inconclusive rule: the mean unusual move's t is between -2 and 2 (neither confirm nor reject)
- Reading: situation recomputed from in-window prices (cloud = 9/26/52 spans displaced 26; below the cloud with the first close below after the last close above at most 26 bars back), checked on the 387 of 2171 active bars where the in-window history makes it determinable; a case is the first short bet (|forecast| rising >= 2 from its lowest since the last bet) in each 26-bar cell counted from each window's first row, and cases are split into thin (|forecast| above the median) and thick (at or below the median).
- Size: unusual move -0.19 % per case over 26 bars, -0.020 of the coin's usual move (25.48 %); normal drift in its direction -4.39 %, total -4.58 %; 198 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-04_thin-cloud-downward-breakdown_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-04_thin-cloud-downward-breakdown_1d`
Measure: `measure.py`
