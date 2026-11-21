---
line: 7.e profitable but not proven
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4106 USD
---
## Findings
- **F1:** The book earns 0.0695 % per coin-day. Of that, 0.0280 % (40 %) is the market's own rise (position held times the coin's mean daily return), leaving 0.0415 % from timing. It earns on all six coins (0.018 % to 0.121 % per day), and its loss years are 2018 (-0.045 %/day) and 2022 (-0.063 %/day), the two years the coins fell (-0.35 % and -0.18 %/day).
- **F2:** The move after the book's entries keeps growing well past the plan's 5 days. The unusual move per entry is +0.99 % at 5 days (t 2.73, 1219 entries), +1.99 % at 10 days (t 3.48, 1171), +3.83 % at 20 days (t 3.77, 1090) and +5.59 % at 30 days (t 4.01, 979). The trades already last 6.9 days on average, longer than the 5-day horizon the test judged.
- **F3:** The gain sits in a few large trades. The top 5 % of the 1684 trades (84 trades) carry 4361 of the 5142 summed net percent (85 %). Only 50.8 % of trades win, and the median trade earns 0.05 %, the profile of a book riding a few long continuations.
- **F4:** The gain depends on the period. Entries' 5-day unusual move is -9.3 % in 2018 (38 entries), -2.0 % in 2022 (92) and -0.3 % in 2023 (215), against +3.9 % in 2019, +2.8 % in 2020 and +2.4 % in 2024. Over 20 days, ZEC (+10.3 %) and XRP (+6.0 %) gain far more than LTC (+0.7 %).
- **F5:** The plan's grading by distance above the 50-day average is not monotone. On the book's entries, the 5-day unusual move rises from +0.49 % (distance 0 to 5 %) to +2.05 % (11 to 22 %), then falls to +0.12 % above 22 %. On the non-overlapping 10-day grid of all bars, the 7 to 17.5 % band gains +4.8 %, above 17.7 % gains +0.4 %, and the bands between -16 % and +7 % lose 1.6 to 2.1 %.
- **F6:** On the 10-day grid of all bars, closeness to the 90-day highest close is graded at its top. Closes within 4 % of that high (or above it) gain +3.2 % unusual over 10 days and +5.5 % over 20 days (138 and 66 cases). Closes 4 to 11.5 % below it gain +2.6 % over 10 days, and closes 11.5 to 45 % below it lose 1.5 to 3.3 % (Spearman 0.056, 827 cases).
- **F7:** The trend condition alone (close above its 50-day average and positive 60-day return) carries most of the edge at longer horizons. Over 10 days, trend grid cells gain +1.82 % (t 1.89, 338) against -1.24 % outside it. Inside the trend, 5-day cells where the book is long gain +2.73 % (t 2.96, 151) against +0.35 % where it is not. Over 10 days the two are equal (+1.86 % vs +1.80 %).

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average.e1_resistance-break-continues-for-weeks` (from F2, F3, F6, F7): When a coin closes above a price where it turned down several times in the past 90 days, it keeps rising over the next 20 days, and the closer that close stands to its highest close of the past 90 days, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average.e2_nearness-to-90-day-high` (from F6, F2, F1): The closer a coin's close stands to its highest close of the past 90 days, the more it rises over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
