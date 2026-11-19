---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more evenly a coin's volume was spread across the hours of its past-24-hour move, the larger the share of that move it gives back over the next 24 hours.
Consequence: A trader fading a daily move would lean harder against moves built on steady volume than against those made in one volume burst.
Why:
- F4: Contrary to the brief, moves made with evenly spread volume reverse more than volume-burst moves. The reversal slope is -0.135 (t -9.91) in the least-concentrated volume tercile, -0.075 (t -5.56) in the middle one and -0.032 (t -2.56) in the most-concentrated one. In the pooled regression, past × max-hour volume share is +0.375 (t 4.63). The share of the move made in a single hour changes little (slopes -0.071 / -0.101 / -0.078).
- F2: The 24-hour reversal sits almost entirely in high-volatility days. On the non-overlapping daily grid, the slope of the next-24h excess return on the past-24h return has t -8.91 in the top quintile of 24h summed absolute hourly moves (n 3422), against t between -0.50 and +1.24 in the other four quintiles. It is negative in all six coins on those days (t -2.15 to -4.92).
