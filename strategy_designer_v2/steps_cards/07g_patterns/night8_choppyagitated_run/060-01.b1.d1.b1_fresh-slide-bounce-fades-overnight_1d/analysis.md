---
line: 7.g patterns
backtest: 060-01.b1.d1.b1_fresh-slide-bounce-fades-overnight_1d
idea tested: 060-01.b1.d1.b1_fresh-slide-bounce-fades-overnight
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4724 USD
---
## Findings
- **F1:** The giveback after up days in falling agitated markets is a level shift, not a graded effect. Up days of 0.5 to 1.5 thirty-day standard deviations are followed by a next-day excess of -1.20 % (t -2.45, 234 cases, 116 days) and a 3-day excess of -3.16 % (t -2.36, 88 non-overlapping cases, 41 days). Days above 1.5 deviations give back no more (-1.09 % next day, t -1.10, 72 cases). The next-day slope on the rise's size is only -0.55 % per deviation (t -1.04, 623 cases, 202 days).
- **F2:** The book's forecast does not order its own trades. Short-signed next-day excess by forecast quartile, weakest to strongest, is +0.77 % (t 1.42), +1.51 % (t 1.97), +1.46 % (t 1.50) and +0.42 % (t 0.38) (about 108 cases each). The strongest shorts are the weakest, which is why the slope's t is -0.65 even though the mean short earns +0.52 %.
- **F3:** The graded effect in falling agitated markets is on the other side: a rebound after down days. The next-day excess rises by 2.28 % per deviation of the fall (t 2.60, 642 cases, 213 days), and falls of more than 1.5 deviations are followed by +3.95 % (t 2.37, 67 cases, 30 days). In falling calm markets the slope is -0.17 % (t -0.31, 520 cases). The map already holds this rebound in falling agitated long (13 strategies, among them 035-01 "falling agitated scaled fall rebound"), so it is not a discovery.
- **F4:** The same down-day rebound grows with the fall in choppy agitated markets: 3.59 % per deviation next day (t 2.28, 91 cases, 70 days). The map already holds this in choppy agitated long (5 agitated rebound strategies).
- **F5:** Other patterns reach a t of about 2 to 3 in one bucket but are not graded, out of more than 100 cells examined:
- **F6:** The book is thin and concentrated. It is in a position on 298 book-days, its median day is 0, and its 10 largest absolute days carry 26 % of its summed return. Its daily 1 % and 99 % quantiles are -0.45 % and +0.86 %.

## Ideas
- No ideas: The only graded pattern that stands out among the many angles examined (F3, F4) is the agitated down-day rebound the profile map already holds. The brief's own up-day giveback appears as a level but does not grow with the rise (F1, F2), and the other cells reaching a t near 2 to 3 lack grading and do not stand out from chance given how many were looked at (F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
