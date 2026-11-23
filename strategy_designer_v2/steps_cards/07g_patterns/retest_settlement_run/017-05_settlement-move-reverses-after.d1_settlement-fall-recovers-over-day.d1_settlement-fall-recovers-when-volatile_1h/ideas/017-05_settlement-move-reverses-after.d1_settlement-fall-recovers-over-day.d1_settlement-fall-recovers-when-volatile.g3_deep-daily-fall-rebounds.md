---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The deeper a coin's 24-hour fall against its usual 24-hour move, the more it rises over the next 24 hours, and more so the higher its 7-day hourly volatility stands against its 30-day volatility.
Consequence: A deep one-day fall in a coin that has recently turned volatile is a reason to be long for the next day, sized by the depth of the fall.
Why:
- F5: A deep 24-hour fall reverses over the next 24 hours, but only in the tail.
- F7: Only the most volatile state shows an excess return. The top quintile of 7-day over 30-day volatility (ratio 1.37) earns +0.28 % excess over 24 hours (t 2.4), while the other four quintiles are between -0.18 % and +0.04 %.
