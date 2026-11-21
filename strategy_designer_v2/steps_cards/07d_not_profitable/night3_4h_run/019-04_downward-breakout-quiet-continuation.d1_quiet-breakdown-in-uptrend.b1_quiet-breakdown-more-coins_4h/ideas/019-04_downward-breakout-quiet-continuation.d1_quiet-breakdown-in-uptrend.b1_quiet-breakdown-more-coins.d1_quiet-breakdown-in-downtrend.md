---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day narrow stretch, the coin falls over the next three days, and the narrower that stretch was compared with the coin's 30-day average four-hour range, the larger the fall, only while the coin's 30-day return is negative.
Consequence: Short a narrow-range breakdown only in a coin that has fallen over the past month, where the narrowest stretches fall several times a round trip's cost, and refuse it in a rising month.
Why:
- F1: The book's regime points the wrong way. On downward breaks (n 1965, one per 18-bar grid cell) the coin then rises more than its usual drift while its 30-day return is positive: the unusual 18-bar move is +0.60 %, t 2.9, so the short loses. While the 30-day return is not positive, the same breaks are followed by a fall: -0.34 %, t -2.2, n 2938.
- F2: The narrowness gradient is real and runs the way the idea says. Across all downward breaks, the unusual 18-bar move goes from -1.04 % (t -3.9, n 981) in the narrowest fifth of the two-day range (about 1.5 times the 30-day mean bar range) to +1.30 % (t +4.0, n 981) in the widest fifth (about 4.7 times). The correlation of range width with the unusual move is +0.12.
- F3: The narrow-break fall is concentrated in falling months. While the 30-day return is not positive, the narrowest fifth falls -1.35 % unusual (t -4.4, n 649, strength 0.13) and -0.81 % in total, about 6 and 3.7 times the 0.22 % round-trip cost. While the 30-day return is positive, the same narrowest fifth gives only -0.43 % (t -0.9, n 332).
