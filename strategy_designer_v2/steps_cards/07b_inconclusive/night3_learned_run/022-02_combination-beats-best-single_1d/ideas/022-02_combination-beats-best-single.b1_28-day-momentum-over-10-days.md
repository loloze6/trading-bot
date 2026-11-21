---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 10 days.
Consequence: A trader would lean long a coin after a strong 28-day rise and short after a deep 28-day fall, and hold each bet for about 10 days, without re-weighting by recent predictive power.
Why:
- F3: What each signal predicts does not carry from one year to the next: the year-by-year 5-day correlation of closeness to the 90-day high has a -0.38 correlation with the previous year's, the 1-day return's -0.17, the 30-day volatility's 0.06. A weighting learned on the past 365 days is therefore re-weighting noise.
- F4: The 28-day return alone lines up with the coming return, more clearly at 10 days than at 5: correlation 0.059 (t 2.9, 2,432 cases) over 5 days, 0.086 (t 3.0, 1,199 cases) over 10 days, 0.026 (t 0.6, 514 cases) over 20 days. Over 5 days its top fifth ends 0.86 % above the drift (strength 0.073) and its bottom fifth 0.49 % below it, against a round trip of 0.19 %.
- F5: The 28-day return's effect depends on the period: its 5-day correlation is -0.22 in 2018, -0.12 in 2022 and 2023, and +0.12 and +0.19 in 2024 and 2025. Across coins it ranges from -0.05 (XMR) to +0.12 (ZEC). A single signal held fixed is steadier than the learned weights (year-to-year persistence +0.27), but it is not uniform.
