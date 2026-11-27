---
line: 7.b inconclusive
backtest: 061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade_1d
idea tested: 061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3972 USD
---
## Findings
- **F1:** The fall is real and on the idea's side, so the result is unclear only because of the grading check. In folds B and C, the 53 cases have a mean short-side unusual 10-day move of +8.34 % (t 3.85, 48 days), against +0.61 % (t 0.15, 40 grid cases) on in-profile bars outside the situation; step 5's full-data measure is +3.00 % with t 3.16 over 225 cases.
- **F2:** The raw close location grades the fall cleanly, but the plan's forecast does not. The forecast is that location standardised over its last 60 values. Its correlation with the 10-day unusual move is only 0.068, against 0.165 for the raw location, and the two share only 0.78 of their variation. On all folds the forecast split came out at −0.00004, which is why the check failed.
- **F3:** Graded by the raw close location, the 10-day short-side unusual move rises step by step. It is +4.5 % (t 1.17, 18 cases) for a location of 0.75 to 0.85, +9.6 % (t 3.16, 28 cases) for 0.85 to 0.95, and +13.3 % (t 3.52, 7 cases) above 0.95. Split at the median location, the closer half beats the other by +3.7 % over 10 days and by +2.0 % over 5 days.
- **F4:** The day's gain grades the fall the other way, and holds back the location grading. The gain's correlation with the 10-day unusual move is −0.168, and the larger-gain half trails the smaller-gain half by −2.9 % (22 cases each). Below a location of 0.95, the cases with a gain under half a usual swing fall more: +5.3 % against −0.8 % for locations 0.75 to 0.85, and +12.6 % against +5.5 % for 0.85 to 0.95.
- **F5:** Ten days is the plan's horizon and the right one. The unusual move's t is 2.00 over 2 days, 3.48 over 5 days, 3.85 over 10 days and 1.73 over 20 days. The effect is not concentrated in one period: it is positive in every year from 2018 to 2021 and in 10 of the 12 windows.

## Ideas
- `061-01.b1.b1.b1.d2.d1.b1_raw-range-location-ten-day-fade` (from F1, F2, F3, F5): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range on a day whose gain is small against its usual daily swing, its price falls over the next ten days, and the larger the share of that day's own range the close sits above the low, the larger the fall, whatever the coin's closes did on the days before.
- `061-01.b1.b1.b1.d2.d1.b2_smallest-gain-high-close-fade` (from F1, F4, F5): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range on an up day, its price falls over the next ten days, and the smaller the day's gain against its usual daily swing, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
