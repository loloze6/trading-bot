---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is lower than usual, the larger its 28-day return, the larger its return over the next 5 days in the same direction.
Consequence: Four-week momentum is a reason to bet in calm markets and a reason to stand aside in turbulent ones.
Why:
- F4: The momentum slope fades as the coin's 20-day volatility rises: t 2.68 in the calmest tercile, 1.97 in the middle one and 0.80 in the most volatile (about 860 cases each). The book's Sharpe is 0.91 and 0.98 in the two calmer market-volatility terciles and 0.38 in the most volatile.
- F6: The book's failed Calmar comes from 2022 and 2023, when it earned -1.8 and -4.5 bps a day (Sharpe -0.19 and -0.54), while holding the coins had a Sharpe of 1.18 in 2023. In 2020 it earned 26 bps a day (Sharpe 1.99).
