---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The deeper a coin's fall over the last 24 hours, measured against its usual daily move over the past 30 days, the more it rises over the next 2 days.
Consequence: A trader buys a sharp daily drop for a two-day rebound, and the larger the drop against the coin's usual daily range, the more confident the trade.
Why:
- F2: The depth of a 24-hour fall predicts the rebound. Among net falls, the 24-hour return in units of the coin's 30-day hourly volatility has a pooled slope t of -4.36 on the 48-hour excess (n 3841), and the slope is negative on all 6 coins (t -1.17 to -2.41). Over all grid bars, the deepest-fall quintile ends +0.46 % above drift (t 2.62, n 1575, strength 0.068), which is 2.4 times the 0.19 % round trip.
- F1: The tested shape adds nothing beyond the fall itself. Among net 24-hour falls, the largest hourly move's share of the day's moves has a pooled slope t of -0.97 against the 48-hour excess return (n 4101, coins -2.11 to +0.73). The largest hour's share of volume has t -1.30. This matches the step-5 strength of 0.011 and the unusual move of 0.4 times the cost.
