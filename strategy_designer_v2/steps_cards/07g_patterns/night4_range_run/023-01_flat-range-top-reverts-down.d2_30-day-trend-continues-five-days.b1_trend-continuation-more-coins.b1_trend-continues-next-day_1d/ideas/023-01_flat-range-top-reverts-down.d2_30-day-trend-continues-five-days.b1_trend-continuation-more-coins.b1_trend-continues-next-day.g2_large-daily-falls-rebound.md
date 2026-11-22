---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its 20-day volatility, the larger its rise over the next day.
Consequence: A trader would buy a coin after an unusually large daily drop rather than follow the drop.
Why:
- F3: After the largest one-day falls relative to 20-day volatility, the next day rebounds, and the rebound shrinks as the fall gets smaller. By decile of that move, the next-day excess was +0.37 % for decile 0 (t 2.23), +0.26 % for decile 1 (t 2.71) and +0.01 % for decile 2 (t 0.16), about 3070 bars each. The top decile of rises showed a weaker +0.19 % (t 1.67).
- F4: Five-day extremes show the same U shape. By decile of the 5-day move over its volatility, the next-day excess was +0.25 % for the lowest decile (t 2.20) and +0.33 % for the highest (t 2.80). Middle deciles ran down to −0.20 % (t −2.30).
