---
line: 7.g patterns
backtest: 036-02_range-scaled-rally-continuation_1d
idea tested: 036-02_range-scaled-rally-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4107 USD
---
## Findings
- **F1:** The tested range-scaled 3-day rise does not predict the next 7 days on folds B and C. The quintiles of the scaled rise give a 7-day excess return of -0.72 %, -1.45 %, -0.43 %, +1.73 % and -0.53 %, with no quintile at |t| ≥ 2. The pooled slope t is 0.10 on 1,075 non-overlapping cells. This matches step 5's unusual move of -0.15 % (t -0.33), so the book's +0.76 % total move per case is the coins' drift and not the idea.
- **F2:** The strongest pattern in the bars is a next-day rebound after a large one-day fall, scaled by the coin's 30-day daily standard deviation. It is graded:
- **F3:** The rebound lives on the falling side only:
- **F4:** The rebound is concentrated in agitated markets that are not rising. Trend here is the 30-day return (the 60-day trend is not available inside the windows), and agitation is the 30-day swing against its last 120 days:
- **F5:** Patterns that did not stand out against the number of angles looked at:
- **F6:** Within big down days, where the day closes in its range matters little. Next-day excess is +1.25 %, +1.03 % and +0.82 % from low close to high close (t 3.92, 3.00 and 2.16). The size of the fall, not the shape of the day, carries the rebound. Per case, a 1 to 2 standard deviation fall rebounds +0.75 %, about 3.9 times the 0.19 % cost of a trade.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `036-02.g1_scaled-one-day-fall-rebounds` (from F2, F3, F6): A coin whose one-day fall is large against its usual daily swing (the standard deviation of its daily returns over the past 30 days) rises over the next day, and the larger that swing-scaled fall, the larger the rebound.
- `036-02.g2_falling-agitated-fall-rebound` (from F4, F2, F3): In an agitated market that is falling, a coin whose one-day fall is large against its usual daily swing over the past 30 days rises over the next day, more the larger the swing-scaled fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
