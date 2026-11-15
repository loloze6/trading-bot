---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3258 USD
---
## Findings
- **F1:** Measured on non-overlapping 20-bar blocks, bars with the close above the long SMA beat the coin's mean by only +0.52% (t 0.32, n 399), against −0.02% for bars below it (n 412); the difference above minus below is +0.53% with Welch t 0.27, so the effect barely differs from holding the coin.
- **F2:** The positive mean comes from a few large outcomes, not from a typical drift: the median 20-bar excess on above-SMA bars is −3.6%, only 40.6% of them beat the coin's mean, the skew is 7.4, and the 10 largest cases add up to 5.6 times the total sum of excess returns.
- **F3:** The forecast is not graded the way the idea needs: across forecast quartiles the 20-bar excess goes −3.5% (t −1.81), −0.4%, −1.3%, then +7.2% (t 1.34), and across quintiles of the raw distance it stays flat (−0.7% to +0.8%, Spearman rho −0.04, p 0.25, n 811).
- **F4:** The effect depends on whether the long average itself is rising: above-SMA bars with a rising SMA average +2.6% excess over 20 bars (t 1.17, n 266), while above-SMA bars with a falling SMA average −3.3% (t −1.46, n 64), so the two cases mix opposite results.
- **F5:** Prior momentum splits it the same way: above-SMA bars with the top third of 60-bar momentum average +2.5% (t 0.94, n 118), and those in the bottom third average −8.7% (n 13, 23% beat).
- **F6:** The effect is drowned by market regimes: above-SMA 20-bar excess is −13.2% in 2018 (t −2.76) and −17.3% in 2022 (t −3.12), and slightly positive (+0.4% to +3.6%) in 2019–2021 and 2023–2025, with every year showing a similar sign for below-SMA bars too.
- **F7:** Calm conditions favour it: above-SMA bars in the lowest third of 30-bar volatility average +2.3% excess (5%-trimmed +0.9%, t 1.33, n 102), against −1.2% in mid and −0.3% (trimmed −2.8%) in high volatility.
- **F8:** The book's mean daily return of 0.000554 is mostly the market's own rise (0.000345, from a mean position of 0.27 that is invested 56% of days) rather than timing (0.000209).
- **F9:** Other horizons do not clarify it: at 5 bars the above-SMA excess is +0.09% (t 0.32, n 1640) and at 60 bars +4.0% (t 0.49, n 120), with medians negative (−0.4%, −10.5%) at both.

## Ideas
- `002-03_price-cross-above-long-sma.b1_cross-with-rising-average` (from F1, F3, F4, F5): After the coin's close has crossed above its long moving average, price keeps rising further than holding the coin over the following bars, only while the long average itself is rising, and the faster the average rises, the larger the move that follows.
- `002-03_price-cross-above-long-sma.b2_cross-in-calm-markets` (from F2, F6, F7): After the coin's close has crossed above its long moving average, price keeps rising further than holding the coin over the following bars, only while the coin's recent volatility is low, and the calmer the market, the larger the move that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
