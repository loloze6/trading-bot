---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
line: 7.b inconclusive
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day narrow stretch, the coin falls over the next three days, and the narrower that stretch was compared with the coin's 30-day average four-hour range, the larger the fall, only while the coin's 30-day return is positive.
Consequence: Short a downward break out of a narrow range only in a coin that has risen over the past month, and refuse the short in a falling month, where the drift and the rebound eat it.
Why:
- F1: The tested short is on the predicted side but small, and it does not grow with narrowness. The mean short-signed unusual 18-bar move is +0.56 % (t 1.74, 670 cases). The narrowest quartile of stretches gives +1.01 % (t 1.15) and the widest +0.29 % (t 0.44). The Spearman correlation between narrowness and the move is -0.015, and the larger-minus-smaller forecast split is -0.17 %. So more t alone would still leave the supporting check failing.
- F2: The effect is mixed across the data. By coin it runs from LTC at -1.62 % (t -2.05, 94 cases) to XRP, ZEC and XMR at +1.32 % to +1.69 % (t 1.77 to 1.86). By year, 2018 alone gives +5.07 % (t 4.06, 63 cases), while 2020 and 2021 give -1.21 % and -1.22 %. Much of the mean rests on one year.
