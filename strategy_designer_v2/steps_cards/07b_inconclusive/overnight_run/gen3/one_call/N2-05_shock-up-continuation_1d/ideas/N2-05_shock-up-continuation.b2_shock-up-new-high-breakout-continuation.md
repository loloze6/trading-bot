---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.b inconclusive
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's outsized up day closes above its highest close of the prior 20 days, the coin keeps rising over the following five days.
Consequence: A trader would buy shock-up days that set a new 20-day closing high and skip those that stay inside the recent range.
Why:
- F6: Big up days that close above the prior 20-day closing high gain +1.82% over 5 bars (t 2.01, n 245), against −0.02% (t −0.04, n 242) for those that do not. Similarly, events above the 50-bar average gain +1.27% (t 1.91, n 299), against +0.03% (t 0.04, n 157) below it.
- F1: The 601 independent big-up-day events have a mean 5-bar excess return of +0.88% (t 1.67), but the median is −0.22%, the hit rate is 48.9%, the skew is 2.4 and the 5%-trimmed mean is only +0.34%, so a few large winners lift the mean while the typical event goes nowhere.
- F7: The effect is not stronger for bigger shocks: the z-score quartiles give +1.37%, +1.22%, −0.17% and +1.20% with no ordering. It also varies by coin, from ZEC +3.14% (t 1.75, n 98) to XMR −1.33% (t −1.33, n 90).
