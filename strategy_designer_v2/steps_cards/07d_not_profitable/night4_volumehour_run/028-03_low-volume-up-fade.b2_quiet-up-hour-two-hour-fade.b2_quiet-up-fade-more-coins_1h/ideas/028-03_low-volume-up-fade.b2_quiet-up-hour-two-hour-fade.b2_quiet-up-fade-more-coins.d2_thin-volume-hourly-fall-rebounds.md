---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days while its volume is well below its average hourly volume over the past 30 days, the price recovers part of that fall over the next two hours; the larger that hour's fall in typical moves, the larger the recovery.
Consequence: A trader would refuse to sell a sharp hourly drop on thin volume and would buy it instead, because it more often bounces back than extends.
Why:
- F7: Large falls on unusually thin volume also rebound: for falls beyond 3 usual moves at volume below 0.8 times its mean, the 2-hour long-direction excess is +0.37 % (t 4.56, 471 cases).
- F4: Large hourly falls on surging volume are followed by a rebound that grows with the fall and is several times the cost. For falls of more than 3 usual moves, the 2-hour excess return in the long direction is +0.48 % (t 5.73, 1529 cases) at volume above 4 times its 30-day mean and +0.15 % (t 2.46, 1526) at 2-4 times. It is +0.003 % (t 0.02, 465) on ordinary volume.
- F2: The fade has no gradient over most of its range: after quiet-volume rises (volume 0.8-1.25 times its 30-day mean), the short-direction 2-hour excess is +0.013 % (t 0.53, 3905 cases) for rises of 1-2 usual moves and +0.011 % (t 0.24, 1323 cases) for 2-3. It reaches +0.24 % (t 2.1, 371 cases) only at 3-4 usual moves, then turns to -0.09 % (t -0.47, 130 cases) at 4-6. Over 6 hours the 3-6 bands run against the short (-0.33 %, -0.99 %).
