---
line: 7.b inconclusive
backtest: 041-02_agitated-fall-rise-vs-range-giveback_1d
idea tested: 041-02_agitated-fall-rise-vs-range-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3620 USD
---
## Findings
- **F1:** Inside the falling agitated profile, up-days are followed by a next-day fall, but its size does not grow with the rise. The 500 up-days average −0.99 % next day after drift (t −4.13), or −0.74 % pooled over 192 days (t −2.16). The slope of the next-day return on the rise in 30-day mean ranges has t 0.14 (Spearman −0.001), and the rise quartiles give −0.70 %, −1.23 %, −1.33 % and −0.71 %. Step 5's graded test therefore finds a slope of zero (t −0.52) even though the supporting check passes (+0.56 %).
- **F2:** The grading the brief claims is there on the mirror side. On the profile's 517 down-days the next-day return falls with the scaled move, so larger falls bounce more: slope on the move in 30-day mean ranges t −3.03, on the move in 30-day daily swings t −4.07, clustered over 211 days. The fall quartiles, largest first, give +1.93 %, +1.76 %, +0.63 % and +0.64 %.
- **F3:** Taking all profile days together, both sides, the next-day return falls steadily as the day's move against the 30-day average daily range grows (slope t −3.75 over 1,013 cases on 338 days, Spearman −0.21). By bin it runs from +6.7 % after moves of 1.5 ranges or more down (18 cases) and +1.5 % after 0.5 to 1 range down (t 3.31), to −1.28 % after 0.2 to 0.5 range up (t −3.94) and −3.59 % after 1 to 1.5 ranges up (t −3.39).
- **F4:** The effect lives in the profile. Outside it, the same bins are flat or small (−0.21 % to +0.51 % for moves between −1 and +1.5 ranges); only the largest falls of 1.5 ranges or more bounce (+1.40 %, t 2.36, 99 cases).
- **F5:** The up-day fall is on the predicted side in every year: 2018 −1.47 %, 2019 −0.66 %, 2020 −0.45 %, 2021 −1.30 %. It is also on that side in the five windows with 30 or more cases (w9 −0.29 %, w13 −1.56 %, w14 −1.42 %, w15 −1.16 %, w16 −0.44 %, w18 −1.35 %). Within up-days, what grades the giveback is how much the day's own range spread, not the size of the rise: slope on the day's range in 30-day mean ranges t −2.03. Up-days closing in the lowest third of their range fall −1.38 % against −0.47 % for the top third.

## Ideas
- `041-02.b1_agitated-fall-two-sided-fade` (from F3, F2, F4, F1): In a falling, agitated market, the larger a coin's one-day move against its 30-day average daily range, the larger the opposite move over the next day: a large rise is followed by a larger fall and a large fall by a larger rise.
- `041-02.b2_agitated-fall-down-day-bounce` (from F2, F4): In a falling, agitated market, the larger a one-day fall against the coin's 30-day average daily range, the larger the rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
