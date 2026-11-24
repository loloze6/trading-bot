---
line: 7.g patterns
backtest: 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d
idea tested: 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3812 USD
---
## Findings
- **F1:** Over all 2903 XMR days, where the close sits inside the day's high-low range predicts the next day's return: the lowest-close quintile is followed by an excess of +0.85 % (t 4.19, n 577) and the highest-close quintile by −0.60 % (t −3.31, n 581), with the middle quintiles graded in between (+0.11 %, −0.06 %, −0.30 %).
- **F2:** This close-location effect is not one period's: the top-minus-bottom quintile difference in next-day excess is negative in 7 of 8 years, from −0.45 % to −2.91 %, with t ≤ −2.4 in 2020, 2023 and 2024, and is only positive in 2025 (+0.23 %, t 0.47).
- **F3:** Close location accounts for the tested idea's own signal: in a regression of the next-day excess on the day's scaled return z, the close location and close location × range size, z's slope is −0.0007 (t −0.47), while close location × range carries −0.0056 (t −2.96). Among the down-day tercile, low-close days give +0.61 % (t 3.29, n 586), and middle-close days give only +0.22 % (t 0.74).
- **F4:** The fade after up days that close high happens on days the long-only book is flat: up days in the highest close tercile give a next-day excess of −0.62 % (t −3.20, n 509). Among the top z tercile, high-close days give −0.42 % (t −2.45, n 588), and on the book's flat bars the fourth close quintile gives −0.85 % (t −3.26).
- **F5:** The fade lasts two days: on a 2-day grid, the highest-close quintile is followed by a 2-day excess of −0.72 % (t −2.24, n 290), and the lowest two quintiles by +0.43 % and +0.58 % (t 1.03 and 1.62).
- **F6:** Two patterns that are weaker given how many angles were looked at:

## Ideas
- `031-03.g1.b1.d2.e2.g1.g1.d1.g1_low-close-next-day-rebound` (from F1, F2, F3, F5): The lower XMR closes within its day's high-low range, the more it rises over the next day, and the wider that day's range against its 30-day daily volatility, the stronger this rebound.
- `031-03.g1.b1.d2.e2.g1.g1.d1.g2_high-close-up-day-fade` (from F1, F3, F4, F5): The nearer an XMR up day closes to its high, the more its price falls back over the next one to two days, and more so the wider that day's range against its 30-day daily volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
