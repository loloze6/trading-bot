---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next two hours. The larger that hour's rise, the larger the giveback.
Consequence: A trader would refuse to chase a quiet-volume hourly rise for the next two hours, since its first hours more often slip back than extend.
Why:
- F2: The giveback shows most clearly over the first two hours and fades after. It is +0.015 % (t 2.05) over 1 hour, +0.035 % (t 3.29) over 2 hours, +0.023 % (t 1.84) over 3 hours, +0.020 % (t 1.12) over 6 hours and +0.021 % (t 0.82) over 12 hours. The 2-hour reading holds on both coins: BTC +0.029 % (t 2.15) and ETH +0.054 % (t 3.13).
- F3: The effect is not graded by the size of the rise. The correlation of the hour's rise, in usual moves, with the next 2-hour giveback is -0.003, and with the 6-hour giveback also -0.003. Across |forecast| quintiles the 6-hour giveback goes +0.053 %, +0.005 %, +0.029 %, -0.034 %, +0.047 % with no trend. Rises of 2 to 3 usual moves show a 6-hour continuation of -0.062 % (t -1.22). Step 5's larger-half minus smaller-half difference is -0.0018 %.
