---
line: 7.g patterns
backtest: 060-01.b1.d1.b1.b1_deep-slide-bounce-fades-overnight_1d
idea tested: 060-01.b1.d1.b1.b1_deep-slide-bounce-fades-overnight
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4465 USD
---
## Findings
- **F1:** In the falling agitated profile, the next day's return falls as the day's own move in swing units rises: the regression of the next-day excess return in swing units on that move has slope -0.178 (t -3.19, clustered by day, 1297 bars on 410 days), against -0.029 (t -0.98, 6967 bars on 1172 days) outside the profile. Almost all of it comes from down days: slope -0.300 (t -3.13, 658 bars on 248 days) on down days, against +0.084 (t 0.97, 639 bars on 235 days) on up days.
- **F2:** The deepest scaled down days in the profile (bottom quintile, below -0.71 swings) are followed by a next-day excess return of +2.22 % (t 2.42, 258 bars on 112 days). Their 3-day non-overlapping excess is +3.64 % (t 1.46, 35 days). This is the falling-agitated scaled-fall rebound the map already holds (047-01, 051-01), so it is not a discovery.
- **F3:** The tested cases (an up day after a scaled 5-day fall, in the profile) are followed by a negative next-day excess in the three lower quartiles of the rise's size: -1.28 % (t -2.89), -1.24 % (t -2.18) and -2.17 % (t -3.48), on 50 to 63 days each. The largest quartile shows +0.59 % (t 0.96). The slope of the next-day move on the rise's size is +0.176 (t 1.47, 377 cases on 160 days), so the giveback does not grow with the rise; it fades on the largest rises, against the brief's grading.
- **F4:** The tested grading by slide depth is weak in folds B and C. Its slope is +0.067 (t 1.01, 377 cases), which points the idea's way but cannot be told from 0. By depth quartile the next-day excess is -0.91 %, -2.52 % (t -2.42), -0.71 % and +0.03 %: not monotone.
- **F5:** In the profile, closing in the top third of the day's range is followed by -0.81 % next day (t -2.18, 506 bars on 203 days), and the close-position slope is -0.43 (t -2.68). Inside up days alone this slope is +0.03 (t 0.11), and inside down days it is -0.36 (t -1.20). The pattern therefore repeats F1's down-day rebound, the low-close rebound already held by 039-02 and 045-01, and is not a separate effect.
- **F6:** The book's gain is thin and concentrated. Its daily standard deviation is under 0.011 in every window, and windows w7 and w10 have no position at all. Window w14 carries the largest mean, +0.080 % a day (std 1.07 %). BTC (summed +0.49) and ETH (+0.31) carry most of the coins' total, while DOGE (-0.10) and ADA (about 0) lose.
- **F7:** Weekday shows nothing that stands out, inside or outside the profile: every |t| is at most 1.63.

## Ideas
- No ideas: The only effect that stands out after the many angles looked at is the next-day rebound after scaled down days in falling agitated markets (F1, F2, F5), which the map already holds (047-01, 051-01, 039-02, 045-01). The short-side pattern on up days (F3) is not graded with the rise, and runs against the brief's grading, so it gives no graded idea to propose.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
