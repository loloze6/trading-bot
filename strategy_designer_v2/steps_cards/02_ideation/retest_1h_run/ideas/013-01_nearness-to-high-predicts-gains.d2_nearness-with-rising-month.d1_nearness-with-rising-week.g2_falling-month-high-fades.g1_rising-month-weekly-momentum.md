---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its 7-day return, the higher its return over the next 7 days.
Consequence: In a rising month, a coin's strongest recent week is a reason to add or hold a long rather than fade it, and a weak week is a reason to stay out.
Why:
- F1: When the coin's 30-day return is positive, its 7-day return predicts its next 7-day excess return. The pooled slope is +0.0150 per standard deviation with t 3.33 over 888 non-overlapping cases. Quintiles of the 7-day return run from -0.011 in the weakest to +0.020 and then +0.040 (t 2.94) in the strongest, so the effect is graded and sits mostly in the top two fifths.
- F2: This momentum inside rising months has a positive slope in all six coins, but only XRPUSD (t 2.29) and ZECUSD (t 2.65) are significant on their own. It is positive in 6 of 8 years (2022 t 3.08, 2024 t 2.71, 2025 t 4.99), and 2023 goes the other way (t -2.54).
- F3: When the 30-day return is negative, the same 7-day return slope turns negative (-0.0081, t -1.93, n 789). Short-term moves tend to continue in rising months and partly reverse in falling months, which is a split the tested distance-from-high forecast does not capture.
