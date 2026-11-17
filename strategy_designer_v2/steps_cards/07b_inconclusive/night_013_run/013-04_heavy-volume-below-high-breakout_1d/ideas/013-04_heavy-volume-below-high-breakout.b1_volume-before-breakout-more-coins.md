---
brief: 013_anchoring-to-recent-high
source-idea: 013-04_heavy-volume-below-high-breakout
line: 7.b inconclusive
backtest: 013-04_heavy-volume-below-high-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 52-week high, the heavier its volume over the preceding 10 days, relative to its own 90-day average, the larger its return over the next 30 days.
Consequence: Anchored selling shows as heavy volume just under the high, and once that supply is absorbed the price moves more easily after the break.
Why:
- F1: The tested measure lands on the predicted side but just short of the bar: over 50 de-duplicated breakout events (25 per half), the top-forecast half beats the bottom half by +0.273 in 30-day excess return, Welch t 1.99, and the quartile means climb in order: -0.060, -0.028, +0.169, +0.283.
- F2: The gap rests on a few large top-half events rather than a broad shift. The top half's spread is far wider (std 0.644 vs 0.239, max +2.31), its median is only +0.047 vs -0.032, and dropping its single largest event cuts the Welch t to 1.69. A rank test shows the same weakness: Mann-Whitney p 0.23, Spearman 0.17.
- F4: Within coins, the top half beats the bottom half in 5 of 6 coins: BTC 0.145 vs 0.031, ETH 0.112 vs 0.090, LTC -0.056 vs -0.200, XRP 0.403 vs -0.194, ZEC 0.712 vs -0.287. The only exception is XMR, with a single top event. Each coin has only 5 to 16 events, so the test is limited by too few breakouts, and more coins would add more.
