---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, and the more it rose over the past 5 days against its own 20-day volatility, the larger that rise.
Consequence: A trader would size level breaks by the sharpness of the run that carried price through the level, not by how far price stands above its average.
Why:
- F1: Across all coins on a non-overlapping 5-day grid, the bars the detector marked as breakouts ("trending") were followed by a 5-day move +1.81 % above the coin's normal drift (t 2.72, 217 cases), while all other bars gave -0.12 % (t -0.62, 3202 cases), so the level break carries the effect.
- F2: Inside those breakouts, the rise does not grow with distance above the 50-day average: Spearman -0.043 on raw distance and -0.007 on volatility-scaled distance (217 cases). By distance tercile the unusual 5-day move is +1.18 % (t 1.07), +4.61 % (t 2.40) and +0.80 % (t 0.51), at mean distances of 2.8 %, 7.0 % and 15.6 %. This is why the slope check failed.
- F3: The book's trades run against its own sizing: mean net profit per trade falls from 6.07 % in the lowest entry-forecast quintile to 0.93 % in the highest, with medians of +0.87 % and -0.59 % (224 trades each).
- F6: The book's best 5 % of days come after the coin rose 17.5 % over 5 days and 29.8 % over 20 days; its worst 5 % come after -0.6 % over 5 days and +8.6 % over 20 days (233 days each). The book earns when the break is already part of a sharp run, and loses when the break comes without one.
