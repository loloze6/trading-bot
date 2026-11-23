---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's daily high-low range is relative to its average range over the past 30 days, the higher that coin's return over the next 5 days, while the coin's own 20-day return is negative.
Consequence: A trader should read a sharply widened daily range in a falling coin as a reason to buy for the next 5 days, rather than as a sign that the fall will continue.
Why:
- F2: The effect is as large in falling coins (20-day return ≤ 0), which the tested idea leaves out. There the upper half earns +0.38 % against −1.06 % for the lower half, a difference of 0.0144 with Welch t 3.24 on 3074 cases, positive in 19 of 19 coins and 6 of 8 years. It is graded by quintile (−0.72 %, −1.32 %, −1.26 %, +0.44 %, +1.15 %, top quintile t 2.66), and it matches the uptrend difference (0.0149, t 2.89, 17 of 19 coins).
- F3: In falling coins the day's direction does not matter. Wide-range down days and wide-range up days end the next 5 days alike (+0.41 % vs +0.38 %, difference 0.0003, t 0.05). The down-day top range quintile earns +1.44 % (t 2.45, mean ratio 2.09), and the up-day top two quintiles earn +0.83 % and +0.60 % (t about 1.0).
- F4: The falling-coin effect is uneven over time. Its yearly Spearman is 0.29 in 2024, 0.17 in 2025, 0.14 in 2021 and 0.08 in 2022, but −0.03 in 2018 and −0.01 in 2023, so it rests mostly on recent years.
- F1: Across all bars, whatever the trend, the range ratio (the day's high-low range over its 30-day mean) separates the next 5 days clearly: the upper half's mean excess 5-day return is +0.89 % and the lower half's is −0.89 %, a difference of 0.0178 with Welch t 5.22 on 6046 non-overlapping cases; the sign is positive in 19 of 19 coins and in 6 of 8 years (Spearman 0.091).
