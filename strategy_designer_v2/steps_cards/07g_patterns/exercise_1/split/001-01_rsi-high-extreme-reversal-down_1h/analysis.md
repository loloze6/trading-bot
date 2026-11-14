---
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
idea tested: 001-01_rsi-high-extreme-reversal-down
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.4403 USD
---
## Findings
- **F1:** Costs, not direction, sink the book: it loses -1.88 bp per bar, of which only -0.265 bp is the gross position-times-return P&L and 1.615 bp is fees and slippage, because the position is changed on 67.6% of bars (mean |Δposition| 0.166 per bar, 7,700 trades, 0.29% commission per trade).
- **F2:** Trade P&L turns on holding time. Trades shorter than about 4 hours make money: mean duration 1.4 h, gross +0.35%, and mean duration 3.4 h, gross +0.21%. The longest quartile (mean 38.6 h) loses -2.55% gross, so the 60% gross win rate still gives a mean of -0.52% per trade.
- **F3:** Entry forecast size does not separate trades: |entry forecast| quartiles of 3.9, 8.5 and 17.6 all lose about the same gross (-0.51%, -0.48%, -0.55%, win rates 57–62%), and larger forecasts only shorten the trade (19.9 h vs 8.9 h).
- **F4:** The extreme bars that follow a fall continue down, on the side the idea never trades. In the top decile of 50-RSI (RSI far below 50, raw mean 8.6), the 12-bar excess return is -24.0 bp pooled (non-overlapping t -2.0), with -20.3 bp for BTC and -27.7 bp for ETH. The opposite decile (RSI far above 50) shows +10.4 bp (+8.3 / +12.4 bp).
- **F5:** The past 12 hours' move points weakly toward continuation. The top past-12h decile is followed by +19.5 / +19.0 bp of 12-bar excess return (BTC / ETH). The bottom decile is followed by -3.4 / -13.0 bp. The top-minus-bottom spread is positive in 10 of 12 coin-windows (up to +91 bp) but strongly negative in w6 for both coins (-57, -75 bp), and no single decile reaches non-overlapping |t| > 2.1.
- **F6:** Volatility conditions this continuation. When 24h volatility is in its top tercile relative to its own recent median, bars after a 12h rise see +24.9 bp of 12-bar excess return, versus +5.4 bp in the low-volatility tercile. In the low-volatility tercile, falls continue (-16.9 bp). In absolute volatility terms, the top tercile shows +11.6 / +8.8 bp excess for BTC / ETH, against -8.5 / -9.1 bp in the middle tercile.
- **F7:** The book is flat when the coin drifts down and short when it rises. On flat bars the coin returns -1.37 bp next bar and -8.9 bp of 12-bar excess. Moderate shorts (allocation -0.5 to -0.1, 5,691 bars) sit before +18.0 bp of 12-bar excess. The largest shorts (< -0.95, 250 bars) sit before -20.8 bp, but pay 4.6 bp per bar in fees.
- **F8:** The book's largest 1% bar losses and gains come from the same setup: allocation about -1.9 (beyond full size), after a +296 / +355 bp 12h run-up, in relative volatility of 1.32 / 1.34. The coin then moves +188 bp or -160 bp in the next bar, so the tails are symmetric coin flips taken with leverage.
- **F9:** The book loses in all 12 coin-windows, and worst in the rising windows: BTC loses -86.4 and -61.1 bp/day in w4 and w6 while the coin gains +51.3 and +42.9 bp/day; ETH loses -62.6 and -52.8 bp/day while the coin gains +41.4 and +30.7.
- **F10:** Bar size has a stable weekly and daily rhythm, with no stable direction. Mean absolute hourly return is 27.8 / 32.1 bp on Saturday and Sunday versus 42–46 bp on weekdays, and peaks at 13–14 UTC (55.6 / 51.6 bp) versus 26.5 bp at 03 UTC. The directional hour effects do not repeat across years: hour 19 is +8.6 bp in 2022 and +0.1 bp in 2023, and hour 21 is +0.2 bp in 2022 and +7.4 bp in 2023.

## Ideas
- `001-01_rsi-high-extreme-reversal-down.g1_oversold-rsi-keeps-falling` (from F4, F7): When a coin's 14-bar RSI sits in its most extreme low readings, far below 50 after a one-sided fall, the coin keeps falling over the next 12 hours more than its usual drift.
- `001-01_rsi-high-extreme-reversal-down.g2_high-volatility-run-ups-continue` (from F5, F6, F8): When a coin has risen over the past 12 hours while its 24-hour volatility is high relative to its own recent median, it keeps rising over the next 12 hours more than its usual drift.
- `001-01_rsi-high-extreme-reversal-down.g3_quiet-declines-keep-sliding` (from F6, F7): When a coin has fallen over the past 12 hours while its 24-hour volatility is low relative to its own recent median, it keeps falling over the next 12 hours more than its usual drift.
- `001-01_rsi-high-extreme-reversal-down.g4_moderate-rsi-strength-continues` (from F7, F4, F9): When a coin's 14-bar RSI is moderately above 50 but not at an extreme, the coin rises over the next 12 hours more than its usual drift.
- `001-01_rsi-high-extreme-reversal-down.g5_brief-give-back-after-highs` (from F2, F3): After a coin's 14-bar RSI rises to a high extreme, the coin gives back part of the move within the next few hours, before any continuation over longer horizons.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
