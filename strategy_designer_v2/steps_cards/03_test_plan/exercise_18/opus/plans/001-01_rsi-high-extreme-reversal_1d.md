---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a high extreme -> adapted: graded RSI excess above 50, amplified toward extremes by signed_power; "after" made "while".
- Comparison: extreme readings judged against neutral readings -> kept: forward returns after the largest short positions are compared with those after near-zero positions.
- Outcome: price falls back over the following bars -> kept: the 5-bar forward return of the coin after high readings, expected negative.
- Verdict transfer: yes: a short position sized by how far RSI sits above 50 profits exactly when high RSI readings are followed by retracement, and loses when they are followed by continuation.
Forecast: Use the 14-bar Wilder RSI, the usual setting on daily bars. Take 50 − RSI, which is negative when RSI is above 50. Standardise it against its own past 60 values, so a typical reading is about 10. Square its size with signed_power (exponent 2, pivot 10): mild readings shrink toward 0 and extreme readings grow, keeping the sign. Then clip at a maximum of 0, so only the high-RSI side the idea names is kept. The forecast is 0 whenever RSI is at or below 50. Above 50 it is negative and continuous, and the short grows quickly as RSI moves toward a high extreme, up to the −20 cap (200% short).
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after "extreme" bars minus its 5-bar forward return after "neutral" bars. Extreme bars are the 20% most negative forecasts. Neutral bars are those with forecast exactly 0, where RSI is at or below 50. Returns are pooled across coins and windows, using only non-overlapping 5-bar returns. Subtracting the neutral return removes the coin's own drift, which is the benchmark of simply holding the coin.
- Supporting check: Run the same extreme-minus-neutral difference separately for each coin. The sign should agree on at least 2 of the 3 coins.
- Confirm: The difference is negative with t ≤ −2, and the supporting check agrees on at least 2 of 3 coins.
- Reject: The difference is positive with t ≥ +2, meaning price keeps rising after high RSI.
- Inconclusive: Any t between −2 and +2, or a main result whose sign holds on fewer than 2 coins. Also inconclusive if there are fewer than 30 non-overlapping extreme cases or fewer than 30 neutral cases in the pool.
