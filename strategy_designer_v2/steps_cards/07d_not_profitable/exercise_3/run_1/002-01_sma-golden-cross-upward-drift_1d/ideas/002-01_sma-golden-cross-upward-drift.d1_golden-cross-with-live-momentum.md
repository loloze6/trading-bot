---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA is above the 200-day SMA, the coin keeps drifting upward, and the drift is larger the stronger the coin's own return over the last several weeks, only while that recent return is positive.
Consequence: Size a golden-cross long by the coin's recent momentum rather than by the width of the averages' spread, and stand aside when price has turned down inside the uptrend, because that is where the book's deepest falls occur.
Why:
- F2: The size of the forecast does not grade what follows: the mean excess 10-bar return across forecast buckets (0-5, 5-10, 10-15, 15-20) is -0.85%, +0.23%, +1.05% and +0.004% (n = 212, 183, 174, 263), the step-5 slope has t = 0.37 over 832 active blocks, and the raw-spread quartiles show no rising pattern either (+0.14%, +1.30%, -0.53%, -0.70%).
- F3: On the book's invested days, the coin's own 20-bar return sorts the gain: in the lowest r20 quartile the position earns a mean of -0.00139 per day and carries -24% of the total gain, while in the highest quartile it earns +0.00495 per day and carries 86% of it (next-day coin return t = 2.77, n = 1132).
- F4: The same sort holds on non-overlapping 10-bar blocks while the forecast is positive: blocks whose 20-bar return is in the lowest quartile have a mean excess 10-bar return of -2.94% (t = -2.73, 174 blocks), and those in the highest quartile have +3.39% (t = 1.83, 174 blocks).
- F5: The losing state is a spread that is still widening while price has already turned down over 20 bars: on invested days in that state the next-day coin return averages -0.245% (n = 885) and the state carries -33% of the book's gain, while the r20-positive states earn +0.40% and +0.32% per day (t = 2.38 and 2.49).
- F6: The book's deepest falls sit in that state: across windows w12, w13, w16 and w18 (book -23%, -55%, -35% and -60%), invested days with a falling 20-bar return and a widening spread average -1.45% per day (t = -2.13, n = 168), and 12.5% of those days drop more than 8%.
- F8: The result rests on one window: w11 alone returns +405% for the book against +281% for holding, while most other windows lose or stay near flat even when holding gains (w16 -35% against +36%; w23 +0.4% against +32%).
