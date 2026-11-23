---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower its power over the following 90 days. The larger both the excess past power and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a rise, the larger the coin's fall over the next 5 days, only while the coin's 20-day return is negative.
Consequence: A trader should short the nearness-power reversal only on coins already falling over 20 days, sized by the joint reading, and stay out of these shorts in rising coins.
Why:
- F1: The book loses on its short side and earns on its long side. Bars held short gained −0.043 % a bar (10,133 bars, mean allocation 0.39), while bars held long gained +0.124 % a bar (11,104 bars, mean allocation 0.46), with fees of only 0.006 % a bar on each side. The short side's loss comes from the coins' rise, not from a missing effect: on the 5-day grid the unusual move is almost the same on both sides (shorts +0.40 %, t 1.74, n 2275; longs +0.37 %, t 1.73, n 2454), but the total move is −0.34 % for shorts and +1.09 % for longs.
- F3: The short side works only while the coin's 20-day return is negative. In a downtrend the short cases' unusual move is +0.85 % over 5 days (t 2.59, n 822). In an uptrend it is −0.11 % (t −0.31, n 1082). The condition alone is not the effect: trading the sign of the 20-day return without the signal gives only +0.26 % (t 1.50), and signal and trend agreeing give +0.59 % (t 2.39, n 1728). The long side holds in both trends (+0.35 % in uptrends, +0.11 % in downtrends).
