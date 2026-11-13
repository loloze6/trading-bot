---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-03_deep-month-loss-rebound
line: 7.b inconclusive
backtest: N2-03_deep-month-loss-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin has fallen more than about 20% over 20 days and is still falling over its last 5 days, closing in the bottom quarter of its 20-day range, it rises over the next 20 days by more than its usual 20-day move.
Consequence: A trader buying deep monthly falls should buy only while the fall is still running near its low, and refuse falls that have already bounced or are shallower.
Why:
- F3: The rebound is limited to falls that are still running: top-decile bars whose last 5 days were also down give +4.1% (hit 58%, t 1.98, n 88), while those that had already turned up over 5 days give −0.1% (t −0.05, n 20).
- F4: The rebound also needs the close to sit near the bottom of its 20-day range: with the close in the lowest quarter of the high-low range it is +5.8% (n 24) and +6.2% (t 1.87, n 35), against +0.1% (t 0.04, n 36) higher in the range; with the close within the lowest third of distance from its 5-day low it is +5.4% (t 2.02, n 32).
- F5: Raw depth splits the result in two directions: across all non-overlapping bars, 20-day falls deeper than 20% are followed by +3.5% (n 38) and +3.9% (n 65) excess, but falls of 10–20% are followed by −5.1% (hit 34%, t −2.36, n 88).
- F2: The effect depends heavily on the period: top-decile excess is +13.7% in 2020 (t 3.5, n 9), +7.9% in 2022 (t 2.25, n 22) and +10.5% in 2023 (t 2.06, n 10), but −6.3% in 2018 (t −1.22, n 20) and −5.3% in 2024 (t −1.37, n 11); among windows, 15 of 22 have a positive mean.
