---
line: 7.g patterns
backtest: 067-01.b1.b1_choppy-stretch-carries-both-ways_1d
idea tested: 067-01.b1.b1_choppy-stretch-carries-both-ways
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3898 USD
---
## Findings
- **F1:** Inside the choppy profile (the strategy's active regime, 249 non-overlapping 5-day cases), the stretch below the average carries forward: the lowest fifth of the stretch (below -1.45 swings) is followed by a 5-day excess return of -6.0 % (t -3.3, n 50). The highest fifth (above +1.88 swings) is followed by only +0.2 % (t 0.1, n 50). The carry is on the short side only.
- **F2:** Inside the choppy profile, the pooled slope of the 5-day excess return on the stretch is 0.0094 per swing, with a t of 1.83 when cases on the same day are clustered (249 cases, 128 days). It is positive but cannot be told from chance, because the upper half adds almost nothing (the fourth fifth is +1.4 %, t 1.3).
- **F3:** My own recomputation of the 60-day choppy band on the 5-day grid gives the same result. The lowest fifth of the stretch (below -1.11 swings) is followed by -8.0 % (t -2.9, n 26), the second fifth by -3.5 % (t -2.0, n 25), and the top fifth by only +2.5 % (t 0.8, n 26).
- **F4:** Outside the profile, in markets that rose or fell more than 10 % over 60 days (1173 cases, 254 days), the stretch also carries. The slope t is 1.75, and both upper fifths are followed by gains: +1.8 % (t 2.7) and +2.5 % (t 2.8). This is trend continuation near highs, which the map already holds in rising markets (034-01.b1, 035-01.b1, 058-02 family), so it is not a discovery.
- **F5:** The book's positions inside the profile earn on both sides, 0.128 % a day held long (707 coin-days) and 0.069 % held short (750 coin-days). The whole book earns 0.031 % a day on days in a position, about 2.6 % a year, below holding the coins in 11 of 12 windows' coin means.
- **F6:** Daily excess returns by weekday are +0.47 % on Thursday (t 3.2) and +0.39 % on Friday (t 2.9), against -0.49 % on Wednesday (t -2.7). These t's are not clustered by day across six co-moving coins, so they overstate the evidence. The late-week gain is also already held (045-01), so I leave it out.

## Ideas
- `067-01.b1.b1.g1_choppy-downside-stretch-keeps-falling` (from F1, F2, F3): In a choppy market, the further a coin's close stands below its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
