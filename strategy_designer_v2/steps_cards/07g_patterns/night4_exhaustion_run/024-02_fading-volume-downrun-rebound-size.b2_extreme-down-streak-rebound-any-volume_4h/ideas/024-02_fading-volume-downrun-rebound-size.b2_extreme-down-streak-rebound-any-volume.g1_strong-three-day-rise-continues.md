---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days by much more than its usual 3-day move, it keeps rising over the next 3 days; the larger the 3-day rise relative to its usual 3-day move over the past 30 days, the larger the further rise.
Consequence: A trader can buy a coin after an unusually strong 3-day rise rather than fading it, expecting a move several times the cost of a trade.
Why:
- F1: A coin's 3-day (18-bar) return, measured in its usual 3-day moves, predicts the next 3 days' unusual move in the same direction. Across all six coins on the base grid, the slope is 0.037 (t 2.78). It holds on every one of six grid offsets: slopes 0.037 to 0.056, t 2.78 to 4.28, about 882 cases per coin per grid.
- F2: The continuation sits in the strongest 3-day rises. Among rising 3-day stretches, the top quartile (mean z18 1.84) is followed by +0.149 usual moves (t 3.33, 673 cases), while the three lower quartiles give -0.02 to -0.04. With a usual 3-day move of about 8.2 %, +0.149 is roughly +1.2 % per case, about 6 times the 0.19 % cost of a trade. This is unlike the tested idea's strength of 0.007, which is 0.3 times the cost.
- F3: The top quintile of 3-day rises is followed by +0.10 usual moves (t 3.02, 1059 cases). It stays positive on all six grid offsets (t 1.91 to 3.02) and is positive in 5 of 6 coins (ZEC +0.198 t 2.40, BTC +0.148 t 1.82, XRP +0.181 t 1.68). It is positive in 6 of 8 years, with 2018 and 2022 the exceptions (-0.047 and -0.153).
