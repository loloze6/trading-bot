---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way, in periods when its 24-hour volatility is high against its own volatility of the past 30 days.
Consequence: In a volatile stretch, a trader would lean against a coin's large daily move for about a day, more as the move is larger, and would refuse to chase it.
Why:
- F2: The same reversal over a day is concentrated in volatile markets. With the 24-hour return scaled by 24-hour volatility, on a non-overlapping 24-hour grid, the slope of the next 24-hour excess return is:
- F3: The high-volatility 24-hour reversal holds across the sample:
- F4: In high volatility the reversal grows with the move's size, and it is large next to the cost. By quintile of the scaled 24-hour move (mean |z| 0.14, 0.42, 0.73, 1.08, 1.69), the unusual 24-hour reversal is:
- F1: The hourly reversal is real but far too small to trade. On every bar, the next-hour slope on the scaled 1-hour move has a t of -11.4 over 413,189 cases. Even the top decile of hourly moves gives back only +2.76 bp (t 4.0), against a trade cost of 19 bp. That is why a book trading 20.77 times a day ends at Sharpe -13.77 and -98.6 % a year.
