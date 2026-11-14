---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-08_twenty-day-momentum
line: 7.g patterns
backtest: N1-08_twenty-day-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin has fallen sharply over 20 days, its price rises over the next 20 days by more than its usual 20-day move, so deep 20-day losses mark rebounds rather than continuing downtrends.
Consequence: A trader should refuse to short a coin after a steep 20-day decline, and should treat that decline as a long setup instead.
Why:
- F1: The 20-bar forward return is U-shaped in the forecast rather than rising with it: bars in the bottom fifth of forecasts (the sharpest 20-day falls) are followed by a mean 20-bar excess return of +3.99% (t=2.51, 166 non-overlapping cases), while the three middle fifths are all negative (-1.7%, -2.6%, -2.0%). The slope of excess return on |forecast| has t=2.61 over 827 cases.
- F2: The bottom-fifth rebound appears in every coin, with means from +3.0% to +6.9% (t 0.71 to 1.35, 24 to 32 cases each). It is concentrated in 2020 (+16.6%, t=2.70, n=16) and 2021 (+19.6%, t=3.13, n=20), and it turns negative in 2018 (-6.3%, t=-1.77, n=30).
- F3: The top fifth of forecasts (the strongest 20-day rises) is followed by only +2.3% excess (t=0.73, 166 cases). Bars with |forecast|≥15 earn +3.3% (t=1.24, n=199). Continuation after strong rises is therefore not distinguishable from chance.
- F7: The book's gains come only from its long side. Longs average +4.61% net per trade (4507 trades, 40% winners), while shorts average -0.76% (4864 trades, 34% winners). Shorts lose in 5 of 6 coins, and ZEC longs alone contribute +10611 of summed percent.
