---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the next 24 hours after a fall over a coin's last 24 hours runs upward. The rise is larger the larger that fall is against the coin's usual 24-hour move, and the higher the coin's volatility over its last 24 hours is against its volatility over its last 30 days.
Consequence: A trader buys one-day falls that come with a burst of volatility, scaling up with the size of both, and passes on falls that happen in quiet conditions.
Why:
- F1: On the non-overlapping 24-hour grid (about 15,800 cases), the coin's 24-hour fall, scaled by its usual 24-hour move, predicts the next 24 hours better than the tested 2-hour fall: the lowest quintile of the scaled 24-hour return gives a strength of +0.102 (t 5.04), against +0.075 (t 3.97) for the lowest quintile of the scaled 2-hour return.
- F3: The reversal also grows with the coin's last-24-hour volatility against its 30-day volatility. In the top tercile of that ratio the slope is −0.051 (t −7.05, n 5,175), against +0.006 (t 0.36) in the bottom tercile. The deepest-fall quintile gives a strength of 0.178 (t 5.85, total +1.04 %) in the top tercile, against 0.021 (t 0.33) in the bottom tercile.
- F4: The 24-hour reversal holds across coins and years. The slope is negative in all 6 coins (t from −2.35 for LTC to −4.69 for XMR), in 7 of 8 years (2024 is +0.008, t 0.66), and in 71 % of the 24 windows.
