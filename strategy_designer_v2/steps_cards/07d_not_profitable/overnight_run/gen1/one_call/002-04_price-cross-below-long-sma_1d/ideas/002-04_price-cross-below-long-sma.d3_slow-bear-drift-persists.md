---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose close has stayed below a falling 200-day average for weeks, the downward drift shows itself over multi-week holds rather than over days.
Consequence: A trader would hold a short through the downtrend for weeks instead of re-entering on every brief dip.
Why:
- F5: The trades are short-lived and rarely right. There were 2,488 shorts with a 23.8% win rate and a median hold of 9 days. The three shorter duration quartiles (1.5 to 15 days) each lost about -6.2% gross per trade, while the longest quartile (55 days) earned +3.1%.
- F6: Gains come only from periods when the coin fell, and losses from periods when it rose. 2018 earned +0.00166 gross per bar while the coin fell -0.0035, and w2, w7, w9 and w14 were also positive with the coin falling. w16 lost -0.0084 with the coin up +0.0045, and 2020 lost -0.0030 with the coin up +0.0042.
