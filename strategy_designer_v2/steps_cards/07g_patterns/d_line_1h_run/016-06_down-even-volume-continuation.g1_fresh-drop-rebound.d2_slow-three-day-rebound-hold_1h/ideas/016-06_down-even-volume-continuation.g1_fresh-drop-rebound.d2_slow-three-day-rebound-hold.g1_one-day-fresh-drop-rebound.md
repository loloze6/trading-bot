---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 1 day.
Consequence: Hold a rebound after a fresh drop for about a day, and do not keep it for three days or re-size it hour by hour.
Why:
- F1: The rebound after a fall in the last day is concentrated in the first one to two days and largely spent by day three. When the coin is down over 72 bars, the slope of forward excess return on the standardised 24h move is -0.0019 (t -12.4, n 33184) at 6h, -0.0084 (t -14.2, n 8272) at 24h, -0.0117 (t -10.4, n 4040) at 48h and -0.0069 (t -4.07, n 2669) at 72h, and the verdict's 24-to-72-bar slope is only 6.0e-05.
- F2: The reversal needs a falling 3-day backdrop; when the coin is up over 72 bars, the 24h reversal slope is -0.0022 (t -3.8, n 8542) and the 48h slope is -0.0009 (t -0.76, n 4251).
- F3: Measured unconditionally on a 24h grid, the lowest quintile of 24h move is followed by +0.48% excess over the next 24h (t 4.59, n 3308), and the highest quintile by -0.32% (t -3.24, n 3305).
- F6: The book fails because hourly re-sizing churns a signal whose edge lives at the daily scale. The mean gross gain per bar is 4e-06 (t 0.70) on turnover of 0.046 of the book per bar. Over 58401 trades with a median length of 5 hours, the mean return is -0.39% before fees and -0.49% after, and the mean daily book return is negative in every year from 2018 to 2025.
