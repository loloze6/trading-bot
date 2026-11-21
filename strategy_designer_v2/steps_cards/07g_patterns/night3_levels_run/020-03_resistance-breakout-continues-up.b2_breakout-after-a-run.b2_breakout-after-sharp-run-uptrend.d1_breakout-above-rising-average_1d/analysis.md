---
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.5827 USD
---
## Findings
- **F1:** The move after a break grows with the horizon and goes well past the plan's 5 days. From the first bar of each long bet (1240 starts), the unusual move is +0.95 % over 5 days (t 2.65, strength 0.083), +1.93 % over 10 days (t 3.41, 1192 starts, strength 0.114) and +3.62 % over 20 days (t 3.61, 1111 starts, strength 0.129). The total move over 20 days is +6.04 %, about 30 times the 0.19 % cost of a trade.
- **F2:** Most of the 20-day move comes after the plan's 5-day bet ends. From day 5 to day 20 after a break start, the unusual move is +1.98 % (t 2.41, 1111 starts). The book's longest-held trades (mean 15.3 days, 421 trades) earn +9.95 % net with 62 % winners, against −0.85 % for trades held about 4.7 days. Starts can overlap, though: kept at least 20 days apart, the same moves are +2.88 % over 20 days and +1.95 % from day 5 to 20, both with t 1.27 to 1.59 on 357 starts. So F1 and F2 are partly inflated by counting nearby starts more than once.
- **F3:** The idea's grading fails at its top: the largest distances above the 50-day average are followed by the smallest rises. Split into four groups by that distance:
- **F4:** The strongest breaks follow the same pattern as F3. The break's touch count times its margin, top group (mean 8.75), is followed by +0.48 % unusual over 20 days, against +3.1 % to +6.5 % for the lower three groups (about 275 starts each). Spearman is −0.065.
- **F5:** Bear years carry the breaks' losses. Starts kept 20 days apart lose −24.2 % unusual over 20 days in 2018 (t −5.18, 19 starts) and −6.2 % in 2022 (t −1.97, 28 starts). Every other year is positive: +0.7 % to +7.4 %.
- **F6:** Saturday stands out among the weekdays, but it is a fixed calendar condition and I could not grade it.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average.g1_breakout-continues-three-weeks` (from F1, F2, F5): When a coin closes above a price where it turned down several times in the past 90 days, while its 60-day return is positive, it keeps rising over the next 20 days, and the more times that level turned it down before, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average.g2_overextended-breakouts-fade` (from F3, F4): When a coin closes above a price where it turned down several times in the past 90 days, the further its close stands above its 50-day average, the smaller its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
