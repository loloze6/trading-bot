---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin moves far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price moves back against that hour's move over the next two hours. The larger the hour's move in typical moves times its volume multiple, the larger the move back.
Consequence: A sharp hourly move on a volume surge is a reason to fade it for a couple of hours, never to chase it.
Why:
- F1: The idea's effect is missing. After rising hours of more than 2 typical 30-day moves, the next 2 hours move by -0.005 to -0.062 strength across every volume bin (t between -0.03 and -0.52, 134 to 629 cases per bin). At 4 hours, the top decile of return-in-sd times volume ratio (mean 20.6) moves by -0.008 strength (t -0.13, 642 cases). The idea's size is 0.000 of a usual move: a total move of 0.04 % per case against a 0.11 % cost per trade.
- F4: Large moves on surging volume fade rather than continue. At 2 hours, hours of more than 2 typical moves (either direction) are followed by a move against them of 0.0695 strength (t -2.51, 3542 cases). The same holds on volume above 3 times its average (-0.128 strength, 1667 cases).
- F5: Falling hours on surging volume rebound, and the rebound grows with volume. After a fall of more than 2 typical moves, the 2-hour strength is:
