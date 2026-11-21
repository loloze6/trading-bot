---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's last daily move in either direction, relative to its 30-day volatility, the higher its return over the next 10 days.
Consequence: A trader would lean long a coin after an unusually large day, up or down, more so the larger the day was, and hold it for about ten days.
Why:
- F6: A large day in either direction is followed by a higher 10-day return than a quiet day. By fifth of the day's absolute move over the coin's 30-day volatility, the unusual 10-day move rises from −1.73 % (t −1.9) to +1.50 % (t 1.5), about 282 cases each. The gap of 3.2 % has Welch t of about 2.4, which is borderline given the number of angles.
