---
plan: 061-01.b1.b1_small-gain-high-close-fades_1d
idea: 061-01.b1.b1_small-gain-high-close-fades
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per short bet, in the short direction: 0.0250603; t of the mean, cases of one day pooled: 3.44141 (threshold: confirm: mean > 0 with day-pooled t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of smaller-gain half minus larger-gain half (split at median raw gain): -0.00471755, passed: False
- Counts: cases: 140, distinct days: 122
- Decided by: The mean unusual move is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive.
- Reading: Situation checked as close location (close-low)/(high-low) >= 0.8 on the short side only, since the profile's 365-day volatility percentile and 60-bar trend cannot be rebuilt from the recorded windows; a case is the first short bet (forecast falling >= 2 points below its least-short level since the last bet, reset to 0 after a flat or long bar) in each 5-bar grid cell from the window's first row with a full 5-bar return inside the window; the day-pooled t uses per-day sums of deviations with a D/(D-1) correction; the median split puts cases strictly below the median in the smaller-gain half and strictly above it in the larger-gain half, cases at the median and without a raw value left out.
- Size: unusual move +2.51 % (t 3.46, the cases of one day together: 122 days) per case over 5 bars, 0.227 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +1.86 %; 140 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1_small-gain-high-close-fades_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1_small-gain-high-close-fades_1d`
Measure: `measure.py`
