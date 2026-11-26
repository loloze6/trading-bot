---
line: 7.b inconclusive
backtest: 032-03.b1_thin-volume-decline-more-coins_1d
idea tested: 032-03.b1_thin-volume-decline-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3938 USD
---
## Findings
- **F1:** The tested slope points the way the idea predicts but is too small to clear the bar. Step 5's slope t is 1.25 over 3307 in-regime cases on 498 days. The size is an unusual move of +0.42 % per case (t 1.09, 814 days), a strength of 0.024, about half the 0.05 seen in real ideas. In folds B and C the slope stays positive at 3, 5 and 10 days (t 0.40, 1.02, 0.76; about 1,100 cases) and fades at 20 days (t 0.18), so the plan's 5-day horizon is not where the problem lies.
- **F2:** The effect is mixed across periods and coins. By year the slope t is 2.10 in 2018 (312 cases), 0.99 in 2019, -0.42 in 2020 and -0.76 in 2021. By coin it is positive for BTC (t 1.24), LTC (1.57) and XMR (1.14) and negative for ADA (-0.84), LINK (-1.55) and UNI (-1.88).
- **F3:** The grading is not monotonic. The 5-day excess return is:
- **F4:** The volume effect is tied to how deep the fall is, but not clearly.
- **F5:** The move after any 28-day fall is larger than what the volume grading adds. In-regime cases average -0.93 % beyond drift over 5 days whatever their forecast, and the middle-depth tercile averages -3.0 %. This is why the idea's own total move (-0.37 %) is mostly the coin's drift (-0.79 %).
- **F6:** The clear effect in these declines is set by the daily range, not by volume. Among 28-day falls whose mean daily high-low range is above the median, a deeper fall is followed by a higher return:

## Ideas
- `032-03.b1.b1_thin-volume-decline-all-coins` (from F1, F2): Among coins that have fallen over the past 28 days, the lower the volume over that period compared with the coin's own usual volume, the larger the further fall over the next 5 days.
- `032-03.b1.b2_violent-decline-rebounds` (from F6, F5): Among coins that have fallen over the past 28 days with daily high-low ranges wider than the coin's own usual range over that period, the larger the 28-day fall, the larger the rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
