---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 24-hour volatility stands against its own volatility over the past weeks, the more its next 24 hours run against its last 1-hour return measured against that 24-hour volatility.
Consequence: A trader would fade hourly shocks harder in turbulent stretches of a coin and barely at all in calm ones.
Why:
- F7: Across all grid bars, the fade grows with the coin's own 24-hour volatility quintile: +0.04 % (t 0.72) in the lowest quintile, +0.12 % (t 1.64) in the middle and +0.41 % (t 3.19, n 3422) in the highest.
- F2: At hour 0 the reversal is graded by the size of the shock. The drift-removed next-24-hour return is +1.04 % after shocks of −3 to −2 (t 4.06, n 509), +0.48 % after −2 to −1 (t 4.37), −0.29 % after +0.5 to +1 (t −2.94) and −0.52 % after +1 to +2 (t −4.72). Ranked by |shock| into terciles, the fade rises from +0.17 % to +0.22 % to +0.52 % (t 7.46, n 5567). Beyond ±3 there is no reversal (t −0.72 and −0.66).
