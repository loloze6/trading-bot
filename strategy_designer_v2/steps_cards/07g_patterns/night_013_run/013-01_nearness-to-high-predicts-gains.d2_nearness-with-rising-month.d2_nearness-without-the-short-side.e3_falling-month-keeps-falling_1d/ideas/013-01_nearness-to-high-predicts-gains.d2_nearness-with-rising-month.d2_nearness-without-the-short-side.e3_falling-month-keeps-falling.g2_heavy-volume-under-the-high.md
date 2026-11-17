---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin closes to its own 30-day high on a day of heavy volume relative to its 30-day average, the higher its return over the next 3 days.
Consequence: A coin pressing its monthly high on heavy volume is a reason to take a long over the next few days rather than fade the high.
Why:
- F3: Nearness to the 30-day high predicts in single sorts but not on its own. The top quintile's excess 3-day return is +0.0073 (t 2.89, 1061 cases) and the second quintile's is -0.0068 (t -2.83). Inside the regression with volume and the 7-day return its t falls to 0.77, and in windows w1-12 the top-minus-rest is only +0.0034 (t 1.04).
- F4: Near the high, heavy volume and the high go together. The cell nearest the high with the heaviest volume tercile has an excess 3-day return of +0.0120, while the other heavy-volume cells are +0.0022 and +0.0026. The interaction itself is only t 1.57.
- F5: Closes above the prior 30-day high show weak follow-through. They have a mean excess 3-day return of +0.0142 (t 2.25, 217 cases), and 69% are still above that high 3 days later. Low-volume breakouts give -0.0032, against +0.033 and +0.012 in the middle and heavy terciles, but with 72 cases per tercile.
