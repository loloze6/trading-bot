---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: not observable
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 (minus holding baseline): -0.0675101; t of the mean: -1.84161 (threshold: confirm: negative with t <= -2 and negative in >= 2 of 3 coins; reject: positive with t >= +2; min 30 non-overlapping cases)
- Supporting check: number of coins (of 3) with negative mean excess return: 1, passed: False
- Counts: non-overlapping extreme cases pooled: 3, coins with negative excess return: 1, coins in record: 1
- Decided by: Only 3 non-overlapping extreme cases pooled, below the plan's minimum of 30.
- Reading: Holding baseline is the mean forward 5-bar return over all bars of the coin's window with a valid forward return (overlapping), extreme cases are the non-overlapping grid bars (positions 0,5,10,... of each window) with forecast <= -10, t is the ordinary t of the pooled mean, and a coin absent from the record or without cases counts as not negative among the plan's 3 coins.
Plan: `steps_cards/05_verification/exercise_11/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/05_verification/exercise_11/records/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
