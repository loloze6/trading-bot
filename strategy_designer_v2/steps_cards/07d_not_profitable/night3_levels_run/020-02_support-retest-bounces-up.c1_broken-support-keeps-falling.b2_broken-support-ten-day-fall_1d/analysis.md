---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3554 USD
---
## Findings
- **F1:** The book loses because it is a short book in coins that rise. On its 1164 short grid cases, the 10-day return is still +0.55 % on average (raw short gain -0.55 %, t -1.33). The normal drift against the short is -1.19 % and the total move is -0.66 % per case, which is -3.4 times the 0.19 % cost of a trade. In window after window the book's mean daily return mirrors the coin's with the opposite sign (w11: book -0.50 %, coin +1.26 %; w21: -0.39 % against +0.57 %; w7: +0.38 % against -0.47 %).
- **F2:** The situation picks out relatively weak stretches, not falling ones. Closes with a past turning-up low above them rise +0.55 % over 10 days. Closes with none above (the flat bars) rise +2.58 % (t 3.10, 527 cases). Welch t of active minus flat is -2.18.
- **F3:** The effect is graded but too small for a short to earn. The drift-adjusted short gain climbs from -0.45 % in the smallest |forecast| quartile to +0.64 %, +0.75 % and +1.62 % (t 2.24) in the largest. The raw short gain is -1.61 % (t -2.03) in the smallest quartile and only +0.43 % (t 0.59) in the largest.
- **F4:** The small-forecast half of the shorts loses in every 30-day trend tercile (raw short -0.89 % to -1.27 %). The large half gains +0.25 % to +0.46 % in all three, so the trend does not explain the loss; the weak, distant-level cases do.
- **F5:** After a deep fall the short loses most. In the lowest quartile of the 90-day return (mean -48 %), the drift-adjusted short gain is -2.42 % and the raw gain -3.62 %. In the other three quartiles the drift-adjusted gain is +1.90 % to +2.93 % (64 to 65 cases each).
- **F6:** Position in the 60-day range carries the move the book misses. Grid closes in the lower three fifths of the range rise only +0.43 % to +0.61 % over 10 days (t 0.5 to 0.8), and the book is short on 86 % to 100 % of them. Closes in the upper two fifths rise +2.24 % (t 2.18) and +2.70 % (t 2.45), and the book is short on only 40 % and 15 % of them.

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation` (from F3, F4, F5): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, except when its 90-day return is a deep fall, after which it rebounds instead.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d2_clear-of-supports-rises` (from F1, F2, F6): When a coin's daily close sits high in its 60-day range, above every price where it turned up in the past 90 days, it tends to rise over the next 10 days, and the nearer the close is to its 60-day high, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
