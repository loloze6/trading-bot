---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-04_dip-in-uptrend
line: 7.d not profitable
backtest: N3-04_dip-in-uptrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In an uptrend, a large one-day drop that follows a previous day's drop of more than the coin's mean absolute move is followed by a larger next-day rebound than a single drop after an up day.
Consequence: A trader keeps full size for second-day dips and less for isolated dips after up days, which carry most of the losses.
Why:
- F2: The falls are concentrated on a few days when many coins are held at once. The 58 worst book days (2%) sum to -3.04, against +1.67 summed over all days. On those days the book holds 3.9 coins on average, against 2.3 on ordinary negative days. Coin-days with 4 or more coins held show a summed coin P&L standard deviation of 0.288 and a worst of -1.23, against 0.037 and -0.38 when one coin is held (167 vs 764 days).
- F3: The large positions carry both the edge and the losses. Bars held at allocation ≥1 have a next-day excess return of +0.0069 (t 3.56, n 821), but their summed losses are -22.7 against -7.2 for all smaller positions (n 1949), and their P&L standard deviation is 0.102 against 0.019.
- F7: A dip that follows a prior down day of more than one mean absolute move is followed by an excess of +0.0062 (t 2.35, n 356). After a prior up day the excess is +0.0022 (t 1.68, n 1319), and these bars carry -15.4 of losses.
