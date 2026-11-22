---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past day is high against its own past month, its 24-hour return reverses over the next 24 hours. The larger that 24-hour rise or fall, measured in the coin's usual daily moves, the larger the opposite move that follows.
Consequence: After a sharp one-day move in a turbulent market, a trader has a reason to fade it for the next day, more strongly the larger the move, and never to chase it.
Why:
- F1: When the coin's last-24-hour volatility is in its top quartile against its 30-day level, the next 24 hours' unusual move falls as the past 24-hour return rises: slope -35.7 bp per 24-hour z-unit, t -4.55, on 1328 non-overlapping cases. Over 12 hours the slope is -12.8 bp (t -3.15, 2668 cases), and over 48 hours it is -28.0 bp (t -2.00, 661 cases).
- F2: This high-volatility reversal holds on each coin alone: BTC slope -30.7 bp (t -3.19, 649 cases) and ETH -40.6 bp (t -3.29, 679 cases). It holds in both halves of the windows: w1-12 at -19.6 bp (t -2.04) and w13-24 at -50.7 bp (t -4.16). Its sign is negative in 6 of 8 years.
- F3: The reversal is graded across quintiles of the past 24-hour z in high volatility. The lowest quintile is followed by an unusual 24-hour move of +101 bp (t 3.03) and the second lowest by +93 bp (t 2.91). The highest quintile is followed by -55 bp (t -2.02). Trading against the past day's sign earns about 55 bp per case on BTC (t 3.28) and 56 bp on ETH (t 2.69), five times the 0.11 % cost of a trade.
- F4: The reversal comes from the last day's move and not from the last three days'. In the same high-volatility cases, the slope on the 72-hour z is only -10.6 bp (t -1.22).
