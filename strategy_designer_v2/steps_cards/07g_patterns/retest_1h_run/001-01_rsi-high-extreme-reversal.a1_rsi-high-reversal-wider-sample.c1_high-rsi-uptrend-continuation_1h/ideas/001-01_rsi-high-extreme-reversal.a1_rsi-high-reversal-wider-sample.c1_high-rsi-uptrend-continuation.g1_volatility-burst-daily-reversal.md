---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's volatility over the last 7 days is high relative to its volatility over the last 60 days, the larger its 24-hour return measured in units of its recent volatility, the more the coin moves the opposite way over the next 24 hours, and the reversal is stronger the higher that volatility ratio.
Consequence: In a volatility burst, a trader should fade the last day's move in proportion to its size, buying after sharp falls and refusing to chase sharp rises, for about one day.
Why:
- F2: In 24-hour steps on a non-overlapping grid, a coin's past 24-hour return in volatility units predicts reversal only when its 7-day volatility is high against its 60-day volatility: the slope of the next 24-hour excess return on the past return is -0.080 (t -5.37, n 4309) in the top tercile of that ratio, +0.006 (t 0.38) in the middle tercile and +0.060 (t 2.60) in the bottom tercile, and the interaction of past return with the volatility ratio has t -5.70 (n 12926).
- F3: The high-volatility-ratio reversal is the same sign on all six coins, with slopes from -0.052 (ETH, t -1.40) to -0.128 (ZEC, t -3.46), and in 7 of 8 years, from -0.045 (2024) to -0.247 (2018, t -5.82); the only positive year is 2020 (+0.030, t 0.67).
- F4: Within the high-volatility-ratio tercile the effect is graded across the five quintiles of the past 24-hour return: the next 24-hour excess return falls steadily from +1.21% (t 5.31) after the largest falls to +0.43% (t 2.41), then -0.20% and -0.15%, and -0.53% (t -2.53) after the largest rises.
- F5: Using the 7-day volatility level alone gives the same split: the reversal slope is -0.087 (t -6.64) in the highest volatility tercile against +0.054 (t 2.70) in the lowest, while the unconditional slope by coin stays between t -2.25 and +1.00.
