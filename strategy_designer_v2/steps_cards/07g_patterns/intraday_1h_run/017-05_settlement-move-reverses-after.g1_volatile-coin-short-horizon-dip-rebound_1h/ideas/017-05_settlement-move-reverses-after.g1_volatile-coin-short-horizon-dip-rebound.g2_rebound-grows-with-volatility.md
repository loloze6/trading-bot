---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 7-day mean absolute hourly move, the larger the rebound over the next day after a 1-day fall, measured in the coin's own usual daily moves.
Consequence: A dip-buying trade can be sized up as the coin's own volatility level climbs, and refused in calm coins.
Why:
- F2: The rebound after a fall grows with the coin's volatility level, measured in the coin's own usual moves: in the high-volatility regime, the slope of the forward return on the size of the fall rises across volatility terciles from 0.011 (t 1.07) to 0.028 (t 2.71) to 0.147 (t 15.1) at 2 hours, and from -0.031 (t -0.69) to 0.066 (t 1.80) to 0.342 (t 10.3) at 24 hours.
- F6: The 2-hour rebound strength rises from the large coins to the small ones: high-regime slope BTC 4.47 bp (t 2.67), ETH 8.16 (t 3.90), LTC 15.02, XMR 12.89, XRP 16.76, up to ZEC 26.28 bp (t 8.56).
