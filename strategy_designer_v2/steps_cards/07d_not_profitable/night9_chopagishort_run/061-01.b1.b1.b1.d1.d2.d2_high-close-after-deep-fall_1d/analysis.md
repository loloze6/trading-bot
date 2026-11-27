---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall_1d
idea tested: 061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4169 USD
---
## Findings
- **F1:** Calmar failed because the book's deepest fall, −13.0 % over 164 days across w16 and w17, came while the coins themselves rose +121 % (book −10.7 % in that stretch); w17 alone lost −7.9 % while its coins rose +32 %, and w10 (−3.2 %, coins +84 %) and w11 (−1.3 %, coins +597 %) also lost, so the book falls when it shorts coins in a rising market.
- **F2:** Split by the coin's 60-day trend at the signal, the short's 5-day total move is −0.80 % (t −0.90, 146 cases) in rising markets, against +2.32 % (t 2.94, 166 cases) in falling and +3.54 % (t 2.22, 49 cases) in choppy ones; the book's own position-bar gain is −0.0005 % per bar over 604 bars in rising markets, against +0.36 % over 780 bars in falling and +0.48 % over 234 bars in choppy ones.
- **F3:** Not being in a rising market is no effect of its own: on grid bars with no signal, the 5-day short earns −0.66 % (497 cases) in falling and −2.10 % (178) in choppy markets, against +1.67 % (t 3.66, 544 cases) with the signal outside rising markets; the brief's own theory says a rising trend brings trend followers who carry a push further, which is why the fade fails there.
- **F4:** Outside rising markets the effect is graded and lives in the deep falls: the deepest third of 5-day falls (mean −13.1 %) gives a 5-day short move of +3.98 % and a 2-day move of +2.58 %, the middle third (−5.1 %) +1.21 % and +0.93 %, and the shallowest third (−1.5 %) −0.23 % and −0.09 %; on all signals the deepest fifth (−15.5 %) gives +4.86 %, against −0.23 % to −0.80 % for the two shallowest fifths, which pay less than the 0.22 % cost of a trade.
- **F5:** The move comes early: on all signals the short earns +0.91 % after 1 day (t 4.17), +0.94 % after 2 days (t 3.46) and +1.15 % after 5 days (t 2.82, 690 cases), then −0.32 % after 10 days, so days 3 to 5 add little and add the exposure to rising markets.
- **F6:** Limits: 329 of the 705 signal cases fall in the first 60 days of a window, where the 60-day trend cannot be read (5-day short +1.06 %, t 1.79), and the choppy agitated subset of the brief is too small to judge (11 cases, −1.35 %).

## Ideas
- `061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market` (from F1, F2, F3, F4): When a coin's daily close sits near the top of that day's high-low range after a 5-day fall, in a falling market, its price falls over the next five days, and the deeper the 5-day fall, the larger the fall that follows.
- `061-01.b1.b1.b1.d1.d2.d2.d2_high-close-fall-choppy-market` (from F2, F3, F4): When a coin's daily close sits near the top of that day's high-low range after a 5-day fall, in a choppy market, its price falls over the next five days, and the deeper the 5-day fall, the larger the fall that follows.
- `061-01.b1.b1.b1.d1.d2.d2.d3_high-close-fade-two-days` (from F1, F4, F5): When a coin's daily close sits near the top of that day's high-low range after a 5-day fall, its price falls over the next two days, and the deeper the 5-day fall, the larger the fall that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
