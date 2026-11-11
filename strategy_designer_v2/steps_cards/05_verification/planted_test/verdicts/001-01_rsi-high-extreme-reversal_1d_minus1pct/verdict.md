---
plan: 001-01_rsi-high-extreme-reversal_1d_minus1pct
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 (non-overlapping), vs coin/window holding mean: 0.00564968; t of the mean: 0.585901 (threshold: confirm: excess < 0 with t <= -2 and negative in >= 2 coins; reject: excess > 0 with t >= +2; else or < 30 cases inconclusive)
- Supporting check: number of coins with negative mean excess return: 0, passed: False
- Counts: non-overlapping extreme cases pooled: 60, coins with negative excess: 0, coins in record: 2
- Decided by: The t-statistic lies strictly between -2 and +2, meeting the inconclusive rule.
- Reading: Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10 and a defined 5-bar forward return, the holding baseline is the mean forward 5-bar return over all bars of that coin and window, the per-coin sign is that of the coin's mean excess over its cases, and since only the coins present can be counted, 'at least 2 of the 3 coins' is applied as at least 2 coins with negative excess among those in the record.
Plan: `steps_cards/05_verification/planted_test/plans/001-01_rsi-high-extreme-reversal_1d_minus1pct.md`
Record: `steps_cards/05_verification/planted_test/records/001-01_rsi-high-extreme-reversal_1d_minus1pct`
Measure: `measure.py`
