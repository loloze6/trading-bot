---
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3060 USD
---
## Findings
- **F1:** The book's fees exceed its gross gain: fees summed to 9.38 against 4.84 of gross gain. The fees fall almost entirely on the entry hour (19:00, 4.16), the rebalance hour (20:00, 1.03) and the exit hour (21:00, 4.15). So the 11,085 trades average +0.076% before fees but −0.024% after them.
- **F2:** The 2-hour rebound is too small for a round trip. The deepest fifth of 24-hour falls is followed by +21.5 bps over 2 hours (t 5.4, n 3194), against the coin's own mean of +5.0 bps, which leaves about 16 bps of excess. The next fifth gives only +5.0 bps, the same as the mean. That is about one round trip of fees (about 10 bps), and it explains a Sharpe of −1.08 and a mean daily return of −0.00026.
- **F3:** The rebound grows over the following day rather than fading after 2 hours. The second-deepest decile of falls scaled by volatility is followed by +22 bps at 2 hours, +34 bps at 12 hours (t 4.0) and +50 bps at 24 hours (t 3.8, n 1597). The coin's mean over 24 hours is +13 bps. The deepest decile gives +41 bps at 24 hours and +78 bps at 48 hours (t 4.3), against a 48-hour mean of +25 bps.
- **F4:** The rebound is concentrated in high-volatility states. Among the two deepest deciles of falls, the top tercile of 10-day volatility is followed by +43.6 bps at 2 hours, +63 bps at 12 hours and +121 bps at 24 hours (n 1028). The low and middle terciles give only +6.5 bps at 2 hours and −10 to +28 bps at 24 hours.
- **F5:** The volatility-target sizing holds the smallest position exactly where the rebound is largest. The mean position was 0.49 in the high-volatility deep falls, against 1.05 in the low-volatility ones, where the rebound barely beats holding.
- **F6:** The loss is spread across the windows, not caused by one bad period. The book's mean daily return is −2.6 bps across the 24 windows, with a median of −1.5 bps and three quarters of windows at or below +0.36 bps. With any one window left out, the Sharpe is still −1.21.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day` (from F1, F2, F3): The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound` (from F3, F4, F5): The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours, only while its 10-day hourly volatility is high, and the higher that volatility the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
