---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits above its 200-day simple moving average, the coin's return over the next 20 days beats its average return, by more the further the close sits above that average.
Consequence: If confirmed on the wider set of coins, being long a coin in proportion to how far it trades above its 200-day average earns more than simply holding it; if rejected, distance above the long average is no reason to hold the coin.
Why:
- F1: The main measure is on the side the idea predicts but short of the bar: the forecast-weighted 20-day excess return has a block mean of +0.126 with t = 1.73 over 811 non-overlapping blocks (502 with a position). The book agrees with that sign, with a Sharpe of 0.68 against a holding Sharpe about 0.11 lower.
- F2: The raw effect is small next to the market's own 20-day moves. On the 399 non-overlapping 20-day grid bars with a positive forecast, the mean excess return is only +0.0052 (t = 0.32), against −0.0002 (t = −0.01) on the 412 flat bars. The median above-average case is −0.036, and only 40.6 % of cases beat the coin's mean, so a few large rises carry the mean.
- F4: The effect is mixed across coins and years. Block means are positive for BTC (+0.23, t = 1.69), ZEC (+0.37, t = 1.27) and XRP (+0.20, t = 0.84), and negative for XMR (−0.10, t = −1.00). By year they run from −0.15 (t = −3.02) in 2018 to +0.46 (t = 2.03) in 2020, and each year has only 86–108 blocks. Six coins on daily bars give too few independent cases to separate this effect from the swings between years.
- F5: The test's horizon is not where the effect hides. On bars above the average, the excess return has t of 0.32, 0.61, 0.32, −0.25 and 0.49 at 5, 10, 20, 40 and 60 days, with no horizon clearly stronger. Splitting by the prior 20-day return also shows nothing clear (t from −1.13 to 1.34). No part of the data shows the effect clearly enough to justify narrowing the idea.
