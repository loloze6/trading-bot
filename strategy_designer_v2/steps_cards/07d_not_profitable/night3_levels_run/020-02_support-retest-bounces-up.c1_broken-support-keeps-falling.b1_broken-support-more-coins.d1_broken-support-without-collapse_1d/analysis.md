---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4189 USD
---
## Findings
- **F1:** The book loses because it is short most of the time in coins that rise. It is short on 78 % of bars. Its gain from the market's own rise is -31.3, against +11.6 from timing, for a net -19.7 (summed daily position gains). It loses in the windows where the coins rose, for example w21 (book -8.3, coins +15.3), w6 (-9.2, +12.9) and w11 (-5.9, +22.7), and earns where they fell, for example w2 (+5.6, -5.9).
- **F2:** The idea is real but smaller than the coins' drift, so a short on it loses before any cost. Over 2251 grid cases the total 10-day move on the short side is -0.26 % (t -0.86, 50.7 % winners). The verdict's own figures agree: unusual move +0.48 %, against a normal drift of -1.38 % in the short's direction. A round trip costs 0.22 %.
- **F3:** The short pays only when the coin is already falling, and loses after a rise. Cases after a 10-day fall of 6 % to 13 % gain +1.75 % on the short side (t 2.4, 407 cases). Cases after a 10-day rise above 5.8 % lose -2.12 % (t -2.7, 408 cases).
- **F4:** The coin's trend splits the cases the same way. Cases with the close below its 50-day average gain +0.43 % on the short side (unusual +1.8 %, 895 cases). Cases above that average lose -1.23 % (unusual +0.2 %, 320 cases).
- **F5:** The 90-day trend shows the same split. Cases whose 90-day return is between -20 % and -8 % gain +3.8 % on the short side (t 3.8, 97 cases), while across all bars the coins with the highest 90-day return rise +6.3 % over the next 10 days.
- **F6:** The forecast's grading is largely lost. Two thirds of the cases sit at the -20 cap. The third with the weakest forecast loses -1.12 % on the short side (t -2.2, 751 cases), so many shorts are taken where the support signal is faint.
- **F7:** Volatility also separates the cases. Cases in the calmest fifth (30-day daily volatility below 3 %) lose -1.41 % on the short side (t -1.8). Cases in the most volatile fifth gain +1.09 %.

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse.d1_broken-support-below-average` (from F1, F2, F4, F5): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the coin's daily close is below its average close of the past 50 days.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse.d2_broken-support-after-decline` (from F1, F2, F3, F6): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the coin's 10-day return is negative.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse.d3_broken-support-in-volatility` (from F2, F6, F7): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close and the more volatile the coin's daily returns over the past 30 days, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
