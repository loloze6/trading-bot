---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's short moving average stands far above its long one, compared with the gap's own recent history, the coin's next rise is smaller than when the gap is modest.
Consequence: A trader should not make the long position larger as the gap widens, and should keep it the same size or cut it when the gap is stretched.
Why:
- F4: A larger raw spread does not earn more, yet the book sizes up with it. The coin's daily return is 0.00187 and 0.00226 in the two lowest in-position spread quartiles, where mean positions are 0.16 and 0.71. It is 0.00092 in each of the two highest quartiles, where mean positions are 1.31 and 1.62.
- F5: Measured per trade, a larger entry forecast earns less. 530 trades entered at forecast 15–20 average −2.89% before fees. 150 trades entered at forecast 0–5 average +9.15%.
- F6: Measured per day, the coin's return grows only weakly with the forecast: 0.00094 at forecast 0–5 against 0.00155 at 15–20, with 0.00130 when the forecast is 0. The forward 20-day return is not monotone in the forecast either: its mean is 0.026, 0.074, 0.021 and 0.038 across the four positive buckets, against 0.028 at forecast 0. This is consistent with the inconclusive slope t of 0.37.
- F2: The higher risk comes from leverage, not from edge. The average position when in the market is 0.95, with a maximum of 2.2. Book sd rises from 0.0130 at positions 0–0.5 to 0.1096 at positions 1.5–2.3. Window max drawdowns have a median of −22%, a lower quartile of −49% and a worst of −96%, which gives a Calmar of 0.00098.
