---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next two to six hours. The larger that hour's rise, the larger the giveback.
Consequence: A large up-move without a volume surge is noise from thin liquidity, which fades.
Why:
- F1: The test's own result is on the side the idea predicts but too small for this data to show clearly. Recomputed on 12,172 cases, the 6-hour giveback after the short bets, drift removed, is +0.020 % with t 1.12, against step 5's +0.022 % with t 1.21. It is the same sign on both coins: BTC +0.019 % (t 0.86, 6,276 cases) and ETH +0.021 % (t 0.74, 5,896 cases).
- F4: The effect is mixed across years. The 6-hour giveback is +0.112 % (t 1.69) in 2018 and +0.068 % (t 1.62) in 2025. It is -0.101 % (t -2.03) in 2020 and -0.057 % (t -1.73) in 2023.
