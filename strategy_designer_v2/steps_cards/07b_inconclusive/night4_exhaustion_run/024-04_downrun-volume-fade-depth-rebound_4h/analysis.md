---
line: 7.b inconclusive
backtest: 024-04_downrun-volume-fade-depth-rebound_4h
idea tested: 024-04_downrun-volume-fade-depth-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3481 USD
---
## Findings
- **F1:** The tested effect is close to zero rather than small but real: step 5's mean excess return is +0.06 % over 18 bars (t 0.54, 5713 cases, strength 0.008). My recount gives −0.06 % (t −0.52, n 5017), and at the other horizons it stays at zero or below: 6 bars −0.04 % (t −0.70), 12 bars −0.07 % (t −0.75), 36 bars −0.32 % (t −1.88).
- **F2:** The volume fade works against the idea instead of for it. The highest fifth of raw volume_fade has a mean excess return of −0.38 % (t −1.57, n 996) against +0.01 % for the lowest fifth. The Spearman correlation of fade with the 18-bar excess return is −0.037, and step 5's above-minus-below-median check is −0.58 %.
- **F3:** The rebound exists only in the deepest streaks. By fifth of streak loss in usual moves, the first four fifths are −0.08 % to −0.26 % (|t| ≤ 1.0) and the top fifth is +0.52 % (t 1.89, n 1000). Inside that fifth, the 9th decile is −0.40 % (t −1.10, n 497) and the 10th decile +1.43 % (t 3.46, n 503), still +1.42 % at 36 bars (t 2.79).
- **F4:** The rebound appears when the coin is in a 30-day rise and reverses in a 30-day fall. Cases with a positive 30-day return average +0.42 % (t 2.36, n 1873); cases with a negative one average −0.35 % (t −1.92, n 1881). The same split on 7-day returns gives +0.28 % (t 1.68) against −0.44 % (t −2.71).
- **F5:** Inside a 30-day rise the effect is graded by streak loss: +0.05 %, +0.31 %, +0.17 %, +0.76 % (t 1.80), +1.10 % (t 2.29, n 323) from the lowest to the highest fifth. Inside a 30-day fall there is no such order, and the middle fifth is −1.07 % (t −2.38).
- **F6:** The effect also rises with the strength of the 30-day trend itself. By fifth of 30-day return, the strongest-rise fifth (median +35.6 %) averages +0.82 % (t 2.51, n 759); the second-weakest fifth (median −11.3 %) averages −0.63 % (t −2.33).
- **F7:** The market regime shows in the years. The rising years 2020 and 2021 are +0.83 % (t 2.59) and +1.11 % (t 2.69); the falling years 2018 and 2022 are −1.84 % (t −4.44) and −0.92 % (t −3.01). These opposite years cancel in the pooled mean.
- **F8:** The forecast fires early in short streaks, so the test barely measured "long runs". Almost every case sits on a 2-bar streak (4650 of 5017; mean length about 2.06 to 2.09 in every loss fifth). The forecast is capped at 20 from its second fifth onward, so "the largest forecasts" cannot be told apart, and its lowest fifth is −0.61 % (t −2.54).

## Ideas
- `024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound` (from F3, F4, F5, F6, F7): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days, only while the coin's 30-day return is positive. The larger the streak's loss in typical moves, and the stronger the coin's 30-day rise, the larger the rebound.
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling` (from F4, F6, F7): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin keeps falling over the next three days, only while the coin's 30-day return is negative. The more negative the 30-day return, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
