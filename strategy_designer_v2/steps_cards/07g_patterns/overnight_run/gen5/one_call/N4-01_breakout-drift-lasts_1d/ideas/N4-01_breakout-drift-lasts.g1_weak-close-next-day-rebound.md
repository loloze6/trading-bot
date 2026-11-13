---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.g patterns
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In each coin, a daily close that falls more than half a typical daily move and finishes in the lower part of the day's range is followed by a rise over the next one to three days.
Consequence: A trader can buy, or refuse to sell, after a weak close near the day's low, rather than reading the drop as the end of the move.
Why:
- F1: A daily close down more than 0.5 of its 20-day volatility is followed by a rise the next day. In the (-1.5,-0.5] band the mean is +0.46% (t 4.82, n 2796, hit 56%); in the (-2.5,-1.5] band it is +0.49% (t 2.38, n 662, hit 61%). Days with no move average 0.01% (t 0.13, n 6729), and up moves above +0.5 sd average about 0% (hit 42–46%).
- F2: The down-day rebound holds in all six coins, at +0.29% to +0.83% next day (t 1.64 to 4.68, hit 55–61%, n 577–653 each). It is positive in every year, from +0.11% to +1.20%, and is significant in 2018, 2020, 2021 and 2023. Over non-overlapping 3-day spans, down days are followed by +0.93% (t 3.39, n 1172) against +0.21% (t 1.76, n 4551) for other days.
- F3: Where the close sits in the day's range predicts the next day in order. Closes in the bottom fifth of the range are followed by +0.50% (t 5.03, n 2655, hit 57.7%), and closes in the top fifth by -0.10% (t -1.21, n 3735, hit 44.8%). Among down days, those closing in the bottom third rebound +0.55% (t 5.71, n 2675). The 56 down days that closed in the top third show no rebound (-0.83%, t -1.15).
