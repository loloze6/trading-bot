---
line: 7.b inconclusive
backtest: 032-02.b1_flat-range-upside-break-continues_1d
idea tested: 032-02.b1_flat-range-upside-break-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3773 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts (mean unusual 5-day move +1.85 %, t 2.17 over 232 cases on 190 days), and the slope on the entry forecast (−0.0038) is what made it inconclusive; that slope can barely be measured, because in folds B and C 91 % of the cases have a forecast pinned at the cap of 20 (median 20), so it rests on the 12 uncapped cases (+5.9 %) against the 117 capped ones (+2.4 %, t 1.77).
- **F2:** Measured on the uncapped distance above the old high, the grading is weak and not monotonic: the four quartiles of the raw break (mean 0.11, 0.35, 0.73 and 1.60 mean daily ranges) give +5.0 % (t 2.42), +3.3 % (t 1.50), −1.9 % (t −1.20) and +4.8 % (t 1.54); the slope on the raw distance is +0.018 (t 1.11) and the Spearman correlation is −0.11 over 129 cases, so this data cannot tell the grade apart from flat.
- **F3:** The horizon is not the cause, because the rise shows at every horizon near the plan's: over 3 days +1.6 % (t 1.91), over 5 days +2.7 % (t 2.11) and over 10 days +4.4 % (t 1.85), and it fades only by 20 days (+2.9 %, t 1.06), on 110 to 132 cases.
- **F4:** The level of the effect is spread over most coins and is diluted by one: BTC gives −2.9 % (t −2.43, 23 cases), while ETH, XMR, XRP and ZEC give +3.5 % to +11.5 % and LTC +0.1 %; without BTC the move is +4.0 % (t 2.71, 106 cases on 85 days).
- **F5:** Inside the choppy regime the effect does not sit in one part of it: the three terciles of the 60-day efficiency ratio give +4.9 %, +4.8 % and +5.5 %. Across periods, 6 of the 10 windows with cases are positive (for example w15 +8.6 %, w17 +7.5 %), and w12 (−3.4 %) and w18 (−1.7 %) are negative.

## Ideas
- `032-02.b1.b1_flat-range-upside-break-continues` (from F1, F2, F3, F4, F5): In a coin whose price has gone nowhere over the past 60 days, a daily close above the prior 60-day high is followed by a further rise over the next 5 days, and the further that close sits above the old high, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
