---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the smaller the share of that fall that came from its few biggest hourly losses (a grind of many small hourly steps down), the more the coin keeps falling over the next 3 days.
Consequence: A trader would short grinding 3-day falls, sized by how evenly the fall was spread across hours, rather than buying them as oversold.
Why:
- F6: On the down side the mirror effect is clearer than on the up side. On 2,669 falling grid cases, the share of the 3-day fall not made by its 3 biggest hourly losses has coefficient -0.0315 with t = -2.06 on the next 72-bar excess return, net of fall size. The more evenly spread the fall, the more the coin keeps falling.
- F4: The effect appears only at the plan's own 3-day horizon. The forecast t is -0.29 over the next 24 hours, 1.52 over the next 72 hours and 0.54 over the next 144 hours, on 2,926, 2,865 and 2,802 cases.
