---
line: 7.g patterns
backtest: 066-02_falling-agitated-year-scaled-fall-rebound_1d
idea tested: 066-02_falling-agitated-year-scaled-fall-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.7451 USD
---
## Findings
- **F1:** Inside the falling agitated profile, the next-day excess return grows with the size of the fall measured against the coin's 30-day swing. It is +6.58 % after falls beyond 2 swings (t 1.89, 28 cases, 11 days), +2.16 % from 1 to 2 swings (t 1.80, 112 cases), +1.07 % from 0.5 to 1 swing (t 1.82, 190 cases) and +0.61 % below 0.5 swing (t 1.06, 292 cases). The slope of excess return on the 30-day-scaled fall is -0.0222 (t -2.59, 622 falls on 245 days). The recent yardstick grades the rise at least as well as the yearly one did (forecast slope t 2.44). That is the brief's first falsifier, and that 30-day-scaled rebound is already held (051-01, 058-02.b1.g1.b1.b1).
- **F2:** Outside the profile, in rising markets (60-day return above +10 %), a fall of 1 to 2 swings of the last 30 days is followed by a next-day excess of +2.06 % at 1.5 to 2 swings (t 2.56, 63 cases, 33 days). It is +1.15 % at 1 to 1.5 swings (t 1.61, 132 cases) and nothing below 1 swing (-0.34 %, t -0.65; +0.35 %, t 0.89). All falls beyond 1 swing together give +1.40 % (t 2.41, 219 cases, 83 days).
- **F3:** That rising-market rebound lasts two days. The 2-day excess is +2.82 % after falls of 1.5 to 2 swings (t 3.12, 63 cases) and +1.54 % at 1 to 1.5 swings (t 1.59). In the profile itself, day 2 adds nothing after falls (+0.30 %, t 0.08 beyond 2 swings; -0.17 %, t -0.17 at 1 to 2 swings).
- **F4:** The rising-market rebound after falls beyond 1 swing holds in every year of folds B and C: 2019 +0.41 %, 2020 +1.16 %, 2021 +2.03 % (t 2.32). It is positive on all 8 coins with enough cases (ETH +1.52 % t 2.57, XMR +2.56 % t 3.16, BTC +1.07 % t 2.28). It is at least as strong in the calmer half of 30-day swings (+1.55 %, t 2.99, 109 cases) as in the more agitated half (+1.26 %, t 1.56, 110 cases).
- **F5:** In falling markets outside the profile (calm), falls beyond 1 swing earn no rebound: -0.18 % (t -0.28, 203 cases, 87 days). This supports the brief's claim that agitation is needed in a downtrend.
- **F6:** Inside the profile, up days are followed by a below-drift next day of -0.82 % (t -1.89, 605 cases, 235 days). This is negative in every year, from -0.40 % to -1.42 %, and on 8 of 9 coins. It is not graded by the size of the rise (slope t +0.81; the smallest rises fade most, -0.95 %). Its t is under 2 and the both-sided reversal in this profile is already held, so it is no idea.
- **F7:** Inside the profile, falls closing in the lower half of their range rebound: +1.49 % (t 2.37, 339 cases) and +1.12 % (t 2.40, 286 cases). Falls closing in the upper half do not (+0.65 %, t 0.62; +0.41 %, t 0.29). This is the low-close rebound already held (045-01, 039-02).
- **F8:** The book's gain sits in two windows of the twelve shown, w16 (summed daily return 0.272) and w14 (0.137), out of about 0.65 in all. Trades entered on forecasts above 10 average +1.56 % net, against +0.55 % for forecasts of 1 to 3 (390 and 35 trades).

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `066-02.g1_rising-market-dip-rebound` (from F2, F3, F4, F5): In a rising market, a one-day fall that is large against the coin's swing over the last 30 days is followed by a rise over the next two days, and the larger the fall against that swing, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
