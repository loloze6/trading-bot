---
brief: 010_rsi-midline-regime-direction
source-idea: 010-05_rsi-above-share-reversal
line: 7.d not profitable
backtest: 010-05_rsi-above-share-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is positive, the larger the share of the past 30 days that its 14-day RSI has spent above 50, the higher the coin's return over the next 14 days.
Consequence: In rising coins, persistent RSI dominance above the midpoint is a reason to stay long rather than to fade it.
Why:
- F1: The book loses on its shorts, not on fees. Short bar-days earned a mean -0.001703 a day over 2826 days, while the coin rose +0.002623 the next day on those same days. Long bar-days earned -0.000345 over 2800 days. Short trades averaged -9.78% net (646 trades) against +0.21% net for long trades (601 trades). Fees cost only 0.0000338 of the book a day.
- F2: The losses sit where the coin had risen over the past 30 days. There the book was short on 1775 bar-days and lost -0.002498 a day while the coin gained +0.003101 a day. Where the 30-day return was negative, shorts gained +0.000490 over 388 bar-days.
- F4: On the non-overlapping 14-day grid, the RSI-above-50 share does not predict reversal overall: slope +0.005, t 0.15, n 192. Its sign splits by trend. Where the 30-day return was positive the slope was +0.079 (t 1.33, n 109), meaning continuation. Where the 30-day return was non-positive it was -0.102 (t -1.42, n 83), meaning reversal. In the rising 90-day tercile the slope was +0.256 (t 2.43, n 18).
- F5: The share quartiles are not monotone against the next 14 days' demeaned return: +0.040, -0.057, -0.001, +0.021 from the lowest share to the highest. The most persistent above-50 stretches (mean share 0.96) were followed by gains, not falls.
