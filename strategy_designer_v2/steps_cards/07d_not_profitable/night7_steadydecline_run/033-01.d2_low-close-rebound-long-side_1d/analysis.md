---
line: 7.d confirmed, not profitable
backtest: 033-01.d2_low-close-rebound-long-side_1d
idea tested: 033-01.d2_low-close-rebound-long-side
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4429 USD
---
## Findings
- **F1:** The tested effect lives on wide-range days. On low-half closes, the next-day unusual move by quartile of the day's range against its prior 20-day mean range is −0.10 % (r1, t −0.23, 306 cases), −0.28 % (r2, t −0.71, 364), +0.56 % (r3, t 1.34, 433) and +1.43 % (r4, t 3.45 with one day's cases taken together, 553). On the non-overlapping grid, the wide-range low closes give +1.13 % (t 3.14, 384 days) against +0.35 % (t 1.98, 1025 days) for all low-half closes, so they are 5.9 times the 0.19 % cost of a trade instead of 1.3 times.
- **F2:** The wide range is not an effect of its own; it is the size of the forced flow the idea's theory names. On wide-range days that close in the upper part of the range, the next day's unusual move is −0.47 % (t −1.61, 1057 cases); at mid-range it is +0.81 % (t 1.69, 532). Only together with a low close does the wide range give +1.43 %.
- **F3:** The book spends much of its time in positions that earn nothing. Of its 3137 bars in a position after a low-half close, 1395 follow narrow-range days (r1, r2), and those bars carry only 0.34 of the summed 2.37 position gain, while the r4 bars carry 1.43. This dilutes the mean daily return on days in a position to 0.0225 % (rule: at least 0.05 %).
- **F4:** The book's falls are not tied to one kind of case. Positions held into the 40 worst book days come from every range quartile (r1 38, r2 42, r3 69, r4 65 positions; losses −0.43, −0.61, −0.98, −1.03). The deepest fall, −8.6 % in w14, is the one that fails Calmar (0.59, rule above 0.75). Cutting the r1 and r2 bars removes those falls without removing gain.
- **F5:** The wide-range low-close case holds across time; the plain low-half case does not. Its unusual move is positive in every year (2018 +0.85 %, 2019 +0.36 %, 2020 +1.01 %, 2021 +2.31 %) and in all 12 windows (lowest w9 +0.05 %). All low-half closes lose −0.26 % in 2018 (t −1.39, 1103 cases).
- **F6:** Within low-half closes the effect is graded by the close's position. The next-day unusual move is +0.68 % for closes in the bottom tenth of the range (t 2.82, 526 cases), +0.51 % for 0.1–0.2 (t 2.38, 740) and +0.12 % for 0.4–0.5 (t 0.58, 896). Yet the book's mean position is only 0.17 even in the bottom tenth.
- **F7:** The move lasts into a second day. On the 2-day grid, wide-range low closes give +1.38 % (t 2.20, 207 days); at 3 days the move fades to +0.70 % (t 0.77, 137 days). A 2-day holding keeps the same total move with half the trades.
- **F8:** By market profile, low-half closes rebound most in a falling, agitated market: +1.02 % (t 4.48, 682 cases). They give +0.12 % in falling calm (t 0.78, 830), +0.02 % in choppy calm (t 0.07, 331), and +0.47 % to +0.49 % in rising agitated and rising calm (t 1.95 and 2.57). The agitated profiles are stronger than the calm ones in falling and choppy markets.

## Ideas
- `033-01.d2.d1_wide-range-low-close-rebound` (from F1, F2, F3, F4, F5, F6): Among days that close in the lower part of their own high-low range, the nearer the close sits to the day's low and the wider that day's range against the coin's ranges of the previous 20 days, the larger the rise in the coin's price over the next day.
- `033-01.d2.d2_wide-range-low-close-two-day-rebound` (from F1, F2, F7): Among days that close in the lower part of their own high-low range, the nearer the close sits to the day's low and the wider that day's range against the coin's ranges of the previous 20 days, the larger the rise in the coin's price over the next two days.
- `033-01.d2.d3_agitated-decline-low-close-rebound` (from F8, F6): In a falling, agitated market, among days that close in the lower part of their own high-low range, the nearer the close sits to the day's low, the larger the rise in the coin's price over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
