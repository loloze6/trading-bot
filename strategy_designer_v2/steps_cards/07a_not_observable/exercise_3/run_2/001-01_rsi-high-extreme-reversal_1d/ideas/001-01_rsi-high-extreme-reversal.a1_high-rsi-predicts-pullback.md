---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C and D
---
Idea: When a coin's 14-day RSI sits above its neutral level, the coin's return over the next 5 days is lower than its usual 5-day return. The higher the RSI, the larger the shortfall.
Consequence: If confirmed, a trader would lean short or reduce long exposure as a coin's 14-day RSI climbs to its extremes; if rejected, a trader would refuse to fade high RSI readings.
Why:
- F1: The test ran on a single coin and window (BTCUSD w1, 2022, 120 daily bars, 23 non-overlapping 5-bar grid cases). ETH and BNB are absent from the record, so only 3 extreme cases (forecast ≤ −10) were found, against the plan's minimum of 30.
- F2: The extreme situation is not rare. 15 of 120 bars (12.5%) have forecast ≤ −10 and 3 of 23 grid cases (13%) do, so a coin-window of about 120 daily bars yields roughly 3 extreme cases. Reaching 30 needs about 10 such coin-windows, or about 230 grid cases.
- F3: The extreme bars come in clusters. There are 3 runs of forecast ≤ −10, with lengths of 1, 2 and 12 bars (mean 5). The 5-bar grid therefore samples a long run only every fifth bar, which keeps the case count small relative to the bars spent at an extreme.
- F5: The outcome varies widely from case to case. The standard deviation of the 5-bar forward return on the grid is 0.076, against a mean excess after extremes of −0.068 (t −1.84 on 3 cases). The direction cannot be judged on this count, but 30 cases would give a standard error near 0.014.
- F6: The available Kraken data can supply the count. The six default coins (BTC, ETH, LTC, XMR, XRP, ZEC) run in all four folds A–D, and at about 3 extreme cases per coin-window this gives well over the 30 the plan requires. BNB is not available.
