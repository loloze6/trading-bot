---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin, the return over the 2 hours from 20:00 UTC is positive, and the higher the coin's hourly volatility over the past 3 days, the larger that rise.
Consequence: The early-evening hours give a long bias that is worth taking mainly when the coin has been volatile.
Why:
- F3: There is an unconditional rise from 20:00 to 22:00 UTC: the 20:00 bar averages +5.5 bp (t = 6.7) and the 21:00 bar +4.4 bp (t = 5.7). Every coin is positive (+2.7 to +8.8 bp; t = 2.4 to 2.6 for BTC, ETH, XRP and ZEC). The rise grows with the 3-day hourly volatility: +1.0 bp (t = 0.9) in the calmest quartile and +12.3 bp (t = 3.4) in the most volatile.
