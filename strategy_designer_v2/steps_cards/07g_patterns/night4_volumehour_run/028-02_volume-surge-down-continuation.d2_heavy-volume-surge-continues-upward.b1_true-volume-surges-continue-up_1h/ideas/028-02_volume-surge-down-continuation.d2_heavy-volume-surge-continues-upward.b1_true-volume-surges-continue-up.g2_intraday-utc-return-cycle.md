---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: The coin's return over the next four hours follows a daily cycle in UTC time: highest when the four hours start in the late US session around 18:00–20:00 UTC and lowest when they start around midnight UTC, the move larger the closer the start is to those two peaks.
Consequence: The late-US-session hours are a reason to lean long and the hours around midnight UTC a reason to avoid longs, mainly as timing for trades taken on other grounds, since the cycle alone moves less than a trade costs.
Why:
- F1: Each coin's 4-hour return, minus its drift, follows a daily cycle by UTC start hour. The cycle was sampled once a day per hour, about 5,836 independent cases per hour. Starts at 17–20 UTC gain +4.6, +9.0, +6.7 and +8.4 bp (t 2.1, 4.4, 3.2, 3.9). Starts at 22–01 UTC lose −4.9, −6.7, −9.0 and −6.1 bp (t −2.3, −3.1, −4.5, −3.2). The other 16 hours lie within |t| < 1.7.
- F2: The midnight-UTC weakness holds in both coins: BTC −8.2 bp (t −3.3, 2,918 cases), ETH −9.8 bp (t −3.1, 2,918 cases). It is negative in every year from 2018 to 2023 (−24.2 to −3.1 bp, four years with t ≤ −2.3) and gone in 2024 (+0.1 bp) and 2025 (+4.9 bp, t 1.1). It is at most about 9 bp per 4 hours, below the 0.11 % a trade costs.
