---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA is above the 200-day SMA, the coin's following return falls as the spread between the two averages stretches beyond its usual width, so the widest spreads are followed by a pullback.
Consequence: A trader would cut or refuse trend longs when the golden-cross spread is at its most stretched.
Why:
- F3: The response to the forecast is not graded. Forecast bins 0–5, 5–10, 10–15 and 15–20 give 10-bar excess means of −0.0085 (n 212), +0.0023 (n 183), +0.0105 (n 174) and +0.0000 (n 263). By raw spread, the widest sextile (n 277) gives −0.0069, while the bin just below zero gives +0.0078 (n 276) and the two middle positive bins give +0.0028 and +0.0046. Moderate spreads drift up and the most stretched spreads fall back.
- F1: The effect is too small to separate from noise at any horizon: the forecast slope's t is 0.20, 0.37, 0.55 and −0.06 at 5, 10, 20 and 40 bars (3349, 1657, 811 and 388 non-overlapping cases), while the 10-bar excess return has a standard deviation of 0.14–0.22 against a mean shift of under 0.011.
