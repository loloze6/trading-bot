---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal
line: 7.g patterns
backtest: 016-04_down-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return measured in units of its past 7-day hourly volatility, the more it moves the opposite way over the next 24 hours. This reversal is stronger the higher the coin's past 7-day volatility stands relative to its own usual level.
Consequence: After a sharp one-day move in a coin that is unusually volatile, fade it for a day rather than follow it, and fade harder the more volatile the coin is.
Why:
- F2: Over the next 24 hours, coins revert their last 24-hour move scaled by volatility. On the non-overlapping 24-hour grid, the 24-hour return in units of 7-day hourly volatility has a slope of -0.00198 on the next-24h excess return (t -5.12, n 17,102). The slope is negative in every coin (t -1.61 to -3.53) and in both halves of the windows (w1–w12 t -3.92, w13–w24 t -3.43). The last single hour alone gives slope -0.00179 (t -5.18).
- F3: The same 24-hour reversal depends on how volatile the coin is relative to its usual level. With an interaction term, the scaled 24-hour return has coefficient +0.011 (t 12.7) and its product with relative volatility (7-day vol over the coin's mean vol) has -0.0131 (t -17.0). So reversal appears only once volatility is above about 0.83 of its usual level and deepens as volatility rises.
