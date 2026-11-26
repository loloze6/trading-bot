---
line: 7.b inconclusive
backtest: 032-01.b1.b1_flat-range-breaks-more-coins_1d
idea tested: 032-01.b1.b1_flat-range-breaks-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3723 USD
---
## Findings
- **F1:** The supporting check fails because the forecast's two parts grade the outcome in opposite directions. In folds B and C, 39 cases over 28 days, the post-pipeline narrowness component ranks the 20-day unusual move upward: low tercile −6.9 % (t −1.08), mid +4.9 %, high +19.1 % (t 3.90, 13 cases, all 13 rising), Spearman +0.40. The flatness component ranks it the other way: low tercile +8.9 %, mid +10.3 %, high −2.1 % (t −0.27), Spearman −0.21. The equal-weight forecast mixes the two, so its terciles barely separate (+3.3 %, +5.3 %, +8.6 %).
- **F2:** The width of the prior 60-day range, as a share of price, grades the move the same way narrowness does. Over 20 days, the narrowest-range tercile gains +19.4 % unusual (t 2.29, 84.6 % rising) against −0.6 % and −1.6 % for the wider terciles (Spearman −0.36). Over 10 days, the narrow half gains +15.7 % (t 2.50, 34 cases) against +2.6 % (t 0.50) for the wide half.
- **F3:** The move is carried by small breaks, not large ones. By how far the close sits above the prior 60-day high, the terciles give +13.9 % (mean break 1.0 %), +5.1 % (3.4 %) and −1.9 % (9.3 %) unusual over 20 days, Spearman −0.19. A big overshoot does not extend the rise.
- **F4:** The rise shows sooner than the plan's 20 days. The mean total return after a break is +6.4 % at 5 days, +13.6 % at 10 days and +9.0 % at 20 days. On the 10-day grid the unusual move is +9.2 % with t 2.21 (67 cases, 44 days), against t 1.20 for the 20-day grid on the same folds.
- **F5:** The effect is uneven across periods and coins, and these folds hold few cases. The 2020 cases gain +18.7 % (t 2.21, 14 cases) while the 2021 cases lose −1.3 % (t −0.22, 20 cases). XMR (+25.2 %, 4 cases) and XRP (+21.9 %, 6 cases) gain, while BTC (−6.5 %) and LINK (−29.9 %) lose. This is why the full-data t of 2.53 rests on its grading rather than its mean.

## Ideas
- `032-01.b1.b1.b1_compressed-range-breakouts-continue` (from F1, F2, F5): In a coin whose price has gone nowhere over the past 60 days, a daily close above the prior 60-day high is followed by a further rise over the next 20 days. The narrower that 60-day range was against the coin's 180-day range, the larger that rise.
- `032-01.b1.b1.b2_tight-range-breaks-ten-days` (from F2, F3, F4): In a coin whose price has gone nowhere over the past 60 days, a daily close above the prior 60-day high is followed by a further rise over the next 10 days. The narrower the 60-day range it broke out of, as a share of price, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
