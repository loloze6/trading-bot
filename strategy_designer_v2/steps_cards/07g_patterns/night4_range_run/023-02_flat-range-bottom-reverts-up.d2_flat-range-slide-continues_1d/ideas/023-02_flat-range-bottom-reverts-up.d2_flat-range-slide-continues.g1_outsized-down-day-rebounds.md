---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its usual daily move over the past 20 days, the more that coin rises over the next 1 day.
Consequence: After an outsized down day a coin is a short to close or a long to take for the next day, not a short to open.
Why:
- F4: A coin's one-day move scaled by its 20-day daily volatility predicts the next day's excess return, graded on the down side.
- F1: The book loses because it is short into sharp rallies. On its worst 1 % of coin-days the book lost -7.57 % while the coin rose +10.40 %, and on its best 1 % it gained +7.26 % while the coin fell -9.88 %. Its trades lost on average after fees on every coin, from -1.03 % (ZEC, 501 trades) to -2.34 % (XRP, 501 trades).
- F2: The book's trades do worse the larger the 10-day fall they enter on, the reverse of the idea. Trades in the most negative entry-forecast quartile lost -2.39 % on average (727 trades, median -2.37 %), against -0.71 % in the least negative quartile (727 trades). This matches the step-5 slope t of -0.02 on 1085 grid bars.
