---
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a large one-day move while 20-day volatility ranks low against its last 100 days, larger the lower the rank -> adapted: the low-rank condition made graded by (1 − rank), which no component computes multiplied with a signed move.
- Comparison: the day's move against the coin's 60-day mean absolute daily move -> kept: the 1-bar return standardised over 60 bars divides by exactly that mean.
- Outcome: price continues in the move's direction over the next 3 to 7 days -> adapted: the 3–7 day hold dropped; judged at a 5-bar horizon.
- Verdict transfer: no: the config can only gate by a rank threshold (dropping the "lower rank, larger continuation" gradation) or add the rank as a directionless term, so neither result would transfer to the idea as stated.
Reason: The forecast must be the signed day's move, in 60-day mean absolute moves, multiplied by how low the 20-day volatility rank is. The config's weighted mean cannot multiply two strategy components. The detector can only switch the rank on or off, which drops the idea's gradation in rank, and no catalogue component computes that product. All the data is in the coin's own closes.
