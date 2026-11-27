---
line: 7.b inconclusive
backtest: 077-02_agitated-low-close-week-fall_1d
idea tested: 077-02_agitated-low-close-week-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3743 USD
---
## Findings
- **F1:** The tested idea points the predicted way but is far from the bar. Over 7 days the unusual move is +0.65 % in the short direction, with t 1.00 on 679 case days and 1738 cases. In the explored folds B and C the 498 cases give +1.26 % (t 0.90, 233 days), so the week's fall is too small for this data to show. The test already used every coin and fold, so no more daily data exists to add.
- **F2:** The first day after a low close goes against the idea. That day's unusual move in the short direction is −1.03 % (t −2.07, 233 days, 498 cases). Across all agitated bars, a close in the bottom quarter of the range is followed next day by +0.83 % (t 2.07, 340 days), and a top-quarter close by −0.67 % (t −2.16, 494 days). This is the next-day reversal the brief says the week must first pay back.
- **F3:** With that first day removed, the fall shows more clearly. From the next day's close, over the following 6 days the unusual fall is +2.13 % (t 1.69, 233 days). Over the 7 days that start one day later it is +2.52 % (t 1.94, 230 days), twice the plan's +1.26 % on the same cases.
- **F4:** The delayed fall is graded the way the idea says. On the 7 days that start one day later, the third of cases with the largest |forecast| (closes nearest the low) falls +4.49 % (t 1.83). The middle third falls +1.75 % (t 1.13) and the smallest third +1.31 % (t 0.94). On the plan's own horizon the order is the same: +2.65 %, +1.04 %, +0.08 %.
- **F5:** The delayed fall holds across periods and is not confined to one regime or coin group. It is positive in every year of the explored folds: 2018 +5.53 % (t 2.23), 2019 +1.87 %, 2020 +3.51 % (t 1.69), 2021 +1.01 %. It is similar for narrow, middle and wide days (+2.33 %, +2.03 %, +2.25 %). On the plan's horizon it is positive on 8 of 10 coins.
- **F6:** The same-day 7-day grid of all agitated bars is too thin to settle the matter. Bottom-quarter closes give −3.16 % in the long direction (t −1.02), but on only 49 days.

## Ideas
- `077-02.b1_agitated-low-close-delayed-fall` (from F1, F2, F3, F4, F5): In an agitated market, a daily close near the bottom of that day's high-to-low range is followed by a fall over the 7 days that start one day after it, larger the nearer the close sits to the day's low.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
