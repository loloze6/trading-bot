---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 8 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend, and the stronger the 24-hour trend, the larger the move back.
Consequence: A trader takes the reversal bet at settlement only when the move into settlement goes against the recent trend, and sizes it by the trend's strength, holding it through the 8 hours to the next settlement.
Why:
- F7: The tested 8-hour result is on the predicted side but weak, and it splits by side and coin. The mean is +0.026 % with t 1.25 over 17,689 cases. By side, the long dip-in-uptrend cases give +0.011 % (t 0.42) and the short rally-in-downtrend cases +0.042 % (t 1.52). By coin, BTC is negative (-0.014 %) and ZEC highest (+0.077 %, t 1.32).
