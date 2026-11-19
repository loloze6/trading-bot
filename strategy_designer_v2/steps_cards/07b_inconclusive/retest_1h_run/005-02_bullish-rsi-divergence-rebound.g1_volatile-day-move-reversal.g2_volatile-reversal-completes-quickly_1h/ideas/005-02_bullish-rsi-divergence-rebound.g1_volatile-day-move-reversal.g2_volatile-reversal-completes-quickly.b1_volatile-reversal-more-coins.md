---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, the give-back after a large one-day move happens within the next 3 days. The larger the day's move relative to its 60-day mean absolute daily move, the larger the opposite move over those 3 days.
Consequence: A fade of a sharp move in a volatile stretch should be held for days, not a week, and a fade still held after about 3 days is a reason to close it.
Why:
- F1: The main measure is on the predicted side but too noisy for 195 cases: the mean signed 72-hour excess return is 0.0075 with t 1.35, a standard deviation of 0.077, a positive share of only 52.8 % and a median of 0.0046, so at this mean and spread about 426 independent cases would be needed to reach t = 2.
- F3: At 72 hours both coins point the same way but neither is clear on its own: BTC 0.0050 with t 0.95 on 96 cases and ETH 0.0098 with t 1.02 on 99.
- F4: One year pulls the 72-hour result down: 2018 gives −0.0387 with t −1.93 on 23 cases, 6 of the 8 years are positive, and without 2018 the mean is 0.0136 with t 2.48 on 172 cases.
