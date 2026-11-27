---
line: 7.d confirmed, not profitable
backtest: 070-01.g1_calm-decline-long-run-break_1d
idea tested: 070-01.g1_calm-decline-long-run-break
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3881 USD
---
## Findings
- **F1:** The idea's own move covers its costs, so cost is not why the book fails. The 273 trades gain 0.647 % before fees and 0.547 % after, held about 0.99 days, with 52.8 % winners. What fails is the risk side: the book's deepest fall on folds B, C is -14.5 %, reached in w9, against a +3.0 % yearly return.
- **F2:** The book's falls come from short positions caught by sharp up days. Its ten worst days came on days the coins rose: on its -6.31 % day they rose 12.2 %, on its -3.88 % day 8.1 %, and on its -2.47 % day 12.5 %. The deepest falls sit in windows where the cases lost: w9 averaged -0.08 % per case (n 60) and w13 -1.07 % (n 22, fall -9.9 %), while w7 earned +2.22 % (t 3.54) and w14 +2.32 % (t 2.51).
- **F3:** Within falling calm bars, the effect lives only where the coin's 20-day return is already deeply negative. On break days, the short side's next-day excess move by 20-day return tercile is:
- **F4:** The deep 20-day fall is not an effect of its own. On falling calm days with no break signal, the low tercile earns only +0.17 % short (t 0.77, n 481), against +1.65 % when the break signal is there. The middle tercile alone earns +0.59 % (t 3.04, n 464), half its +1.20 % with the signal. The run-length grading holds inside the deep tercile: breaks of 3+ down days earn +2.07 % (t 2.68, n 42) against +1.18 % (t 1.32, n 37) for breaks of 2. This fits the brief's theory: a deeper recent decline leaves more trapped holders waiting to sell into relief.
- **F5:** The 20-day fall scaled by the coin's own 20-day swing grades the cases the same way. The lowest third earns +1.54 % (t 2.49, n 77), the middle third +1.28 % (t 2.43, n 79) and the highest third +0.29 % (t 0.74, n 78).
- **F6:** The fade does not depend on the falling calm profile. On break days outside the profile, the raw next-day short move is:
- **F7:** The gain is concentrated in time and does not grow with a longer hold. By year, cases earn +1.65 % in 2018 (t 3.25, n 120), +0.08 % in 2019, +0.02 % in 2020 and -0.06 % in 2021. Holding 2 days earns +0.88 % (t 2.13) and 3 days +0.76 % (t 1.35), against +0.76 % (t 2.77) for 1 day. The size of the bounce itself does not grade the fall: each up-day tercile earns +0.72 % to +0.73 %.

## Ideas
- `070-01.g1.d1_deep-slide-calm-run-break-fade` (from F3, F4, F5, F1, F2): In a falling, calm market, an up day that ends a run of down days is followed by a fall over the next day, only while the coin's 20-day return is deeply negative. The fall is larger the deeper that 20-day decline, measured against the coin's own recent swing, and the more down days the run held beyond the first.
- `070-01.g1.d2_run-break-fade-every-market` (from F6, F7, F1): An up day that ends a run of down days is followed by a fall over the next day. The fall is larger the more down days that run held beyond the first, so the up day after a single down day is followed by almost no fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
