---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d
idea tested: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3736 USD
---
## Findings
- **F1:** Across all days, the next day's excess return falls with the day's own volatility-scaled move only when volatility is high: in the top volatility tercile the slope is -0.00709 (t -8.05, n 5075), in the middle tercile it is -0.00045 (t -0.72), and in the bottom tercile it is +0.00115 (t 2.36), so the day-ahead reversal is a high-volatility effect, not a weekend one.
- **F2:** The Sunday 3-day reversal the idea tested follows the same volatility grading: the slope of the Sunday-to-Wednesday excess return on Sunday's scaled move is -0.00085 (t -0.30, n 708) in the low-volatility tercile, -0.00779 (t -2.18, n 707) in the middle tercile and -0.01502 (t -3.23, n 708) in the high-volatility tercile, while weekend volume adds nothing (z×volume-ratio t 0.89).
- **F3:** The 1-day reversal is not limited to the weekend; its slope is about as negative after Tuesday (t -3.32), Wednesday (t -3.35) and Saturday (t -4.65) bars as after Sunday bars (t -3.21), which contradicts the brief's claim that weekend moves reverse more.
- **F4:** Over longer spans, moves continue rather than reverse: on the non-overlapping 7-day grid, the 14-day volatility-scaled return predicts the next 7-day excess return with slope 0.01213 (t 4.40, n 2011), and the 7-day return gives slope 0.01024 (t 3.67), led by XRP (t 2.87) and ZEC (t 2.36); the slope drops to t 0.56 once each window's own mean is removed, so it reads as persistence of trends lasting several weeks.
- **F5:** The book's whole gain lands on Monday, with mean book return 0.000798 (t 2.36, n 2484), while Sunday costs -0.00021 per coin-day (t -29.5) in fees; held one day a week, the book cannot match holding the coins, whose mean daily return is above 0.0027 on Wednesday, Friday and Saturday.
- **F6:** Calendar drift is uneven across weekdays: Friday's return (the day after a Thursday close) has an excess of +0.00305 (t 3.76, n 2479), and Saturday's return is positive in 6 of 8 years (t 2.2 to 2.7 in 2019, 2020, 2024 and 2025).

## Ideas
- `011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal` (from F1, F2, F3): A coin whose last day's move was large relative to its 20-day volatility moves the opposite way over the next 1 day, and the reversal is larger the larger that scaled move and the higher the coin's 20-day volatility stands against its own history.
- `011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly` (from F4): A coin's 14-day return scaled by its 20-day volatility is followed by a move in the same direction over the next 7 days, larger the larger that scaled return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
