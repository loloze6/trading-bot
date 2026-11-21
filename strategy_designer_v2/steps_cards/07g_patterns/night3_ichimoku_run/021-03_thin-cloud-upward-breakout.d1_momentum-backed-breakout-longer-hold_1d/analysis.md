---
line: 7.g patterns
backtest: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d
idea tested: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3847 USD
---
## Findings
- **F1:** On daily bars a coin rises the day after a fall that is large against its own recent 20-day volatility, and the rise grows with the fall: the next day's move above the coin's drift is +0.24 % after a z of -0.5 to -1 (t 2.2, n 2101), +0.66 % after -1 to -1.5 (t 4.0, n 971), +0.49 % after -2 to -3 (t 1.9, n 337) and +1.26 % after a fall beyond -3 (t 2.1, n 185); over all days the one-day z against the next day's unusual move has a rank correlation of -0.076 (p 1e-21, n 15689) and a standardised slope of -0.028 (t -3.4).
- **F2:** This rebound grows with the coin's recent volatility: after a z of -1 or less, the next day's unusual move is -0.18 % in each coin's calmest volatility tercile (t -1.2, n 826), +0.71 % in the middle tercile (t 3.6, n 658) and +1.66 % in the most volatile (t 4.9, n 496). That move is 3 to 8 times the 0.19 % this backtest charged for a buy and a sell, which F11 says an idea must cover.
- **F3:** The rebound holds in every coin, with means of +0.21 % (BTC, t 0.9) to +0.99 % (XMR, t 3.4). It is uneven over time: strong in 2020 (+1.41 %, t 3.4) and 2021 (+1.72 %, t 3.9) and near zero in 2019, 2024 and 2025. Because the coins fall on the same days, averaging the down-day coins by day leaves +0.38 % (t 2.1, n 687 days). It is a real pattern but weaker than the pooled t suggests.
- **F4:** The cross's 60-day return does not grade what follows, which explains the inconclusive slope. On cross bars the rank correlation of the 60-day return with the next 20 days' move is 0.020 (p 0.79, n 189). Crosses the forecast left flat still rose +6.9 % over 40 days (n 65), against +14.8 % for those it took (n 94).
- **F5:** Several other angles show nothing that stands out from chance:

## Ideas
- `021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold.g1_volatile-down-day-next-day-rebound` (from F1, F2, F3): After a daily close that falls far against the coin's own volatility of the past 20 days, the coin rises over the next day, and the larger that fall and the higher the coin's 20-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
