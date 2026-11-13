---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day average is above the 200-day average but the coin has fallen over the prior 20 days, the coin's forward return falls below its average return.
Consequence: A trader should go flat on a golden-cross long whenever the 20-day return turns negative, which would cut the losses of falling-market years and the deep drawdowns.
Why:
- F7: All of the invested profit comes when the coin has risen over the prior 20 days. Those 4342 invested bars earn a book mean of 0.003263, a sum of +14.17. The 5622 invested bars after a 20-day fall earn −0.000046, a sum of −0.26.
- F8: The losses cluster in falling-market years. The book summed −1.92 in 2018 and −1.08 in 2022 while invested 25% and 36% of bars, with the coin returning −0.0020 and −0.0022 per invested bar. In 2021 it earned +7.65 while invested 83% of bars.
- F10: The poor Calmar of 0.00098 comes from deep per-window drawdowns. The mean book drawdown is −28.7% (coin −39.0%), but the worst book drawdown reaches −96.1% against the coin's worst of −77.0%. Windows w13 and w18 have mean book drawdowns of −75.6% and −71.1%.
