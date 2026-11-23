---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin falls over 24 hours, measured in its usual 30-day daily moves, it rises over the next 24 hours more than its normal drift. The rise is larger the larger the fall and the higher the coin's 30-day hourly volatility, while the coin's 24-hour rises are followed by no comparable fall.
Consequence: A trader would buy a coin after an unusually deep 24-hour fall in a volatile month, and refuse to sell short after unusual rises.
Why:
- F2: The reversal on the next day is one-sided across all weekdays. After a day in the coin's lowest decile of its move in usual 30-day daily moves, the next day's excess return was +0.57 % (t 3.78, n 1,440), and +0.28 % (t 2.33) in the second decile. The top decile was followed by −0.15 % (t −1.14), and the middle deciles were flat to slightly negative.
- F3: The rebound after down days only appears when the coin's 30-day volatility is high. The graded measure (fall in usual moves × next-day excess) was +0.0152 (t 4.35, n 2,336) in the highest volatility tercile, against +0.0010 (t 0.54) and −0.0012 (t −0.83) in the other two. For the largest falls in that tercile the mean next-day excess was +1.27 %, against −0.07 % in the lowest volatility tercile.
- F4: The signed next-day reversal of all days grew with volatility: −0.04 % (t −0.68), +0.11 % (t 1.68) and +0.39 % (t 4.52) from the lowest to the highest 30-day volatility tercile, n 4,787 each.
- F1: The book's whole gain comes from its long side. Long bars summed to +2.51 of gain against −0.05 for short bars (60,885 and 54,816 bars). Long trades averaged +0.49 % after fees and short trades −0.49 % (3,746 trades in all, mean net −0.003 %), even though up Sundays did reverse on Monday at the day level (+0.50 %, t 3.21, n 1,113).
- F5: By year, the down-day rebound was strong in 2020 (+0.77 %, t 3.50) and 2021 (+0.74 %, t 3.76) and absent elsewhere (from −0.18 % to +0.19 %, |t| ≤ 1.5). The signed reversal of all days faded in 2024 (−0.02 %, t −0.19) and 2025 (−0.15 %, t −1.37).
