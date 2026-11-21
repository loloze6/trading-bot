---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
line: 7.b inconclusive
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two days while its 30-day return is positive, the coin rises over the next three days, and the wider those two days' range was compared with the coin's 30-day average four-hour range, the larger the rise.
Consequence: Buy a sharp break below the two-day low in a coin rising over the past month, sizing up as the preceding range was wider, rather than shorting it.
Why:
- F2: In rising months, a 4h close below the prior 2-day low is followed by a rise, not a fall. Over all such breaks the short-side unusual move is -1.03 % over 18 bars (t -3.85, 1152 untested cases), -0.56 % over 6 bars (t -3.90) and -1.32 % over 36 bars (t -3.00).
- F3: In rising months, the rebound grows with the stretch's width, which is the opposite of the tested grading. By width quintile (narrowest to widest), the short-side unusual move is +0.46 %, +0.06 %, +0.39 %, -1.27 % (t -3.18) and -1.69 % (t -3.77, 539 cases). It also grows with the 30-day return: -0.14 % in the weakest rising quartile and -1.13 % (t -2.32) in the strongest.
- F6: Both moves are large next to the cost of a trade (0.22 % for a buy and a sell). The falling-month narrowest-quintile short has a total move of +0.60 % (2.7 times the cost) and an unusual move of +1.13 % (5 times). The rising-month widest-quintile break, read as a long, has a total move of +2.22 % (10 times) and an unusual move of +1.69 % (7.7 times). By F11, both are in the size range where books have paid.
