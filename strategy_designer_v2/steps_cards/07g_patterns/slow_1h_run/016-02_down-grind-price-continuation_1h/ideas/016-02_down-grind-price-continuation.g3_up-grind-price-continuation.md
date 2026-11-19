---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of that rise made by many small hourly gains rather than by its few biggest hours, the more the coin keeps rising over the next 3 days.
Consequence: An up move built as a grind gives a reason to stay long for a few more days, while a rise from a few spike hours gives a reason not to chase it.
Why:
- F5: After 3-day rises the brief's mirror holds, though weakly. Rises in the upper half of grind share have an excess 72-hour return 0.71% higher than the lower half (Welch t 2.21, n 2865), and the difference is positive for all 6 coins (+0.41% to +1.20%) and in 7 of 8 years. Once the size of the rise in volatility units is controlled for, the grind term falls to t 1.20, while size keeps t 3.32. Across the whole grid, the rise's size in volatility units does not predict the next 3 days (Spearman ρ −0.0002, n 5539).
- F4: The tested down-grind pattern is absent. After 3-day falls, the excess 72-hour forward return by grind quartile is −0.14%, −0.45%, −0.36% and +0.18%, none with |t| above 1.7. The main measure's t was 0.95. The book's Sharpe is −1.31, its mean daily return is negative in 6 of 8 years, and the coins' own mean daily return is positive in 6 of those 8 years.
