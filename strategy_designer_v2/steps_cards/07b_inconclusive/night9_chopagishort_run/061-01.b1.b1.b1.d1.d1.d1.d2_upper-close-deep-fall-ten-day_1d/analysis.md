---
line: 7.b inconclusive
backtest: 061-01.b1.b1.b1.d1.d1.d1.d2_upper-close-deep-fall-ten-day_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d1.d2_upper-close-deep-fall-ten-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3915 USD
---
## Findings
- **F1:** The 20-day-fall grading does not hold. Step 5's Spearman between forecast size and the short-direction move is -0.14 on 120 cases. On folds B and C, the Spearman of the 20-day fall's depth with the move is -0.03 / -0.04 / +0.09 / +0.03 at 2 / 3 / 5 / 10 days. The deepest third of 20-day falls is not the largest: at 10 days the mean is +4.2 % for the deepest, +13.5 % for the middle and -1.5 % for the shallowest.
- **F2:** The tested 10-day horizon misses where the move shows. On folds B and C the short-direction unusual move is +3.6 % per case at 2 days (t 1.69, 74 cases), +5.3 % at 3 days (t 1.79, 62), +8.0 % at 5 days (t 2.13, 58), then +3.6 % at 10 days (t 0.86, 51). By 10 days most of the gain has been given back.
- **F3:** The 10-day result is mixed by period and carried by a few cases. Window w16 gives +23.1 % (10 cases) and w15 gives +8.1 % (7), while w11 gives -47.5 % (3) and w12 gives -6.1 % (5). By year, 2020 gives +15.1 % and 2021 gives -5.0 %. Dropping the 5 best cases cuts the mean from +3.6 % to +0.9 %.
- **F4:** The depth of the 5-day fall grades the move at every horizon. Its Spearman with the move is +0.16 / +0.19 / +0.14 / +0.13 at 2 / 3 / 5 / 10 days. At 5 days the terciles from deepest to shallowest 5-day fall give +12.3 % (t 1.46), +10.1 % (t 2.25) and +3.7 % (t 1.66), with 18 cases each.
- **F5:** At 5 days the move is clearest when the close is nearest the high. The top band of close location (0.85 to 1) gives +10.4 % (t 3.19, 15 cases, 80 % positive) and the middle band (0.7 to 0.85) gives +6.3 % (t 2.58, 18). The lowest band (0.5 to 0.7) gives +7.7 % but only t 1.14 with 52 % positive. The Spearman with close location is +0.11.
- **F6:** The 5-day move is not confined to the small coins. The six core coins give +7.9 % (t 2.18, 50 cases) and the others +8.6 % (8 cases). The step 5 result already used every coin and fold the 1d data holds, so no more data is available for the tested idea unchanged.

## Ideas
- `061-01.b1.b1.b1.d1.d1.d1.d2.b1_upper-close-five-day-fade` (from F1, F2, F4, F6): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, while its 20-day return is a deep fall, its price falls over the next five days, and the deeper that 5-day fall, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d1.d2.b2_pinned-close-five-day-fade` (from F1, F2, F5, F6): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, while its 20-day return is a deep fall, its price falls over the next five days, and the nearer the close is to the day's high, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
