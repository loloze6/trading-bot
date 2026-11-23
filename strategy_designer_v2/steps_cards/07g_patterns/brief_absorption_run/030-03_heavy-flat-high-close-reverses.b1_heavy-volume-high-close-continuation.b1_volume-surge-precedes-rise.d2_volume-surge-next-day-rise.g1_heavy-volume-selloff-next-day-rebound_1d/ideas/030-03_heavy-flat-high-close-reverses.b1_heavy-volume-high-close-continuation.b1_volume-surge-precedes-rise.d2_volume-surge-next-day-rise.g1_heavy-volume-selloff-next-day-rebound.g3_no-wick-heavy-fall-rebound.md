---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of a day's fall that remains at the close, measured as how small the lower wick is against the day's range, the more the coin rises over the next day. This holds on down days whose volume is heavy against the prior 20-day average, and more so when 20-day volatility is high.
Consequence: A trader buys for one day after heavy-volume down days with no intraday bounce, and skips the ones already bought back within the day.
Why:
- F2: The same pattern shows in the lower wick. Heavy down days in the smallest lower-wick tercile (close near the low, no buying-back intraday) gave +0.90 % next-day excess (t 5.19, n 950). The middle and largest wick terciles gave only +0.17 % (t 1.01) and +0.17 % (t 0.87).
- F1: Among down days on volume at or above the prior 20-day mean, where the close sat in the day's range sorts the next day sharply. Closes in the lowest third of the range were followed by +0.64 % excess (t 4.81, n 1553). Middle-third closes gave +0.23 % (t 1.21, n 955) and top-third closes gave −0.26 % (t −0.84, n 210). Light-volume down days closing low gave −0.02 % (t −0.19, n 2388). The tested idea's rebound is therefore carried by heavy down days that close near their low, which the idea does not name.
- F3: Among the bottom fifth of daily returns, the next-day excess grows with the volume ratio: +0.02 % (t 0.09), +0.42 % (t 2.17), +0.32 % (t 1.66) and +1.14 % (t 4.66) from the lowest to the highest quartile, about 725 cases each. It also grows with 20-day volatility on heavy days: −0.08 % (t −0.37), +0.35 % (t 1.72) and +1.54 % (t 5.25) from the low to the high tercile. This repeats the tested idea's grading.
