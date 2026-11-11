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
- Situation: RSI at a high extreme -> adapted: graded as how far the 14-bar RSI sits above 50, damped near neutral, with "after X" read as "while X".
- Comparison: returns after neutral RSI readings -> kept: neutral readings give a forecast near zero, and the criterion compares them with the largest positions.
- Outcome: price keeps rising over the following bars -> kept: measured as the coin's forward return over a fixed horizon, long side.
- Verdict transfer: yes: the forecast is large only when RSI is high, so returns after the largest positions versus neutral bars answer the idea directly.
Forecast: The forecast starts from the 14-bar Wilder RSI on daily bars, the standard setting. It takes the contrarian RSI score (50 − RSI), standardises it against its previous 60 values, and flips its sign, so it is positive when RSI is above 50. It then removes the negative side, so it is zero whenever RSI is at or below 50. Finally a signed power with exponent 3 and pivot 10 applies the strongest dead zone the guide allows. Moderate readings stay close to zero and the forecast grows steeply as RSI reaches a high extreme. It is long only and never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's forward 5-bar return after bars in the top decile of the forecast, minus its forward 5-bar return after neutral bars (forecast below 1). Cases are pooled over coins and windows, and only non-overlapping 5-bar returns are counted. Subtracting the neutral baseline removes the market's own drift, so the result is judged against simply holding the coin, before costs.
- Supporting check: The same difference computed per coin should have the same sign on at least 2 of the 3 coins.
- Confirm: The difference is positive with t ≥ 2 on non-overlapping returns, and the supporting check holds.
- Reject: The difference is negative with t ≤ −2, meaning returns after high RSI are clearly lower than after neutral readings.
- Inconclusive: Any t between −2 and 2, or a confirm-level t that fails the supporting check, is inconclusive. Fewer than 30 non-overlapping top-decile cases, or fewer than 30 non-overlapping neutral cases, is also inconclusive.
