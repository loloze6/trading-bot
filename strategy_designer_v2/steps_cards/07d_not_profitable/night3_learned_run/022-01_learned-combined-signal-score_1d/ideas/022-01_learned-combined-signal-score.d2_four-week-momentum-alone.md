---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 5 days.
Consequence: Lean long a coin in proportion to its 4-week rise, and refuse shorts that bet against a strong 4-week rise.
Why:
- F5: The book falls behind holding in every year the coins rose: in 2020, -0.17 % a day against +0.42 %; in 2021, -0.04 % against +0.41 %. It beats holding only in the two falling years, 2018 (+0.08 % against -0.39 %) and 2022 (+0.01 % against -0.18 %).
- F6: Taken alone, with its usual direction, the 28-day return is the largest single effect. Its top fifth is followed by a +1.11 % excess 5-day move (strength 0.104, t 1.98, 490 cases) and a +1.79 % total move, about 9 times the 0.19 % round-trip cost.
- F7: That momentum effect is not stable across years either. Its top-minus-bottom-fifth spread is positive in 4 of 8 years (2019 to 2021 and 2025, +2.3 % to +4.8 %) and negative in the other 4 (2018 -5.9 %, 2022 -2.8 %, 2023 -2.7 %, 2024 -0.1 %).
