---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: (new idea) In a coin's own bars, the forward drift over the next days is graded by the coin's recent return: the stronger the gain over the last several weeks, the further price continues upward.
Consequence: Recent price momentum, not the moving-average spread, is the quantity to grade a long position by, so trade it as a book of its own.
Why:
- F2: The size of the forecast does not grade what follows: the mean excess 10-bar return across forecast buckets (0-5, 5-10, 10-15, 15-20) is -0.85%, +0.23%, +1.05% and +0.004% (n = 212, 183, 174, 263), the step-5 slope has t = 0.37 over 832 active blocks, and the raw-spread quartiles show no rising pattern either (+0.14%, +1.30%, -0.53%, -0.70%).
- F3: On the book's invested days, the coin's own 20-bar return sorts the gain: in the lowest r20 quartile the position earns a mean of -0.00139 per day and carries -24% of the total gain, while in the highest quartile it earns +0.00495 per day and carries 86% of it (next-day coin return t = 2.77, n = 1132).
- F4: The same sort holds on non-overlapping 10-bar blocks while the forecast is positive: blocks whose 20-bar return is in the lowest quartile have a mean excess 10-bar return of -2.94% (t = -2.73, 174 blocks), and those in the highest quartile have +3.39% (t = 1.83, 174 blocks).
