---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C and D
---
Idea: For a coin whose 14-day RSI is above 50, the higher that reading stands relative to its own past 60 days, the larger the coin's fall over the next 5 days.
Consequence: If confirmed, a trader would fade a coin's strong RSI readings over a 5-day horizon, more heavily the more extreme the reading; if rejected, a trader would refuse to short simply because RSI is high.
Why:
- F1: The test ran on one coin and one window only: BTC, w1, 2022, 120 daily bars. ETH and BNB never ran, so the plan's 3-coin design was reduced to 1 coin with 23 non-overlapping 5-bar grid points.
- F2: The situation is not rare within a window. 39 of 120 bars (32.5%) had a short forecast, 15 bars (12.5%) reached forecast ≤ −10 (mean recomputed RSI 64.0, against 33.0 on flat bars), and 9 bars sat at the −20 cap. The forecast's 10% quantile was −13.2.
- F3: The extreme bars come in clusters, not spread out. The 15 extreme bars form 3 runs of length 1, 2 and 12, so the 5-bar grid caught only 3 extreme cases (3 of 23 grid points, 13%), against the plan's minimum of 30.
- F4: The forecast is graded in the expected way. Mean RSI rises from 54.6 at forecasts in (−5, 0) to 59.1 at (−10, −5] and 64.0 at ≤ −10.
- F5: The outcome is large and fairly consistent across the few cases, but the count is too small. The 3 cases had a mean excess 5-bar return of −6.75% with a standard deviation of 6.35%, giving t = −1.84. The spread of all grid 5-bar returns was 7.6%.
- F6: The year was a bearish one (2022: mean RSI 41.6, only 32.5% of bars with RSI > 50, base 5-bar return −0.5%). Because the forecast is standardised over 60 days, extremes are relative, so a rate of about 3 grid cases per 120-bar coin-window should hold in other years. About 10 coin-windows would then reach 30 cases, and the default 6 coins over folds A–D give many more than that.
