---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation
line: 7.b inconclusive
backtest: 016-02_down-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger the share of that fall made by many small hourly losses in the same direction, rather than by its few biggest hours, the more the coin keeps falling over the next 3 days.
Consequence: Down moves built as a grind keep going, because a patient seller's split order is not yet finished.
Why:
- F1: The main measure's small positive mean comes from one year. Over all 2,762 grid bars it is a gain of 0.00151 with t 0.95, but 2018 alone gives 0.0218 (t 4.58, n 417). With 2018 left out, the gain is -0.0021 (t -1.26, n 2,345), and the other seven years split three positive and four negative, none with |t| above 1.72.
- F2: The forecast hardly varies once a fall has happened, so the test is close to "short after any 3-day fall". Its standard deviation is 0.76 around -10.0, with an interquartile range of -10.41 to -9.63. Its Spearman correlation with the excess 72-hour return is -0.015 (p 0.43).
- F4: Short grid bars are followed by an excess 72-hour return of only -0.0015 (t -0.96, n 2,762), against +0.0014 (t 0.89, n 2,921) on flat bars. Any continuation after a fall is too small to stand out from the coins' own moves.
