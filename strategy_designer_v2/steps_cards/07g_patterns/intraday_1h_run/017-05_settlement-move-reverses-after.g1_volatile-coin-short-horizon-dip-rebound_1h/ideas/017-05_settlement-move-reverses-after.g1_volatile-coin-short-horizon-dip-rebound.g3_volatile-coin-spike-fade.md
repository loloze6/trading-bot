---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 7-day mean absolute hourly move is high, the larger its 2-hour rise relative to its usual 2-hour move, the larger its fall over the next 2 hours.
Consequence: A sharp 2-hour spike in a volatile coin is a reason to sell or short for a 2-hour pullback, scaled to the spike's size.
Why:
- F5: Rises reverse too in volatile hours: in the high-volatility regime, the 2-hour rise's slope on the next 2-hour return is -6.42 bp (t -6.43, n 77,297) against -0.90 bp (t -1.47) in the low regime, and the ninth z-decile gives -9.05 bp (t -4.92); the long-only forecast never uses this.
- F2: The rebound after a fall grows with the coin's volatility level, measured in the coin's own usual moves: in the high-volatility regime, the slope of the forward return on the size of the fall rises across volatility terciles from 0.011 (t 1.07) to 0.028 (t 2.71) to 0.147 (t 15.1) at 2 hours, and from -0.031 (t -0.69) to 0.066 (t 1.80) to 0.342 (t 10.3) at 24 hours.
