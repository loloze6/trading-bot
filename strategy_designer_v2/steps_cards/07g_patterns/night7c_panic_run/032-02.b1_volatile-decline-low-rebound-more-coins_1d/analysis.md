---
line: 7.g patterns
backtest: 032-02.b1_volatile-decline-low-rebound-more-coins_1d
idea tested: 032-02.b1_volatile-decline-low-rebound-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4199 USD
---
## Findings
- **F1:** On 5-day non-overlapping grids across all coins in windows w7–w18, closes in each coin's top quintile of distance from the prior 20-day high (at or above that high) were followed by a 5-day unusual move of +4.18 % (t 2.25, cases of one day together, 332 cases on 107 days); over 10 days it was +6.76 % (t 2.22, 166 cases on 53 days).
- **F2:** The pattern is not graded across the quintiles: the second-lowest quintile of distance from the 20-day high showed −3.43 % over 5 days (t −3.21, 326 cases on 128 days) and −4.82 % over 10 days (t −2.30), while the lowest quintile was near 0 (−0.19 %, t −0.13).
- **F3:** The 20-day return points the same way over 10 days: its two top quintiles were followed by +4.29 % (t 1.60) and +5.29 % (t 1.62), and its second-lowest quintile by −5.37 % (t −2.69, 160 cases on 63 days).
- **F4:** A day whose high-low range is wide compared with its prior 20-day mean range (top quintile) was followed by +2.81 % over 5 days (t 1.67, 114 days) and +5.92 % over 10 days (t 2.12, 166 cases on 61 days).
- **F5:** The tested situation itself, on the bars of these folds where the regime was active and the forecast was positive, was followed by +5.28 % unusual over 5 days (t 1.42, only 16 cases on 9 days), against −0.60 % across all folds in step 5. Its depth correlated −0.53 with the 5-day unusual move, which means deeper breaks rose more, but on only 16 cases.
- **F6:** The book's 50 trades show where holding length mattered: trades closed within 5.5 days averaged +11.9 % net (33 trades), those held 5.5–10.5 days −20.4 % (7 trades), and those held over 20 days +27.1 % (10 trades). Windows w16–w18 carried the gain (+2.9 %, +26.2 %, +13.8 % mean per trade).
- **F7:** These patterns come from about 15 features, 3 horizons, weekdays and windows. With that many angles, only F1 holds at |t| above 2.2 on two horizons. Each of F1–F4 is marginal on its own, and the weekday effects (Wednesday −2.27 %, Thursday −2.15 %) were not tested with cases of one day counted together, so they are not used.

## Ideas
- `032-02.b1.g1_twenty-day-high-breakout-continuation` (from F1, F3, F7): In a coin whose daily close sits at or above the highest high of its prior 20 days, the coin rises over the next 10 days, and the further the close sits above that prior 20-day high, the larger the rise.
- `032-02.b1.g2_wide-range-breakout-continuation` (from F1, F4, F7): In a coin that closes at or above the highest high of its prior 20 days, the wider that day's high-low range compared with its mean range over the prior 20 days, the larger the rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
