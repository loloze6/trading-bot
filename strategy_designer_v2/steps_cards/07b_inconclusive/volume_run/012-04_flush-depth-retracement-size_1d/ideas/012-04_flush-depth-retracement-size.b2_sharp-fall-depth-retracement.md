---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.b inconclusive
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's drop from its open to its low, the larger the price rise over the next 3 days, as price drifts back toward where it traded before the fall.
Consequence: A deeper intraday plunge on a sharp down day leaves more to retrace over the following days, so a trader leans long in proportion to the depth of the plunge.
Why:
- F6: Among all sharp falls, the raw open-to-low drop in percent predicts the rebound strongly: t 5.74 at 1 day, 4.90 at 2 days, 4.41 at 3 days, and 1.12 at 5 days. Scaled by 20-day volatility, the same drop shows nothing (t −0.13 at 3 days), so part of this grading may come from high-volatility periods.
- F4: The long-lower-wick condition works against the rebound. Among all 354 declustered sharp falls, the wick-over-range slope on the excess return is t −3.34 at 1 day and −1.96 at 3 days. The highest wick quartile averages −0.0112 over 3 days and the lowest +0.0131. Volume-burst falls without the wick average +0.0100 (n 119); those with it average −0.0026 (n 41).
- F1: The test's forecast barely grades the flush bars: 78% of kept flush bars sit at the cap of 20, and the middle and top forecast terciles both average exactly 20.0. Their mean excess 3-day returns run lo −0.0041, mid +0.0117, hi −0.0011, so the slope (t −0.65 recomputed, −0.75 in the verdict) has almost no spread to work on.
