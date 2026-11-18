---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-midpoint-continues-up
line: 7.b inconclusive
backtest: 010-01_rsi-above-midpoint-continues-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 14 days that a coin's 14-day RSI has spent above its midpoint, the larger the coin's rise over the next 7 days.
Consequence: Sustained RSI above the midpoint marks buyers in control, and their persistent order flow carries the uptrend forward.
Why:
- F1: The tested slope is on the side the idea predicts but short of the bar: 7-day slope 0.000629, t 1.82 on 815 independent cases. Only BTC and ETH ran (BNB is absent), so the test had about two thirds of the roughly 1,200 cases its plan expected.
- F2: The sign holds at every horizon, but only the shorter ones clear the bar: t 2.65 at 1 day (5,794 cases), 2.48 at 3 days (1,907), 1.82 at 7 days (815), 1.03 at 14 days (384) and 1.97 at 21 days (240). As cases thin out at longer horizons, the t falls, which fits a small effect that this data is too short to show.
- F3: Both coins point the same way at 7 days, each too weak alone: BTC slope 0.000379, t 0.90 (408 cases); ETH slope 0.000882, t 1.61 (407 cases).
