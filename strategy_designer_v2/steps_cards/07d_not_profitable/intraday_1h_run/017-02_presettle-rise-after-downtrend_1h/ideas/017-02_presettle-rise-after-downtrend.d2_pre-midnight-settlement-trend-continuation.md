---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In the 2 hours before the 00:00 UTC settlement, a coin's return is positive, and the stronger its 3-day rise, the larger that rise.
Consequence: The late-day pre-settlement window rewards being long after up-trends, not after down-trends, so a trader should not fade a 3-day rise into the 00:00 settlement.
Why:
- F5: The pre-settlement hours do not lean against the trend as a group.
- F6: The strongest hourly drift falls at a clock time with no settlement. The bar stamped 20:00 UTC rises +0.055 % on average (t = 6.75), more than any pre-settlement bar. Hour-of-day drift exists apart from the funding clock.
