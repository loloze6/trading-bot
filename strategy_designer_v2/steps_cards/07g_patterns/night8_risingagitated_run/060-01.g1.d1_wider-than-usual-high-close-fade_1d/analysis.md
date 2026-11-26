---
line: 7.g patterns
backtest: 060-01.g1.d1_wider-than-usual-high-close-fade_1d
idea tested: 060-01.g1.d1_wider-than-usual-high-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4677 USD
---
## Findings
- **F1:** In falling agitated bars, the next day's unusual move (in usual moves) has a correlation of -0.25 with the day's return scaled by the 20-day swing and -0.20 with the close location. In falling calm bars both are near zero (+0.01 and +0.02). The fading of strong days lives where the brief puts it: a downtrend with forced swings.
- **F2:** In falling agitated bars, the next-day unusual move by quintile of the day's volatility-scaled return runs from +0.30 (z1) and +0.25 (z2) down to -0.33 (z4, t -2.95 with cases summed per day, 153 cases on 83 days) and -0.21 (z5, t -1.70). Over the next 3 days on the non-overlapping grid, it runs from +0.19 and +0.25 (z1, z2) down to -0.24 (z4) and -0.51 (z5, t -2.44, 60 cases on 23 days). The larger the up day, the larger and longer the give-back.
- **F3:** The range multiple the tested idea grades by is not graded by itself here. Across all falling bars, the next-day move by range-multiple quartile is +0.02, -0.15, +0.04, -0.03 usual moves, while close location and the day's return carry the effect (F1).
- **F4:** On the book's active bars, 94 of 160 sit in the top quintile of the day's scaled return. There the next day is -0.27 usual moves (t -2.56), which is a gain for the short. The 9 active bars in the bottom quintile lose (+0.71), and the 20 active bars closing at 0.4–0.6 of the range lose (+0.42), against -0.35 and -0.33 for closes at 0.6–0.8 and 0.8–1.0.
- **F5:** In choppy agitated bars the next day is weak overall: -0.20 usual moves, t -2.64 over 257 bars. High closes there fade by -0.40 (c4, t -2.08) and -0.34 (c5, t -1.78). These are too marginal for the number of angles looked at, so this is not a finding to build on.
- **F6:** The weekday pattern has the same sign in all six coins: Wednesday -0.094 usual moves (t -2.82), Thursday +0.077 (t 2.84), Friday +0.068 (t 2.79). It is not graded and is close to the held late-week gain idea (045-01), so it is not a discovery.
- **F7:** In falling agitated bars, a close in the bottom fifth of the range rebounds +0.41 usual moves the next day (t 1.96, 86 days). That cell already holds 12 long rebound strategies, so this is already held.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-01.g1.d1.g1_falling-agitated-surge-fades` (from F1, F2, F4): In a falling, agitated market, a coin whose day's return is large and positive against its usual daily swing of the last 20 days falls over the next three days; the larger that day's rise against its usual swing, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
