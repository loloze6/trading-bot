---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall on the day, measured against its typical daily move over the past 20 days, the more it rises over the next 1 to 2 days.
Consequence: A trader should read a large one-day fall, relative to recent volatility, as a reason to be long for the next day or two, not to cut exposure.
Why:
- F1: Across all 6 coins, a day's fall measured against the coin's past-20-day daily volatility is followed by a next-day rebound that grows with the size of the fall. On down days, the slope of the next-day excess return on that standardised move is negative for every coin. It is significant on three: XMR (t −3.88, 1247 cases), XRP (t −2.71, 1326) and ZEC (t −2.08, 1328).
- F2: The rebound after falls holds on non-overlapping 2-day stretches: slope −0.0047, t −2.83 over 3885 cases. The next-day excess return is +0.69 % after a fall of 1 to 1.5 standard deviations and +0.75 % after a fall beyond 2. Both are several times this backtest's 0.19 % round-trip cost. After falls of under half a standard deviation it is −0.06 %. With cases averaged by date, the 1 to 1.5 band keeps t 2.95, while the beyond-2 band drops to t 1.48, so part of the effect is shared across coins on the same days.
- F3: The rebound after falls is not steady over time. It is strong in 2020 (t −4.23), 2021 (t −3.91) and 2018 (t −2.25), and close to zero in 2022, 2023 and 2024 (t from −0.77 to +0.04). On up days there is no such effect, except for XRP (t +3.05, with the opposite sign: continuation).
- F4: The book cuts its position just before these rebounds. Its average allocation is 0.46 after falls of under half a standard deviation and 0.35 after falls beyond 2 standard deviations, which are the days followed by the largest next-day excess return.
