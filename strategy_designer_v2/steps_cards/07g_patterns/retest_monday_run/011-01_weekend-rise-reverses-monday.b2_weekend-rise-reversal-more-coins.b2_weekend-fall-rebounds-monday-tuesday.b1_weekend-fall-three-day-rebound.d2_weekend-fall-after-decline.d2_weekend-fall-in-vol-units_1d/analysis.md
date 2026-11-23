---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4295 USD
---
## Findings
- **F1:** The Sunday-fall rebound depends on the coin's 20-day trend. Sunday falls (more than 0.3 usual daily moves) whose 20-day return, in usual-move units, sits in the lowest fifth gain +3.05 % over the next 3 days beyond drift (t 5.85, 316 cases). The next two fifths gain +2.25 % (t 3.35) and +1.19 % (t 2.47). The top two fifths gain −0.02 % (t −0.04) and +0.60 % (t 1.00). Across all 4,264 Sundays, the Sunday return × 20-day return interaction has t 4.53.
- **F2:** The Sunday falls that came during a 20-day decline rebounded in all 19 coins (means +0.68 % to +8.43 %) and in every year from 2019 to 2025 (+0.20 % to +14.8 %). 2018 alone was negative (−1.31 %, t −1.04, 44 cases).
- **F3:** Sunday rises reverse too, which the tested idea leaves out. After a Sunday rise of more than 1 usual move, the next 3 days run −1.10 % beyond drift (t −3.10, 699 cases). Only Sunday shows a strongly negative slope of the 3-day return on the day's scaled move (−0.0070, t −6.13); the other weekdays run from −0.0020 to +0.0034.
- **F4:** The Sunday-rise reversal is strongest in a 20-day decline. Rises in the lowest third of the 20-day return run −1.60 % (t −5.01, 537 cases), the middle third −0.88 % (t −2.69) and the top third −0.19 % (t −0.40).
- **F5:** The coin's 20-day return in usual-move units predicts the next 3 days in its own direction from midweek closes, not from Sunday. Its coefficient is +0.0087 per unit from Thursday (t 10.3, 4,259 bars) and +0.0061 from Wednesday (t 6.0). From Sunday it is −0.0006 (t −0.70). These t's are inflated because the coins share the same days.
- **F6:** The brief's volume grading is absent. Sunday falls on the lowest third of volume (relative to the 60-day mean) gain +1.22 % (t 3.66), against +1.58 % (t 3.08) on the highest third.
- **F7:** The book's gain sits on a few days. All of the book's top 2 % and bottom 2 % days fall Monday to Wednesday (58 each, mean +3.79 % and −3.20 %). The top 2 % days sum to 227 % of the book's total gain, which explains a Calmar of 0.30 despite a Sharpe of 0.71.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units.g1_sunday-fall-in-decline-rebounds` (from F1, F2, F7): A coin that fell on Sunday rises over the next 3 days. The rise is larger the more the coin had already fallen over its past 20 days, with that 20-day return measured in units of its usual daily move over the past 60 days.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units.g2_sunday-rise-reverses-by-wednesday` (from F3, F4): A coin that rose on Sunday falls over the next 3 days. The fall is larger the larger that Sunday rise is in units of the coin's usual daily move over its past 60 days, and larger still when its 20-day return is negative.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units.g3_trend-carries-into-weekend` (from F5): A coin's 20-day return, measured in units of its usual daily move over the past 60 days, continues in the same direction over the next 3 days from Thursday's close, and the continuation is larger the larger that 20-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
