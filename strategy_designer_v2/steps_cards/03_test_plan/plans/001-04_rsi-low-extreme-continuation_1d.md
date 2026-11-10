---
idea: 001-04_rsi-low-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a low extreme -> adapted: the RSI threshold is made graded (depth of RSI below 50, squared to stress extremes), and "after X" becomes "while X".
- Comparison: returns after low extremes vs after neutral readings -> kept: the criterion compares forward returns after extreme bars with those after neutral bars.
- Outcome: price keeps falling over the next bars -> kept: a short position that pays when price falls.
- Verdict transfer: yes: the test measures whether bars with low-extreme RSI are followed by lower returns than neutral bars, which is the idea's claim.
Forecast: RSI(14) on daily closes. The component outputs (50 - RSI) x 0.4 when RSI is below 50, and 0 otherwise. Its value is standardised against its own past 60 values, negated so the position is short, then raised to the power 2 (sign kept, pivot 10). The forecast is 0 whenever RSI is 50 or above. It is negative when RSI is below 50: small near 50 and growing quadratically as RSI falls toward a low extreme, so the largest shorts come at the deepest oversold readings. It is never positive.
Config: 001-04_rsi-low-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after extreme bars (raw component >= 8, i.e. RSI <= 30) minus its 5-bar forward return after neutral bars (RSI between 40 and 60, recomputed from the recorded closes). Pooled over coins and windows, using non-overlapping 5-bar returns. Both groups share the same market drift, so the coin's own rise is not credited to the idea.
- Supporting check: Per coin, the strategy's cumulative return before costs minus the return of holding a short position of the same average size on every bar, using the same per-window drift.
- Confirm: Pooled extreme-minus-neutral 5-bar return is below 0 with t <= -2 on the non-overlapping cases, and is negative in at least 2 of the 3 coins.
- Reject: Pooled extreme-minus-neutral 5-bar return is >= 0, or it is positive with t >= 2 (reversal instead of continuation).
- Inconclusive: A negative difference with t between -2 and 0, or coins that disagree in sign. Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for any coin, is inconclusive whatever the sign.
