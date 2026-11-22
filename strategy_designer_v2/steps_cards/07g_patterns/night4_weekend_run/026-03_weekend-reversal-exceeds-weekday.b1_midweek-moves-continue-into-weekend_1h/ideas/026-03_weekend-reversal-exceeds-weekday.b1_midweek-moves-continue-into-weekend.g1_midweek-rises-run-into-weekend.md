---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 48-hour rise over Wednesday and Thursday is followed by a further rise over the next two days, Friday and Saturday, and the larger the midweek rise, the larger the rise that follows.
Consequence: A trader would buy a coin into the weekend after a midweek rise, with more conviction the larger the rise, rather than sell after a midweek fall.
Why:
- F1: The Friday-Saturday continuation is carried by midweek rises. After a Wednesday-Thursday rise the drift-removed 48-hour move is +0.70 % (t 3.77, 1138 cases, slope t 3.69). After a midweek fall it is only +0.09 % (t 0.50, 1254 cases, slope t -0.64). By quintile of the midweek move, the top quintile earns +1.36 % (t 4.19, 480 cases) and the bottom three are near zero (t between -0.25 and 0.52).
- F2: The book shows the same split. Long trades earn +0.62 % per trade after fees and short trades lose -0.94 %. Every quartile of entry forecast loses after fees (from -0.11 % to -0.30 % per trade).
- F6: The tested idea is unstable across coins and years. By coin, only ZEC is significant (t 3.53); the others range from t -1.70 (XMR) to t 1.24 (XRP). Yearly slope t values swing from 4.12 (2018) and 3.88 (2025) to -1.98 (2019) and -1.83 (2020).
