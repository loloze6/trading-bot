---
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a high extreme -> adapted: graded RSI above 50, strongly damped so that only extreme readings take a sizeable short; "after" becomes "while".
- Comparison: behaviour after extreme readings versus neutral ones and the usual move -> kept: extreme-bar returns are judged against the coin's average return.
- Outcome: price falls back over the following bars -> kept: short position, 5-bar forward return (the conventional one-week horizon on daily bars).
- Verdict transfer: yes: a short that grows with RSI extremity and pays only if price falls more than usual after high RSI is exactly the claim.
Forecast: The forecast uses the 14-bar Wilder RSI as (50 - RSI), which is negative when RSI is above 50. It is first standardised against its own past 60 values. It is then clipped at 0 from above, so it only ever goes short. Last, it is passed through signed_power with exponent 3 and pivot 20, the strongest graded dead zone the guide allows. The forecast is zero whenever RSI is at or below 50. It is near zero for moderately high RSI: a standardised -10 gives -2.5. It grows smoothly with the cube to -20 at the most extreme readings, and it is never positive.
Config: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the bars of a non-overlapping 5-bar grid in each window where the forecast is -5 or lower (the extreme high-RSI cases). For each case, take the coin's 5-bar forward return and subtract that coin's mean 5-bar return over all its windows. Pool these excess returns over all coins and test their mean with the ordinary t of the mean.
- Supporting check: The mean excess return of these extreme cases is negative in at least 4 of the 6 coins.
- Confirm: The pooled mean excess return is below 0 with t ≤ -2, on at least 30 cases, and the supporting check passes.
- Reject: The pooled mean excess return is above 0 with t ≥ +2, on at least 30 cases. This means price rises more than usual after extreme high RSI.
- Inconclusive: Any of these is inconclusive: - t lies between -2 and +2; - t ≤ -2 but the coin check fails; - there are fewer than 30 cases.
