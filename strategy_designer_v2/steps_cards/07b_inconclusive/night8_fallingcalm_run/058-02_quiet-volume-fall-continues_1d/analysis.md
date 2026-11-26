---
line: 7.b inconclusive
backtest: 058-02_quiet-volume-fall-continues_1d
idea tested: 058-02_quiet-volume-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3739 USD
---
## Findings
- **F1:** The test's result points the idea's way but is too weak to show clearly. Over the 5 days after a signal, the coin fell 0.87 % more than its normal drift (strength 0.082, t 1.40 over 311 days, 443 cases). On folds B and C the same move is 1.08 % (t 1.11, 246 cases, 97 days), and the weighted main measure is -0.0154 (t -1.33).
- **F2:** The plan's main measure has the wrong sign. It multiplies the coin's drift-removed return by -forecast/10, which is positive on every short, so a continued fall gives a negative value, and the plan confirms only a positive one. Step 5's -0.0042 (t -0.55) is therefore on the idea's side, not against it.
- **F3:** The effect does not grow with the forecast. The supporting check gives +0.00024, above minus below the median |forecast|, so it fails. The correlation of the forecast with the drift-removed return is 0.037. The forecast quartiles' short gains are 0.82 %, 1.53 % and 0.98 % at 5 days, and 2.37 %, 2.13 % and 0.55 % at 10 days, with no order.
- **F4:** Neither element of the situation grades the move in folds B and C.
- **F5:** The continuation sits in one period. In 2018 and 2019 the weighted main measure is -0.0265 (t -2.20, 203 cases, 75 days), meaning a strong continuation. In 2020 and 2021 it is +0.037 (t 1.18, 43 cases, 22 days), meaning a rebound.
- **F6:** The calm side of the profile matters. Falling coins with a 30-day fall continue down by 1.71 % more than drift when calm (t -1.28, 142 cases). When agitated they do not continue (+0.31 %, t 0.14, 123 cases), as the brief claims.
- **F7:** The effect is on the idea's side on all six coins and at every horizon from 1 to 20 days, but no t reaches 2.

## Ideas
- `058-02.b1_quiet-calm-fall-more-coins` (from F1, F2, F6, F7): In a falling, calm market, the deeper a coin's 30-day fall and the lighter its volume over those 30 days compared with its own average volume over the past year, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
