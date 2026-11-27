---
line: 7.g patterns
backtest: 077-01.b1.b1.b1_extreme-swing-scaled-moves-carry_1d
idea tested: 077-01.b1.b1.b1_extreme-swing-scaled-moves-carry
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3898 USD
---
## Findings
- **F1:** On the non-overlapping 7-day grid, the swing-scaled 14-day move (14-day return over the 30-day daily swing × √14) carries forward only when the coin is calm. With calm meaning a 30-day swing at or below the median of its last 120 days, the mean of z × the unusual 7-day move is +0.057 (t 4.13, 215 cases); with the coin agitated it is −0.016 (t −1.28, 192 cases).
- **F2:** The calm carry is not limited to the choppy market the brief names. For calm cases with |z| > 1, the signed unusual 7-day move is +5.6 % in falling markets (t 3.11, 61 cases), +11.0 % in choppy markets (t 3.14, 22 cases) and +5.8 % in rising markets (t 2.22, 73 cases). In agitated markets it is negative in all three trends (−3.6 %, −7.6 %, −3.0 %; t −1.1 to −1.4).
- **F3:** The calm carry is roughly graded by size but not cleanly monotonic. By |z| bin, the signed unusual 7-day move is +0.8 % for |z| ≤ 0.5 (t 0.37, 62 cases), +3.9 % for 0.5–1 (t 2.37), +3.3 % for 1–1.5 (t 1.87), +14.2 % for 1.5–2 (t 3.37, 19 cases) and +4.7 % above 2 (t 1.71, 32 cases). The agitated bins fall from +3.6 % to about −3 % as |z| grows.
- **F4:** The calm carry for |z| > 1 holds when cases of the same day are counted together: +5.8 %, day-clustered t 2.47, 102 cases, using an expanding calm rank. It is stronger after rises (+8.1 %, day t 2.28, 60 cases) than after falls (+2.4 %, day t 1.13, 42 cases).
- **F5:** The calm carry is not steady across time or coins, which weakens F1 to F4. By year it is +7.1 % in 2018, −0.7 % in 2019 (t −0.40), +11.0 % in 2020 and +7.6 % in 2021 (t 3.15). Eight of the nine windows with at least 5 cases are positive (w9 is −2.7 %). By coin, ETH is +8.1 % (t 2.79) and BTC is −0.6 % (t −0.30).
- **F6:** The standardised version of the move, the tested forecast's input, predicts the calm unusual 7-day move a little better than the raw swing-scaled move. Its correlation with the outcome is 0.286, against 0.232 for the raw move (215 calm cases).
- **F7:** Across all bars, the 3-day reversal after a coin's largest one-day falls against its swing is small. The bottom quintile of the one-day move is followed by a +1.0 % unusual 3-day move (t 2.27, 519 cases), and the other quintiles are near 0. The profile map already holds many one-day-fall rebound books, so this is not new.
- **F8:** The tested book cannot pay at this size. Its unusual move is +0.20 % per case (t 0.31) against a 0.22 % trade cost, and the plan's own top-third versus bottom-third growth check fails (Welch t 0.17). The carry in F1 and F2 is far larger per case but comes from only about 100 to 215 grid cases in folds B and C.

## Ideas
- `077-01.b1.b1.b1.g1_calm-swing-scaled-move-carry` (from F1, F2, F3, F4, F6): In a calm market, a coin's 14-day return measured in units of its own 30-day daily swing keeps moving the same way over the next 7 days, and the larger the move in swing units, the further it carries.
- `077-01.b1.b1.b1.g2_calm-swing-scaled-rise-continues` (from F2, F3, F4): In a calm market, a coin whose 14-day rise is large against its 30-day daily swing keeps rising over the next 7 days, the more so the larger the rise in swing units.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
