---
line: 7.g patterns
backtest: 067-01_choppy-up-stretch-keeps-rising_1d
idea tested: 067-01_choppy-up-stretch-keeps-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5055 USD
---
## Findings
- **F1:** Outside the choppy profile, the tested stretch carries forward only in calm markets. On the 10-day non-overlapping grid, with the trend recomputed from each window's own 60 days, the slope of the excess 10-day return (in usual moves) on the clipped stretch has these t values, clustered by date:
- **F2:** In falling calm markets, a close below its 20-day average is followed by further fall. On the 10-day grid, the excess move in the short direction is +3.94 % for all closes below the average. For stretches beyond −1.5 swing units it is +5.49 % (36 cases), against +5.4 % of a usual 14.5 % move. In falling agitated markets the same deep-below cases give −1.01 % (52 cases), a small rebound rather than a continuation.
- **F3:** Inside the choppy profile the idea's own slope is not reliable, and its short side loses in the book:
- **F4:** The bar-level patterns that stand out are all one-day reversals or weekday effects the map already holds. They are not discoveries:
- **F5:** Rising calm continuation of the stretch is the strongest of these patterns. It reaches +6.18 % excess for closes above the average over 10 days and +6.58 % for stretches beyond +1.5 (47 cases). It repeats ideas the map already holds in rising calm (058-03.e1 calm rise stretch ten days, 035-01.b1, 058-02 range-edge continuation), so it is left out as already held.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `067-01.g1_falling-calm-stretch-keeps-falling` (from F1, F2): In a falling, calm market, the further a coin's close stands below its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin falls over the next 10 days.
- `067-01.g2_agitated-stretch-below-rebounds` (from F1, F2, F3): In an agitated market, the further a coin's close stands below its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin rebounds over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
