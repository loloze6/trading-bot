---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin, the higher its 5-day average volume against its 30-day average, the higher its return over the next 7 days, whatever the direction of its last 5 days, and the more so the higher its 30-day return.
Consequence: A trader would lean long on volume surges mainly in coins that have risen over the past month, and would give volume little weight in coins that have fallen.
Why:
- F1: The book is short on 58% of bars (10,285 short against 7,063 long) while every coin rose on average (0.0007 to 0.0016 a day), so its gain from the market's own rise is negative for every coin (-0.00005 to -0.00014 a bar). Shorts lose 0.000581 a bar to drift and net only 0.000082 a bar, while longs earn 0.001624 a bar.
- F4: The forecast's information is concentrated where the coin's 30-day return is high. In the top 30-day-return tercile, the slope of 7-day excess return on the forecast is 0.001378 (t=2.52, n=575), against 0.000464 (t=1.01) and 0.000155 (t=0.37) in the lower two terciles. Across all samples, the forecast × z(30-day return) interaction has t=2.02.
- F5: At bar level, longs in the top 30-day-return tercile earn 0.003218 a bar (n=2,144), while shorts there earn 0.000024 a bar even though the coin rose 0.0011 a bar. Shorts earn only 0.000208 even in the bottom tercile.
