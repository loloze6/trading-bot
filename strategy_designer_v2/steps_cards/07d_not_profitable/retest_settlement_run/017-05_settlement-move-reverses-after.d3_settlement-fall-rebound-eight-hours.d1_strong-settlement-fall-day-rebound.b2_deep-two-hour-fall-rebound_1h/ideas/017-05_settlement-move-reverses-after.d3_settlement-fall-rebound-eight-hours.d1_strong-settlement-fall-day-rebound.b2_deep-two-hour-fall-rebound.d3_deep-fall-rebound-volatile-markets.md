---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the next 24 hours after a fall over a coin's last 2 hours, at any hour of the day, runs upward, only while the coin's last 7 days have been more volatile than its last 30 days, and the larger the fall against the coin's usual 2-hour move, the larger the rise.
Consequence: A trader buys deep 2-hour falls only when the coin's recent volatility is raised, and refuses them in calm markets where they do not rebound.
Why:
- F6: The deep-fall rebound holds only when the coin's recent volatility is high. Volatility here is the 7-day hourly volatility against the 30-day one, split in thirds.
- F2: The effect sits only in the deepest falls. Over 24 hours on the non-overlapping grid, the forecast quintiles 1 to 4 earn an excess of 0.00 %, +0.02 %, +0.02 % and +0.09 % (all t < 0.9, about 1,740 cases each). The top quintile (forecast ≥ 15.7) earns +0.60 % excess (t 4.29, 1,742 cases), and the 1,138 cases at the cap of 20 earn +0.71 % (t 3.84). This is why the idea's size over all 17,241 cases is only +0.01 % unusual move.
- F7: The deep-fall rebound is on the same side in every coin, with excess from +0.29 % in BTC to +0.84 % in ZEC (t 1.2 to 2.2). It is also there after both 7-day trends (+0.70 % down, t 3.54; +0.46 % up, t 2.40). It is weak in windows w1 to w6 (-0.08 %, t -0.36) and strong in w7 to w18 (+0.98 % and +1.21 %, t 3.5 and 3.2).
