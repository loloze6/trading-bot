---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the higher its daily volume relative to its own 20-day average volume, the higher its return over the next 3 days.
Consequence: A rising coin trading on unusually heavy volume is a reason to be long for the next few days, and a rising coin on thin volume is a reason to refuse the trade.
Why:
- F1: The main measure falls on the side the idea predicts but just short of the bar: the pooled 72-hour slope is +0.000469 with t 1.90 on 2,837 trending grid cases (1,190 with a positive forecast), and the supporting check passes (top third of positive forecasts minus forecast 0 = +0.0098), so the shortfall is about precision, not direction.
- F2: The effect is small against the market's own moves and uneven across slices: the 72-hour excess return has a standard deviation of 0.090; per-coin t runs from -0.78 (LTC) to 2.08 (ETH); per-year t runs from -0.78 (2018) to 3.10 (2020); and per-window t ranges from -1.66 to 3.73 with many near zero, so the six default coins alone give too few independent cases to clear t 2.
