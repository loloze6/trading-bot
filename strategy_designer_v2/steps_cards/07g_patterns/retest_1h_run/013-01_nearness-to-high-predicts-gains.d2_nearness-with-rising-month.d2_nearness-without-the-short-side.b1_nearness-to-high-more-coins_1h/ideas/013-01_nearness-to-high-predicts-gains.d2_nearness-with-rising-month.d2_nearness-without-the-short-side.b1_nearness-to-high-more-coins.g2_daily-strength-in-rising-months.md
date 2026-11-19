---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its 1-day return, the higher its return over the next 7 days.
Consequence: Inside a rising month, a strong last day is a reason to add to the long rather than fade it.
Why:
- F4: While the 30-day return is positive, a higher 1-day return predicts a higher 168-bar excess return. The top 1-day-return quintile earns +0.0321 (t = 3.14, n = 320) against +0.0016 in the bottom quintile. In a joint regression with volume ratio and distance from the high, the slope is +0.0095 per standard deviation (t = 2.38, n = 1598).
- F5: The book's forecast is graded at the top but not at the bottom. The highest forecast quintile earns +0.0303 (t = 3.76) in 168-bar excess return, while the lowest positive quintile earns -0.0115 (t = -1.71). Grid bars with the book flat earn -0.0065 against +0.0069 with a forecast above zero.
