---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's daily high-low range is relative to its 20-day volatility on a day it closes higher, the larger its rise over the next 5 days.
Consequence: A trader would lean long a coin after an unusually wide up day, more so the wider the day, and would refuse shorts there.
Why:
- F1: The wider a coin's daily range relative to its 20-day volatility, the larger its drift-removed rise over the next 5 days: Spearman rho +0.083 (t about 5.4, 4177 non-overlapping cases). The top range quintile gains +1.28 % beyond drift (t 3.22), while the bottom three quintiles sit between -0.55 % and -0.75 %. Rho is positive in all 16 coins and in 6 of 8 years.
- F2: The range effect comes from days that close up. In the top range quintile, up days are followed by +2.29 % beyond drift over 5 days (t 3.29, 385 cases), while down days are followed by only +0.41 % (t 1.05, 454 cases). Lower range quintiles stay near -0.5 % to -0.8 % whichever way the day closed.
