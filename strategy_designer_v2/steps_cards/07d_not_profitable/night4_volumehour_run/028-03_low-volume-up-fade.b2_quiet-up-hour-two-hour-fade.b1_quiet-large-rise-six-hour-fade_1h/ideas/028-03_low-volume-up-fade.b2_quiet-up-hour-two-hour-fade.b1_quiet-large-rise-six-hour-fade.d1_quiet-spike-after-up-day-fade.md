---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next 24 hours, only while the coin's 24-hour return is also up. The larger that 24-hour rise, the larger the giveback.
Consequence: A trader would fade a quiet-volume hourly spike only when it extends a day-long rise, and would expect a larger giveback the more the coin rose over that day.
Why:
- F1: The book loses 0.129 % a day (Sharpe -1.58) while holding the coins earned +0.127 % a day. The idea it trades is too small to cover a trade: per case over 6 hours, the unusual move is +0.02 % (strength 0.009) and the total move is -0.02 %, against a cost of 0.11 % per buy and sell, over 9180 cases.
- F5: Shorting pays only in a falling month. On bars held short, the gain is +0.23 bp per bar (timing +0.46 bp) in the lowest tercile of the coin's 30-day return. It is -0.74 bp in the middle tercile and -0.57 bp in the top tercile.
- F6: The quiet-volume rise fades only when the prior day also rose. The 6-hour short-signed unusual move after quiet rises is +8.7 bp (t 1.31, n 1004) in the top tercile of the 24-hour return. It is -12.0 bp (t -1.85, n 1003) in the bottom tercile.
- F7: Large 24-hour moves reverse over the next 24 hours, by more than a trade costs. On a non-overlapping 24-hour grid, the top quintile of the prior 24-hour return (above +2.5 %) is followed by an unusual move of -26.3 bp (t -2.10, n 1072). The bottom quintile (below -2.3 %) is followed by +42.9 bp (t 2.66, n 1072). The middle quintiles show between -11 and +2 bp, with t inside ±1.
