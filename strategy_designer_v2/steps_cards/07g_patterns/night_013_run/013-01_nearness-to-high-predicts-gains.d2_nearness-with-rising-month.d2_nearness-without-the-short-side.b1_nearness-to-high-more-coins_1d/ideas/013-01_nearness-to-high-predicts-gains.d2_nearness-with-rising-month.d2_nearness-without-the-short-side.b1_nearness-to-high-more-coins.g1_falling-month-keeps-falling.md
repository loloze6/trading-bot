---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the further its close sits below its 60-day high, the lower its return over the next 7 days relative to its own average, through the range of ordinary declines.
Consequence: A coin in a falling month that has slid well below its recent high is a candidate for a short or a reduced long, rather than only for standing aside.
Why:
- F1: The 7-day moves after a falling month run below the coin's own average, which the idea does not explain because it only says to stand aside there: on bars with a 30-day return at or below 0, the mean excess 7-bar return is -0.79 % (t -3.10, 2244 non-overlapping cases), against +0.83 % (t 2.66, 2157 cases) on the active bars.
- F2: Inside that falling-month state, the shortfall sits in the middle of the decline, not at its extreme. By per-coin quintile of the 30-day return, the mean excess 7-bar return is +0.48 % (t 0.59, n 314) for the deepest falls (median -33 %), -2.22 % (t -3.76, n 301) and -2.15 % (t -3.15, n 302) for falls with medians of -22 % and -15 %, and -1.06 % (t -1.58, n 308) for the mildest (median -3 %). The distance below the 60-day high gives the same shape: +0.81 % (t 1.10) at the deepest gap, -2.03 % (t -3.12) and -1.74 % (t -3.00) at gaps with medians of 36 % and 27 %.
- F4: Over all bars, regardless of the 30-day regime, closeness to the 60-day high orders the next 7 days: the nearest quintile (median gap 0.8 %) earns +1.66 % excess (t 2.85, n 728), while the quintiles with median gaps of 25 % and 15 % earn -1.18 % (t -2.83) and -1.11 % (t -2.60).
