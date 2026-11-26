---
line: 7.g patterns
backtest: 040-02_agitated-fall-vs-swing-rebound_1d
idea tested: 040-02_agitated-fall-vs-swing-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4187 USD
---
## Findings
- **F1:** Among agitated down days, next-day excess return regressed on the fall and on the fall × log(volume / its 20-day mean) gives the interaction a t of 2.99 (coefficient 0.0126, 1439 cases on 537 days), while the fall alone drops to t 0.26. The day's volume against its recent average carries the rebound, more than the size of the fall measured in usual daily moves.
- **F2:** The volume interaction is absent in calm markets: t -0.45 (1978 cases, 665 days), with the fall alone at t 1.58. The volume-graded effect is tied to agitation, as the brief's forced-selling reason requires.
- **F3:** Agitated falls beyond 0.75 usual daily moves, split into volume terciles, give next-day excess returns of +0.16 % (t 0.23), +0.96 % (t 1.30) and +2.01 % (t 2.07, 170 cases on 91 days) from low to high volume. In calm markets the high tercile gives only +0.76 % (t 1.52).
- **F4:** The high-volume tercile leads in 2018, 2019 and 2020 (+3.04 %, +2.32 %, +2.10 %) and weakens in 2021 (+0.73 %). It extends to three days on the non-overlapping 3-day grid: high volume +4.29 % (t 1.95, 49 cases) against low volume -1.23 % (t -0.63). That is far above the 0.19 % cost of a trade.
- **F5:** The prior 5-day fall, tested next to volume, adds nothing on its own: t -0.16 additively and t 0.82 as an interaction with the fall, in 1439 agitated cases. The tercile split (lowest 5-day return +2.39 %, t 2.51) is mostly the heavy-volume cell (+4.10 %, t 2.33, 74 cases), so it is not a separate effect.
- **F6:** The book's best days follow held bars with heavier volume than the book's average held bar (relative volume 1.67 against 1.05) and deeper falls (z -1.45 against -0.55). Its worst days follow ordinary-volume falls (1.09). The book's gain is concentrated where volume is heavy.

## Ideas
- `040-02.g1_agitated-heavy-volume-fall-rebound` (from F1, F2, F3, F6): In an agitated market, the larger a coin's one-day fall and the heavier that day's volume against its average daily volume over the past 20 days, the larger its rise over the next day.
- `040-02.g2_heavy-volume-fall-three-day-rebound` (from F1, F3, F4): In an agitated market, the larger a coin's one-day fall and the heavier that day's volume against its average daily volume over the past 20 days, the larger its rise over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
