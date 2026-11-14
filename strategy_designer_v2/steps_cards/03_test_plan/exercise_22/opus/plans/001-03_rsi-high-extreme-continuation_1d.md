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
- Situation: RSI reaches a high extreme -> adapted: graded upside RSI distance from 50, sharply damped away from the extreme.
- Comparison: versus neutral readings -> adapted: neutral RSI gives a position near zero, so held bars are compared with near-flat bars.
- Outcome: price keeps rising over the following bars -> adapted: "after X" becomes "while X", with no holding period.
- Verdict transfer: yes: a long position that grows with RSI extremity profits only if high readings come before further rises beyond those after neutral readings.
Forecast: RSI(14) on daily closes, read as RSI minus 50 (RSIPullback with its sign flipped). It is standardised against its own last 60 values (target 10), and its negative side is clipped to 0, so the position is long only when RSI is above 50. A signed power with exponent 3 and pivot 20, the strongest graded dead zone allowed, keeps the position near zero at neutral readings. An average reading gives about 2.5. The forecast reaches 20 (200% long) only when RSI's distance above 50 is twice its recent average or more. It is never negative, and it is zero whenever RSI is at or below 50.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after bars with forecast >= 10 (high-extreme cases), minus its 5-bar forward return after bars with forecast < 2 (neutral or below-50 cases). Pooled over coins and windows, with overlapping returns counted once (non-overlapping blocks or Newey-West t, lag 4). The difference to holding the coin is built in, because both sides use the coin's own return.
- Supporting check: Before costs, the strategy's return per unit of average exposure should exceed the buy-and-hold return over the same windows, in at least 2 of the 3 coins.
- Confirm: Mean difference > 0 with t >= 2.
- Reject: Mean difference < 0 with t <= -2, which means high readings are followed by weaker moves than neutral ones.
- Inconclusive: Any t between -2 and 2, or fewer than 20 non-overlapping high-extreme cases pooled across coins and windows.
