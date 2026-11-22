---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next four hours. The higher that hour's volume against its 30-day average, and the deeper the fall in typical moves, the larger the rise.
Consequence: A sharp hourly drop on a volume surge is a reason to go long for a few hours rather than short it, with more conviction the bigger the surge.
Why:
- F4: Large moves on surging volume fade rather than continue. At 2 hours, hours of more than 2 typical moves (either direction) are followed by a move against them of 0.0695 strength (t -2.51, 3542 cases). The same holds on volume above 3 times its average (-0.128 strength, 1667 cases).
- F5: Falling hours on surging volume rebound, and the rebound grows with volume. After a fall of more than 2 typical moves, the 2-hour strength is:
- F6: The rebound is graded along the combined measure. At 4 hours, the two most negative deciles of return-in-sd times volume ratio show strength 0.138 (t 1.83) and 0.130 (t 2.17), 642 cases each. Strength falls to 0.020 in the third decile.
- F7: The rebound is on both coins but not in every year. At 4 hours after a fall of more than 2 typical moves on volume above 3 times its average, strength is 0.166 on BTC (218 cases) and 0.181 on ETH (224 cases). It is positive in 2020 to 2024 (0.23 to 1.24) but negative in 2018 (-0.39) and 2025 (-0.10).
