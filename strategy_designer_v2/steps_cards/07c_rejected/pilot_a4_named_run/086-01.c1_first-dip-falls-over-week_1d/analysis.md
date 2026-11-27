---
line: 7.c no effect
backtest: 086-01.c1_first-dip-falls-over-week_1d
idea tested: 086-01.c1_first-dip-falls-over-week
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3927 USD
---
## Findings
- **F1:** Over every window, the step-5 verdict found that coins rose after the first down day of an up run instead of falling: the short-direction unusual 7-day move was -1.50 % (t -0.89, 257 cases on 195 days), and the slope on the streak's size was -0.0015. In the explore half (w1 to w18) the same cases fell, -4.99 % over 7 days (t -1.58, 65 cases on 57 days). The windows step 5 saw and these windows therefore disagree in sign.
- **F2:** The fall does not grow with the number of up days in the streak; it is the opposite. Over 7 days, 2-day streaks were followed by -9.2 % (t -2.13, 39 cases), 3-day streaks by +1.6 % (t 0.36, 15 cases) and streaks of 5 days or more by -1.0 % (t -0.33, 8 cases). The correlation between streak length and the 7-day move over all in-profile down days is -0.10 (103 cases).
- **F3:** Inside the profile, what grades the move is how deep the down day is against the coin's 30-day swing, not how long the streak was. For dips after a run of at least one up day, the deepest third (mean drop 1.27 swings) was followed by -8.8 % over 7 days (t -1.95, 26 cases). The shallowest third rose +1.7 % (t 0.36) and the middle third rose +6.5 % (t 1.52). The slope on the drop was -0.084 (t -1.66, 93 cases).
- **F4:** The deep-dip continuation lasts beyond a week. Over 14 days, in-profile dips after 2-day-plus runs fell -9.8 % (t -1.92, 46 cases), against -5.0 % at 7 days and +0.6 % at 3 days. Over all in-profile down days, the deepest third fell -11.5 % over 14 days (t -1.85, 13 cases).
- **F5:** The pattern is specific to the profile. Outside rising agitated markets, a down day is followed by a rebound that grows with its depth: the slope of the 7-day move on the drop was +0.038 (t 2.71, 265 cases), and the 3-day slope was +0.017 (t 2.47, 525 cases). Inside the profile the slopes are negative (-0.050 at 7 days and -0.108 at 14 days, all down days).
- **F6:** The explore-half fall is not even across coins or years. ZEC carries it (-5.1 %, t -1.65, 37 cases) more than BCH (-2.9 %, t -0.60, 25 cases), and 2020 (-9.5 %, t -2.17, 24 cases) more than 2021 (-2.1 %, t -0.40, 33 cases). Together with F1, this means any amended idea rests on weak evidence.

## Ideas
- `086-01.c1.c1_deep-first-dip-continues` (from F3, F4, F5, F2): In a rising, agitated market, when a coin closes down after a streak of up days, it keeps falling over the next 14 days, and the fall is larger the deeper that down day was measured against the coin's usual daily swing over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
