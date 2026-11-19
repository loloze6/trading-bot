---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its past 6 hours relative to its own hourly volatility, the more it rises over the next 4 hours, and the more it has risen the more it falls.
Consequence: A sharp 6-hour drop in a coin is a reason to lean long for the next few hours rather than chase the move.
Why:
- F3: Short moves partly reverse over the next 2 to 4 hours. The 2-hour return regressed on the 6-hour volatility-scaled return gives a slope of −2.39 bp (t −6.99, n 206550 non-overlapping cases), negative in 7 of 8 years. It is strongest in XMR (−5.14, t −6.21) and ZEC (−5.36, t −4.96) and absent in BTC (+0.38, t 0.67) and ETH (+0.16, t 0.22). On 4-hour returns, the two lowest 6-hour-return quintiles gain +5.06 bp (t 3.16) and +5.62 bp (t 3.96), while the top quintile gains −0.04 bp (t −0.03).
- F5: How a move was built adds nothing to its size. The interaction of the 24-hour volatility-scaled return with path efficiency (net move over summed absolute hourly moves) has t 0.32 at 24 hours (n 17102) and −0.21 at 72 hours (n 5539). Next-day return signed by the past day's direction shows no ordered pattern across volume quintiles (−18.9, −10.7, +10.3, −28.6, −7.5 bp).
