---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its 200-day average and its own 20-day return is strongly negative, the coin keeps falling over the next 20 bars. It does worse than it does on bars below the average with the same weak momentum.
Consequence: A trader long on the "above the average" condition should step aside when the coin's recent 20-day momentum has turned sharply down.
Why:
- F4: Whether being above the SMA helped depended on 20-day momentum. Long bars in the bottom 20-day-momentum quintile (≤ −13.9%) returned −4.75% over the next 20 bars, against +2.74% for flat bars in the same quintile. Long bars in the top two quintiles returned +5.56% and +6.54%, against +1.61% and +3.11% for flat bars.
- F11: The book's extreme days fall in stretched, high-vol conditions. The best 1% of book days (mean +26.7%) came at a mean distance of 132% above the SMA after +71% 20-day momentum. The worst 1% (mean −21.9%) came at 80% above after +27% momentum. Both had 20-day vol of about 0.073 against 0.042 on other days. The top 5% of book days account for 2.9× to 16.5× the net book sum per coin, and for XMR the net is near zero or negative (share −96.5).
