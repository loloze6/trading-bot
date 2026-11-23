---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower its power over the following 90 days. The larger both the excess past power and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a rise, the larger the coin's fall over the next 5 days, only while the coin's 20-day return is negative and its 5-day return is positive.
Consequence: A trader should short the nearness-power reversal only on bounces inside a 20-day fall, sized by the joint reading, and refuse these shorts when the coin is still falling over the last 5 days.
Why:
- F3: The effect sits in coins that rose over the 5 days before the signal inside their 20-day fall. Those 269 cases fall +2.04 % more than the coin's drift (t 3.53, weighted t 3.16, strength 0.18). The 430 cases after a falling 5 days show +0.08 % (t 0.17, weighted t −0.30). Inside the rising-5-day cases the above-median readings fall +0.84 % more than the below-median ones (t 0.72).
- F1: The main measure is on the side the idea predicts but short of the bar (weighted t 1.50 over 699 cases), and it is weaker than the unweighted excess fall, whose mean is +0.83 % per 5 days with t 2.24. Weighting by |forecast| removes signal instead of adding it, because the move is not graded: the Spearman correlation of |forecast| with the excess fall is −0.015, and the supporting check is −0.40 % (t −0.53).
- F6: The plan's 5-day horizon is where the effect is clearest. Unweighted t is 2.17 over 1 day, 1.76 over 3 days, 2.24 over 5 days, 1.52 over 10 days and 0.35 over 20 days. Strength is 0.07 over 5 days.
