---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-02_weekend-drop-rebounds-monday
line: 7.g patterns
backtest: 011-02_weekend-drop-rebounds-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that falls on a day of high trading volume relative to its own last 20 days rises over the next 1 day. The larger the fall in usual daily moves and the higher that relative volume, the larger the rise.
Consequence: Heavy-volume sell-offs are a reason to buy for a one-day rebound rather than to follow the move.
Why:
- F1: The day after a coin's largest falls it rebounds. Across all coins, bars in the lowest fifth of one-day return (in 20-day usual moves) are followed by a next-day excess return of +0.44 % (t 4.73, n 3188). The middle-upper fifth is followed by −0.25 % (t −3.01, n 3188), and the top fifth by −0.07 % (t −0.76).
- F2: The rebound after a fall is concentrated on high-volume days. Down days in the top third of relative volume (volume over its 20-day mean) are followed by +0.47 % excess the next day (t 4.31, n 2607). Down days in the low and middle thirds are followed by −0.04 % and +0.10 % (t −0.43 and 1.11). Up days on low and middle relative volume are followed by −0.21 % (t −2.52, n 2746) and −0.27 % (t −3.14, n 2661).
- F7: A day-range effect matches F1. Days in the top fifth of relative high-low range (over its 20-day mean) are followed by +0.32 % excess the next day (t 3.06, n 3216).
