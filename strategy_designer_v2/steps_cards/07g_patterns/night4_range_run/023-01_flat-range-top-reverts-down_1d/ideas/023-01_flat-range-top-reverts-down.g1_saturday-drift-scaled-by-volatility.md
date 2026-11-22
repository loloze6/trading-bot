---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin rises from Friday's daily close to Saturday's daily close, and the rise is larger the higher the coin's 20-day volatility.
Consequence: A trader would hold the coin long over Saturday, and hold more when its recent volatility is high, and would refuse a short across that day.
Why:
- F1: Saturday is the one day that stands out across all seven weekdays: the coins' daily return from Friday's close to Saturday's close, averaged over the six coins each day, is +0.454 % with t 3.04 on 414 days (no other weekday reaches t 2 on that coin-averaged series), and against all other days the Welch t is 4.26.
- F2: The Saturday rise holds coin by coin and year by year: its mean is positive in all six coins (ETH 0.40 % t 2.40, LTC 0.57 % t 2.92, XMR 0.45 % t 2.57, XRP 0.57 % t 2.15, ZEC 0.58 % t 2.30, BTC 0.16 % t 1.40; 414 days each), and positive in 7 of 8 years, with t above 2.7 in 2019, 2020, 2024 and 2025, near 0 in 2022 (0.07 %) and 2023 (−0.001 %).
- F3: The Saturday rise is larger in the more volatile half of each coin's 20-day volatility (0.45 % t 2.74 and 0.47 % t 1.74 in the top two quartiles, 0.29 % and 0.23 % in the bottom two, about 522 days each), so the grading is loose and not monotone; the 20-day window includes Saturday's own bar, so this ordering is weak evidence.
