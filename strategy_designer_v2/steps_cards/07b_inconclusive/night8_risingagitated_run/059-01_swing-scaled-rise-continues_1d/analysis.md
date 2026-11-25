---
line: 7.b inconclusive
backtest: 059-01_swing-scaled-rise-continues_1d
idea tested: 059-01_swing-scaled-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4751 USD
---
## Findings
- **F1:** The tested measure clears its bar on all folds (slope t 2.08 over 3419 grid cases) but points the other way on the check folds A and D (slope −0.000103), so it is mixed rather than weak. On the explored folds B and C the 5-day slope has t 3.05 over 1710 cases, yet it is negative in 2018 (t −0.33) and in 5 of the 12 windows (w9: t −2.11).
- **F2:** The effect lives in calm markets only. In a coarse calm/agitated split (30-day swing against each coin's median over the explored windows, not the profile's past-year median), the 5-day slope is +0.00209 with t 6.55 over 642 calm cases, against +0.00010 with t 0.22 over 636 agitated cases. The same split holds at 1 day: calm t 5.23, agitated t 0.96 (each about 3,265 cases).
- **F3:** The calm effect is not carried by one coin or one year. All six coins have a positive calm slope (t from 1.55 for XMR to 3.86 for ETH), and calm cases are positive in every year from 2018 to 2021 (t 1.46, 1.18, 3.13, 1.80). The agitated slopes are all within t ±0.7 in every year, and only 6 of 12 windows have a positive calm slope, so window-level evidence is thin (about 53 cases per window).
- **F4:** In calm markets the effect is graded and works on both sides. The signed unusual move grows across the tertiles of forecast size: +1.20 % (t 2.18), +2.78 % (t 4.03), +3.11 % (t 4.06). Calm rises go on to +2.32 % (t 4.16, 359 cases) and calm falls to −2.42 % (t −4.54, 283 cases).
- **F5:** In calm markets the move per case is large against the cost of a trade. The unusual move is +2.36 % per case over 5 days (t 4.03 with each day's cases taken together, 159 days, 642 cases), or about 0.33 of the coin's usual 5-day move. That is about 12 times the 0.19 % cost, against +0.48 % (t 1.66) for the idea as a whole.
- **F6:** The swing scaling carries the signal, as the brief claims. Over 1422 cases, the scaled forecast predicts the 5-day excess return with t 4.33 (r 0.114), against t 1.92 (r 0.051) for the raw 20-day return.
- **F7:** The plan's 5-day horizon is where the effect shows; longer horizons lose it. The pooled slope has t 3.04 at 1 day, 3.05 at 5 days, 1.63 at 10 days and −0.25 at 20 days. The first 30 bars of each window, where the 60-value standardisation is still short, are negative (t −1.15 over 432 cases).

## Ideas
- `059-01.b1_calm-swing-scaled-move-continues` (from F2, F3, F4, F5, F6): In a calm market, the larger a coin's 20-day rise measured in units of its own daily swing over those 20 days (the 20-day return divided by the standard deviation of its daily returns over the same days), the larger its rise over the next 5 days, and the larger such a fall, the larger its fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
