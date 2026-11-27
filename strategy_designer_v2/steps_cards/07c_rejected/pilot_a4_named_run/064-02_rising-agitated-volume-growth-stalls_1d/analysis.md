---
line: 7.c no effect
backtest: 064-02_rising-agitated-volume-growth-stalls_1d
idea tested: 064-02_rising-agitated-volume-growth-stalls
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3558 USD
---
## Findings
- **F1:** Inside the rising agitated profile, the tested slope of the 5-day excess return on the 30-day log volume change is near zero at every horizon on the non-overlapping grid: -0.016 (t -0.36, 44 cases) at 5 days, +0.001 (t 0.17, 223 cases) at 1 day, -0.044 (t -0.81, 23 cases) at 10 days. Across the five grid offsets at 5 days the slope ranges from -0.016 to +0.024, with every t between -0.37 and +0.55. Shrinking volume does not lead to a larger rise, so the brief's long-side claim is absent.
- **F2:** The relation is not straight. The strongest volume growth (top fifth, log change about +1.10) is followed by a 5-day excess return of -8.9 %, with only 11 % of cases up (9 grid cases). The middle fifths show -1.9 % to +3.5 %. The top-fifth growth cases are negative on all five grid offsets (-8.9 %, -2.9 %, -4.7 %, -8.1 %, -0.2 %), while the other cases sit at +0.7 % to -3.7 %. Over all bars, the top fifth falls 7.2 % in excess over 5 days and 12.7 % over 10 days, and 78 % of those cases fall over 5 days.
- **F3:** The fall after growing volume depends on how far the coin has already risen. When both the 30-day return and the volume growth are above their medians, the excess return is -6.7 % over 5 days and -13.2 % over 10 days (55 bars). When the 30-day return is high but volume growth is low, it is +3.7 % and +6.4 % (46 bars). On the grid, the product of positive growth and positive 30-day return has a slope of -0.26 (t -1.57, 44 cases), against -0.04 (t -0.61) for growth alone.
- **F4:** The 30-day rise alone points the same way at its top. The top fifth of 30-day returns (+63 %) is followed by a 5-day excess return of -6.3 %, while the middle fifths show +2.3 % to +5.4 %. This places the reversal in the most stretched, crowded rises.
- **F5:** The evidence is thin and uneven. The profile covers only BCH (19 grid cases) and ZEC (25 cases) in the explore half, and only 2020 and 2021. The tested slope's sign flips by coin (BCH -0.09, t -1.12; ZEC +0.02, t 0.43) and by year (2020 +0.055, t 1.21; 2021 -0.088, t -1.14). Any follow-up rests mainly on the check half.

## Ideas
- `064-02.c1_crowded-rise-volume-reversal` (from F2, F3, F4): In a rising, agitated market, the more a coin's total volume over the last 30 days has grown against the 30 days before, and the larger its 30-day rise, the more it falls over the next 10 days.
- `064-02.c2_volume-surge-precedes-fall` (from F2, F3): In a rising, agitated market, the more a coin's total volume over the last 30 days has grown against the 30 days before, the more it falls over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
