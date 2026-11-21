---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-03_combined-extremes-larger-moves
line: 7.d not profitable
backtest: 022-03_combined-extremes-larger-moves_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 28-day rise relative to its own usual 28-day moves, the more the coin rises over the next 5 days.
Consequence: A trader would bet long behind a coin's strongest month-long rises with one fixed direction, instead of a learned mix whose signs flip, and would refuse shorts that this rise does not support.
Why:
- F1: The book's loss comes from its shorts. Summed over bars, short positions lost 10.22 against +2.98 for longs. The 2,281 short trades lost 5.58 % each after fees, while the 1,981 long trades gained 1.89 %. Of the book's -0.044 % mean gain per bar, -0.037 % is timing and only -0.007 % is the market's own rise.
- F3: The weights learned from the past do not carry forward, because each effect's sign flips from year to year. The Spearman correlation of 28-day momentum with the next 5-day move is -0.13 in 2018, +0.09 in 2021 and -0.13 in 2022. Nearness to the 90-day high goes from +0.16 in 2019 to -0.24 in 2022. Pooled over all years, every effect is near zero (|rho| ≤ 0.037, p ≥ 0.31).
- F5: Of the raw effects, only the strongest 28-day rises are followed by a move that clears the cost. The top coin-relative quintile of 28-day return has a next-5-day unusual move of +1.21 % (t 2.15, n 490), about 6 times a round trip. The other four quintiles lie between -0.73 % and +0.44 %, none with |t| above 1.8.
