---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the smaller the percent by which its daily close sits below its highest close of the past 52 weeks, the lower its return over the next 7 days.
Consequence: In a falling month, the nearer a coin still trades to its yearly high in plain percent terms, the stronger the case to lighten or short it rather than buy.
Why:
- F1: The tested forecast is the distance below the 52-week high standardised over its own past year, not the distance itself, and on the 1177 falling-month 7-day cases it correlates only -0.42 with the raw percent distance, so the test graded the cases differently from the idea's "how close to the high".
- F2: Graded by the raw percent distance below the 52-week high, the 7-day excess return falls as the close nears the high (pooled slope -0.000229 per point, t -1.43, n 1177), and the nearest third earned -0.0113 against -0.0011 for the farthest third, a difference of -0.0102.
- F3: The raw-distance slope is negative in all 8 years (2018 to 2025) and reaches t -3.04 in 2019, -2.26 in 2022 and -2.07 in 2025, with n between 109 and 197 per year; it is also negative in 5 of the 6 coins, the strongest being XRP at t -1.76 (n 199). The effect is consistent in direction but small next to its noise.
