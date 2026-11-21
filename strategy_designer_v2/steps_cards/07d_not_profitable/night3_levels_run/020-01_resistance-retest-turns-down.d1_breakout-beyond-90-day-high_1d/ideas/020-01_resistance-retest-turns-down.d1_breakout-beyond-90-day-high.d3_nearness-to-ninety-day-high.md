---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close stands to its highest close of the previous 90 days, the more it rises over the next 20 days.
Consequence: A trader should lean long as a coin's close approaches its 90-day high, and refuse longs on closes far beneath it.
Why:
- F7: Measured over 20 days, closes just below the 90-day high are followed by more than deeper closes, though none of these differences is significant. Closes 0 to 5 % below the high are followed by a 20-day unusual move of +3.1 % (60 cases, t 1.05), and closes 5 to 15 % below by +1.9 % (151, t 1.06). Closes 15 to 50 % below are followed by -2.9 % to -3.5 % (250 cases, t -1.6 to -1.7).
- F1: The book is almost always out of the market, which keeps its mean daily return at 0.000165 against the 0.0005 required. It holds a position on only 17.6 % of bars, and its mean position is 0.036 of the book. When it is in, the position is only 0.15 to 0.38 of the book, because the forecast is 0.9 to 1.7 on average. Between 28 % and 48 % of those in-position bars already carry a forecast of 0, depending on the coin.
- F2: The breakout's move keeps growing well past the 5-day horizon that was tested. The mean total move after a breakout case is +1.4 % over 5 days, +3.2 % over 10, +4.8 % over 20 and +6.9 % over 40 (175, 172, 162 and 124 cases). The unusual move is +0.8 %, +2.0 %, +2.4 % and +2.5 % (t 0.81, 1.32, 1.14, 0.64).
