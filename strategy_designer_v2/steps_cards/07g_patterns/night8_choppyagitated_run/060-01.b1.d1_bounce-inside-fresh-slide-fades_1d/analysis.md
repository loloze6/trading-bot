---
line: 7.g patterns
backtest: 060-01.b1.d1_bounce-inside-fresh-slide-fades_1d
idea tested: 060-01.b1.d1_bounce-inside-fresh-slide-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6326 USD
---
## Findings
- **F1:** In the falling agitated profile, an up day that follows a down day is given back the next day. The mean unusual next-day return is -1.36 %, with a day-pooled t of -2.49 over 370 cases on 145 days. An up day that follows an up day is not given back: -0.15 %, day-pooled t -0.24, 267 cases on 117 days. The theme's fade therefore lives in the first bounce of a slide and shows over one day, not three.
- **F2:** Among those up-after-down days in the profile, the giveback is larger when yesterday's fall was shallow in 30-day-swing units. Mean next-day unusual return by yesterday's fall: -2.01 % for a fall of 0 to 0.3 swings (t -4.37, n 100), -1.12 % for 0.3 to 1 (t -2.79, n 184) and -0.45 % for 1 to 2 (t -0.59, n 67). The tail beyond 2 swings is -3.47 % (t -1.94, n 19), too few cases to read.
- **F3:** Those up-after-down days are not graded by the size of today's rise. Mean next-day unusual return by today's rise: -1.38 % for 0 to 0.5 swings (t -3.41), -1.93 % for 0.5 to 1 (t -3.73), +0.80 % for 1 to 1.5 (t 0.89) and -1.89 % for above 1.5 (t -2.09). The brief's grading by rise size is not what carries the fade.
- **F4:** The tested 3-day horizon dilutes the effect. Across all in-profile up days, the next-day giveback is -0.85 % (day-pooled t -1.97, 639 cases on 235 days). The 2-day unusual move by rise size is mixed: -0.29 %, -0.46 %, +2.40 %, -1.46 %. The book's 3-day total move is +0.12 %, which is 0.5 times the 0.22 % cost of a trade.
- **F5:** In the profile, the next day reverses today's move across all days. The correlation of today's scaled return with the next day's unusual return is -0.20 over 1,297 days. After down days the next-day rebound is +1.25 % (day-pooled t 2.74, 658 cases on 248 days), largest after the largest falls: +6.2 % below -2 swings (t 3.69). This is the falling-agitated daily-fall rebound the map already holds (047-01, 051-01, 038-01), so it is not a discovery.
- **F6:** Weekday effects outside the profile fade once same-day cases are pooled. Wednesdays show -0.61 % next day (bar t -3.32, day-pooled t -1.46). Thursdays show +0.50 % (bar t 3.38, day-pooled t 1.49). After this many angles, these are not findings to act on.

## Ideas
- `060-01.b1.d1.g1_first-bounce-after-mild-dip-fades` (from F1, F2, F3, F4): In a falling, agitated market, a coin's up day that comes right after a down day is given back over the next day. The giveback is larger the shallower that preceding down day was against the standard deviation of the coin's daily returns over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
