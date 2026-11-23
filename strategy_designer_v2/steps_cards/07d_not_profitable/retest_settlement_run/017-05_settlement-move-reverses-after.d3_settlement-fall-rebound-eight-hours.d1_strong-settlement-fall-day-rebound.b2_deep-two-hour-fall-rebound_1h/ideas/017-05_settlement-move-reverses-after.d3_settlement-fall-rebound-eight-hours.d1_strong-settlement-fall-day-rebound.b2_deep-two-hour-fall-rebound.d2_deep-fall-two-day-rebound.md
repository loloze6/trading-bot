---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the next 48 hours after a fall over a coin's last 2 hours, at any hour of the day, runs upward, and the larger the fall against the coin's usual 2-hour move, the larger the rise, held for two days instead of one.
Consequence: A trader who buys deep 2-hour falls holds them for two days, which captures the larger part of the rebound for the same cost per trade.
Why:
- F2: The effect sits only in the deepest falls. Over 24 hours on the non-overlapping grid, the forecast quintiles 1 to 4 earn an excess of 0.00 %, +0.02 %, +0.02 % and +0.09 % (all t < 0.9, about 1,740 cases each). The top quintile (forecast ≥ 15.7) earns +0.60 % excess (t 4.29, 1,742 cases), and the 1,138 cases at the cap of 20 earn +0.71 % (t 3.84). This is why the idea's size over all 17,241 cases is only +0.01 % unusual move.
- F5: The rebound keeps building past the idea's horizon. For the top quintile, the excess return is +0.60 % at 24 hours (t 4.28) and +0.78 % at 48 hours (t 4.39); the raw return is +0.42 % at 12 hours, +0.75 % at 24 hours and +1.03 % at 48 hours. Cases at the cap of 20 show +0.71 % and +0.89 % excess (t 3.84 and 3.97).
