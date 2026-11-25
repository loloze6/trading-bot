---
line: 7.b inconclusive
backtest: 032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising_1d
idea tested: 032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3742 USD
---
## Findings
- **F1:** In folds B and C the plan's own split separates clearly: the small-margin half beats the large-margin half by +9.9 % against −3.5 % excess over 20 days (Welch t 3.11, 118 cases). On all four folds the same measure gave only +1.1 % (t 0.28, 240 cases), so the effect holds in folds B and C and must be flat or reversed in folds A and D (104 cases).
- **F2:** In folds B and C the excess 20-day return falls steadily across the margin quintiles, from smallest to largest margin: +11.9 %, +7.6 %, +4.8 %, −0.6 %, −8.3 % (about 25 cases each; Spearman −0.27). The grading the idea predicts is present where the effect shows.
- **F3:** The rise after a breakout depends on how tight the prior 60-day range of closes was (high/low − 1). In the narrowest third (mean width 27 %) the excess 20-day return is +14.7 % (t 3.57, 36 cases); in the middle third (51 %) it is +3.3 % (t 1.00, 32 cases); in the widest third (96 %) it is −1.4 % (t −0.37, 26 cases). Spearman of width against the excess 20-day return is −0.28.
- **F4:** The margin effect holds inside every range-width third, with Spearman of margin against the excess 20-day return of −0.37 (narrow), −0.36 (mid) and −0.38 (wide). So narrowness adds to the margin effect rather than replacing it.
- **F5:** The effect is mixed across periods and coins. By year the excess 20-day return is +8.4 % in 2019 (t 2.61, 26 cases), +10.0 % in 2020 (t 2.61, 47), −4.7 % in 2021 (t −1.31, 40) and −24.5 % in 2018 (5 cases). The margin Spearman is negative for LTC, XRP, ZEC and ETH (−0.38, −0.49, −0.44, −0.10) but slightly positive for BTC and XMR (+0.13, +0.15).
- **F6:** The small-minus-large split peaks at the plan's horizon. Its Welch t is 1.28 at 5 days, 2.32 at 10, 3.11 at 20 and 2.12 at 40 (133, 132, 118 and 92 cases), so the plan measured the right horizon.

## Ideas
- `032-02.b1.e1.e1.e1.e1.b1_marginal-breakouts-from-tight-ranges` (from F1, F2, F3, F4, F6): When a coin closes above its highest close of the prior 60 days, the smaller the margin by which that close exceeds the prior high, the larger the coin's rise over the next 20 days, only while the coin's closes over those prior 60 days stayed within a narrow range.
- `032-02.b1.e1.e1.e1.e1.b2_tight-range-breakouts-keep-rising` (from F3, F4, F5): When a coin closes above its highest close of the prior 60 days, the narrower the range of its closes over those 60 days, the larger its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
