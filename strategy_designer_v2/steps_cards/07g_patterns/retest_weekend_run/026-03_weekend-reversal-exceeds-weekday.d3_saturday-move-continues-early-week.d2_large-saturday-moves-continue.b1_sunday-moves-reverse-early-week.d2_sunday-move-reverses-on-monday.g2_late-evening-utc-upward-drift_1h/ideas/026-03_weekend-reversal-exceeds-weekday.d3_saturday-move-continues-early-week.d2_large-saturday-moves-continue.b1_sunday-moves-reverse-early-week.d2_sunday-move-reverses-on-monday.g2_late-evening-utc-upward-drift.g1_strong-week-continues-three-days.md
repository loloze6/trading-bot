---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin whose 7-day return is large and positive relative to its 30-day daily volatility keeps rising over the next 3 days, by more than its normal drift, and the stronger the 7-day rise relative to that volatility, the larger the 3-day gain.
Consequence: A trader would buy coins after unusually strong weeks and hold them for about three days, a move of about 2 % that clears the 0.19 % cost of a trade many times over.
Why:
- F1: Over 7 days and 3 days, momentum shows at the extreme: on a non-overlapping 3-day grid, the decile of the largest 7-day returns (scaled by 30-day daily volatility × √7) is followed by a 3-day return +1.99 % above the coin's drift (t 3.98, 429 cases). The middle deciles 1–8 run from −0.49 % to +0.16 %. The effect is positive in 4 of 6 coins (BTC +1.80 % t 3.07, ETH +2.02 % t 2.56, XRP +6.42 % t 3.29) and in 6 of 8 years (2024 +3.56 % t 3.54, 2020 +3.43 % t 2.62). Its Spearman correlation with the next 3 days, among positive 7-day returns, is +0.065.
