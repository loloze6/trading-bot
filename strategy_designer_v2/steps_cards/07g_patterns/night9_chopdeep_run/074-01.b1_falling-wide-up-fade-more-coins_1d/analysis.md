---
line: 7.g patterns
backtest: 074-01.b1_falling-wide-up-fade-more-coins_1d
idea tested: 074-01.b1_falling-wide-up-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6104 USD
---
## Findings
- **F1:** In the falling market, the next-day fade after up days does not grow with width. Next-day excess by width quintile was -0.13 % (t -0.32), -0.25 % (t -0.67), -0.87 % (t -2.62, 232 days), -0.77 % (t -1.58) and -0.67 % (t -1.46), from narrowest to widest. The fade peaks in the middle quintile and does not grow at the widest, which matches step 5's failed check (Welch t -0.93).
- **F2:** Falling-market up days are weaker the next day whatever their size. All five width quintiles are negative, as are all five quintiles of the up move scaled by the 20-day average range (from -0.84 % with t -2.33 to -0.06 %). Falling-market down days lean the other way (widest quintile +1.08 %, t 1.86, 144 days). This is the falling-market next-day reversal the map already holds (058-02.b1.g1.b1.b1).
- **F3:** Where a wide falling-market up day closes in its range is not stable from half to half. Over all windows the high-close third gave -1.21 % (t -1.70) and the low-close third -0.06 % (t -0.10). In w7–w12 the high-close third gave -0.87 % (t -2.28) and in w13–w18 the low-close third gave -0.91 % (t -1.93), so the pattern flips between halves.
- **F4:** The falling-market wide-up fade does not move to a later day. On non-overlapping grids, up days with width above 1.3 gave -0.67 % at 1 day (t -1.24, 148 days), +0.31 % at 2 days (t 0.33), -1.93 % at 3 days (t -1.49) and -1.89 % at 5 days (t -1.28). None of these is told apart from 0.
- **F5:** Outside the falling market, wide down days rebound over the next days. Down days with width above 1.3 gave +0.99 % at 1 day (t 2.07, 231 days), +2.18 % at 2 days (t 2.48, 115 days) and +3.53 % at 3 days (t 2.47, 68 days). Where the 60-day trend is above +10 %, the 2-day rebound is +3.65 % (t 2.86, 53 days) and the 3-day rebound +5.12 % (t 2.16, 28 days).
- **F6:** In the rising market, the 2-day rebound after a down day sits in the widest quartile of range against the 20-day average. That quartile gave +3.73 % (t 2.85, 51 days), against -0.33 %, +0.90 % and -0.57 % for the three narrower quartiles. It is positive in both halves: w7–w12 +2.92 % (t 2.78, 37 days), w13–w18 +5.78 % (t 1.51, 14 days). Its low-close days gave +3.17 % (t 2.35, 34 days).
- **F7:** The coin's agitation could not be read here, because the past-year swing percentile is missing inside these windows. So F6 cannot be split into calm and agitated. In the agitated half it overlaps the held rising-agitated rebound books (044-01, 044-02, 039-02.d1). The rising-calm long cell holds only continuation ideas.
- **F8:** The other angles showed nothing that stands out over this many cells. Weekday next-day excess ran from -0.36 % to +0.39 %, all |t| < 1.5. The 5-day return quintiles gave |t| < 1.3 at 2 days in both profiles.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `074-01.b1.g1_rising-wide-down-day-rebound` (from F5, F6, F7): In a rising market, a down day whose high-to-low range is wide compared with the coin's average daily range over the past 20 days is followed by a rise over the next two days, and the wider that range is against the 20-day average, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
