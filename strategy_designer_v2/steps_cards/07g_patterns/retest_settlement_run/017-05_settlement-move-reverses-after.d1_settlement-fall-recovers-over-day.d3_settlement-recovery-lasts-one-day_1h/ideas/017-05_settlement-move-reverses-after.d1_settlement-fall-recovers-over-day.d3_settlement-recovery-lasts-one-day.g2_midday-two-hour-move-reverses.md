---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 2-hour move into the 12:00 or 13:00 UTC close is followed over the next 4 hours by a move the opposite way, larger the larger that 2-hour move is against the coin's usual 2-hour move.
Consequence: A trader fades large 2-hour moves into the US-morning hours for a 4-hour hold, and declines to follow them.
Why:
- F4: The 2-hour move into a 12:00 or 13:00 UTC close reverses over the next 4 hours, with slope t 10.4 and 8.5 (about 16 500 daily cases each), and t above 4 in 6 of 8 years. The effect sits in the largest moves: the top quintile of the scaled 2-hour move gives an unusual 4-hour move of 0.28 % (strength 0.137), while the other quintiles give 0.00–0.08 %.
- F5: The 2-hour-move reversal is not tied to funding settlements, against the brief's third test.
