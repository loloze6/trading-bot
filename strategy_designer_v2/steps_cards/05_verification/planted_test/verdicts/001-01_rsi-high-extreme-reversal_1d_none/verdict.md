---
plan: 001-01_rsi-high-extreme-reversal_1d_none
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 (minus same coin/window mean forward 5-bar return), non-overlapping: -0.0119429; t of the mean: -1.32313 (threshold: confirm if excess < 0 with t <= -2 and negative in >= 2 coins; reject if excess > 0 with t >= +2; inconclusive if -2 < t < +2 or fewer than 30 non-overlapping extreme cases)
- Supporting check: number of coins with negative mean excess forward return (need >= 2): 2, passed: True
- Counts: non-overlapping extreme cases pooled: 60, coins with negative excess: 2, coins in record: 2, extreme cases BTCUSD: 32, extreme cases ETHUSD: 28
- Decided by: The t-statistic lies strictly between -2 and +2, meeting the inconclusive rule.
- Reading: The holding baseline is the mean forward 5-bar return over every bar of the coin/window that has one, extreme cases are grid bars (positions 0,5,10,... per window) with forecast <= -10, and with only the coins present in the record the rule 'negative in at least 2 of the 3 coins' needs at least 2 of those coins negative, with a coin that has no cases not counting as negative.
Plan: `steps_cards/05_verification/planted_test/plans/001-01_rsi-high-extreme-reversal_1d_none.md`
Record: `steps_cards/05_verification/planted_test/records/001-01_rsi-high-extreme-reversal_1d_none`
Measure: `measure.py`
