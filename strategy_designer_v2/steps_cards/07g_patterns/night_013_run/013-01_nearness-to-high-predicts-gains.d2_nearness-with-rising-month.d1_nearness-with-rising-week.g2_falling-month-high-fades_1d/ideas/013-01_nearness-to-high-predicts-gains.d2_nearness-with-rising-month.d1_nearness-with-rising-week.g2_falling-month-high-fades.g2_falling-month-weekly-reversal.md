---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the larger its 7-day return, the lower its return over the next 7 days.
Consequence: In a falling month, a sharp one-week bounce is a reason to lighten or short rather than chase it.
Why:
- F3: When the 30-day return is negative, the same 7-day return slope turns negative (-0.0081, t -1.93, n 789). Short-term moves tend to continue in rising months and partly reverse in falling months, which is a split the tested distance-from-high forecast does not capture.
- F1: When the coin's 30-day return is positive, its 7-day return predicts its next 7-day excess return. The pooled slope is +0.0150 per standard deviation with t 3.33 over 888 non-overlapping cases. Quintiles of the 7-day return run from -0.011 in the weakest to +0.020 and then +0.040 (t 2.94) in the strongest, so the effect is graded and sits mostly in the top two fifths.
