---
line: 7.g patterns
backtest: 031-03_yearly-low-break-extends_1d
idea tested: 031-03_yearly-low-break-extends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3859 USD
---
## Findings
- **F1:** Closes under the prior 365-day closing low are rare and show no reliable 10-day move either way. On the 10-day grid, the 24 break cases (13 days) ended +3.80 % above the coin's normal drift (t 0.77), against −0.06 % (t −0.08) for the 1,622 other cases. The step-5 size reading (33 cases on 24 days) leans the same bounce way, at −5.50 % on the short side, but its t of −1.96 does not clear 2.
- **F2:** The bounce leans on breaks that come inside an ongoing break episode, but neither group stands out. Repeat break bars (another break in the prior 10 days) ended +3.76 % above drift over 10 days (t 1.58, 158 bars on 85 days, overlapping). Fresh breaks ended −1.27 % (t −0.42, 62 cases on 48 days), and fresh breaks stay between −0.7 % and −2.2 % at 3, 5, 10 and 20 days, with every t below 1 in size.
- **F3:** Depth below the old low does not grade the move the way the tested idea says. On the grid, the shallowest third of breaks ended +10.3 % above drift (t 1.66) and the deepest third −5.2 % (t −1.58), with 8 cases each. Among fresh breaks the Spearman correlation between depth and the 10-day move is −0.11, and the two depth halves differ by 0.3 points (−1.42 % vs −1.11 %).
- **F4:** Among fresh breaks, a larger break-day return comes before a weaker 10-day move. The half with the higher 1-day return ended −4.68 % below drift (t −1.99, 31 cases on 29 days) and the lower half +2.14 % (t 0.41), with Spearman −0.19. This is one of about a dozen splits tried, so it does not stand out.
- **F5:** Across all bars, nothing I checked separates from chance once the number of looks is counted (about 40 groups). The checks were:
- **F6:** The day after a break bar the coin rose more than on other days, +0.98 % against +0.12 % (226 against 16,678 bars, standard deviations 6.5 % and 4.8 %). The break bars cluster in episodes, so this gap is not independent evidence; it is roughly a t of 2 before clustering.

## Ideas
- No ideas: The data gives no stable pattern to build on. The breaks are few (24 grid cases on 13 days), the hints of a post-break bounce (F1, F2, F6) and of a falling break day continuing (F4) all have t below 2, and none of the bar-wide angles I examined (F5) stands out from chance after that many looks.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
