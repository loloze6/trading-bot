---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
line: 7.g patterns
backtest: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's daily up move relative to its 20-day volatility of daily returns, the more the coin rises over the next 5 days, most clearly while the coin's 20-day return is positive.
Consequence: A trader would lean long for several days after an unusually strong up day, and would refuse to short into it.
Why:
- F4: On the 5-day grid, a strong up day predicts a further rise, graded by its size in units of 20-day volatility. The next 5 days average -0.022 usual moves after days within ±1 sigma (t -1.05, 2072 cases), +0.126 after 1–2 sigma up days (t 2.25, 286) and +0.222 after days above 2 sigma (t 1.82, 94). Down days of any size show nothing (−2 sigma or worse: +0.046, t 0.45).
- F5: The continuation after strength depends on the period. Up days above 1 sigma give +0.273 usual moves (t 3.11, 163 cases) in 2018–21 but only +0.058 (t 0.93, 217 cases) in 2022–25. Breakout cases give +0.278 (t 3.41) in 2020, +0.438 (t 3.39) in 2021 and +0.221 (t 2.14) in 2024, against −0.234 (t −2.33) in 2022.
- F1: Closes above the prior 20-day closing high are followed by a rise, which is the opposite of the brief: over 799 non-overlapping breakout cases, the 5-day unusual move is +1.34 % (t 3.13) and the total move +1.93 % (t 4.49), about 10 times the 0.19 % cost of a trade. Fresh first-day breakouts alone show the same, mean 0.130 usual moves (t 3.20, 708 cases).
