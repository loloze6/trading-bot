---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: The further a coin's 24-hour return falls below zero, measured against its typical hourly move over the past 30 days, the more it rises over the next 24 hours, and the further its 24-hour return rises above zero, the more it falls over the next 24 hours.
Consequence: After a sharp day a trader should lean against it for the following day rather than chase it, and most of all after a sharp fall.
Why:
- F1: Over a day the bars mean-revert, graded: on a non-overlapping 24-hour grid, the slope of the next 24-hour return on the past 24-hour return (scaled by the 720-hour hourly standard deviation) is -22.7 bp per unit (t -4.21, 5312 cases); the same 24-hour horizon after a 12-hour past return gives -13.1 bp (t -2.58), and a 12-hour horizon after a 24-hour past return gives -5.9 bp (t -2.20).
- F2: The reversal is strongest after falls: the lowest quintile of the past 24-hour return is followed by +53.7 bp over the next 24 hours (t 3.52, 1067 cases), about five times the 0.11 % cost of a trade; the two lowest deciles carry unusual moves of +36 bp (t 1.63) and +46 bp (t 2.22), against -30 bp (t -1.79) for the highest decile.
- F3: The 24/24 reversal slope is negative in 12 of 16 coin-years, for example ETH 2021 at -79 bp (t -2.35) and BTC 2020 at -44 bp (t -2.22); it is positive only in 2022 for both coins (+0.3 and +8.4 bp) and in BTC 2023 and ETH 2024.
