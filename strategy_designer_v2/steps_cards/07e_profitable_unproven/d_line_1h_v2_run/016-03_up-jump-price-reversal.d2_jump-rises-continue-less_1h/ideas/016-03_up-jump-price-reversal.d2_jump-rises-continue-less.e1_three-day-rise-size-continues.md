---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
line: 7.e profitable but not proven
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return has been on the upside, the larger its rise over the next 3 days, whatever the way the rise was built.
Consequence: A trader would size long exposure up with the size of a coin's recent 3-day rise rather than with how evenly that rise was spread across hours.
Why:
- F2: The size of the 3-day rise, not how it was built, predicts the next 3 days: on the non-overlapping 72-bar grid, coins in their top quintile of past 72-bar return (mean +0.118) went on to gain +0.0108 over the next 72 bars, against -0.0040 in the middle quintile (Welch t 3.96, about 1,100 cases each), and among rising cases the pooled slope of the forward 72-bar return on the past 72-bar return is 0.066 (t 2.77, n 2,802).
- F3: Once the size of the rise is held fixed, the share carried by the 3 biggest hours adds nothing: grind minus jump inside size terciles has Welch t 1.20, 1.65 and 0.14 (about 465 cases per group), and in a regression of the forward 72-bar return the past rise keeps t 2.34 while the top-3 share has t -1.02 and volatility t -0.09.
- F4: The book's top-3 share mostly measures the size of the rise: in the lowest share quartile the rise averaged +0.121 and the next 72 bars gained +0.0135, while in the highest share quartile the rise averaged only +0.0115 and the next 72 bars lost -0.0028, so the "grind" signal ranks rises by their size.
- F5: The book is long where rises were large: in its top position tercile (mean allocation 0.96) the past 72-bar return averaged +0.057 and the forward 72-bar return +0.0059, against +0.0003 in the flat tercile.
- F7: The effect also persists at a longer horizon: the top past-return quintile gained +0.0135 over the next 144 bars, against +0.0007 for the middle quintile.
