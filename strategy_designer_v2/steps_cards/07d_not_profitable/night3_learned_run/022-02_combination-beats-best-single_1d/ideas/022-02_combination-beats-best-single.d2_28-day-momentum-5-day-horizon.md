---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 5 days.
Consequence: A trader leans long a coin after a strong 28-day rise and away from it after a weak one, holding about 5 days, since the edge is gone by 20 days.
Why:
- F3: The best-single score does no better, with a correlation of -0.034. The 365-day correlation weights trail effects that flip from year to year. The 28-day return's correlation with the next 5 days was -0.22 in 2018, -0.12 in 2022 and 2023, and +0.12 and +0.19 in 2024 and 2025. Weights learned on the previous year are therefore often of the wrong sign.
- F5: Taken alone, the coin's 28-day return carries a move larger than the cost, but it is not yet confirmed.
