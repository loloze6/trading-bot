---
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4569 USD
---
## Findings
- **F1:** Only breakouts after a deep week pay. Grouped by the 7-day fall measured in the coin's usual 7-day move, the deepest fifth (beyond -0.69 of a usual move) returns +0.91 % total per case on the short (t 2.1, 427 cases), with strength 0.16; the shallowest fifth (fall under 0.09 of a usual move) loses -1.07 % (t -3.0, 427 cases), so the coin rises after those breakouts.
- **F2:** In the book's own gains the deepest fifth by entry depth earns +1.53 (sum of bar gains) and every other fifth earns 0.03 down to -0.35, so the shallow-fall entries eat almost all of the deep entries' gain. These are the entries that drive the mean daily return of 3.7e-05 and the Sharpe of 0.15.
- **F3:** Only the deepest fifth covers the cost of a trade. Its total move of +0.91 % is about 4 times the 0.22 % round trip. The three middle fifths have total moves between -0.08 % and +0.45 %, below or about at the cost, and the pooled total is only +0.31 %, 1.4 times the cost.
- **F4:** The forecast grades the shallow falls too lightly to keep them out of the book. It is standardised over its own last 60 values, so its correlation with depth in usual-move units is only 0.57. Its weakest fifth (|forecast| under 1.9) still trades and loses -1.30 % per case (t -3.3, 427 cases), while its strongest fifth earns +0.94 % (t 2.2).
- **F5:** A falling month carries the effect.
- **F6:** The result rests on falling windows, which fails the leave-one-out check.
- **F7:** Positions last longer than the horizon and lose money. The book's 3434 short trades last 127 hours on average, against the 72-hour horizon, and average -1.02 % before fees and -1.12 % after, even though the idea's cases are positive on average.
- **F8:** The narrowness of the preceding range does not grade the move. Unusual move per case by range width against its 30-day median runs 0.44 %, 0.90 %, 0.79 %, 0.74 % and 0.73 % from the narrowest fifth to the widest. The brief's quiet range adds nothing to this book.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails.d1_breakout-fails-after-deep-week` (from F1, F2, F3, F4): When a four-hour bar closes above the highest high of the preceding two days after the coin has fallen over the past 7 days, the coin falls over the next three days, and the deeper the past week's fall measured against the coin's usual 7-day move, the larger the decline.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails.d2_failed-breakout-in-falling-month` (from F5, F6, F1): When a four-hour bar closes above the highest high of the preceding two days after the coin has fallen over the past 7 days, the coin falls over the next three days, and the deeper the past week's fall, the larger the decline, only while the coin's 30-day return is negative.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
