---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the two hours from 21:00 to 23:00 UTC is above its normal hourly drift, and the excess is larger the higher the coin's 30-day hourly volatility.
Consequence: A trader would hold the coin long through 21:00–23:00 UTC, or time purchases before that stretch and sales after it.
Why:
- F6: The hours starting 21:00 and 22:00 UTC carry a persistent positive drift. Hour 21 averaged +0.055 % (t 6.87, n 17,417) and hour 22 +0.044 % (t 5.76), the strongest of all 24 hours. Over the two hours, the excess was positive in all six coins (t 2.61 to 4.04), on every weekday (t 3.0 to 3.6 except Monday, 1.54) and in 7 of 8 years (2022: −0.028 %, t −1.87).
