---
line: 7.g patterns
backtest: 037-01_choppy-swing-scaled-fall-continues_1d
idea tested: 037-01_choppy-swing-scaled-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4158 USD
---
## Findings
- **F1:** In calm markets (the coin's 30-day swing at or below its own median), the next 5 days follow the 5-day move measured in 20-day swings, in steps across the quintiles: −3.71 % (t −2.77, 157 cases, 63 days) after the largest falls, −1.19 %, −0.08 %, +0.98 %, and +4.40 % (t 1.87, 207 cases, 69 days) after the largest rises. In agitated markets every quintile is flat (−0.94 % to +0.48 %, all |t| < 0.5).
- **F2:** The calm-market continuation points the same way in every year shown: the mean of z5 × unusual move is positive in 2018 (t 1.51), 2019 (t 0.36), 2020 (t 1.84) and 2021 (t 2.12). The same 20-day measure in calm markets also steps from −3.33 % (t −2.25) to +4.92 % (t 1.88).
- **F3:** In choppy markets, a coin's 20-day fall in its own swings continues, and the continuation grows with the fall. Over 5 days the bottom two quintiles return −7.58 % (t −2.22, 52 cases, 34 days) and −2.58 % (t −2.25). Over 10 days they return −10.20 % (t −2.37, 30 cases) and −6.87 % (t −2.77, 35 cases). Over 3 days the bottom quintile returns −3.44 % (t −2.26).
- **F4:** Inside the tested book's own short cases in choppy markets, folds B and C show the effect in steps. The most negative forecast tercile is followed by −7.77 % over 5 days (t −2.40, 30 days), the middle tercile by −3.22 % (t −1.45) and the mildest by −1.25 % (t −0.94). This is far more than the 0.22 % cost per trade, so the inconclusive verdict over all folds (t 0.94) comes from the folds hidden here.
- **F5:** The choppy 20-day continuation is not steady across years. Its slope term is near zero in 2018 (0.0028, t 0.14) and 2019 (0.0029, t 0.53) and carries the effect only in 2020 (−0.0287, t −0.98) and 2021 (−0.1321, t −1.91). The choppy evidence rests on few days and on part of the period.
- **F6:** Other angles showed nothing that clearly beats chance across this many looks:

## Ideas
- `037-01.g2_choppy-month-fall-continues-longer` (from F3, F4, F5): In a choppy market, the more of its own 20-day daily swings a coin's 20-day fall spans, the more the coin falls over the next 10 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `037-01.g1_calm-market-swing-scaled-momentum` (from F1, F2): In a calm market, the more of its own 20-day daily swings a coin's 5-day move spans, the further the coin keeps moving the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
