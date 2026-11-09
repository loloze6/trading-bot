---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Take the 14-bar Wilder RSI of the close on daily bars and measure how far it sits above 50 (RSI − 50). Put that distance on the scale of its own recent past by dividing by the mean absolute RSI deviation over the previous 60 bars, times 10, capped at ±20. Keep only the upper side: the forecast is zero whenever RSI is at or below 50. Then square it with a pivot of 20 (20 × (x/20)²), so the forecast stays graded but is damped hard near neutral and grows quickly toward strong readings. A typical deviation of 10 gives a forecast of 5; the cap of 20 (200% long) is reached at about twice the typical deviation, roughly RSI ≥ 70. The forecast is positive and grows with how extreme the high RSI is, near zero for neutral readings, and never negative.
Config: 001-03_rsi-high-extreme-continuation_config.json
Confirm: The horizon is 5 bars. Pool all 3 coins × 6 windows. Count only non-overlapping samples: a bar enters only if no earlier sampled bar of the same group lies within 5 bars. Confirmation requires both of the following: - The mean 5-bar forward close-to-close return after bars with forecast ≥ 10 (strong high-RSI readings) exceeds the mean 5-bar forward return after bars with forecast < 2 (neutral or low readings). The difference must be positive with a t-statistic ≥ 2 and positive in at least 2 of the 3 coins. - Supporting check: the strategy's total return before costs exceeds its average exposure times the coin's buy-and-hold return over the same windows.
Reject: The pooled difference (high-forecast minus neutral 5-bar forward return, non-overlapping) is zero or negative. Alternatively, it is negative in at least 2 of the 3 coins with the strategy failing to beat exposure-matched buy-and-hold.
Inconclusive: A positive pooled difference with a t-statistic below 2. Also inconclusive: a positive pooled difference with only 1 of 3 coins positive, or fewer than 30 non-overlapping high-forecast samples in total.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by how far above". The position grows smoothly toward extremes rather than firing at a fixed threshold such as 70. Readings below 50 (low extremes) are not tested and are held flat.
