---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return is partly reversed over the next 24 hours, and the reversed share grows with the size of that return and with the coin's hourly volatility over the past 24 hours.
Consequence: After a large 24-hour move made in a volatile day, a trader leans against it for the next day, and refuses that trade after a calm day or a small move.
Why:
- F1: Over 24 hours, a coin's past 24-hour move is partly reversed when its last 24 hours were volatile, and the reversal grows with that volatility. In the top quintile of past-24-hour hourly volatility, the slope of the next 24-hour standardised return on the past one is -0.125 (t -9.18, 3422 non-overlapping cases), with an unusual move against the past move of 0.56 % per case (strength 0.12). The next quintile down gives a slope of -0.036 (t -1.90), and the three lower quintiles give slopes between +0.010 and +0.058.
- F2: Inside that top volatility quintile, the reversal grows with the size of the past move. The unusual move against it is -0.13 % (t -0.64), 0.42 % (t 2.05) and 1.40 % (t 5.66) for the small, middle and large terciles of the absolute past move (about 1140 cases each). The large tercile is about 7 times the 0.19 % cost of a trade.
- F3: The high-volatility 24-hour reversal holds on every coin, with slopes from -0.072 (XRP, t -2.77) to -0.156 (XMR, t -5.81), and in 6 of 8 years with t at or beyond -2.5. It weakens in 2022 (t -1.16) and in 2024 (t -0.13).
- F4: The reversal is specific to the 24-hour horizon. In the top volatility quintile, the slope is -0.001 (t -0.11) over 12 hours and -0.031 (t -1.60) over 48 hours. Volatility relative to the past 7 days grades it less than the absolute level does: slope -0.106 (t -8.70) in the top relative-volatility quintile against -0.089 (t -3.36) in the bottom.
