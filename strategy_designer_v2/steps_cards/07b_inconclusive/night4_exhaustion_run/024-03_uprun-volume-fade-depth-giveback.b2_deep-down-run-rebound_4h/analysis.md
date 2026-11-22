---
line: 7.b inconclusive
backtest: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3557 USD
---
## Findings
- **F1:** The tested idea fires on almost any down-closing bar, and its forecast barely grades the cases. Of 5717 replicated cases (the verdict counts 5709 at +0.05 %, t 0.48; the replication gives +0.084 %, t 0.76 over 18 bars), 3470 come from a single down bar and 1545 from two. The forecast sits at its cap of 20 in more than half of the cases (median 20.0). So the mean is a blend of a few deep streaks with thousands of one-bar dips, and its strength is 0.007 of a usual 8.17 % move.
- **F2:** The effect is present only in the deepest streaks and absent or reversed in the middle, so it is mixed, not uniformly weak. Cases in the top fifth of streak loss (more than 2.25 usual 4h moves) gain +0.95 % beyond drift over 3 days (t 3.37, n 1144). The middle fifth (1.0–1.4 usual moves) loses −0.68 % (t −2.93), and the lowest fifth gains +0.25 % (t 1.04).
- **F3:** The give-back rises with the volume behind the fall, the opposite of the brief's "fading volume". Cases whose streak traded more than 1.29 times the volume of the preceding 30 bars gain +0.77 % over 3 days (t 3.11, n 1395). Cases in the lowest volume quarter, under 0.44 times, lose −0.45 % (t −2.10).
- **F4:** Deep streaks with heavy volume carry most of the effect. The top fifth of streak loss inside the top quarter of volume gains +1.27 % (t 3.09, n 548), more than 6 times the 0.19 % cost of a trade. The top fifth of loss inside the lowest volume quarter loses −2.18 % (t −2.03, n 85).
- **F5:** The deep-streak effect holds across coins and years, while the full case set swings with the market. Deep streaks are positive in 6 of 6 coins (BTC +0.00 % up to ZEC +1.89 %, t 2.28) and in 7 of 8 years (2020 +2.04 %, t 2.17; 2024 +1.61 %, t 2.40; only 2019 −0.08 %). All cases together swing from −1.12 % in 2018 (t −2.83) and −0.81 % in 2022 (t −2.85) to +1.06 % in 2020 (t 3.18).
- **F6:** The plan's horizon is not where the full set shows best, but no horizon rescues it. All cases give t 1.39 at 12 hours, 0.76 at 3 days and 0.13 at 6 days. Measured from the streak's end instead of while it runs, the 3-day move is −0.07 % (t −0.60).

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound.b1_deep-down-run-rebound-wider` (from F1, F5): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days. The larger the streak's loss in typical four-hour moves, the larger the rise.
- `024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound.b2_capitulation-volume-deep-fall-rebound` (from F2, F3, F4, F5): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days. The rise is larger the deeper the streak's loss in typical four-hour moves, and the more the volume traded during the streak exceeds the coin's volume over the five days before it began.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
