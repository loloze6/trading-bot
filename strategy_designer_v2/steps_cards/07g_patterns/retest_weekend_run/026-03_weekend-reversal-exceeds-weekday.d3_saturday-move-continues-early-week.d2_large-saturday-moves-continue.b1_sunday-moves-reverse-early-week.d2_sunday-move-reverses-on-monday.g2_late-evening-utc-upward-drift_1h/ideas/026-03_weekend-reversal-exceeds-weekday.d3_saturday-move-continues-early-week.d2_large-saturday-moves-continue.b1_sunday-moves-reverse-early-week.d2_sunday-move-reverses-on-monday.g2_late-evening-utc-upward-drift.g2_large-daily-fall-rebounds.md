---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a one-day fall that is large relative to the coin's 30-day daily volatility, the coin rises over the next day by more than its normal drift, and the larger the fall in units of that volatility, the larger the rebound.
Consequence: A trader would buy a coin at the daily close after an unusually large fall and hold it about a day, a move of about 0.5 % that clears the cost of a trade.
Why:
- F2: Large one-day falls are followed by a rebound the next day, graded by the size of the fall. On a daily grid, the next day's excess return is +0.51 % in the decile of the largest falls (scaled by 30-day volatility; t 3.34, 1307 cases), +0.28 % in the second decile (t 2.31) and +0.03 % in the third. It is positive in all 6 coins (XMR +1.11 % t 3.38) and all 8 years, though near zero in 2024 and 2025 (+0.02 %, +0.04 %). Large one-day rises show no matching reversal (top decile −0.04 %, t −0.29).
