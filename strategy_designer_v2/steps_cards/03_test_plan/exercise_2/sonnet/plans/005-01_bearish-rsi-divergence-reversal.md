---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 005-01_bearish-rsi-divergence-reversal_config.json
Confirm: Over a 10-bar horizon, before costs, the forecast correlates negatively with the next 10-bar return on each coin. The most negative forecasts (top decile of |forecast|, price at the top of its 20-bar range with weak RSI) are followed by a clearly lower 10-bar return than the bars with price at the top of its range but ordinary RSI. The portfolio also gains more than holding each coin over the same bars.
Reject: The 10-bar returns after the most negative forecasts are no lower than after price-at-range-top bars without weak RSI, or the forecast's correlation with the next 10-bar return is zero or positive. Alternatively, the portfolio does not beat buy-and-hold before costs, or its gains do not grow with the size of |forecast|.
Inconclusive: The sign is right on only one or two of the three coins, or the effect is too small to separate from the spread across coins. The top-decile |forecast| bars are too few or too clustered in one episode to judge. The portfolio beats holding only because of the long-side (bullish-divergence) bars.
Deviation: The config does not detect a divergence event against the previous price high. It reads the state: price near the top of its 20-bar range while RSI(14) is weak relative to its recent level. This is a graded sum of two standardised parts, with no product or swing-high comparison. The position therefore also shrinks, rather than vanishing, when price is high and RSI is also high. The config is symmetric: price near the 20-bar low with strong RSI (a bullish divergence) goes long, which the idea does not state. The reversal is tested as a short while the state holds, not as the retracement of the run-up to the high.
