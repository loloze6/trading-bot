---
line: 7.b inconclusive
backtest: 060-01.g1.d2.d2_wider-squeeze-day-fades-harder_1d
idea tested: 060-01.g1.d2.d2_wider-squeeze-day-fades-harder
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2141 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but short of the bar. It is a mean short-signed unusual move of +0.41 % with t 1.83 on 1,380 cases over 669 days. On folds B and C alone it is +0.68 % with t 1.73 on 625 cases over 271 days. The size is +0.55 % with t 2.13 over 501 days, which is 0.113 of a usual move, more than twice the 0.19 % cost of a trade.
- **F2:** The grading the idea claims shows clearly and in order. By quartile of |forecast| the next-day unusual move is −0.03 %, +0.37 %, +0.89 % and +1.49 % (t −0.04, 0.68, 1.28, 2.35). By quartile of the raw range ratio it is −0.13 %, +0.47 %, +0.97 % and +1.53 % (top quartile t 2.14). The supporting check passed with an upper-minus-lower difference of +0.62 %.
- **F3:** The effect points the same way on every coin and every year, but each part is too small to show alone. By coin the means run from +0.12 % to +1.09 % (t 0.18 to 2.16). By year they are +1.23 % in 2018, +0.81 % in 2019, +0.28 % in 2020 and +0.40 % in 2021 (t 0.38 to 1.88). By window, the large windows w14, w16 and w18 give +1.75 %, +0.21 % and +0.35 %, with only w13 slightly negative (−0.25 %).
- **F4:** The effect lives at the planned one-day horizon and is gone by two or three days. The two-day move is −0.02 % (t −0.04) and the three-day move −0.18 % (t −0.29), so the test measured it in the right place.
- **F5:** Within the falling agitated profile, next-day moves order with close location. They are −1.51 % for closes in the bottom quarter of the range (t −2.40), −0.62 % for the second quarter, +0.74 % for 0.5–0.75, +0.82 % for 0.75–0.9 and +0.22 % above 0.9. This matches the brief's close-location reversal, although the very highest closes are weak.
- **F6:** Among the cases, high-close up days carry the fade at +1.01 % (t 2.55, 505 cases, 225 days), while high-close down days show −0.70 % (t −0.86, 120 cases). Part of the dilution comes from down days that still close above mid-range.
- **F7:** Each coin enters the falling agitated profile on only 80 to 125 of its days in folds B and C, and there are 625 cases over 271 days. The effect is limited by how few cases the six coins provide. Data on 13 more coins exists in folds A and D and partly in B and C.

## Ideas
- `060-01.g1.d2.d2.b1_wider-squeeze-fade-more-coins` (from F1, F2, F3, F4, F7): In a falling, agitated market, a coin that closes above the middle of its day's high-low range falls over the next day, and the wider that day's range against its average range of the last 20 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
