---
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4699 USD
---
## Findings
- **F1:** A day whose high-to-low range is wide against the coin's own last 20 days is followed by a larger 5-day rise. The widest quintile gives +1.56 % excess over the coin's normal 5-day drift, a strength of 0.111, over 1251 non-overlapping cases. That excess is positive in 19 of 19 coins and in 71 % of the windows, with a window-clustered t of 1.73. The relation is graded: the per-coin Spearman rho has a median of 0.083 and is positive in 17 of 19 coins, and the two narrowest quintiles give -0.79 % and -0.97 %.
- **F2:** The wide-range effect is strongest when the day closes up. Wide days that close up give +2.33 % 5-day excess (strength 0.142, 592 cases). Wide days that close down give +0.88 % (strength 0.083, 663 cases). All other days give -0.53 % to -0.57 % (about 5,000 cases). The +2.33 % is about 10 times the 0.22 % round-trip cost of this backtest.
- **F3:** The break moves of the tested idea outlast its 5-day horizon. From the bars where the forecast turns on (3171 onsets), the mean raw return is +1.06 % over 5 days against a grid mean of +0.76 %. Over 10 days it is +2.06 % against +1.55 %, and over 20 days +4.58 % against +3.38 % (2786 onsets, raw t 7.45). The excess roughly quadruples from 5 to 20 days, as the earlier finding F9 saw on other continuation books.
- **F4:** Inside those break onsets the 10-day run grades the 5-day move. The top tercile gives +1.36 % excess (t 2.01, 959 cases), the middle -0.02 % and the bottom -0.67 % (t -1.89).
- **F5:** Some patterns sort the coins but do not hold within windows, so they are not findings.
- **F6:** The book earns mostly in windows where the coins rise and loses little elsewhere. Its best windows (w11, w21, w6) match holding's best (+1.90 %, +0.70 %, +0.63 % mean daily). In falling windows its loss is a fraction of holding's (w7 -0.003 % vs -0.47 %, w14 -0.07 % vs -0.43 %). Its weakness is depth, not direction: Calmar 0.74.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins.g1_wide-up-day-continues-up` (from F1, F2): When a coin closes up on a day whose high-to-low range is wide compared with its ranges over the past 20 days, it tends to rise over the next 5 days, and the wider that day's range relative to its 20-day average, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins.g2_resistance-breakout-longer-hold` (from F3, F4): When a coin closes above a price where it turned down several times in the past 90 days, while its 60-day return is positive, it tends to keep rising over the next 20 days, and the larger its 10-day return before the break, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
