---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's 4h close falls below the lowest low of its preceding two days while its 7-day return is positive, the coin rises over the next six days. The wider the preceding two days' 4h ranges are relative to its 30-day average 4h range, the larger the rise.
Consequence: A trader would buy a sharp drop inside a rising week that came after wide, agitated ranges, rather than follow it down.
Why:
- F4: The F3 effect is graded by how wide the preceding ranges were: rank correlation 0.114 (p 1.6e-6, 1752 cases) between range width and the 6-day move.
- F5: At the other end of F3, the same downward breaks after the widest fifth of ranges gain +2.46 % over 6 days (t 3.27, 351 cases, 2 of 19 coins negative).
- F7: The quietness gradient appears only in rising weeks. For downward breaks in falling weeks, the quietness fifths range from -0.74 % to +0.52 % over 6 days (all |t| < 1.6).
