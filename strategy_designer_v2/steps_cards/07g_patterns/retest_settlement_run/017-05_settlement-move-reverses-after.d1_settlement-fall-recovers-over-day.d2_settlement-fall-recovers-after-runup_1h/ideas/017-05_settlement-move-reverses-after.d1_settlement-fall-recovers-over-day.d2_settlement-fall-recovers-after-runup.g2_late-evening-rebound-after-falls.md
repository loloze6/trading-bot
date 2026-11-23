---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the 2 hours after the 21:00 UTC close, a coin's price rises, and the rise is larger the deeper the coin's fall over the 24 hours before it.
Consequence: A coin that has fallen over the day into 21:00 UTC is a reason to be long for the next two hours, more so the deeper the fall.
Why:
- F5: The hour after bars closing at 21:00 and 22:00 UTC rises on average. Over the next 1 hour the mean is +0.055 % (t 6.7) and +0.044 % (t 5.6), against about ±0.02 % at most other hours.
- F6: The 2 hours after the 21:00 UTC close rise in every coin (+0.08 % to +0.11 %, t 3.0 to 4.7, about 2,890 cases each) and in 7 of 8 years (2022 -0.04 %, t -1.4). The rise is largest after the lowest past-24h-return quintile (+0.23 %, t 6.9) against +0.00 % to +0.13 % in the other quintiles. That move is only about the size of the 0.19 % trade cost.
