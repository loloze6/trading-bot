---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits far below its 200-day average (forecast at or below -15), the coin tends to rise over the next 10 bars, more than after bars at or above the average.
Consequence: A trader would refuse new shorts deep below the 200-day average and would consider buying there instead.
Why:
- F1: The deepest short zone does not continue falling, it rebounds. Bars with forecast ≤ -15 are followed by a mean 10-bar coin return of +3.57% (t 7.73, 59.5% up) and a next-day return of +0.45% (t 3.24). That is more than the +1.58% after flat bars (forecast 0, t 7.72), and the short book is positioned against this rebound.
- F7: Shallow-entry short trades are not better. Trades entered at forecast ≤ -15 average -5.24% net, against -2.89% to -4.66% for shallower entries, with a median of about -4.4% in every entry bucket.
- F8: The book's worst days follow sharp upside reversals while it is deeply short. On its 171 worst days (mean book return -19.3%), the coin rose +12.7% that day, with mean allocation -1.31 and SMA distance -32%. Its 171 best days came on -11.1% coin days after a -21.7% 10-day slide, at distance -46%.
