---
line: 7.b inconclusive
backtest: 058-02.g1.b1_choppy-agitated-fall-all-coins_1d
idea tested: 058-02.g1.b1_choppy-agitated-fall-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3538 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar: the |forecast|-weighted short-side 5-day excess return is +1.87 % with a day-pooled t of 1.55 (266 cases, 141 days). The test already used all 19 coins, all four folds and the daily bars, which run to the end of the data, so no more data could raise its case count.
- **F2:** The grading the idea claims is barely there. In folds B and C, the deepest, middle and shallowest thirds of the falls are followed by nearly the same short-side 5-day excess returns: +4.5 %, +4.0 % and +3.6 % (20, 20 and 21 cases, t 1.2 to 1.6). The correlation between |forecast| and the excess return is only 0.12 across the 61 cases.
- **F3:** The effect is mixed over time rather than steady. By year, the short-side excess return is +4.9 % in 2019 (t 4.1, 9 days) and +10.8 % in 2020 (t 1.5), but −1.1 % in 2021 (t −0.6, 29 cases, the largest year). Windows w11 and w12 are negative (−6.0 %, t −1.7, and −3.9 %, t −2.1), while w16 alone gives +31 % on 5 cases.
- **F4:** The plan's 5-day horizon is already where the effect peaks. The short-side excess return is +0.4 % at 1 day (t 0.8), +1.3 % at 3 days (t 1.3), +4.0 % at 5 days (t 2.4, 61 cases), +4.2 % at 10 days (t 1.3) and −6.2 % at 20 days (t −1.0), so no other horizon gives a clearer answer.
- **F5:** The volume split the brief names is too thin to locate the effect, and heavy volume does not remove it:
- **F6:** Falls outside the choppy agitated profile also continue a little, without a grading by depth. Their 5-day short-side excess return is +0.97 % (t 2.2, 616 cases), but the deepest third gives −0.7 % (t −0.8), the middle third +3.3 % and the shallowest third +0.3 %.

## Ideas
- No ideas: The result is on the predicted side, but no more data is available. The effect does not show clearly in one part of the data and not elsewhere: it is flat across fall depth (F2), changes sign between years and windows (F3), peaks at the tested horizon (F4), and splits by volume on too few cases (F5). No amended idea on the theme would give a clearer answer.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
