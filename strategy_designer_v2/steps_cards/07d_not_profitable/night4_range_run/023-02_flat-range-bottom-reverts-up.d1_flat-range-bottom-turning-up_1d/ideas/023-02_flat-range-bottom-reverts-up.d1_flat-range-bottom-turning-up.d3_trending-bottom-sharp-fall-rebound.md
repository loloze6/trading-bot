---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move is large relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its fall over the past 10 days, the more it rises over the next 5 days.
Consequence: In a trending coin in the lower half of its month, buy after the sharpest 10-day falls and size by the depth of the fall.
Why:
- F1: The book earns 0.0088 % a day against the 0.05 % required, because it is rarely in the market: the mean_reversion regime covers 18.5 % of bars, each coin holds a position on 16 % to 30 % of bars, the mean allocation while in is 0.14 to 0.31, and over 2898 days only 71 % of days show any book move.
- F7: The brief's reversion toward the middle is not in flat coins. The reversion toward the middle is +0.13 % (t 0.33, n 511) in the flattest net-move quintile, and the 5-day excess return regressed on range position in flat coins has t −0.42 (n 835). Coins of middling trend (net/range about 0.44) move away from the middle (−1.28 %, t −2.87).
- F8: In trending coins the 10-day move grades the next 5 days strongly, in two opposite ways. Above the middle, a larger 10-day rise is followed by a larger 5-day rise (slope t 4.17, n 879, mean excess +0.83 %). Below the middle, a larger 10-day fall is followed by a larger 5-day rise (slope t −3.52, n 841).
