---
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4386 USD
---
## Findings
- **F1:** In bars outside the falling regime with a positive 30-day return, a one-day rise is followed by a further rise above the coin's drift over the next 5 days, and the larger the rise, the larger the follow-through. Rises of 1 to 2 usual daily moves gave +2.14 % (t 3.36, 401 non-overlapping cases), rises above 2 moves gave +7.05 % (t 2.23, 140 cases), and rises up to 1 move gave +0.08 % (t 0.20, 915 cases). 79 % of coins show a positive mean, and 6 of 8 years are positive (2024: +5.37 %, t 4.01), with 2025 negative (−2.45 %, t −1.75).
- **F2:** The same pattern shows over shorter horizons outside the falling regime. Rises of 2 to 3 usual moves were followed by +1.24 % over 2 days (t 2.67, 362 cases) and rises above 3 moves by +3.56 % (t 2.14, 96 cases). Over 5 days, rises of 2 to 3 moves gave +8.10 % (t 2.66, 142 cases). This is the opposite of the fade the brief expects, so its last test ("the same moves as sharp rises in rising markets") separates the two regimes clearly.
- **F3:** Inside the falling regime (90-day and 30-day returns both negative), the 5-day fall after a one-day rise grows steeply with the size of the rise, beyond where the tested forecast saturates (about 1.6 moves):
- **F4:** The fade in the falling regime is concentrated in two years:
- **F5:** The book was short on only 8,462 of 36,466 bar-rows and earned 0.0124 % per bar while short. Against a trade cost of 0.22 % and a total move of +0.22 % per case, a 2-day fade that covers its cost only once cannot pay.
- **F6:** The calendar patterns do not hold up across years:

## Ideas
- `025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins.g1_sharp-rises-extend-uptrends` (from F1, F2): In a coin whose 30-day return is positive, the larger its one-day rise measured in usual daily moves, the larger its further rise beyond its normal drift over the next 5 days.
- `025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins.g2_extreme-bounces-fade-longer` (from F3, F4, F5): In a coin whose 90-day and 30-day returns are both negative, the fall over the next 5 days grows steeply with the size of its one-day rise in usual daily moves, being several times larger after the rarest rises than after ordinary ones.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
