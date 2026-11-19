---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation
line: 7.b inconclusive
backtest: 016-05_up-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the more evenly its hourly volume was spread across those hours, the more the coin keeps rising over the next 3 days.
Consequence: Up moves made with modest, even volume reflect a hidden split buy order that is still working, so they continue.
Why:
- F1: The tested volume-evenness forecast barely separates outcomes: top-minus-bottom third excess 72h return is +0.00265 (Welch t 0.68, 972 vs 972 cases of 2916). The raw median/mean evenness ratio gives +0.0032 (t 0.80, n 2865). Its rank correlation with the 72h excess return is 0.017.
- F2: The volume-evenness effect is mixed across coins and years rather than concentrated anywhere. By coin it runs from +0.0205 (ZEC, t 1.71) to -0.0047 (ETH, t -0.54), and 3 of 6 coins are negative. By year only 2019 clears t 2 (t 2.26), against 2022 at -0.0127 (t -1.39).
