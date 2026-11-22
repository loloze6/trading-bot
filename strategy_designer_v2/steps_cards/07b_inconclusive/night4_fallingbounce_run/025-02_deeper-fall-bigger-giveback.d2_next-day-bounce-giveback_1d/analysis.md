---
line: 7.b inconclusive
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3412 USD
---
## Findings
- **F1:** The result points the way the idea predicts, but the size check fails. Over 1,428 short bets the next day's excess fall is +0.27 % with t 2.40, about 0.058 of a usual daily move. In my recount (1,338 cases) the forecast quartiles go +0.19 %, +0.44 %, −0.19 % (t −0.92) and +0.67 % (t 2.70): they are not monotone, so the top-minus-bottom check comes out at Welch t −0.53.
- **F2:** Grading the cases by the raw scaled rise instead of by the plan's 60-bar standardised forecast gives an orderly ladder. The z quartiles give +0.13 %, +0.09 %, +0.24 % and +0.62 % (t 2.25 for the top quartile, mean z 2.27), and the top half minus the bottom half by z is +0.43 % vs +0.11 % (Welch t 1.26, n 547/548). The grading is there, but this sample is too small to show it at t 2.
- **F3:** Across all up days in a falling coin, the next-day excess fall rises with the scaled rise: 0.17 % (z 0–1), 0.22 % (1–1.5), 0.75 % (1.5–2, t 2.25) and 0.87 % (2–3, t 2.64), with Spearman rho 0.039 (p 0.023). The same bins in rising coins have the opposite sign: −0.50 % and −0.79 %. For z > 1.5, falling-coin cases minus rising-coin cases is +0.79 % vs −0.50 %, Welch t 3.66 (n 386 vs 583).
- **F4:** The effect lasts one day only. The excess fall is +0.27 % (t 2.39) at 1 day, but t is 0.55 at 2 days, 0.50 at 3, 0.75 at 5 and 1.32 at 10.
- **F5:** The effect is uneven across coins and years. By coin, t runs from 2.13 (LTC) and 1.96 (ETH) down to −0.32 (ZEC). By year, falling-coin cases with z > 1.5 are strong in 2018–2020 (+1.5 %, +1.1 %, +2.5 %; t 2.6, 2.3, 3.0) and weak or flat from 2021 on (t between −0.31 and 0.94). The six default coins alone give few large-rise cases, only 386 with z > 1.5.

## Ideas
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins` (from F1, F2, F3, F5): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise in usual daily moves, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
