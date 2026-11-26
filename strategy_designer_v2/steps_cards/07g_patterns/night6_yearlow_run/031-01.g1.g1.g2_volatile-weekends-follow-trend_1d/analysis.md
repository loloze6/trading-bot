---
line: 7.g patterns
backtest: 031-01.g1.g1.g2_volatile-weekends-follow-trend_1d
idea tested: 031-01.g1.g1.g2_volatile-weekends-follow-trend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4855 USD
---
## Findings
- **F1:** The coin's 14-day return grades its next 2-day excess move most on Thursday closes and barely on other days. The day-clustered mean of capped z14 × 2-day excess is 0.073 (t 2.65, 140 days) on Thursdays and 0.057 (t 2.06, 140 days) on Wednesdays, against t of −0.10 to 0.35 on Monday, Tuesday, Saturday and Sunday. Friday, the tested day, gives t 1.91.
- **F2:** The Thursday grading is monotonic and carried by the rises. By Thursday z14 quintile, the next 2-day excess is −0.05 %, −0.04 %, +0.02 %, +0.45 % and +1.78 % (about 357 cases each). Over Wednesday and Thursday the slope is positive in all six coins, with t from 1.56 (XMR) to 2.29 (XRP), 594 cases each.
- **F3:** High volatility does not steepen the 2-day trend grading; it flattens it. On the all-days 2-day grid, the mean z14 × excess by volatility-ratio quartile is 0.013 (t 1.40), 0.015 (t 2.17), 0.009 (t 1.06) and 0.005 (t 0.28). On Fridays the slope is 0.0046 in high volatility and 0.0054 in low volatility, and the step-5 slope difference had t 1.30.
- **F4:** The book's gain comes from its longs. Its 784 long trades average +1.94 % net with 64 % winners, while its 686 shorts average −0.50 % net with 34 % winners. On high-volatility Fridays, weekend excess after a 14-day rise is +1.07 % (t 1.57, 76 days), and after a fall it is +0.32 % (t 0.52, 73 days), which is against the short.
- **F5:** The Wednesday-and-Thursday trend effect is unstable across years. It is positive in 2018 (t 1.74), 2021 (t 2.38) and 2024 (t 3.36), and negative in 2019, 2022 and 2025 (t −0.73, −0.89, −1.33). The tested high-volatility Friday slope is −0.013 (t −2.77) in 2025.
- **F6:** Other angles did not stand out once many angles had been examined:

## Ideas
- `031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend` (from F1, F2, F4, F5): A coin's 14-day return at Thursday's close (UTC) grades its move over the following Friday and Saturday: the larger its 14-day rise, the larger its gain over those two days.
- `031-01.g1.g1.g2.g2_calm-volatility-short-term-trend` (from F3, F1): When a coin's 20-day volatility is low relative to its usual level, its 14-day return grades its move over the next 2 days more steeply: the larger the rise or fall, the larger the move in its direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
