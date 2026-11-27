---
line: 7.b inconclusive
backtest: 070-01.g1.d1_deep-slide-calm-run-break-fade_1d
idea tested: 070-01.g1.d1_deep-slide-calm-run-break-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2201 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: the mean short-side excess next-day return is +1.03 % with t 1.82 over 82 case-days (117 cases). On folds B and C alone, the run-break days with a non-zero short forecast give +1.45 % with t 1.82 over 54 days (79 cases). The effect is there; this data has too few cases to show it clearly.
- **F2:** The effect is spread across coins and is not one coin's artefact. In the deep-slide regime on folds B and C, 5 of 6 coins have a positive next-day excess: ETH +2.18 % (t 2.50, 27 days), XMR +1.87 % (t 1.93, 26), ZEC +1.55 % (t 1.54, 30), BTC +1.05 % (t 1.04, 18) and LTC +0.89 % (t 0.85, 30). Only XRP is negative, at −0.58 % (t −0.54, 20). No single coin carries enough cases to decide.
- **F3:** The effect varies by window, which widens the error. Of the windows with at least 7 case-days, w7 gives +2.59 % (t 2.12, 20 days), w9 +1.38 % (t 1.53, 18) and w14 +3.39 % (t 1.18, 12). Against them, w12 gives −1.47 % (t −2.85, 9 days) and w13 −0.29 % (t −0.17, 14).
- **F4:** The grading the forecast uses is weak inside the regime, and the next-day fade does not grow with the run's length below four days. Breaks after 1, 2 and 3 prior down days give +1.02 %, +0.91 % and +1.04 % (t 1.20, 0.79, 0.75). Only runs of 4 or more stand out, at +3.41 % (t 2.41, 13 days). Terciles of the 20-day fall in usual moves are flat: +1.09 % for the deepest, +1.60 % for the middle and +1.18 % for the shallowest. Narrowing the idea to its strongest cases would leave too few cases.
- **F5:** Run-break days in this data are followed by a fade at more than one horizon. With the forecast non-zero, the excess is +2.03 % over 2 days (t 2.07, 54 days) and +2.78 % over 3 days (t 2.28). The one-day test is on the predicted side, and more cases rather than another shape are what it lacks.
- **F6:** More data exists than the test used. The test ran on 6 coins. ADA, DOGE, LINK, TRX, UNI and AAVE have daily bars in folds A and D and in part of B and C, and AVAX, SOL, INJ and NEAR in folds A and D. Adding these coins would roughly add the cases the t of 1.82 needs to reach 2.

## Ideas
- `070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins` (from F1, F2, F3, F6): In a falling, calm market, an up day that ends a run of down days is followed by a fall over the next day, only while the coin's 20-day return is deeply negative. The fall is larger the deeper that 20-day decline, measured against the coin's own recent swing, and the more down days the run held beyond the first.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
