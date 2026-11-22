---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The wider a coin's hourly moves over the past day relative to its past 30 days, the larger its rise over the next 24 hours after a 24-hour fall of a given size in its typical moves.
Consequence: A trader can scale a rebound long by how turbulent the past day was, not only by the size of the fall.
Why:
- F1: Large 24-hour falls bounce back only when the past day's hourly moves were wide. When the past day's mean absolute hourly move was above 1.189 times the 30-day one, 24-hour falls of more than 1.5 typical-scaled units were followed by an unusual 24-hour rise of +1.29 % (t 6.31, 1066 non-overlapping cases). After the same falls in calmer days it was +0.002 % (t 0.01, 810 cases).
- F2: In wide-moving days the bounce grows with the fall. The unusual 24-hour move after falls of -0.5 to -1.5, -1.5 to -3 and beyond -3 scaled units was +0.77 % (t 3.56, 661 cases), +0.90 % (t 3.94, 693) and +2.00 % (t 5.05, 373). The 24-hour scaled return correlates with the next 24-hour scaled move at -0.111 in wide-moving days and -0.005 in calm ones.
