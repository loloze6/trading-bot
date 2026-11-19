---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
line: 7.g patterns
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour fall, measured in units of its past 7-day hourly volatility, the more it rises over the next 24 hours. The rebound is larger the higher the coin's 7-day volatility stands above its own 30-day average.
Consequence: After a sharp one-day drop in a coin that is unusually volatile, buy it for a day; ignore drops in calm conditions, and do not fade rises with the same strength.
Why:
- F2: Nearly all of the reversal comes from the high-volatility tercile, where the 7-day volatility is well above its 30-day mean. Down-moves (bottom fifth of 24-hour return in volatility units) then rebound by 0.0124 excess over the next 24 hours (t 5.65, n 1,005), and up-moves fall back by 0.0047 (t 2.45, n 1,039). In the low and middle terciles the reversal is between -0.0001 and 0.0017 with every |t| < 1.3. The regression term for scaled move × volatility ratio has t -9.26.
- F3: The reversal is lopsided toward falls. The bottom fifth of scaled 24-hour moves is followed by +0.0041 excess over the next 24 hours (t 4.25, n 3,308), while the top fifth is followed by only -0.0019 (t -2.19, n 3,305).
- F1: The fade's 24-hour forecast is real, but the book loses to costs. On the 24-bar grid the forecast earns a pooled mean of 0.00226 (t 4.89, n 17,246), while fees per day (0.0021 to 0.0035 per coin, from 1.9 to 3.1 turns of the book a day) are larger than gross gains per day (-0.0009 to +0.0025), so every coin's book falls (-0.0010 to -0.0032 per day).
