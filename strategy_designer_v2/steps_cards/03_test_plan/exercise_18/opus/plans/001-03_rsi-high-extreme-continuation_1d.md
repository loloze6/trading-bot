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
- Situation: RSI at a high extreme -> adapted: graded RSI excess above 50, squared so that extreme readings dominate the position.
- Comparison: continuation versus after neutral readings -> kept: neutral RSI gives a forecast near zero, so large positions are compared against small or none.
- Outcome: price keeps rising over the following bars -> adapted: "after" becomes "while"; a long position is held while RSI stays high, scored over a fixed forward horizon.
- Verdict transfer: yes: a graded long position that grows with RSI strength earns above buy-and-hold only if high RSI readings come before further rises.
Forecast: Take the 14-bar Wilder RSI on daily bars as RSIPullbackComponent (50 - RSI), standardised over its past 60 values, then negated so it is positive when RSI is above 50. Clip it at 0, because the idea is only about high extremes, so the forecast is long-only. Then apply signed_power with exponent 2 and pivot 10, so readings near neutral shrink toward 0 and extreme readings grow faster (a standardised 20 becomes 40, and the final forecast is clipped at 20). The forecast is 0 when RSI is at or below 50 and grows smoothly as RSI rises above 50. It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Regress the coin's forward 5-bar return, minus that coin's mean 5-bar return in the same window (the buy-and-hold drift), on the forecast at the bar's close. Pool all coins and windows, before costs, and use Newey-West errors with lag 4 so that overlapping returns count once.
- Supporting check: Compare the mean forward 5-bar excess return after the top 20% of positive forecasts with the mean after bars where the forecast is 0 or in the bottom 20%. The sign of the difference must agree in at least 2 of the 3 coins.
- Confirm: The slope is positive with t ≥ 2, and the supporting difference is positive in at least 2 of the 3 coins.
- Reject: The slope is negative with t ≤ -2, meaning high RSI comes before reversal, and the supporting difference is negative in at least 2 of the 3 coins.
- Inconclusive: Any result with |t| < 2, or a significant slope whose supporting check fails the coin agreement. The test also requires at least 40 non-overlapping 5-bar periods with forecast ≥ 10 (extreme readings) in the pooled data; fewer than that counts as inconclusive.
