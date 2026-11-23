---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5178 USD
---
## Findings
- **F1:** On Sunday closes below the 50-day average, the next 3-day excess return falls as the Sunday move grows: the slope on the Sunday move in units of 20-day volatility is -0.0177 (t -7.48, 1526 cases), while above the average it is 0.0002 (t 0.05, 1507 cases). The reversal works in both directions only under the average.
- **F2:** Sunday rises below the 50-day average are followed by a 3-day excess return of -1.51 % (t -5.23, 692 cases, strength -0.169). The effect is graded: the smallest rise quartile gives -0.04 % (t -0.07) and the largest gives -3.12 % (t -5.11, strength -0.346). Seven of the eight years are negative, and 2022 is the exception (+0.84 %, t 1.28).
- **F3:** Below the 50-day average, the Saturday-plus-Sunday 2-day return also reverses over the next 3 days, step by step across sextiles. The weakest sextile (mean weekend -7.7 %) gives +1.78 % (t 3.14) and the strongest (mean weekend +6.2 %) gives -1.62 % (t -3.31), each from about 255 cases. The Sunday 1-day slope is negative in 6 of 8 years: 2025 t -6.18, 2019 t -4.70, 2024 t -2.72.
- **F4:** A Wednesday rise continues over the next 3 days. The largest Wednesday-move sextile (mean +1.84 volatilities) gives +2.38 % excess (t 5.11, 511 cases, strength 0.234). The slope on the Wednesday move is +0.0072 (t 5.22, 3063 cases) and is positive in 7 of 8 years, with 2024 t 3.24 and 2025 t 3.13. The largest falls do not continue: the bottom sextile gives +0.06 % (t 0.15).
- **F5:** The weekday pattern matches the brief. The slope of the 3-day excess return on the 1-day move is negative only after Sunday (t -4.99) and Monday (t -2.63), and positive after Wednesday (t 5.22) and Friday (t 2.90). Falls below the average rebound only from Sunday (+1.21 %, t 3.85). From Wednesday and Friday they continue down (-0.91 %, t -3.37; -0.88 %, t -3.67).
- **F6:** The tested book earns its gain on the rebound days and loses on the Sunday entry days. On days with a non-zero return, the mean is +0.11 %, +0.17 % and +0.19 % on Monday, Tuesday and Wednesday (about 1,700 to 1,750 days each), against -0.04 % on Sunday (1756 days). The idea uses only the long side. The short side, the Sunday rise under the average (F2), is untested and larger in size.
- **F7:** Many angles were read here, about 20 tables. Patterns with |t| below about 4 are not taken as findings on their own. These include the volume-ratio split of the Sunday cases (terciles +1.18 %, +0.61 %, +1.86 %, not graded), the falls by volatility tercile and the weekday rebound of falls above the average.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.g1_sunday-rise-below-average-fades` (from F1, F2, F5): A coin whose Sunday close is below its 50-day average and that rose on Sunday (its 1-day return) falls over the next 3 days, Monday to Wednesday. The larger the Sunday rise relative to the coin's recent daily volatility, the larger the fall.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.g2_weekend-move-below-average-reverses` (from F1, F3, F5): A coin whose Sunday close is below its 50-day average moves over the next 3 days against its 2-day weekend return (Friday close to Sunday close). The larger the weekend move, the larger the reversal.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.g3_wednesday-rise-continues` (from F4, F5): A coin that rose on Wednesday (its 1-day return relative to its recent daily volatility) keeps rising over the next 3 days, Thursday to Saturday. The larger the Wednesday rise, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
