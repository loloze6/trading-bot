---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its 60-day high, the higher its return over the next 7 days, whatever its 30-day return.
Consequence: Closeness to the recent 60-day high is a reason to hold a coin long even before its 30-day return turns positive.
Why:
- F4: Over all bars, regardless of the 30-day regime, closeness to the 60-day high orders the next 7 days: the nearest quintile (median gap 0.8 %) earns +1.66 % excess (t 2.85, n 728), while the quintiles with median gaps of 25 % and 15 % earn -1.18 % (t -2.83) and -1.11 % (t -2.60).
- F1: The 7-day moves after a falling month run below the coin's own average, which the idea does not explain because it only says to stand aside there: on bars with a 30-day return at or below 0, the mean excess 7-bar return is -0.79 % (t -3.10, 2244 non-overlapping cases), against +0.83 % (t 2.66, 2157 cases) on the active bars.
