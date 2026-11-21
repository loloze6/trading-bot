---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 5 days is higher the larger its 28-day rise, and the extra return grows faster than the rise, so its largest 28-day rises are followed by its largest 5-day gains.
Consequence: Put most of the exposure on long positions after a coin's strongest 28-day rises, rather than spreading it evenly over long and short scores.
Why:
- F2: Almost all the gain is timing (3.14 bps per bar out of 3.23; the market's rise gives 0.09) on a small position (mean absolute allocation 0.17). The long bars (8513) earn 6.1 bps each and the short bars (8660) only 0.4 bps, so half the book's exposure carries nothing.
- F5: Momentum's effect sits in its strongest rises. By 28-day-momentum quintile the 5-day excess return is -0.10 %, -0.32 %, -0.41 %, -0.40 %, then +1.22 % in the top quintile (mean 28-day return +42 %, 684 cases). The long side of momentum alone has t 2.08, its short side t 0.41.
- F6: The book earns in rising states only. With the 28-day return in its top third, per-bar gain is 13.8, 5.7 and 8.4 bps for low, mid and high volatility. In the falling and middle thirds it is -1.8 to 3.3 bps, and longs held there earn 9.2 bps per bar against shorts' 0.5 bps in the falling third.
