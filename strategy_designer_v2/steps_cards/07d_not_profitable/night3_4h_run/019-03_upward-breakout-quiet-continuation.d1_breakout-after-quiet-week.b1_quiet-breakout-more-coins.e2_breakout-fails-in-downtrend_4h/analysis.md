---
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4854 USD
---
## Findings
- **F1:** The book loses because its short bets pay the coins' own rise: summed over all coins and windows, position times next-bar return is -3.46, of which -15.01 is the market's drift against a book that is always short (mean position -0.18 to -0.32 on every coin) and +11.55 is timing; per entry the move from the signal's close over 12 days is +2.53 % unusual (t 9.2, 4027 entries) but only +0.37 % total (t 1.33), and 2548 short trades lost 3.9 % each before fees.
- **F2:** The idea's total move per case, +0.34 %, is only 1.5 times the 0.22 % cost of a round trip, because the coins' normal 12-day drift in the short direction is -2.21 %; the forecast's size does not grade the move: the total move is +0.93 %, +0.12 %, +0.01 % and +0.41 % from the largest to the smallest forecast quartile, and the correlation with the move is only 0.013.
- **F3:** The shallowest 30-day falls lose: breakouts with a 30-day return between -6 % and 0 are followed by a 12-day rise, a total of -2.66 % in the short direction (t -3.79, 701 entries). Falls of -13 % to -24 % give +2.84 % (t 4.86) and falls deeper than -24 % give +1.35 % (t 1.86).
- **F4:** Breakouts after a very deep 90-day fall reverse up: with a 90-day return below -43 %, the 12-day total in the short direction is -14.1 % (t -6.94, 133 entries), against +2.3 % to +4.2 % in the other quartiles (Spearman of 90-day return with the move +0.26). Most of these cases sit in w13 (48 cases, -32.6 %) and w12/w14/w18.
- **F5:** A narrow range before the breakout carries the decline: in the quarter of entries with the narrowest 2-day range against its 30-day mean, the 12-day short total is +2.08 % (t 2.93, 680), and in the widest quarter it is -1.31 % (t -1.89). Combined with a 30-day fall of -13 % to -24 % and a narrow range, it is +4.71 % (t 5.63, 343), 21 times the cost.
- **F6:** The narrow-range effect comes from the later windows: in w13 to w24 the narrowest quarter gives +3.15 % (t 3.54, 413) and the widest -2.09 % (t -2.07). In w1 to w12 the narrowest gives only +0.43 % (t 0.37).
- **F7:** The decline is spent within 12 days and then reverses, while the book keeps holding. Summed position-times-return is +1.12 in a position's first 12 days, -2.19 in days 12 to 24 and -2.33 in days 24 to 36. The mean trade lasts 490 hours (about 20 days). From the signal's close, the 24-day short total is -0.97 % (t -2.08, 3715).
- **F8:** The book's chained deepest fall reaches -64 % and keeps deepening through the windows where the coins rose (w4 +51 %, w6 +76 %, w11 +229 %, w21 +85 % summed coin return, book -7 % to -21 %); it earns only in falling windows (w2 +29 %, w14 +35 %, w24 +27 %). Coins in the calmest quarter of 30-day volatility rose after the breakout (short total -3.10 %, t -4.44).

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend.d1_tight-range-breakout-fails-downtrend` (from F1, F2, F5, F6): When a coin's four-hour bar closes above the high of its preceding two days while its 30-day return is negative, the coin falls more than usual over the next 12 days, and the narrower its four-hour ranges over those two days compared with its ranges of the past 30 days, the larger the decline.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend.d2_breakout-fade-unless-capitulated` (from F3, F4, F8): When a coin's four-hour bar closes above the high of its preceding two days while its 30-day return is negative, the coin falls more than usual over the next 12 days, the deeper that 30-day fall, only while its 90-day fall is moderate; after a deep 90-day fall the same breakout is followed by a rise over the next 12 days, the larger the deeper the 90-day fall.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend.d3_breakout-after-capitulation-rises` (from F4): When a coin's four-hour bar closes above the high of its preceding two days after a 90-day fall, the coin rises over the next 12 days, and the deeper that 90-day fall, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend.d4_failed-breakout-decline-reverses` (from F7, F1): After a coin's four-hour bar closes above the high of its preceding two days while its 30-day return is negative, the coin rises more than usual from 12 to 24 days later, and the larger its decline over the first 12 days, the larger that later rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
