---
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h
idea tested: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5483 USD
---
## Findings
- **F1:** The book's shorts lose over their own holding: 8350 trades lost 1.30 % each before fees and 1.40 % after (25 % won, median hold 72 h). The tested cases moved against the short over 18 bars (−0.20 %, t −1.45, 4153 cases) and more over 72 bars (−1.08 %, t −3.99). The +0.31 % unusual move (t 2.25) exists only because the coins' normal drift is upward, so the total move per case is −0.6 times a 0.22 % round trip and no change of sizing or holding can make the book earn.
- **F2:** The forecast does not grade its bets. It sits at −20 in at least 75 % of cases (median −20, std 3.5), and 85 % to 92 % of cases are saturated in every narrowness third. That is why the supporting check had an empty larger half, and why the book weights a wide-stretch break as heavily as a narrow one.
- **F3:** Among the tested cases the narrowness of the stretch sorts the outcome as the idea says. The widest fifth (narrowness ratio median 0.20) is followed by a rise of 1.22 % over 18 bars (t −3.08 for the short). The narrowest fifth (median 0.68) is followed by a fall of 0.89 % (t 2.91), which is 4 times the cost of a round trip.
- **F4:** The losses come from breaks that follow a sharp fall. Cases in the deepest fifth of the 30-day return (median −36 %) lost 2.44 % to the short over 18 bars (t −5.93). Cases in the deepest fifth of the 7-day return (median −21 %) lost 2.53 % (t −5.83). The other fifths of the 7-day return gained 0.31 % to 0.59 %.
- **F5:** Breaks out of a wide stretch after a deep 7-day fall carry most of the loss. They rose 2.33 % over 18 bars (t −5.28 for the short, 544 cases) and 4.17 % over 72 bars (t −5.81). Narrow-stretch breaks after a moderate 7-day fall fell 0.97 % (t 2.72, 428 cases).
- **F6:** On every downward break in any regime, read once per 18-bar cell, narrowness grades the unusual move from a rebound to a continuation. Breaks out of the widest fifth of stretches rose 1.31 % more than drift (t 3.98, 983 cases). Breaks out of the narrowest fifth fell 0.96 % more than drift (t −3.64, 980 cases); their total move was −0.42 % (t −1.62).
- **F7:** Downward breaks after the deepest fifth of 7-day returns were followed by a rise of 1.98 % over 18 bars (t 6.11, 985 cases) and 3.16 % over 72 bars (t 5.50). That is about 9 times the cost of a round trip.
- **F8:** Upward breaks of the prior two-day high are graded by the 7-day return. After the strongest fifth of 7-day rises they gained 1.79 % over 18 bars (t 3.39) and 5.71 % over 72 bars (t 6.50). After the weakest fifth they lost 0.64 % (t −2.60).
- **F9:** The book loses most in windows where the coins rose: w4 −20.4 bps a day against +42.8 for holding, w21 −13.3 against +69.9, w11 −8.1 against +192.8. It gains only in falling windows (w14 +29.5 against −43.1, w7 +17.6 against −47.3), so it fails with one window left out and falls short of holding.

## Ideas
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend.d1_narrow-breakdown-after-mild-week` (from F1, F2, F3, F4, F5, F6): When a four-hour bar closes below the lowest low of a coin's preceding two-day narrow stretch, the coin falls over the next three days, and the narrower that stretch was compared with the coin's 30-day average four-hour range, the larger the fall. This holds only while the coin's 30-day return is negative and its 7-day decline before the break has been mild.
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend.d2_wide-breakdown-after-sharp-fall` (from F4, F5, F6, F7): When a four-hour bar closes below the lowest low of a coin's preceding two days after a fall in its 7-day return, the coin rises over the next three days. The deeper that 7-day fall and the wider the two-day range compared with the coin's 30-day average four-hour range, the larger the rise.
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend.d3_upward-break-after-strong-week` (from F8, F9): When a four-hour bar closes above the highest high of a coin's preceding two days, the coin rises over the next three days, and the stronger its 7-day return before the break, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
