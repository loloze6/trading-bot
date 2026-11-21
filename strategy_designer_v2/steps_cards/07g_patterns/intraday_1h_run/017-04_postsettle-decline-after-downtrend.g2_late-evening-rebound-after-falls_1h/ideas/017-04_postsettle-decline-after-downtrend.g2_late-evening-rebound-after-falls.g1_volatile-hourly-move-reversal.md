---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin, the return over the next 2 hours runs against its last-hour return, and the larger that last-hour move relative to its 24-hour volatility, the larger the opposite move. The effect grows the higher the coin's 24-hour volatility is.
Consequence: After an outsized hourly move in a volatile coin, a trader would lean against it for the next couple of hours rather than follow it.
Why:
- F4: Across all hours, the next hour runs against the last hour's vol-scaled move. The next-hour excess was +4.6 bp (t 7.1) in the most negative decile and −3.2 bp (t −6.5) in the ninth decile. The regression slope holds on non-overlapping 2-hour (t −11.3, n 206,550) and 4-hour (t −6.3, n 103,224) grids, and it is negative in every year from 2018 to 2025 (t from −0.7 to −7.5).
- F5: The reversal of F4 grows with the volatility level. Its slope rises from 0.03 bp (t 0.2) in the lowest 24-hour-volatility quintile through −0.75 and −1.13 to −7.41 bp (t −12.1) in the highest. It is strong in LTC, XMR, XRP and ZEC (t −5.0 to −7.8) and absent in BTC and ETH (t −1.1 and +0.1).
