---
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d
idea tested: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4293 USD
---
## Findings
- **F1:** The book's failure comes from the ≥3-touch filter, not from the falling-month fade. Breaks of a 90-day turning high after a 30-day decline of 12 to 25 % fell 4.0 % more than the coin's drift over the next 10 days (t -4.3, 248 cases), but only 15 to 80 cases had 3 or more touches, and those show no fall (+1.4 % at exactly 3 touches, t 0.57, 53 cases).
- **F2:** The idea as tested is too small to pay and too rare to trade. Per case its unusual move is +0.30 % and its total move is -1.01 %, which is -4.5 times the 0.22 % cost of a trade. The book made 187 shorts at a mean net -3.86 %, won only 28 % of them, and traded 0.0045 times a day.
- **F3:** Among breaks after a deep fall, fewer touches gave the larger fall, the reverse of the brief's grading. A level touched twice was followed by a 5.6 % excess fall (t -4.6, 77 cases), a level touched once by 2.7 % (t -2.8, 288 cases), and 3 or more touches by 1.5 % (t -0.37, 15 cases).
- **F4:** The break adds to the falling month's own effect. On all grid bars with a 30-day return of -12 to -25 %, the excess 10-day move is -2.2 % (t -3.6, 471 cases), against -4.0 % on breaks in the same band.
- **F5:** The depth grading holds only in part. Breaks after a 30-day return of 0 to -12 % show no fall (+0.9 %, t 0.87, 201 cases; -0.05 %, t -0.04, 178 cases). Breaks after a fall deeper than 25 % fall less (-1.8 %, t -1.3, 132 cases). The correlation of the 30-day return with the excess move is only +0.05 (758 breaks).
- **F6:** The deep-decline break effect is broad across coins but leans on certain years. 17 of 19 coins show a fall on average. By year, 2025 gives -8.4 % (t -6.3, 91 cases) and 2021 gives -5.2 % (t -2.6), while 2018 gives +3.0 % (46 cases).
- **F7:** Breaks in a rising month continue up, more strongly the larger the 30-day rise. The excess 10-day move is +0.8 % (t 1.0, 387 cases) for a rise of 0 to 9 %, +2.1 % (t 2.2, 364 cases) for 9 to 25 %, and +3.6 % (t 2.6, 389 cases) above 25 %.
- **F8:** Most of that continuation is plain momentum. On all grid bars the same bands give -1.7 %, +1.5 % and +3.3 %, against a coin drift of +1.4 % per 10 days and a usual 10-day move of 18 %.

## Ideas
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls.d1_break-fade-in-falling-month` (from F1, F2, F3, F4, F5, F6): When a coin closes above a price where it turned down in the past 90 days while its 30-day return is clearly negative, it tends to fall back over the next 10 days, and the deeper its 30-day decline (up to about a quarter of its price), the larger the fall.
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls.d2_break-continuation-in-rising-month` (from F7, F8): When a coin closes above a price where it turned down in the past 90 days while its 30-day return is positive, it tends to keep rising over the next 10 days, and the larger its 30-day rise, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
