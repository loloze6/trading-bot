---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The more negative a coin's 30-day return, the lower its return over the next 3 days, only while its 60-day return is positive.
Consequence: A coin whose month turns down while its two months are still up is a reason to refuse a long over the next few days, more firmly the deeper the monthly drop.
Why:
- F4: The graded effect shows clearly only when the coin's 60-day return is still positive, that is, a down month inside a rising two months. There the short gain is 0.00855 (t = 2.99, n = 323), and the excess 3-day return falls with the depth of the forecast: deep tercile -0.0278 (t = -3.19), mid -0.0148 (t = -2.05), shallow -0.0005 (t = -0.07).
- F5: When the 60-day return is down, the short gain is 0.0016 (t = 0.52, n = 1038), with deep-half excess -0.0020 against shallow-half +0.0017. The plan's measure is therefore diluted by the majority of cases, where the effect is absent.
- F2: The level of the effect exists but its grading does not. Falling-month cases have a lower excess 3-day return than flat-or-rising cases (-0.0030 vs 0.0031, Welch t = -2.75). But depth within falling months does not order the outcome: the Spearman correlation of forecast with excess return is -0.006, and the deepest forecast quintile has a positive excess (+0.0025, t = 0.79) while q2 to q4 are negative (-0.0069 to -0.0048). This is why the supporting check fails (deep minus shallow = +0.0016).
