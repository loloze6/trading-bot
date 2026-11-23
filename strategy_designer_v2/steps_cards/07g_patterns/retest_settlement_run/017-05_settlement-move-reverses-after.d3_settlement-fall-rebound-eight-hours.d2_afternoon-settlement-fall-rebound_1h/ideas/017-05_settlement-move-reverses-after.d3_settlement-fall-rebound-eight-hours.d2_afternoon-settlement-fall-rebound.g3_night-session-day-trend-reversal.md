---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Between midnight and 09:00 UTC, a coin's 24-hour return reverses over the next 8 hours. The larger the 24-hour move against the coin's usual 24-hour move, the larger the move back.
Consequence: A trader fades the day's trend during the Asian session and refuses trend trades then.
Why:
- F4: During the Asian and European night the 24-hour move reverses instead. The 24-hour continuation product over 8 hours is negative at every close from 00:00 to 09:00 UTC, with t −2.1 to −5.0 (about 15,700 cases each hour). This is the opposite sign to the 15–18 UTC afternoon in F3.
