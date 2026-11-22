---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move is large relative to its 30-day high-low range, the larger its 30-day rise, the higher its return over the next 5 days.
Consequence: A trader would follow strong 30-day rises with long positions and leave out the matching shorts after falls, which have not paid.
Why:
- F1: The tested idea's long side carries all of the book, and its short side gives nothing back. Long trades average +11.24 % net (t 10.75, 3077 trades) and short trades −1.60 % (t −8.29, 3838 trades). On the 5-day grid in the trending regime, the unusual move in the forecast's direction is +1.16 % after a 30-day rise (t 2.73, 1581 cases) against +0.25 % after a 30-day fall (t 0.88, 1539 cases).
- F5: Across all bars, 30-day momentum pays at moderate net-move-to-range ratios, not only above the 0.5 rule. The 5-day unusual move in the 30-day direction is +1.02 %, +1.23 % and +1.13 % in the second to fourth fifths of the ratio (t 3.04, 3.73, 2.24, about 1087 cases each). It is +0.13 % in the flattest fifth (t 0.44) and +0.59 % in the highest (t 1.45).
