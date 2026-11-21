---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's 4h close falls below the lowest low of its preceding two days while its 7-day return is positive, the coin falls over the next six days. The narrower the preceding two days' 4h ranges are relative to its 30-day average 4h range, the larger the fall.
Consequence: A trader would sell, or refuse to buy, a downward break out of a quiet stretch inside a rising week; at 2.6 % per case before drift, the move is several times the cost of a trade.
Why:
- F3: A 4h close below the 2-day low while the 7-day return is positive is followed by a fall when the preceding two days were quiet. After the quietest fifth of ranges the unusual move over 6 days is -2.61 % (t -3.90, 351 cases, strength -0.19, 18 of 19 coins negative), already -1.08 % at 3 days (t -2.75).
- F4: The F3 effect is graded by how wide the preceding ranges were: rank correlation 0.114 (p 1.6e-6, 1752 cases) between range width and the 6-day move.
- F6: The F3 fall holds in both halves of the record for the quietest 40 %: -1.91 % (t -2.17) up to 2021 and -1.43 % (t -3.02) from 2022. Pooled by 6-day date, its t is only -1.52, so it is partly shared across coins.
- F7: The quietness gradient appears only in rising weeks. For downward breaks in falling weeks, the quietness fifths range from -0.74 % to +0.52 % over 6 days (all |t| < 1.6).
