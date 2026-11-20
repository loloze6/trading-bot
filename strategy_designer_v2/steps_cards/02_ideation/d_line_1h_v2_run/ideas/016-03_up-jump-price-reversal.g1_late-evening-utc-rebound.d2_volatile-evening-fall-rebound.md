---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours, only while its 10-day hourly volatility is high, and the higher that volatility the larger the rise.
Consequence: A trader should weight the late-evening rebound long toward volatile days rather than shrink it there, and leave it aside in calm markets where the rebound does not beat holding.
Why:
- F3: The rebound grows over the following day rather than fading after 2 hours. The second-deepest decile of falls scaled by volatility is followed by +22 bps at 2 hours, +34 bps at 12 hours (t 4.0) and +50 bps at 24 hours (t 3.8, n 1597). The coin's mean over 24 hours is +13 bps. The deepest decile gives +41 bps at 24 hours and +78 bps at 48 hours (t 4.3), against a 48-hour mean of +25 bps.
- F4: The rebound is concentrated in high-volatility states. Among the two deepest deciles of falls, the top tercile of 10-day volatility is followed by +43.6 bps at 2 hours, +63 bps at 12 hours and +121 bps at 24 hours (n 1028). The low and middle terciles give only +6.5 bps at 2 hours and −10 to +28 bps at 24 hours.
- F5: The volatility-target sizing holds the smallest position exactly where the rebound is largest. The mean position was 0.49 in the high-volatility deep falls, against 1.05 in the low-volatility ones, where the rebound barely beats holding.
