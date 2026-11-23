---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's high-low range on a day compared with its average daily range over the past 20 days, the larger the coin's rise above its normal drift over the next 5 days, and more so when that wide day closed higher than it opened.
Consequence: A trader should lean long a coin after an unusually wide day, sized by how wide it was against its recent range, and refuse longs after unusually narrow days, which trail the coin's drift.
Why:
- F1: The day's high-low range relative to its 20-day average is the strongest pattern in the bars, and the tested idea does not explain it: over 4334 non-overlapping 5-day cases its pooled slope on the next 5-day strength is +0.055 per standard deviation (t 3.68). It stays at +0.055 (t 3.68) next to the 5-day return and the forecast, while the forecast keeps its own +0.037 (t 2.47).
- F2: The range effect is graded and large next to cost. The top two range deciles end +1.48 % and +1.39 % above the coin's normal 5-day drift (strength +0.136 and +0.130), against −0.88 % and −0.77 % in the bottom two. That move above drift is about 6 times the 0.22 % cost of a trade, where the tested idea's unusual move is −0.07 % per case.
- F3: The range effect holds across time and coins: its slope is positive in 6 of 8 years (t 2.32 in 2022, 3.35 in 2024, 2.05 in 2025, negative only in 2018 at t −1.02 and 2023 at t −0.16) and positive in 12 of 15 coins (AVAX t 2.57, DOGE t 2.25).
- F4: The range effect is stronger after a wide day that closed up, with a slope of +0.082 (t 3.36, 2144 cases), than after one that closed down, with +0.035 (t 1.92, 2190 cases).
