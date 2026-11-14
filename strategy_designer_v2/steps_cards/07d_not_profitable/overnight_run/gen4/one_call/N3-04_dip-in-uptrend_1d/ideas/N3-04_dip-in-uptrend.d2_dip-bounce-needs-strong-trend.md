---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-04_dip-in-uptrend
line: 7.d not profitable
backtest: N3-04_dip-in-uptrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A daily drop in a coin is followed by a rebound when the coin's 20-day return sits clearly above zero, in the upper part of its range. The rebound is absent when the 20-day rise is marginal, as in a falling year.
Consequence: A trader should take dip buys only when the coin's own 20-day rise is strong and refuse them when the uptrend is barely positive.
Why:
- F4: The edge is regime-dependent by year. After forecast > 0 bars, the next-day coin return was -1.59% in 2018 (n=99, t=-1.99) and -0.40% in 2022 (n=150, t=-1.01), the two years the coins fell (mean daily coin return -0.35% and -0.18%). In 2019–2021 it was +0.61% to +1.09% with t between 2.0 and 4.6.
- F5: Within the active days, the book earns little when the 20-day trend is weakest: +0.10% per day (n=715, t=0.78), against +0.65% (t=3.13) and +0.74% (t=2.63) in the middle and strongest 20-day-return terciles. Calm days are also weak, at +0.14% (n=780, t=1.34), against +0.67% and +0.78% in mid and volatile days.
