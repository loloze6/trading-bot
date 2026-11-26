---
line: 7.g patterns
backtest: 060-01.b1.d2_post-slide-bounce-next-day-giveback_1d
idea tested: 060-01.b1.d2_post-slide-bounce-next-day-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4357 USD
---
## Findings
- **F1:** In the falling agitated profile, the next day's drift-adjusted return falls as the day's move in 30-day swing units rises, with a slope of -0.0134 and t -2.94 (1297 cases, 410 days). Outside the profile the same slope is flat: falling t -0.09, choppy t -0.93, rising t -0.13. The grading lives in this profile.
- **F2:** That slope comes from down days only. On down days it is -0.0220 (t -2.52, 658 cases, 248 days). On up days, the tested side, it is +0.0057 (t 0.88, 639 cases, 235 days). Larger scaled rises are not followed by larger givebacks.
- **F3:** Down days in the profile rebound more the larger they are. Next-day drift-adjusted means are +6.2 % for z ≤ -2 (t 1.73, 29 cases on 11 days), +2.2 % for -2 to -1 (t 1.81, 112 cases) and +1.2 % for -1 to -0.3 (t 2.60, 325 cases). This repeats the falling agitated rebound ideas the map already holds (035-01, 047-01, 051-01).
- **F4:** Up days in the profile are followed by a small weakness that does not grow with the rise. The means are -1.0 % for z 0 to 0.3 (t -1.65) and -1.0 % for 0.3 to 1 (t -1.91), then -0.2 % for 1 to 2 (t -0.24) and +0.2 % above 2 (t 0.09). On the 2-day grid they are -0.3 %, -0.5 % and +0.6 %, all with |t| < 0.6.
- **F5:** On rise days in the profile, the prior 5-day scaled return grades the next day only weakly. By quartile, deepest prior fall first, the means are -1.73 % (t -1.61), -0.75 % (t -1.44), -0.31 % (t -0.51) and -0.60 % (t -0.91). No quartile reaches |t| 2, which matches step 5's slope t of -0.59.
- **F6:** In the profile, the close's place in the day's range also grades the next day, with a slope of -0.030 (t -2.81, 1510 cases, 499 days). Closes in the bottom fifth gain +1.95 % (t 2.64). On up days alone the slope is +0.002 (t 0.08). This is again the low-close rebound already held (039-02, 045-01).
- **F7:** Outside the profile, in rising 60-day trends, days of z ≤ -1 are followed by +1.4 % (t 2.39, 223 cases, 83 days). The slope across all moves is -0.0003 (t -0.13). This is one cell among about 40 I examined, and it is not graded.
- **F8:** The book's gain is concentrated in a few days. Its best 2 % of days sum to +0.386, its worst 2 % to -0.307, and all 1449 days to +0.156. Its mean daily return is near 0 in every window from w7 to w18, between -0.00016 and +0.00067.

## Ideas
- No ideas: The only graded patterns are the down-day and low-close rebounds in falling agitated markets (F1, F3, F6), which the profile map already holds. The rise-side giveback is neither graded by the rise nor by the prior fall (F2, F4, F5). Across the forecast, prior-fall quartiles, close position, range, weekday, trend outside the profile and the book's extreme days, nothing else stood out beyond what chance gives over that many angles (F7).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
