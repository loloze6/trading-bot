---
plan: 001-01_rsi-high-extreme-reversal_1d_plus1pct
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: confirmed
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 vs holding baseline: -0.028758; t of the mean: -3.33043 (threshold: confirm if pooled excess < 0 with t <= -2 and negative in >= 2 of 3 coins; reject if pooled excess > 0 with t >= +2; inconclusive otherwise or if < 30 cases)
- Supporting check: number of coins with negative mean excess forward return (need >= 2): 2, passed: True
- Counts: non-overlapping extreme cases pooled: 60, coins with negative excess: 2, coins present: 2
- Decided by: The pooled excess forward return is negative with t <= -2 and negative in at least 2 coins, meeting the confirm rule.
- Reading: The baseline is the mean forward 5-bar return over all bars of each coin and window, the extreme cases are grid bars at positions 0,5,10,... with forecast <= -10, the t is the ordinary t of the pooled mean, and 'at least 2 of the 3 coins' is applied as at least 2 negative coins among the coins present, with a negative t <= -2 lacking that coin support treated as inconclusive.
Plan: `steps_cards/05_verification/planted_test/plans/001-01_rsi-high-extreme-reversal_1d_plus1pct.md`
Record: `steps_cards/05_verification/planted_test/records/001-01_rsi-high-extreme-reversal_1d_plus1pct`
Measure: `measure.py`
