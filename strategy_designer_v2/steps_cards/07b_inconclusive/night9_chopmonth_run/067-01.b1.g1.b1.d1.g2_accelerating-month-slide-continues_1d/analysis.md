---
line: 7.b inconclusive
backtest: 067-01.b1.g1.b1.d1.g2_accelerating-month-slide-continues_1d
idea tested: 067-01.b1.g1.b1.d1.g2_accelerating-month-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4500 USD
---
## Findings
- **F1:** The test graded its shorts by the wrong move. Among the bars where the book was active (choppy market, 30-day fall), the 5-day fall does not grade the following move. By quintile of the 5-day return, the short unusual move over 10 days was 0.045, 0.008, 0.089, 0.032 and 0.037, from the steepest 5-day fall (-18.6 %) to a 5-day rise (+9.0 %). The correlation between the 5-day return and the short unusual move is 0.055. This matches step 5's failed supporting check (larger half minus smaller half -0.018) and its t of 1.18 over 705 cases.
- **F2:** On the same active bars, the depth of the 30-day fall grades the move strongly. By quintile of the 30-day return, the short unusual move over 10 days was +11.5 % (t 1.98, 8 days), +14.3 % (t 3.82, 14 days), +8.2 % (t 2.37, 12 days), +0.8 % (t 0.21) and -7.6 % (t -1.57), for mean 30-day returns of -29 %, -21 %, -15 %, -7 % and -2 %. The correlation between the 30-day return and the short unusual move is -0.51. The book's shallow slides, which went against it, diluted the deep ones that worked.
- **F3:** In every choppy fall (60-day return within ±10 %), the coin's 10-day unusual move by 30-day return bin was -18.6 % (t -2.01, 10 cases), -12.7 % (t -3.15, 14 cases), -1.2 % (t -0.20) and +5.0 % (t 1.04), for slides beyond -20 %, -20 to -12 %, -12 to -6 % and -6 to 0 %. The Spearman correlation between the 30-day return and the next 10 days' move is 0.63 among falls. The month's slide continues, and more so the larger it is.
- **F4:** The effect is larger over 20 days. In choppy falls deeper than -20 % and from -20 to -12 %, the 20-day unusual move was -26.0 % (t -4.03, 9 cases) and -14.3 % (t -2.24, 13 cases). Scaled by the coin's own 30-day swing, the grading holds: by quartile of the volatility-scaled slide, the short move was +14.5 %, +11.4 % (t 2.44), +1.3 % and -2.3 %, and the Spearman correlation is 0.56.
- **F5:** The deep-slide effect is on the short side in every year of these folds: 2019 +10.8 % (t 3.85), 2020 +16.9 % (t 0.91) and 2021 +16.0 % (t 1.58) short unusual move over 10 days. After choppy rises it is weak and does not last. The Spearman correlation is 0.22, the 10-day moves after rises have t below 1.1, and the 20-day moves are flat or negative. The effect lives on the falling side.

## Ideas
- `067-01.b1.g1.b1.d1.g2.b1_deep-month-slide-continues` (from F1, F2, F3, F5): In a choppy market, among coins that fell over the past 30 days, the larger the fall over the past 30 days, the more the coin keeps falling over the next 10 days.
- `067-01.b1.g1.b1.d1.g2.b2_deep-slide-three-weeks` (from F2, F4, F5): In a choppy market, among coins that fell over the past 30 days, the larger the fall over the past 30 days, the more the coin keeps falling over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
