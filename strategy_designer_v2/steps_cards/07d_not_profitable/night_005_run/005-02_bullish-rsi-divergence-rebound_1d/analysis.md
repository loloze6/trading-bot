---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound_1d
idea tested: 005-02_bullish-rsi-divergence-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3340 USD
---
## Findings
- **F1:** The book was almost never in the market, so it could not earn the effect it bets on. It held a position on only 1.4% of its 5794 coin-days, with a mean position of 0.25 when held. After a divergence signal the position lasted a mean of 0.91 bars (median 1, max 8), because the forecast is non-zero only on the new-low bar itself. The mean daily return was -0.0000034 and the Sharpe was -0.04.
- **F2:** The book only captured the next day, and that day loses. After the 44 independent divergence new lows, the next 1-day return averaged -0.49% (t -0.82). The 10-day return averaged +1.22% (t 0.56), against -2.66% for the 43 new lows without divergence. The 20-day return averaged +5.60% (t 1.37, n=38), against -3.00% without divergence.
- **F3:** Inside the divergence cases, the depth of the prior 30-day fall grades the rebound. The deepest tercile of 30-day return (mean -34%) gained +4.56% over 10 days, +3.28% above the coin's mean (t 0.82, n=15). The shallowest tercile (mean -9.9%) lost -2.24%, -3.49% below the coin's mean (t -1.37, n=15). The Spearman correlation of the 14-day return with the 10-day return was -0.31.
- **F4:** The forecast's own size barely grades the outcome. Its Spearman correlation with the 10-day excess return over the 44 divergence cases is only 0.16 (Pearson 0.08).
- **F5:** Across all 87 new 30-day lows, the shallow-decline tercile (30-day return -5.1%) went on to fall 3.78% below the coin's mean 10-day return (t -1.89, n=29). The deep-decline tercile (30-day return -29.6%) was flat at +0.08% (t 0.03, n=29).
- **F6:** The book's small trades split by coin. BTC's 33 trades averaged +0.80% after fees with a book Sharpe of 0.20. ETH's 33 trades averaged -1.31% after fees with a book Sharpe of -0.32. The excess 10-day return after divergence was +0.84% for BTC (n=23) and -1.00% for ETH (n=21).

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence` (from F1, F2, F3, F4): When a coin's close makes a new 30-day low while its 14-day RSI is above its reading at the previous low in that window, the price rebounds over the next 20 days rather than on the next day. The further the RSI stays above its earlier trough, and the deeper the coin's 30-day decline into that low, the larger the rebound.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling` (from F5, F3): When a coin's close makes a new 30-day low, the smaller its 30-day decline into that low, the further it keeps falling over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
