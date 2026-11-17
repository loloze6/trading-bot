---
brief: 010_rsi-midline-regime-direction
source-idea: 010-02_rsi-below-share-continuation
line: 7.b inconclusive
backtest: 010-02_rsi-below-share-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent below its midpoint of 50, the lower the coin's return over the next 14 days.
Consequence: RSI below the midpoint marks sellers in control, and that selling pressure persists, so the downtrend continues.
Why:
- F1: The main measure is on the side the idea predicts but short of the bar: mean forecast/10 × excess 14-day return 0.0156, t 1.59, on 384 independent grid cases. It is about the same in both coins that ran: BTC 0.0149 (t 1.24, n 192) and ETH 0.0163 (t 1.05, n 192).
- F5: The same sign holds at every horizon tried. The 3-day result is 0.0042 (t 2.31, n 1907), 7-day 0.0084 (t 1.81, n 815), 21-day 0.0286 (t 1.92, n 240) and 28-day 0.0235 (t 1.22, n 192). Spearman between share and excess return is negative at all of them (−0.02 to −0.10). So the result is a small, consistent continuation effect that is too small for 384 cases to show, not a sign flip.
- F6: Only two coins ran (BNB is not in the data), while four more coins with all four folds are available (LTC, XMR, XRP, ZEC). Adding them would roughly triple the independent cases from the 384 the test used.
