---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 2-hour move ending in the European late-morning hours (11:00–13:00 UTC) reverses over the next 2 hours, by more the larger the move is relative to its usual 2-hour move.
Consequence: The midday European hours are where short-term fades pay best, so fading activity should be concentrated in them.
Why:
- F6: Large 2-hour moves ending at 11:00 and 12:00 UTC fade by 45.9 bp (t 5.3, n 819) and 27.6 bp (t 5.7, n 2142), against a typical 0 to 10 bp in other hours. These t values stand out even after 24 hours were checked. The funding hours do not line up with the effect: 08:00 is -6.3 bp, 00:00 is 12.5 bp and 16:00 is 18.6 bp.
