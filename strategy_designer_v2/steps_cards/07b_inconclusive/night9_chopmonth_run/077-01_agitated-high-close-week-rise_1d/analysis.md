---
line: 7.b inconclusive
backtest: 077-01_agitated-high-close-week-rise_1d
idea tested: 077-01_agitated-high-close-week-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5467 USD
---
## Findings
- **F1:** The test's result is zero, not merely short of the bar. The forecast-weighted mean excess 7-day return is +0.28 % with t 0.30 over 1138 grid cases on 277 days. The idea's unusual move is -0.00 % (t -0.01, 824 days, strength 0.001), and the test already used every fold and every coin, so no more data is available.
- **F2:** The one positive 7-day reading depends on where the 7-day grid starts, so it is not a real effect. In folds B and C on agitated days, the rank correlation of close location with the excess 7-day return is +0.13 (p 0.0008, 648 cases) on the grid starting at offset 0. On the six other offsets it is -0.02, -0.06, +0.04, +0.03, -0.20 (p 1e-6) and -0.10 (p 0.01). The upper-minus-lower-half difference changes sign the same way (+3.0 % at offset 0, -3.1 % at offset 1, -3.0 % at offset 5).
- **F3:** The weekly gap does not repeat window by window either. On agitated days pooled over all offsets, the upper-half minus lower-half excess 7-day return is between -2.3 % and +1.2 % in each of the 12 windows w7 to w18, with 8 of them negative.
- **F4:** What the close location does predict in an agitated market is the next day, and in the opposite direction to the idea: lower closes are followed by higher next-day returns. The rank correlation of close location with the next-day excess return is -0.108 (p 4e-13, 4487 cases) on agitated days, against -0.071 on calm days. By quintile, the lowest-fifth closes earn +1.08 % next day (t 2.36) and the highest-fifth closes earn -0.54 % (t -1.65).
- **F5:** The next-day rebound after a lower-half close lives in the agitated profile. Agitated lower-half closes earn a next-day excess of +0.57 % (t 1.98, 2048 cases, 685 days), or +0.70 % weighted by distance below mid-range, against +0.16 % (t 0.88, 2441 cases) on calm days.
- **F6:** The next-day effect holds across the data, not in one corner of it, but it is only weakly graded. The rank correlation of close location with next-day excess return is negative in every year (2018 -0.13, 2019 -0.16, 2020 -0.16, 2021 -0.06). It is also negative on all 10 coins (-0.04 to -0.18), and the mean after a lower-half close is positive on 9 of 10 coins. Inside the lower half, the grading is weak (rank correlation of depth below mid-range with the next-day move +0.05).
- **F7:** The rebound's move is about three times the cost of a trade, but the day after gives part of it back. The raw next-day move after an agitated lower-half close is +0.78 %, against 0.22 % per trade, so it could cover costs. The following day's excess is -0.27 %, so the move does not extend.

## Ideas
- `077-01.b1_agitated-low-close-rebounds` (from F1, F2, F4, F5, F6, F7): In an agitated market, a daily close near the bottom of that day's high-to-low range is followed by a rise over the next 1 day, larger the nearer the close sits to the day's low.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
