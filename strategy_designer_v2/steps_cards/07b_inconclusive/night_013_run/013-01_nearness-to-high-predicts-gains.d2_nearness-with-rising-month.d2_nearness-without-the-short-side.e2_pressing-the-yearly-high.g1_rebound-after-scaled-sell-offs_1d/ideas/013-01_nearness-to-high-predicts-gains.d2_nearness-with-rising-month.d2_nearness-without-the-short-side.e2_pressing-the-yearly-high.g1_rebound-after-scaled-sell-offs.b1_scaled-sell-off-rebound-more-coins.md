---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall measured in units of its own 30-day daily volatility, the larger its rebound over the next 3 days.
Consequence: A trader would buy a coin's sharp volatility-scaled sell-off, sized up with the depth of the fall, rather than treat a collapse as the start of further decline.
Why:
- F1: The test's own result is on the predicted side but short of the bar: the 3-day slope is +0.000164 (t 0.90) over 5,723 grid bars, the 2,718 bars with a forecast above 0 have a mean excess return of +0.00065, and the 6 default coins used are only part of the 19 coins available.
- F5: At 3 days the signal is drowned by noise. The standard deviation of the excess return is 0.088 against a mean of 0.00065, the forecast quintiles go up and down with no order (-0.0051 to +0.0051), coin t's range from -0.59 to 1.51, and year t's from -1.70 to 2.69.
