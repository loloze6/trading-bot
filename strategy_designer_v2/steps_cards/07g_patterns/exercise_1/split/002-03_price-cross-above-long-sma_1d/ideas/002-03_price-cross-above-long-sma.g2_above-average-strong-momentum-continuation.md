---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its 200-day average and its own 20-day return is among its strongest, the coin rises further over the next 20 bars than it does at other times.
Consequence: A trader should hold a long position above the average mainly while 20-day momentum is strongly positive.
Why:
- F4: Whether being above the SMA helped depended on 20-day momentum. Long bars in the bottom 20-day-momentum quintile (≤ −13.9%) returned −4.75% over the next 20 bars, against +2.74% for flat bars in the same quintile. Long bars in the top two quintiles returned +5.56% and +6.54%, against +1.61% and +3.11% for flat bars.
- F9: The long-versus-flat edge disappears in high volatility. Next-20-bar return for long bars minus flat bars was +2.25 points in the low 20-day-vol tercile and +2.56 points in the middle tercile, but −0.01 points in the high tercile (3.20% vs 3.21%). Even so, the book's mean daily return on long high-vol bars was the largest of the three (+0.40% vs +0.15% in the low tercile).
