---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: not observable
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10: -0.0675101; t of the mean: -1.84161 (threshold: confirm if negative with t <= -2 (and negative in >= 2 of 3 coins); reject if positive with t >= +2)
- Supporting check: number of coins with negative excess return: 1, passed: False
- Counts: non-overlapping extreme cases pooled: 3, coins with extreme cases: 1
- Decided by: Only 3 non-overlapping extreme cases pooled, below the plan's minimum of 30.
- Reading: Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10 and a defined 5-bar forward return, the baseline is the mean 5-bar forward return over all bars of that coin and window with a defined forward return, t is the ordinary t of the pooled mean, and the 'at least 2 of the 3 coins' rule is applied literally to the coins present, so with fewer than 2 negative coins it cannot be met.
Plan: `steps_cards/05_verification/exercise_11/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/05_verification/exercise_11/records/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
