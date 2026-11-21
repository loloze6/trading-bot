---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue
line: 7.g patterns
backtest: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is low against its own recent history, the larger its 28-day rise relative to its usual 28-day moves, the more the coin rises over the next 5 days.
Consequence: A trader would ride a coin's strong month-long rises in calm markets and stand aside from them when the coin is turbulent.
Why:
- F2: The tested forecast predicts only outside high volatility. Its 5-day slope has t 2.73 in the calmest third of 20-day volatility and t 2.56 in the middle third, with 1044 and 1043 cells. In the most volatile third it has t 0.18, and the cases with a positive forecast lost 0.62 % against the drift (485 cases). In the most volatile fifth, positive-forecast cells lost 1.12 % (281 cells).
- F3: The forecast's 5-day slope changes sign from year to year: t -1.34 in 2018, -2.17 in 2023, +2.35 in 2020, +2.35 in 2024 and +2.88 in 2025, with about 426 cells each. The confirmed effect does not hold steadily through time.
