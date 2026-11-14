---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the short moving average of the close is above the long one, price keeps drifting upward, but only while the coin's own recent return is positive. The drift is larger the stronger that recent rise and the closer price stands to its recent high, and it turns into a decline when the coin has been falling inside the golden-cross state.
Consequence: Hold the golden-cross long in proportion to the coin's recent rise and step aside when the coin is falling inside the cross, which is when the book's deepest falls occur.
Why:
- F1: While the short SMA is above the long one, the 10-bar excess return depends on the coin's recent 20-bar return, not on the spread. When that return is negative the mean excess is -0.0171 (t -2.26, n 333), and when it is positive it is +0.0221 (t 2.07, n 361). Across the 20-bar return quartiles the excess rises steadily, from -0.029 (t -2.73) through -0.001 and +0.010 to +0.034 (t 1.83).
- F3: The book's deepest falls come while it is long in a golden-cross state but the coin is falling. On active bars inside book drawdowns deeper than 15%, 71% have a negative 20-bar return, against 49% of all active bars. Their median 20-bar return is -0.089 against +0.004, and their median distance below the 30-bar high is -0.199 against -0.102.
- F4: How close price sits to its recent high grades the gain the same way. In the active state, bars at the 30-bar high are followed by a 10-bar excess of +0.041 (t 2.37). Bars in the deepest quartile below it (median -0.28) are followed by -0.022 (t -2.03).
- F5: Scaling the position by a positive 20-bar return lifts the proxy coin-averaged book on all its fall measures but not its mean. Calmar rises from 0.39 to 0.57, the deepest fall shrinks from -0.41 to -0.21, and Sharpe rises from 0.71 to 0.81 (holding 0.64). The mean daily gain drops from 0.000501 to 0.000347.
- F6: In the active state the daily book earns 0.001234 when the 20-bar return is up and 0.000443 when it is down. The coin itself earns 0.00335 against 0.00049 in those two states.
- F7: The 20-bar return carries no such effect while the short SMA is below the long one. There, its lowest quartile is followed by an excess of +0.010 (t 0.97) and its highest by -0.003 (t -0.29), so the effect belongs to the golden-cross regime.
