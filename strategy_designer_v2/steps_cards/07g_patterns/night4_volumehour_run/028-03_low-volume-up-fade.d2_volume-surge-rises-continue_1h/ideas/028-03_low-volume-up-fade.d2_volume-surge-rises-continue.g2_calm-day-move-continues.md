---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past day is low against its own past month, its 24-hour return carries on over the next 12 hours. The larger that 24-hour move, measured in the coin's usual daily moves, the larger the further move in the same direction.
Consequence: In a calm market, a steady one-day move is a reason to follow it for the next half day rather than fade it.
Why:
- F5: In the lowest quartile of 24-hour volatility the sign is reversed: the past 24-hour return continues. The slope is +37.7 bp per z over the next 12 hours (t 3.46, 2668 cases) and +43.7 bp over 24 hours (t 1.76). By coin over 24 hours it is BTC +19.3 bp (t 0.62) and ETH +70.7 bp (t 1.78), so this pattern is weaker and less consistent than F1.
