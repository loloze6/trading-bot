---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price recovers part of that fall over the next two hours. The higher that hour's volume against its 30-day average, the larger the recovery.
Consequence: A sharp hourly drop on a volume surge is a reason to buy for a two-hour rebound, or to refuse a short into it.
Why:
- F3: Hours that fall more than 2.5 usual moves are followed by a 2-hour rebound, and the rebound grows with the hour's volume against its 720-hour mean, measured above drift:
- F4: That high-volume rebound is concentrated in a few years. It is +0.88 % in 2020 (t 3.90, n 127) and +1.12 % in 2021 (t 3.54, n 88), and +0.35 % in 2018 (t 1.24). It is near zero in 2019, 2022, 2024 and 2025 (between -0.09 % and +0.05 %).
- F2: The fade the book bets on is not in the data, and no change of holding or sizing can make it pay. The unusual move is +0.02 % per case over 6 hours (strength 0.011, 12,052 cases), and the total move is -0.01 %, against a cost of 0.11 % per trade. Up-hours of 2.5 to 4 usual moves on volume 0.5 to 1.5 times average end 0.06 % lower than drift, not higher (t -0.47, n 209). Those of 1.5 to 2.5 usual moves end +0.01 % (t 0.17, n 704). Trades entered on the larger forecasts lose more (-0.38 % against -0.18 % before fees), and the step-5 size check difference is -0.0018 %.
