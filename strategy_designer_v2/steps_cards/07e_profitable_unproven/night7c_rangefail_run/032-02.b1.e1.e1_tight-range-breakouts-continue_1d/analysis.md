---
line: 7.e profitable but not proven
backtest: 032-02.b1.e1.e1_tight-range-breakouts-continue_1d
idea tested: 032-02.b1.e1.e1_tight-range-breakouts-continue
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3768 USD
---
## Findings
- **F1:** The book earns 0.0706 % a day (t 1.94, 1449 days, folds B and C). Only 0.0264 % of that comes from the market's own rise; the other 0.0442 % is timing. The timing comes mostly from 2020 (0.233 % a day against 0.047 % from the market) and from windows w17, w10 and w11 (0.39 %, 0.19 % and 0.24 % a day). w12, w7 and 2018 lost.
- **F2:** The gain sits in a few trades. 193 trades have a mean net gain of 16.1 % and 69 % win, but the top 10 trades give 1256 of the 3114 summed percentage points. By coin, BTC, ETH and XRP each earn about 0.10 to 0.12 % a day, while ZEC (0.012 %) and LTC (0.024 %) earn barely more than their market part.
- **F3:** The break itself carries the move, more than the grading by range width does. Closes above the prior 60-day closing high are followed by unusual rises at every horizon: +4.0 % over 5 days (t 2.5, 120 cases, 74 days), +10.6 % over 10 days (t 2.6, 84 cases), +14.4 % over 20 days (t 3.1, 47 cases, 34 days). The forecast's slope on the move is flat at every horizon (t 0.68, 1.03 and 0.13).
- **F4:** The raw narrowness does grade the move, which the forecast does not show. The forecast tracks the range width (Spearman -0.75 with W), but it is standardised against its own last 61 values. Against the raw log range width in usual moves, the slope is negative at every horizon: t -2.14 over 5 days, -1.31 over 10, -1.01 over 20. By narrowness tercile, from narrowest to widest:
- **F5:** A narrow range comes before rises even without a break. On 20-day grid bars that are not breaks, the narrowest range tercile (W about 11) has an unusual move of +5.5 %, against -2.5 % and -4.2 % for the middle and widest terciles (191 cases).
- **F6:** The coin's own 60-day return grades its next 20 days on all grid bars. By quintile of the 60-day return, from lowest to highest, the unusual 20-day move is -3.2 %, -0.4 %, -2.5 %, +0.6 % and +6.1 % (about 40 cases each). Break bars sit only in the top two quintiles (8 % and 10 % of their bars).

## Ideas
- `032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster` (from F3, F4): When a coin closes above its highest close of the prior 60 days, the narrower its 60-day range of closes was against its average absolute daily move, the larger its rise over the next 5 days.
- `032-02.b1.e1.e1.e2_compressed-ranges-precede-rises` (from F5, F4): The narrower a coin's 60-day range of closes is against its average absolute daily move, the larger its rise over the next 20 days.
- `032-02.b1.e1.e1.e3_two-month-momentum-continues` (from F6, F1, F2): The higher a coin's 60-day return, the larger its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
