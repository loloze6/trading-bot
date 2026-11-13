---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A short opened when the close drops below the 200-day average and closed within 20 days tends to lose, because the coin rises back over the following days.
Consequence: A trader would not open short trades on a drop below the long average for holding periods under 20 days.
Why:
- F6: Short trades split sharply by holding time. The 1,764 trades closed within 20 days lose about the same price amount whatever their length: -6.5%, -6.2%, -6.2% and -6.4% gross, with win rates of 1% to 22%. The 707 trades held beyond 20 days gain +2.05% gross (53% wins). Fees are small, about 0.1 to 0.3 points per trade.
- F5: The actual price crosses carry no edge. After the 257 crosses below the SMA200, the 10-bar return is +1.20% (t 1.39) and the 20-bar return +1.09% (t 0.83). After the 327 crosses above, the 10-bar return is +1.38% (t 1.57). The unconditional 10-bar mean is +1.35%.
