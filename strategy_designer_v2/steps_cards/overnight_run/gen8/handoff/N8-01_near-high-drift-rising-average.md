---
brief: 002_moving-average-cross-trend-persistence
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a new 20-day closing high, while the close stays near that high and above its 20-day average, the coin rises more than its average over the following days, only while the 20-day average itself has risen over the last few bars.
Consequence: Refuse the near-high long when the 20-day average is flat or falling, which keeps the gain and removes the deepest part of the book's fall.
