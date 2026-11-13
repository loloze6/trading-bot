---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When the coin has risen over the prior 20 days, its forward return is higher than its average return, whether or not the 50-day average is above the 200-day average.
Consequence: A trader should go long on a positive 20-day return, including on bars where the slow averages have not yet crossed, rather than waiting for the golden cross.
Why:
- F7: All of the invested profit comes when the coin has risen over the prior 20 days. Those 4342 invested bars earn a book mean of 0.003263, a sum of +14.17. The 5622 invested bars after a 20-day fall earn −0.000046, a sum of −0.26.
- F2: The book trails holding because it sits flat on 41% of bars (share invested 0.585) while the coin still earns 0.000894 per bar there. On flat bars after a 20-day rise the coin earns 0.001363 (2778 bars). The result is a mean book return of 0.000817 per bar against 0.001287 for the coin, and a mean window return of 18.5% against 23.1%. The book beats the coin in only 41% of coin-windows.
