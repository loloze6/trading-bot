---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, the give-back after a large one-day move happens within the next day. The larger the day's move relative to its 60-day mean absolute daily move, the larger the opposite move over that next day.
Consequence: A fade of a sharp move in a volatile stretch should earn most of its gain within a day, so holding it longer adds noise rather than gain.
Why:
- F2: The give-back shows more clearly over shorter horizons than the plan's 3 days: over 24 hours it is 0.0058 with t 2.79 on 628 cases (BTC 0.0048 with t 2.04 on 313, ETH 0.0069 with t 1.98 on 315), over 48 hours 0.0067 with t 1.90 on 321, and over 72 hours 0.0075 with t 1.35 on 195.
- F1: The main measure is on the predicted side but too noisy for 195 cases: the mean signed 72-hour excess return is 0.0075 with t 1.35, a standard deviation of 0.077, a positive share of only 52.8 % and a median of 0.0046, so at this mean and spread about 426 independent cases would be needed to reach t = 2.
