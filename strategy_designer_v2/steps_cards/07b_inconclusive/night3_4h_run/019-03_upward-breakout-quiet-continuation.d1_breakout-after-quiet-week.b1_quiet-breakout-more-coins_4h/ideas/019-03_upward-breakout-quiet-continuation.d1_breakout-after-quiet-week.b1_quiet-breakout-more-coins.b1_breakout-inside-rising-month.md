---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day narrow stretch, the coin rises over the next three days, only while the coin's 30-day return is positive. Inside that condition, the rise is larger the larger the coin's 7-day return up to the breakout.
Consequence: A trader should take upward breakouts only in a coin whose past month is rising, and weight them by how much the past week rose, rather than by how quiet the stretch was.
Why:
- F1: The tested result points the way the idea predicts but is small. On my recount the mean unusual 18-bar move is +0.17 % per case with t 1.28 over 6,599 cases (step 5's forecast-weighted figure is +0.19 %, t 1.39). Its size is +0.15 %, a strength of 0.015, against a usual move of 9.29 %. That is a third of the usual strength of real ideas (about 0.05, findings F10) and 0.7 times the 0.22 % cost of a round trip. The test already used all 19 coins and all four folds, so no more data is available to test it on.
- F2: The result is blurred mainly because it changes sign with the coin's own 30-day trend. Breakouts while the 30-day return is positive have a mean unusual move of +0.55 % (t 2.50, 2,799 cases, strength 0.059). Breakouts while it is negative have −0.46 % (t −2.59, 2,084 cases, strength −0.046). Averaging the two brings the result close to zero. Inside the positive-trend cases, 15 of 19 coins (0.79) are positive.
- F3: The coin's 7-day return before the breakout grades the move monotonically. From the lowest to the highest fifth of 7-day return, the mean unusual move is −1.12 % (t −4.45), −0.21 %, +0.30 %, +0.38 % and +1.26 % (t 2.36), about 977 cases each. The top fifth's strength is 0.11 and its move is 5.7 times the cost; the bottom fifth's move is a fall.
- F4: The idea's own gradings show no order. By forecast fifth, the mean unusual moves are −0.14 %, +0.52 %, −0.03 %, +0.01 % and +0.47 %. By the 7-day over 60-day range ratio, from quietest to least quiet, they are +0.27 %, +0.70 %, −0.36 %, −0.21 % and +0.22 %. Within the positive-trend cases, the forecast thirds give +0.37 %, +0.91 % and +0.39 %. Neither the narrowness of the stretch nor the quietness of the week carries the effect.
