---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The stronger a coin's 10-day return relative to its own 20-day volatility, the more its price rises over the next 3 days relative to its usual 3-day return, with the extra rise concentrated after the strongest advances.
Consequence: A coin that has risen strongly against its own recent volatility over the last 10 days is a reason to lean long for the next few days, alongside or instead of a volume surge.
Why:
- F1: The 10-day return scaled by 20-day volatility still predicts the 3-day excess return once the volume ratio is in the same regression. Pooled joint OLS gives t_vr = 3.90 and t_z10 = 2.24 on 4283 non-overlapping 3-day cases, and the two signals correlate only 0.162.
- F2: The momentum effect sits in the strongest quintile. On the volatility-scaled 10-day return, the top quintile has a mean excess 3-day return of +1.04% (t 3.25, n 858). Quintiles 1 to 4 run from -0.68% to +0.02%. The raw 10-day return gives the same picture: top quintile +1.06% (t 3.32), the other four between -0.20% and -0.36%.
- F3: The 5-, 10- and 20-day volatility-scaled return slopes all have the same sign pooled (t 2.41, 2.12, 2.03, n 4715). XRP is the strongest coin (t 2.20, 2.09, 2.00) and ZEC/ETH are next (t 0.78 to 1.62), but LTC and XMR slopes are negative (t -0.21 to -0.65). The effect is also uneven in time: t 3.09 in windows w13 to w24 and 0.70 in w1 to w12.
