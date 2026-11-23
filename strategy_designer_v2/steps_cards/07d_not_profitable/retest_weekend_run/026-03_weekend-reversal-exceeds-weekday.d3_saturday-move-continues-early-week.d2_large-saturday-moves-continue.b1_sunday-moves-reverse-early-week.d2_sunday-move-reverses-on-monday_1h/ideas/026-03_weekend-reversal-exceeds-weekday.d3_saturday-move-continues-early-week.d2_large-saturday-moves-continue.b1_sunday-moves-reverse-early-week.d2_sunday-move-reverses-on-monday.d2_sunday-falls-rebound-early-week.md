---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's fall over Sunday's 24 hours, measured against its usual 30-day move, is followed over the next 48 hours (Monday and Tuesday) by a rise, the larger the higher the coin's 30-day hourly volatility.
Consequence: A trader would buy after a falling Sunday in a volatile coin and hold through Tuesday, leaving out the weaker short after a rising Sunday.
Why:
- F1: The book sizes against its own effect: the vol-target sizing holds a mean position of 0.56 on Mondays in the lowest pooled tercile of 30-day hourly volatility, where the reversal is nil (-0.004 %, t -0.03, n 604; position-weighted -0.17 %), but only 0.21 on the highest tercile, where the reversal is +0.98 % per case (t 3.27, n 604); the middle tercile gives +0.56 % (t 3.06) at a position of 0.36.
- F6: The reversal keeps going into Tuesday. Over 48 hours it is +0.58 % per case (t 3.82, n 2404) against +0.39 % over 24 hours (t 3.61), with hours 24–48 alone adding +0.21 % (t 2.19). In the highest volatility tercile it grows from +0.98 % to +1.37 % (t 3.49), and in the middle one from +0.56 % to +0.99 % (t 4.09).
- F7: The down-Sunday side carries most of it: after a falling Sunday the coin rises +0.55 % over Monday (t 3.73, n 1247), while after a rising Sunday it falls +0.22 % (t 1.40, n 1178).
