---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours a coin moves against its own 24-hour return, and the larger that return in multiples of its usual 24-hour move over the past 30 days, the larger the move back.
Consequence: A trader would lean against a coin's large one-day moves for the following day, since the reversal grows with the move and is several times a trade's cost.
Why:
- F1: The book loses 0.129 % a day (Sharpe -1.58) while holding the coins earned +0.127 % a day. The idea it trades is too small to cover a trade: per case over 6 hours, the unusual move is +0.02 % (strength 0.009) and the total move is -0.02 %, against a cost of 0.11 % per buy and sell, over 9180 cases.
- F7: Large 24-hour moves reverse over the next 24 hours, by more than a trade costs. On a non-overlapping 24-hour grid, the top quintile of the prior 24-hour return (above +2.5 %) is followed by an unusual move of -26.3 bp (t -2.10, n 1072). The bottom quintile (below -2.3 %) is followed by +42.9 bp (t 2.66, n 1072). The middle quintiles show between -11 and +2 bp, with t inside ±1.
- F8: The volume split the brief rests on is not in the data either way. After hourly moves beyond 2.5 usual moves, the 6-hour move in the hour's direction is -5.7 bp on volume below 1.5× average (n 2811) and -1.0 bp on volume above 3× (n 3791). At 2 hours the high-volume reading is -10.2 bp, so surging-volume moves do not continue.
