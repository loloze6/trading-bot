---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours.
Consequence: A late-evening long after a deep daily fall pays enough to cover its fees only if it is held through the following day instead of for two hours.
Why:
- F1: The book's fees exceed its gross gain: fees summed to 9.38 against 4.84 of gross gain. The fees fall almost entirely on the entry hour (19:00, 4.16), the rebalance hour (20:00, 1.03) and the exit hour (21:00, 4.15). So the 11,085 trades average +0.076% before fees but −0.024% after them.
- F2: The 2-hour rebound is too small for a round trip. The deepest fifth of 24-hour falls is followed by +21.5 bps over 2 hours (t 5.4, n 3194), against the coin's own mean of +5.0 bps, which leaves about 16 bps of excess. The next fifth gives only +5.0 bps, the same as the mean. That is about one round trip of fees (about 10 bps), and it explains a Sharpe of −1.08 and a mean daily return of −0.00026.
- F3: The rebound grows over the following day rather than fading after 2 hours. The second-deepest decile of falls scaled by volatility is followed by +22 bps at 2 hours, +34 bps at 12 hours (t 4.0) and +50 bps at 24 hours (t 3.8, n 1597). The coin's mean over 24 hours is +13 bps. The deepest decile gives +41 bps at 24 hours and +78 bps at 48 hours (t 4.3), against a 48-hour mean of +25 bps.
