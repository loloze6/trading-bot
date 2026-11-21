---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return, measured against its 30-day volatility, the more its price rises above its usual drift over the next 5 days.
Consequence: A trader would hold or add to a coin after an unusually strong week rather than fade it, and would refuse a short after a sharp up week.
Why:
- F6: The tested idea's own situation, a large up surge after a 7-day fall, shows no fade. On a 120-hour grid, a surge above 2 usual moves after a negative prior 7-day return is followed by +0.39 % excess over 120 hours (t 0.31, 85 cases). After a positive prior 7-day return it is followed by +3.5 % (t 1.96, 92 cases). The verdict's +0.32 % unusual move at t 0.74 matches this.
- F7: A strong 7-day rise tends to continue over the following 5 days, but the evidence is weak. The top quintile of the 7-day return in 30-day volatility units beats the coin's drift by +1.47 % over the next 120 hours (t 2.57, 506 cases), while the other four quintiles lie between -0.66 % and -0.11 %. The effect sits mostly in w13–w24 (t 5.42) rather than w1–w12 (t 1.41).
