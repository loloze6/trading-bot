---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its 52-week high while its 30-day return is positive, the higher its return over the next 7 days, with the gain rising steeply as the close reaches the high itself.
Consequence: Weight longs heavily toward coins closing at or right next to their 52-week high, and give little weight to coins merely in the upper part of their range.
Why:
- F3: The tested gain is concentrated at the very top of the range, not spread across it: among active bars, only the top quintile of the 365-bar range position earns a clear excess, +3.00 % over 7 bars (t 3.09, n 434), while the other four quintiles earn +0.08 % to +0.56 % (all t below 1). The top forecast quintile likewise earns +3.48 % (t 3.84) against -0.69 % to +0.81 % below it.
- F5: The book's profit comes from long holdings and is lost on quick flips: trades lasting a median of 1 day average -3.9 % after fees with 13 % winners, and 3-day trades average -3.0 % with 24 % winners. Trades of a median of 38 days average +53.9 % with 86 % winners (about 950 trades per quintile).
