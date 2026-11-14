---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-03_deep-month-loss-rebound
line: 7.b inconclusive
backtest: N2-03_deep-month-loss-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin has fallen deeply over 20 days, its next 20-day return beats its usual move only in the periods when Bitcoin is also rebounding, so the coin's rise follows the market's bounce rather than its own.
Consequence: A trader should judge a deep-fall long by the market's rebound and expect no gain over simply holding Bitcoin.
Why:
- F1: The top-decile rebound is mostly the whole market bouncing, not the coin itself: the mean excess over the coin's own 20-bar mean is +3.3% (median +1.5%, hit 56%, t 1.85, 108 non-overlapping episodes), but against BTC's forward 20-bar return over the same bars it is −0.15% (hit 44%, t −0.10, 91 episodes), and the coin's forward return correlates 0.72 with BTC's.
- F2: The effect depends heavily on the period: top-decile excess is +13.7% in 2020 (t 3.5, n 9), +7.9% in 2022 (t 2.25, n 22) and +10.5% in 2023 (t 2.06, n 10), but −6.3% in 2018 (t −1.22, n 20) and −5.3% in 2024 (t −1.37, n 11); among windows, 15 of 22 have a positive mean.
