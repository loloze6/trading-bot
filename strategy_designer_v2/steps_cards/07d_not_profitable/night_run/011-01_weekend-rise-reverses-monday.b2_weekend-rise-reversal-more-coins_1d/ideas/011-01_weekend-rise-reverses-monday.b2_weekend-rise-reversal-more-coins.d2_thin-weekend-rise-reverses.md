---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and the larger the weekend rise, the larger the fall, more so the lower Sunday's volume relative to the coin's average daily volume over the past 28 days.
Consequence: Weight weekend-reversal shorts toward large rises made on thin Sunday volume, where each fee buys the most reversal.
Why:
- F1: The book's whole gross gain is spent on fees: the per-bar gain summed over all bars is 2.45 against summed fees of 2.41. The active Mondays earn 0.00114 per bar while each trade bar costs 0.00056, and every one-day short is two trade bars (4316 fee bars for 2156 active bars), so the mean daily return is only 3.9e-05.
- F2: Most of the reversal comes after the bar the book holds. In the top quintile of Sunday returns (mean +6.1%), Monday's next-day return is -0.59% and Tuesday adds another -0.51%. The pooled short-on-rise measure grows from mean 0.0020 (t 2.20) for Monday alone to 0.0037 (t 3.58) for Monday plus Tuesday, over 4382 Sunday cases.
- F6: For the largest weekend rises, low weekend volume deepens the reversal. In the top third by size, the 2-day excess return is -1.63% when Sunday volume is below its 28-day median and -0.89% when it is above. In the smaller thirds volume makes no difference (-1.65% vs -1.59%, -0.61% vs -0.77%).
