---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 005-01_bearish-rsi-divergence-reversal_config.json
Confirm: The test uses a 10-bar horizon, on BTC, ETH and BNB pooled, before costs. Take the bars where the close is the highest close of the last 20 bars. On the ones where the forecast is negative, the next 10-bar return is lower than on the ones where the forecast is zero or positive. The gap must be significant at the 5% level. Also, the coin's 10-bar return minus its unconditional mean 10-bar return (the buy-and-hold drift) falls as the forecast becomes more negative, and is negative in the most-negative forecast decile.
Reject: At 20-bar highs, the 10-bar forward returns after a negative forecast (divergence) are no lower than those after a non-negative forecast (no divergence). Or the most-negative forecast decile is followed by drift-adjusted 10-bar returns at or above zero.
Inconclusive: The difference has the predicted sign but is not significant, or it holds on only one of the three coins. Also inconclusive if fewer than about 30 non-overlapping 20-bar-high bars with a negative forecast exist per coin.
Deviation: The test does not detect the discrete pattern "new price high with an RSI peak lower than at the previous price high". Instead it uses a continuous spread on every bar: where the close sits in its 20-bar range, minus the RSI(14) level, both standardised. A short position grows when price is high in its range but RSI is weak. The spread is symmetric, so it also goes long on the bullish counterpart (price low in its range, RSI not low). It is also mildly long when a new high comes with very strong RSI, which is a part the idea does not claim. The confirm and reject criteria therefore look only at bars at 20-bar highs.
