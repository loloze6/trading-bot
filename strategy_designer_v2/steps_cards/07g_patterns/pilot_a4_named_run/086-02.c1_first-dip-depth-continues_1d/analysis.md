---
line: 7.g patterns
backtest: 086-02.c1_first-dip-depth-continues_1d
idea tested: 086-02.c1_first-dip-depth-continues
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3503 USD
---
## Findings
- **F1:** Inside the rising agitated profile, the bars give no short edge at all: on the 5-day grid the short-direction unusual move is +0.41 % (t 0.26, 128 cases), against -0.15 % outside the profile (t -0.24, 348 cases); step 5's own cases give -0.86 % (t -0.57, 191 days).
- **F2:** The tested grading by dip depth does not hold: across the quartiles of the day's return in 30-day-swing units, the short unusual moves run +2.2 %, +6.1 %, +2.2 % and -3.6 % (27 to 28 cases each), not ordered, and the Spearman correlation is -0.13 (109 cases).
- **F3:** The brief's grading by run length is also absent: after up runs of 0, 1, 2, 3 and 4+ days, the short unusual moves are +2.2 %, -0.5 %, -4.0 %, +1.5 % and -7.4 % (t between -0.7 and +1.0, 3 to 68 cases), with no order.
- **F4:** The strongest pattern is down-run continuation: a short after 2 or more consecutive down closes in the profile gained +9.0 % unusual over 5 days on grid offset 0 (26 cases, t 2.06 on BCH, 2.52 on ZEC, and 2.54 and 2.42 in the earlier and later windows). On the four other grid offsets it gave +3.6 %, -0.1 %, -1.0 % and -2.2 %, so it rests on one sampling grid.
- **F5:** Grading by the depth of the current down run is not stable either: its Spearman correlation with the short unusual move is +0.15, +0.04, +0.05, -0.20 and -0.17 on the five grid offsets (41 to 59 cases each).
- **F6:** A close in the low quarter of the day's range looked strong on offset 0 (+5.0 %, t 2.98, 32 cases), but the same bucket gives +3.8 %, +5.6 %, -2.3 % and +2.8 % on the other offsets. Runs of two or more low closes give +8.1 % (t 1.89, 15 cases), too few to count.
- **F7:** None of the other angles stands out after roughly fifteen groupings: the day's range, volume against its 20-day mean, distance from the 20-day high, the 5- and 10-day returns, weekday and coin all have their best bucket's t at or below 2.5, and none is ordered across its buckets.

## Ideas
- No ideas: After many angles, no pattern in rising agitated markets on the short side survives a change of sampling grid or shows a graded order: the down-run continuation (F4) and the low-close result (F6) vanish on other grid offsets. The brief's effect of a first dip after an up run continuing lower, graded by the run or by the dip, is not in these bars (F1–F3).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
