---
plan: 001-01_rsi-high-extreme-reversal_1d_plus0.1pct
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 (vs coin/window mean 5-bar return): -0.0136589; t of the mean: -1.52158 (threshold: confirm if pooled excess < 0 with t <= -2 and negative in >= 2 of 3 coins; reject if pooled excess > 0 with t >= +2; inconclusive otherwise or if < 30 cases)
- Supporting check: number of coins with negative mean excess return (need >= 2): 2, passed: True
- Counts: non-overlapping extreme cases pooled: 60, coins in record: 2, coins with negative excess: 2
- Decided by: The t-statistic lies strictly between -2 and +2, so the plan rules inconclusive.
- Reading: Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10, the holding baseline is the mean 5-bar forward return over all bars of that coin and window that have one, and with only the coins present in the record the coin rule still requires at least 2 coins negative.
Plan: `steps_cards/05_verification/planted_test/plans/001-01_rsi-high-extreme-reversal_1d_plus0.1pct.md`
Record: `steps_cards/05_verification/planted_test/records/001-01_rsi-high-extreme-reversal_1d_plus0.1pct`
Measure: `measure.py`
