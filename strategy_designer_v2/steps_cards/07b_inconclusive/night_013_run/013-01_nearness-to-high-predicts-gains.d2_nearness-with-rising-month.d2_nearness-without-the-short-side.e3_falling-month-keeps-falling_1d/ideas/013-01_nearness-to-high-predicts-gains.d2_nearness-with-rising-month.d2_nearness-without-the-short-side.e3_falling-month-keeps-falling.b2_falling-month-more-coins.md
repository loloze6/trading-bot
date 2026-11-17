---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: The more negative a coin's 30-day return, the lower its return over the next 3 days.
Consequence: A coin with a falling month is a reason to refuse a long trade over the next few days, more firmly the deeper the fall.
Why:
- F1: The test's main measure is on the side the idea predicts, but it is weak: the mean short gain over holding is 0.00194 with t = 1.29 over 2881 independent 3-day cases, and it varies widely across windows, from t = -1.82 in w10 to t = 2.07 in w2. By year it ranges from t = 1.96 in 2018 to t = -1.76 in 2023.
- F2: The level of the effect exists but its grading does not. Falling-month cases have a lower excess 3-day return than flat-or-rising cases (-0.0030 vs 0.0031, Welch t = -2.75). But depth within falling months does not order the outcome: the Spearman correlation of forecast with excess return is -0.006, and the deepest forecast quintile has a positive excess (+0.0025, t = 0.79) while q2 to q4 are negative (-0.0069 to -0.0048). This is why the supporting check fails (deep minus shallow = +0.0016).
