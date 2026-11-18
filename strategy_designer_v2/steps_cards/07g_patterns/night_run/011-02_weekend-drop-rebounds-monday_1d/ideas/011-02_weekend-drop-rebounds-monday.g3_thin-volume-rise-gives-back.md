---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-02_weekend-drop-rebounds-monday
line: 7.g patterns
backtest: 011-02_weekend-drop-rebounds-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rises on a day of low trading volume relative to its own last 20 days falls over the next 1 day. The lower that relative volume and the larger the rise, the larger the fall.
Consequence: Thin-volume up days are a reason to refuse chasing and to expect a one-day giveback.
Why:
- F2: The rebound after a fall is concentrated on high-volume days. Down days in the top third of relative volume (volume over its 20-day mean) are followed by +0.47 % excess the next day (t 4.31, n 2607). Down days in the low and middle thirds are followed by −0.04 % and +0.10 % (t −0.43 and 1.11). Up days on low and middle relative volume are followed by −0.21 % (t −2.52, n 2746) and −0.27 % (t −3.14, n 2661).
- F1: The day after a coin's largest falls it rebounds. Across all coins, bars in the lowest fifth of one-day return (in 20-day usual moves) are followed by a next-day excess return of +0.44 % (t 4.73, n 3188). The middle-upper fifth is followed by −0.25 % (t −3.01, n 3188), and the top fifth by −0.07 % (t −0.76).
