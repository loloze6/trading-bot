---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4492 USD
---
## Findings
- **F1:** The main t is negative even though the pooled mean is positive, because coins fall and rebound together on the same Sundays: across 2,235 Sunday-fall cases the pooled excess 2-day return is +0.36 % (t 2.21), but the mean of per-Sunday cross-coin means is −0.33 % (t −0.87, 292 Sundays), and the case-level correlation between fall size and the 2-day excess return is only 0.018.
- **F2:** Over 2 days a Sunday fall is followed by nothing a weekday fall is not: the per-date mean 2-day excess return after a fall is −0.33 % (t −0.87) for Sunday, against a range of −0.20 % to +0.46 % (t −0.47 to 1.38, about 280–300 dates each) for the other six weekdays.
- **F3:** Over 3 days the rebound grows with the size of the weekend fall: the per-Sunday mean 3-day excess return by fall quintile is −0.11 %, +0.16 %, +0.75 %, +1.67 % (t 2.12, 146 Sundays) and +1.25 % (t 1.47, 122 Sundays). The same quintiles over 2 days follow no order (pooled −0.48 %, +0.37 %, −0.02 %, +1.66 %, +0.23 %).
- **F4:** The rebound arrives on the third day rather than on Monday: Wednesday's own excess return after a Sunday fall averages +0.53 % per Sunday (t 1.92, 288 Sundays), while Monday's averages −0.24 % (t −0.81, 294 Sundays) and the 2-day return −0.33 %.
- **F5:** The effect is not steady over time: the per-Sunday mean 3-day excess return after a Sunday fall is +1.70 % in 2020 and +1.91 % in 2021, but −0.38 %, −0.60 %, +0.59 % and −0.52 % in 2022–2025, with no year reaching |t| 1.4.
- **F6:** Volume runs against the brief: the per-Sunday mean 3-day excess return after a Sunday fall rises from the low to the high relative-volume tercile (−0.13 %, +0.22 %, +0.52 %). The brief predicts the most reversal on low weekend volume.
- **F7:** On the other side, weekend rises are followed by an underperformance over 2 days: per-Sunday mean −0.84 % (t −2.19, 297 Sundays, 2,147 cases), weaker at 1 day (−0.30 %, t −1.01) and at 3 days (−0.67 %, t −1.56).

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound` (from F1, F3, F4): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), and the larger the weekend fall, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
