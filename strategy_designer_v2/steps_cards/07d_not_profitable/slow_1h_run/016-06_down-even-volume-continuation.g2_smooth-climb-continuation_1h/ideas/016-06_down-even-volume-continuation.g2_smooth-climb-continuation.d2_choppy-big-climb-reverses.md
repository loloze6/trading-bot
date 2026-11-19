---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days but only a small share of its summed absolute hourly moves points up, it gives back part of the rise over the next 3 days, the more so the larger the 3-day rise and the smaller that share.
Consequence: A large but choppy 3-day climb is a reason to sell or stay out rather than to buy.
Why:
- F5: Large 3-day climbs made with a small up-share reverse strongly: in the top tercile of 3-day rise, the low-efficiency tercile is followed by a -3.24% excess return over the next 72 hours, against +0.90% for the high-efficiency tercile; among small climbs the high-efficiency tercile gets +1.85% against -0.43% for the low one.
