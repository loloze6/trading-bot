---
line: 7.g patterns
backtest: 032-02_choppy-agitated-weekly-fall-reverts_1d
idea tested: 032-02_choppy-agitated-weekly-fall-reverts
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4182 USD
---
## Findings
- **F1:** The weekly reversal the brief claims does not appear in folds B and C. On the 7-day grid, the slope of the next week's excess return on the past week's return is +0.0035 (t 0.12, 1,101 cells). Inside the tested profile there are only 60 cells, with slope t -0.18 and a mean excess of -2.38 %. In the choppy, high-swing tercile there are only 12 cells (slope +0.10, t 0.36).
- **F2:** A one-day fall is followed by a rebound the next day, graded with the size of the fall, but only when the coin is agitated. Agitated here means its 30-day swing is above its own median over the sample, which only approximates the profile's past-year median. The slope of the next day's excess return on the previous day's fall, both in units of the 30-day swing, is -0.206 when agitated (day-clustered t -3.17; 1,716 cases on 640 days). When calm it is -0.007 (t -0.07; 1,701 cases on 595 days).
- **F3:** Among agitated days, the graded rebound sits in falling markets and is absent in rising ones. Falling agitated: slope -0.302, t -3.02, 580 cases on 212 days. Choppy agitated: -0.506, t -2.40, only 73 cases on 56 days. Rising agitated: -0.040, t -0.39, 358 cases. Every calm cell has a slope of zero or the wrong sign: falling calm +0.04, choppy calm +0.31, rising calm -0.15 with t -1.34.
- **F4:** The rebound is on the fall side only.
- **F5:** The fall-side slope points the same way on every coin and in every year.
- **F6:** The rebound persists over three days and is still graded, but this reading uses overlapping, unclustered returns, so it is supportive only. Mean 3-day return: +1.40 % after falls of -2 swings or worse, +1.14 % after falls between -2 and -1 swings, and +0.36 % after smaller falls.
- **F7:** Against this backtest's cost of 0.19 % per trade, the one-day rebound is large. It is about 9 times the cost after falls of -2 swings or worse (1.82 %) and about 4 times after falls between -2 and -1 swings (0.75 %). The tested idea's unusual move was -0.39 % (t -0.40), about -2 times the cost.
- **F8:** Two other patterns do not stand out once their evidence is weighed.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `032-02.g1_agitated-one-day-fall-rebounds` (from F2, F4, F5, F7): In an agitated market, the larger a coin's one-day fall relative to its usual daily swing, the larger its rise over the next day.
- `032-02.g2_falling-agitated-daily-rebound` (from F3, F2, F7): In a falling, agitated market, the larger a coin's one-day fall relative to its usual daily swing, the larger its rise over the next day.
- `032-02.g3_agitated-fall-three-day-rebound` (from F2, F6, F7): In an agitated market, the larger a coin's one-day fall relative to its usual daily swing, the larger its rise over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
