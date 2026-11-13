---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.d not profitable
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin in the death-cross state is stretched far below its averages, it tends to rise over the next days. Stretched here means the gap between the short and long average is widening and the price sits below the short average.
Consequence: A trader should not add to or hold a short when the downtrend looks most extended, and may treat that state as a setup for a rebound.
Why:
- F9: The short loses most when the downtrend looks most extended. It loses -0.001628 a bar while the spread is widening against -0.000289 while it narrows. It loses -0.001626 when price is below its 50-day SMA against -0.000490 when price is above it. Both point to reversal after stretched moves rather than persistence.
- F3: A larger forecast loses more in the book: the bottom |forecast| quartile (mean forecast -0.38) earns +0.000074 gross a bar, while the top quartile (mean -15.9) earns -0.002029. At the trade level, small-entry trades average -12.8%, mid-entry trades -13.4% and large-entry trades -7.4%. This is the reverse of the plan's supporting tercile check, which passed at +0.0071.
- F2: The coin rises while the book is short: the mean daily coin return on short bars is +0.000777 against +0.001287 on all bars, and the 10-bar forward return in the short state is 0.0128 against 0.0135 overall, so the death-cross state carries almost no downward drift relative to holding.
