---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's four signals are combined into one score, the coin's return over the next 5 days is higher the higher that score is, only while its 28-day return is up, and there the rise is larger the stronger the score.
Consequence: Hold the combined score's positions mainly while the coin's month is rising, where the book earned 6 to 14 bps per bar, and keep them small elsewhere.
Why:
- F2: Almost all the gain is timing (3.14 bps per bar out of 3.23; the market's rise gives 0.09) on a small position (mean absolute allocation 0.17). The long bars (8513) earn 6.1 bps each and the short bars (8660) only 0.4 bps, so half the book's exposure carries nothing.
- F6: The book earns in rising states only. With the 28-day return in its top third, per-bar gain is 13.8, 5.7 and 8.4 bps for low, mid and high volatility. In the falling and middle thirds it is -1.8 to 3.3 bps, and longs held there earn 9.2 bps per bar against shorts' 0.5 bps in the falling third.
- F7: The book's worst 40 days average -2.07 % against -0.46 % for the coins on those days, so its worst losses come from its own positions, not from falls the coins share.
