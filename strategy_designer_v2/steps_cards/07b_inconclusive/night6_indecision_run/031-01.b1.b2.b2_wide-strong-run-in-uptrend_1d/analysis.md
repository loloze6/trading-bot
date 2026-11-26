---
line: 7.b inconclusive
backtest: 031-01.b1.b2.b2_wide-strong-run-in-uptrend_1d
idea tested: 031-01.b1.b2.b2_wide-strong-run-in-uptrend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3669 USD
---
## Findings
- **F1:** The tested result is on the side the idea predicts but far short of the bar: the mean unusual 3-day move is +0.20 % (t 0.68, 1,484 cases on 825 days), a strength of 0.020 of a usual 7.96 % move, which is 1.1 times the 0.19 % cost of a trade.
- **F2:** The grading the idea claims is present, mostly in the strongest cases.
- **F3:** The test measured the idea at a shorter horizon than where it shows. Over all cases the mean unusual move grows with the horizon:
- **F4:** The effect is mixed across years, and the market's own moves drown it.
- **F5:** Among the six coins, ZEC carries most of the 3-day effect.
- **F6:** Most of the grading comes from the size of the 5-day rise.

## Ideas
- `031-01.b1.b2.b2.b1_wide-run-more-coins` (from F1, F2, F5): After a coin has risen over the past 5 days, only while its 60-day return is positive, the larger that 5-day rise and the wider that day's high-low range compared with its average daily range over the past 20 days, the more the coin rises over the next 3 days.
- `031-01.b1.b2.b2.b2_wide-run-ten-day-follow-through` (from F2, F3, F6): After a coin has risen over the past 5 days, only while its 60-day return is positive, the larger that 5-day rise and the wider that day's high-low range compared with its average daily range over the past 20 days, the more the coin rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
