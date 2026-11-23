---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower its power over the following 90 days. The larger both the excess past power and today's deviation of nearness from its usual level, the larger the coin's move against the past relation over the next 5 days.
Consequence: A trader should size a nearness-power-reversal trade by the joint size of excess power and nearness deviation, so that the fees go only to the readings large enough to cover a trade.
Why:
- F5: The gain sits in the strongest forecasts:
- F2: The losses come from the short side. Bars held short earn -0.033 % per bar (10,664 bars), while bars held long earn +0.119 % per bar (11,964 bars), and the book is short on 44 % of its coin-bars.
