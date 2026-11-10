---
idea: 001-04_rsi-low-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a low extreme -> adapted: graded depth of RSI(14) below 50, and "after" becomes "while"; squaring keeps mild readings near zero.
- Comparison: falls after neutral readings -> adapted: neutral RSI gives a near-zero position, so the comparison is between forward returns after large and near-zero positions.
- Outcome: price keeps falling over the following bars -> kept: a short position gains when price falls.
- Verdict transfer: yes: the short side grows with RSI depth and stays flat near neutral, so the test's result is the idea's result.
Forecast: RSI(14) pullback with long_only on gives (50 - RSI) when RSI is below 50 and 0 otherwise. It is standardised against its own past 60 values, so a typical reading is 10, capped at 20. A signed power with exponent 2 and pivot 10 shrinks mild readings toward 0 and enlarges deep ones. The result is negated, so the forecast is zero when RSI is 50 or above and increasingly negative (a larger short) the further RSI sits below 50. It is never positive. The combined forecast is clipped at -20.
Config: 001-04_rsi-low-extreme-continuation_1h_config.json
Criterion:
- Horizon: 12 bars
- Main measure: The coin's 12-bar forward return after extreme bars (forecast <= -10) minus its 12-bar forward return after neutral bars (|forecast| < 1, RSI near or above 50), measured before costs. Overlapping returns are counted once by keeping only bars at least 12 bars apart.
- Supporting check: The strategy's before-cost return in each window, compared with holding the coin over the same window, adjusted for the strategy's average short exposure. It should be positive in most windows.
- Confirm: The difference is negative with t <= -2 on the non-overlapping samples in at least 2 of the 3 coins, and none of the coins has a positive difference with t >= 2.
- Reject: The difference is >= 0, or its t is above -1, in at least 2 of the 3 coins. A significantly positive difference (reversal) also rejects the idea.
- Inconclusive: Any result between those, or any coin with fewer than 30 non-overlapping extreme cases or fewer than 30 neutral cases across its 6 windows. Such a coin does not count toward either verdict.
