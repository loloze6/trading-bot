---
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
idea tested: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3863 USD
---
## Findings
- **F1:** The book cannot reach the gain asked of it at this frequency. It trades only on the Sunday close and holds for 48 hours, so it is exposed on 17 % of days (0.170), with 912 trades in all (0.050 a day). Each case earns a total move of only +0.49 % at a mean absolute allocation of about 0.45, against a cost of 0.19 % per trade. The mean daily return is 4.7e-05, against the 0.0005 required.
- **F2:** Inside the active Sunday cases, the move is graded by the weekend fall, inversely to what the forecast is built on. Cases are split into terciles by weekend return. The smallest falls are followed by a short-side 48-hour move of +1.45 % (t 2.80, 178 cases). The middle tercile gives +0.52 % (t 1.06). The largest falls give -0.48 % (t -0.73).
- **F3:** On all qualifying Sundays, the ratio of the weekend fall to the prior rise (in usual moves) grades the move in the same way. The lowest quartile, a small fall against a large rise, gives a short-side 48-hour move of +1.46 % (t 2.32, 134 cases). The second quartile gives +1.16 % (t 1.66). The two highest quartiles give -0.71 % and -0.17 %.
- **F4:** The forecast's own size, the prior five-day rise, barely grades the outcome, yet it drives the position. Across prior-rise terciles the short-side 48-hour moves are +0.49 %, +0.08 % and +0.92 % (t 1.02, 0.13, 1.56). Over the same terciles the mean absolute allocation rises from 0.17 to 0.53 to 0.66. The book is therefore largest on cases whose size is not where the move is.
- **F5:** The same situation on weekday closes does not continue but reverses. It gives a short-side 48-hour move of -0.06 % (t -0.54, 3538 cases), against +0.44 % (t 1.36, 533) on Sundays. On weekdays, the quartile with the largest prior rise gives -0.72 % (t -3.19, 885), and the quartile with the largest two-day fall gives -0.66 % (t -2.93, 885): the coin rebounds.
- **F6:** The loss is concentrated in one year and in three coins. In 2020 the active cases moved -1.81 % on the short side (t -2.43, 83 cases), and the trades lost -2.61 % net each. BTC, ETH and LTC trades lost -0.62 %, -1.29 % and -1.00 % net. XMR, XRP and ZEC gained +0.32 %, +0.41 % and +0.01 %.
- **F7:** A quarter of the trades last one hour (25th percentile duration 1 h, median 48 h). These are churned re-entries that each pay the 0.19 % cost on top of the weekly bet.

## Ideas
- `026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week.d1_shallow-weekend-dip-continues` (from F2, F3, F4, F1): When a coin falls over the weekend after rising over the previous five days, it keeps falling over Monday and Tuesday. The fall is larger the smaller the weekend's fall is next to the preceding five-day rise, each measured in the coin's usual moves.
- `026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week.d2_midweek-dip-in-uptrend-rebounds` (from F5): When a coin falls over two days during the week after rising over the previous five days, it rises over the next two days. The rise is larger the larger the preceding five-day rise was, measured in the coin's usual moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
