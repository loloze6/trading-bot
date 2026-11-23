---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose hourly volatility over the past 7 days is low against its own history, its 3-day return continues over the next 24 hours. The continuation is larger the larger that 3-day move is against the coin's usual 24-hour move.
Consequence: In a calm coin, a 3-day move is a reason to hold its direction for the next day rather than fade it.
Why:
- F5: In calm coins, the move continues instead of reversing. In the least volatile third, the 3-day return in usual 24-hour moves correlates +0.069 with the next-day excess (t 7.5, 11 713 cases), and the 24-hour return +0.048 (t 5.2). In the most volatile third, the same correlations are −0.068 and −0.125.
