---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits very far above its 200-day average with high recent volatility, the typical next-20-bar outcome is a decline. The average is held up only by a few very large further rallies.
Consequence: A trader long in such stretched conditions should expect to lose on most entries and depend on rare outsized winners, so should size the position for that.
Why:
- F3: Forward 20-bar returns while long are strongly right-skewed. Long bars had skew 4.30 (mean +3.22%, median −0.53%), against skew 1.23 when flat (mean +2.60%, median +0.60%). In raw distance, the top decile (mean 108% above the SMA, 20-day vol 0.064) had a −2.40% median and a 37.5% hit rate, the lowest of all deciles.
- F2: Bars just above the 200-day SMA (forecast 0–5, n=1,909) had a mean next-20-bar return of −0.25%, a median of −1.65% and a 38.8% hit rate. Flat bars (n=7,297) had +2.60% mean and 43.0% hit. The 15–20 forecast bucket had +6.30% mean but a −0.11% median and 40.0% hit, so the edge from a larger distance is in the mean only.
- F11: The book's extreme days fall in stretched, high-vol conditions. The best 1% of book days (mean +26.7%) came at a mean distance of 132% above the SMA after +71% 20-day momentum. The worst 1% (mean −21.9%) came at 80% above after +27% momentum. Both had 20-day vol of about 0.073 against 0.042 on other days. The top 5% of book days account for 2.9× to 16.5× the net book sum per coin, and for XMR the net is near zero or negative (share −96.5).
