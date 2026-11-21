---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two days, the coin rises over the next three days, and the wider those two days' range was compared with the coin's 30-day average four-hour range, the larger the rise, only while the coin's 30-day return is positive.
Consequence: In a coin that has risen over the past month, buy a breakdown out of a wide, violent two-day range instead of shorting it, because the wider the range the larger the rebound that follows.
Why:
- F1: The book's regime points the wrong way. On downward breaks (n 1965, one per 18-bar grid cell) the coin then rises more than its usual drift while its 30-day return is positive: the unusual 18-bar move is +0.60 %, t 2.9, so the short loses. While the 30-day return is not positive, the same breaks are followed by a fall: -0.34 %, t -2.2, n 2938.
- F4: In rising months, a downward break out of a wide two-day range is followed by a rise, and it grades by width. The unusual 18-bar move across the third, fourth and widest fifths is +0.40 %, +1.13 % (t 2.6) and +1.88 % (t 3.5, n 394), with a total move of +2.4 % (about 11 times the cost) and +3.8 % over 36 bars.
- F5: The book shorts the cases that rise. Because its width is standardised over its own past values (median post-pipeline value 5.97), 865 of its 1606 active cases sit in the three wider fifths. There the coin's unusual move is +0.39 %, +1.07 % (t 2.2) and +1.51 %. This is why the book's Sharpe is -0.39, its trades win 29 % of the time and its mean daily return is -0.00005.
- F6: Downward breaks that come after the deepest 3-day falls (lowest fifth of the 3-day return, n 981) are followed by an unusual rise of +1.43 % (t 4.2) and +3.1 % in total over 36 bars. Their two-day range is wide (median 3.6 times the mean bar range), which is the same rebound as in F4.
