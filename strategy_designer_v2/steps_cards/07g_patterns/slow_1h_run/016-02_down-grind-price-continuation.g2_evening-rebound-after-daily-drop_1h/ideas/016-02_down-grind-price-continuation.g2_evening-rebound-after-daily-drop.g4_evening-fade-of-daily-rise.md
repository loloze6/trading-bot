---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has risen over its past 24 hours relative to its own volatility, as read at the 20:00 UTC close, the more it falls over the two hours to 22:00 UTC.
Consequence: A strong 24-hour rise into the 20:00 UTC close is a reason to refuse a long into the evening and lean short instead.
Why:
- F4: Whether the 24-hour move reverses or continues over the next 2 hours depends on the hour, with |t| above 6 even after scanning 24 hours. After the 13:00 UTC close (bar stamped 12:00) and the 20:00 close (stamped 19:00), the slope on the 24-hour volatility-scaled return is −9.24 bp (t −6.88) and −7.87 bp (t −6.50), so the move reverses. After the 15:00 close (stamped 14:00) and the 23:00 close (stamped 22:00), it is +8.89 bp (t 6.44) and +8.23 bp (t 6.42), so the move continues.
- F1: Every coin rises in the evening whatever the forecast says. The hourly bars stamped 20:00 and 21:00 UTC return +5.45 bp (t 6.75) and +4.36 bp (t 5.66), the largest of all 24 hours. The 2-hour excess return from the 21:00 close is positive in all six coins (+7.2 to +9.6 bp, t 2.7 to 4.1), in 7 of 8 years (2022 is the exception at −5.5 bp), and in 74% of coin-windows. It is +5.13 bp (t 3.66, n 8790) even on days with a zero forecast, against +11.87 bp (t 7.39, n 8613) with a positive one.
