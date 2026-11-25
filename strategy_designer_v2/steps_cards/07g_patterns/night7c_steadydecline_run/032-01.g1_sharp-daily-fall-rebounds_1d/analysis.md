---
line: 7.g patterns
backtest: 032-01.g1_sharp-daily-fall-rebounds_1d
idea tested: 032-01.g1_sharp-daily-fall-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4191 USD
---
## Findings
- **F1:** Where a coin closed within its day's range predicts the next day's return, graded. The slope of the next-day excess return (in usual moves) on the close's location in the range (0 at the low, 1 at the high) is -0.20, with clustered t -2.88 over 8688 cases on 1448 days. The bottom fifth of closes was followed by +0.70 % the next day and the top fifth by -0.17 %. A spread of about 0.87 % in a day is 4.6 times the 0.19 % cost of a trade.
- **F2:** The close-location effect holds across the data:
- **F3:** The close-location effect overlaps the day's scaled return. Inside terciles of the day's return in 20-day usual moves, its slope falls to t -0.88 (falling days), -1.71 (middle) and +0.18 (rising days). The close near the low matters most on days that did not already fall hard.
- **F4:** The rebound after a day's fall is a one-day effect, graded over the whole range of daily returns, and it is gone by the tested 2-day horizon:
- **F5:** The brief's own momentum shows only at 5 days and is not stable:
- **F6:** Weekdays differ in next-day excess return: Thursday +0.086 usual moves (t 3.2), Friday +0.069 (t 2.9), Wednesday -0.090 (t -2.8). Weekday is not a graded situation, so this gives no idea.

## Ideas
- `032-01.g1.g1_close-near-low-rebounds` (from F1, F2, F3): When a coin closes near the low of its day's high-to-low range, it rises over the next day, and the closer the close sits to the day's low, the larger that rise.
- `032-01.g1.g2_one-day-fall-bounces-next-day` (from F4, F3): The larger a coin's one-day fall in units of its typical daily move over the past 20 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
