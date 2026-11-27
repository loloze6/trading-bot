---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d2.d1.d2_upper-close-fade-while-choppy_1d
idea tested: 061-01.b1.b1.b1.d1.d2.d1.d2_upper-close-fade-while-choppy
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4858 USD
---
## Findings
- **F1:** The book's profit comes almost entirely from one window. On days in a position, w16 sums +1.649 of daily book returns, against a total of about +1.585 over all twelve windows. Five other windows are negative, w11 the worst at −0.138. The best 5 % of days carry 175 % of the summed gain, and the book's daily return correlates −0.80 with the coin's, so what the book earns is a few large coin falls.
- **F2:** The situation does not need the choppy agitated profile. A close in the upper half of the day's range after a negative 5-day return falls over the next 2 days in every profile. Outside the profile the unusual 2-day move is −0.94 % (t −2.01, day-clustered, 915 cases on 325 days). Inside it the move is −2.61 % (t −1.25, 66 cases on 48 days).
- **F3:** The 2-day fall is graded by the depth of the 5-day fall, using all bars in the situation:
- **F4:** Both conditions are needed. Removing either one leaves nothing:
- **F5:** The bounce close is not graded by its height. Closes at 0.75–0.9 of the range fall −1.99 % over 2 days (t −2.97, 288 cases, 149 days), closes at 0.5–0.75 fall −0.63 % (t −1.03), and closes above 0.9 fall −0.82 % (t −1.06).
- **F6:** The fade belongs to the 2-day horizon. At 5 days, outside the profile, the same situation moves +0.26 % (t 0.21, 317 cases). In falling agitated markets it reverses: −2.42 % over 2 days (t −2.40, 128 cases, 62 days), then +7.09 % over 5 days (t 2.11, 46 cases, 22 days).
- **F7:** The tested 5-day short rests on very few cases in these folds. In the profile, its situation gives −12.1 % over 5 days, but on only 22 grid cases over 13 days (t −1.83). In choppy agitated bars, the 2-day move is −3.56 % (t −1.59, 34 cases, 23 days): the same sign as everywhere else, but not separable from chance alone.
- **F8:** No weekday pattern survives clustering by day. Sunday's 2-day move is −1.15 % (t −1.42, 111 days); every other weekday has |t| < 1.2.

## Ideas
- `061-01.b1.b1.b1.d1.d2.d1.d2.g2_choppy-agitated-bounce-two-day-fade` (from F2, F3, F6, F7): In a choppy, agitated market, when a coin closes in the upper half of its daily range after its 5-day return has been negative, its price falls over the next two days, the fall growing with the depth of that 5-day fall.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d1.d2.d1.d2.g1_dead-cat-bounce-two-day-fade` (from F2, F3, F4, F6): When a coin closes in the upper half of its daily range after its 5-day return has been negative, its price falls over the next two days, the fall growing with the depth of that 5-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
