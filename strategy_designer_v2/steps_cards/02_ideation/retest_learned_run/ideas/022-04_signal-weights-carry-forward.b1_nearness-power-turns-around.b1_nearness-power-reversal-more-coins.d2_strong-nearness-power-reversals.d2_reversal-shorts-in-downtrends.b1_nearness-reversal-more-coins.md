---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower its power over the following 90 days. The larger both the excess past power and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a rise, the larger the coin's fall over the next 5 days, only while the coin's 20-day return is negative.
Consequence: A trader should short the nearness-power reversal only on coins already falling over 20 days, sized by the joint reading, and stay out of these shorts in rising coins.
Why:
- F1: The main measure is on the side the idea predicts but short of the bar (weighted t 1.50 over 699 cases), and it is weaker than the unweighted excess fall, whose mean is +0.83 % per 5 days with t 2.24. Weighting by |forecast| removes signal instead of adding it, because the move is not graded: the Spearman correlation of |forecast| with the excess fall is −0.015, and the supporting check is −0.40 % (t −0.53).
- F5: A few large rallies drown the effect. Dropping the 2 % tails on each side lifts the 5-day t from 2.24 to 2.99 (weighted t from 1.50 to 2.71, 671 cases). 17 of 24 windows (71 %) and 11 of 15 coins have a positive mean excess fall.
