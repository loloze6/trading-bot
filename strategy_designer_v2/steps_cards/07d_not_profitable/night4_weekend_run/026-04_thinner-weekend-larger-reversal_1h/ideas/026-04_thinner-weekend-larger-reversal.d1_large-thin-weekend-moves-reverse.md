---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The lower a coin's weekend volume is compared with its volume over the preceding five weekdays, the larger the share of its Saturday-Sunday move that is reversed over Monday and Tuesday. This holds only for weekend moves that are large in the coin's usual 48-hour moves, and the reversal grows with the product of the move's size and the weekend's thinness.
Consequence: A trader would bet against only the largest thin-volume weekend moves on Sunday's close, sized by move times thinness, and refuse the small ones that tend to continue.
Why:
- F1: The book loses because its forecast does not carry the graded effect that is in the data. The raw situation (weekend move in usual 48-hour moves × weekday/weekend volume ratio) predicts the next 48 hours with slope -0.038, t -2.78, on 2286 weekly cases. The traded forecast, standardised and negated, has a slope of -0.0003, t -0.18, despite a correlation of 0.85 with that raw product.
- F2: The reversal is carried only by the largest thin-volume weekend moves, and the small ones run the other way. Sorted by the size of the raw signal, the unusual move in the signal's direction over the next 48 hours is:
- F3: Thinness is what makes a weekend move reverse. The 48-hour slope on the weekend move is:
