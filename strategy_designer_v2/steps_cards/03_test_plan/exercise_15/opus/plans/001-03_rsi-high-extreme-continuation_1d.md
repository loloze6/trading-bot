---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme -> adapted: "extreme" becomes graded; the long position grows smoothly with RSI above 50 and is amplified near the top.
- Comparison: versus neutral RSI readings -> adapted: neutral readings near 50 give a position near zero, so extremes are judged against them by the size of the position.
- Outcome: price keeps rising over the following bars -> adapted: "after the extreme" becomes "while RSI is high", and no holding period is set.
- Verdict transfer: yes: RSI is measured as the idea states, and the long side is sized by how extreme it is, so both a confirmation and a rejection carry over to the idea.
Forecast: Use RSI(14) on daily closes. The `RSIPullbackComponent` output, (50 − RSI) × sf, is first standardised against its own previous 60 values. It is then negated, so it becomes positive when RSI is above 50. It is clipped at 0, so the forecast is long-only on the high side. Finally `signed_power` with exponent 2 is applied. The result is near 0 when RSI is near 50 and zero when RSI is at or below 50. It grows quadratically as RSI rises, so the largest long positions come at the highest readings. It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's mean 5-bar forward return after bars with RSI(14) ≥ 70 (the largest positions), minus its mean 5-bar forward return after bars with RSI between 40 and 60. Pool BTC, ETH and BNB over all windows. Use non-overlapping 5-bar returns only, so each period counts once. Comparing against neutral bars means the coin's own drift is not credited to the idea.
- Supporting check: Compare the before-cost strategy return with holding the coin at the strategy's own average allocation over the same bars. The strategy must beat it, meaning the gains come from sizing up at high RSI and not from being long a rising market.
- Confirm: The difference in the main measure is above 0 with a t-statistic of at least 2 on the non-overlapping returns. It is also positive for at least 2 of the 3 coins, and the supporting check is positive.
- Reject: The difference in the main measure is 0 or below. Or it is negative for at least 2 of the 3 coins. Either result rejects continuation after high RSI.
- Inconclusive: The difference is positive but its t-statistic is below 2, or the coins disagree in a way the confirm and reject rules do not cover. The test is also inconclusive with fewer than 30 non-overlapping extreme (RSI ≥ 70) cases or fewer than 30 neutral cases in the pool.
