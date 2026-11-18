---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
line: 7.b inconclusive
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin, the higher its 5-day average volume against its 30-day average, the higher its return over the next 3 days, whatever the direction of its last 5 days.
Consequence: A trader would lean long for a few days on a coin whose recent volume runs above its monthly norm, and would avoid holding a coin whose volume has dried up.
Why:
- F2: The effect is clearer at horizons shorter than the plan's 7 days and fades at longer ones: the slope t is 4.70 at 1 day (17380 cases), 3.51 at 2 days (8650), 3.62 at 3 days (5723), 2.87 at 5 days (3419), 1.94 at 7 days (2443), 0.48 at 14 days (1152) and 0.16 at 21 days (720).
- F5: At 3 days the effect holds across the data and keeps its order. The slope is positive for all 6 coins (t from 0.11 for LTC to 3.14 for XRP) and in 7 of 8 years (t from 0.54 to 3.89, with 2018 at -0.22). The quintile means of excess return rise from -0.0061 in the lowest to +0.0072 in the highest.
