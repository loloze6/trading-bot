---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move is large relative to its 30-day high-low range and whose close sits above the middle of that range, the larger its rise over the past 10 days, the more it rises over the next 5 days.
Consequence: In a trending coin near the top of its month, buy the strongest 10-day risers and size by the strength of the rise, which fills the time the flat-range book spends idle.
Why:
- F1: The book earns 0.0088 % a day against the 0.05 % required, because it is rarely in the market: the mean_reversion regime covers 18.5 % of bars, each coin holds a position on 16 % to 30 % of bars, the mean allocation while in is 0.14 to 0.31, and over 2898 days only 71 % of days show any book move.
- F2: Within that small exposure most of the gain is the coins' own rise: per coin the book's mean bar gain is 0.0013 % to 0.019 %, the market part is 0.003 % to 0.007 %, and timing is near zero or negative (BTC 0.0016 %, XRP 0.0007 %, LTC −0.0015 %), with only XMR (0.014 %) and ZEC (0.008 %) adding clearly.
- F8: In trending coins the 10-day move grades the next 5 days strongly, in two opposite ways. Above the middle, a larger 10-day rise is followed by a larger 5-day rise (slope t 4.17, n 879, mean excess +0.83 %). Below the middle, a larger 10-day fall is followed by a larger 5-day rise (slope t −3.52, n 841).
