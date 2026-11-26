---
line: 7.g patterns
backtest: 065-02_falling-agitated-prior-slide-rebound_1d
idea tested: 065-02_falling-agitated-prior-slide-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4294 USD
---
## Findings
- **F1:** Inside the falling agitated profile, the latest day's own fall carries the next-day rebound, and the four-day slide before it adds nothing. With both regressors in the model (1343 bars, day-clustered), the latest day's scaled return has slope -0.0118 with t -3.62. The prior four-day slide has slope -0.0015 with t -0.95, which is the wrong sign for the brief.
- **F2:** The rebound is graded by the latest day's fall. In the profile, the bottom octile of the latest day's return is followed by +2.91 % excess the next day (t 2.73, 174 bars, 74 days). The second octile is followed by +1.28 % (t 2.96). The middle octiles are followed by -1.27 % (t -2.57) and -1.19 % (t -2.37). The same grading is about three times weaker outside the profile: slope -0.0039, t -2.47, against -0.0118 inside.
- **F3:** The brief's own claim that "a small down day ending a deep slide still rebounds" is not in the bars. In the profile, a deep slide with a latest day above the median is followed by -1.00 % (t -1.64, 355 bars). A deep slide with a latest day below the median is followed by +1.97 % (t 3.01, 318 bars). A shallow slide with a low latest day is followed by +0.75 % (t 1.62).
- **F4:** Sorted by the four-day slide, the profile's next-day excess return shows no gradient. The deepest-slide quintile gives +0.58 % (t 0.83, 388 bars) and the shallowest gives -0.30 % (t -0.43). Three days ahead, the deepest-slide quintile gives +1.39 % (t 0.77, 117 cases).
- **F5:** A low close inside the day's range adds nothing once the day's return is known. In the profile, a close in the bottom fifth of the range is followed by +2.01 % (t 2.73). In the regression, the close position has t 0.53 while the latest day's return keeps t -2.62. This rebound is the same pattern as the held idea 045-01 (agitated wide low close rebound).
- **F6:** Up days in the profile are followed by a fall on average: the constant is -1.22 % (t -2.49, 659 bars). The fall is not graded by the size of the rise: the slope is +0.0038 with t 0.93, and the largest-rise tercile is followed by only -0.23 % (t -0.38). With the many angles looked at, this cannot be written as a graded idea.
- **F7:** The book's gain rests on a few days. Its mean is 0.0117 % a day over 1449 days. The ten best days sum to +50.1 % and the ten worst to -40.5 %, so the top ten days are 2.95 times the book's total gain.

## Ideas
- No ideas: The theme's effect is not in the data: the slide's depth adds nothing once the latest day's fall is known (t -0.95, F1, F3, F4). The only graded pattern found, the falling agitated latest-day fall rebound (F2, F5), is already held (047-01, 038-01, 051-01, 045-01). The up-day fall in the empty short cell is not graded (F6). I looked at the forecast, the latest day, the slide, the 5- and 10-day returns, close position, volatility, weekday, year, the 2- and 3-day horizons and the book's extreme days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
