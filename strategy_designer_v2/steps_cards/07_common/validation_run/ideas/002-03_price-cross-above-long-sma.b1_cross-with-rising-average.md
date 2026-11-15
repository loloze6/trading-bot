---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After the coin's close has crossed above its long moving average, price keeps rising further than holding the coin over the following bars, only while the long average itself is rising, and the faster the average rises, the larger the move that follows.
Consequence: A trader would take the long cross only when the long average is sloping upward, and would refuse it when the average still slopes down.
Why:
- F1: Measured on non-overlapping 20-bar blocks, bars with the close above the long SMA beat the coin's mean by only +0.52% (t 0.32, n 399), against −0.02% for bars below it (n 412); the difference above minus below is +0.53% with Welch t 0.27, so the effect barely differs from holding the coin.
- F3: The forecast is not graded the way the idea needs: across forecast quartiles the 20-bar excess goes −3.5% (t −1.81), −0.4%, −1.3%, then +7.2% (t 1.34), and across quintiles of the raw distance it stays flat (−0.7% to +0.8%, Spearman rho −0.04, p 0.25, n 811).
- F4: The effect depends on whether the long average itself is rising: above-SMA bars with a rising SMA average +2.6% excess over 20 bars (t 1.17, n 266), while above-SMA bars with a falling SMA average −3.3% (t −1.46, n 64), so the two cases mix opposite results.
- F5: Prior momentum splits it the same way: above-SMA bars with the top third of 60-bar momentum average +2.5% (t 0.94, n 118), and those in the bottom third average −8.7% (n 13, 23% beat).
