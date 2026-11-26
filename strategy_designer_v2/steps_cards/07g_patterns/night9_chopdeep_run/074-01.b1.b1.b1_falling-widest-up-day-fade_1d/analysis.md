---
line: 7.g patterns
backtest: 074-01.b1.b1.b1_falling-widest-up-day-fade_1d
idea tested: 074-01.b1.b1.b1_falling-widest-up-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6172 USD
---
## Findings
- **F1:** In a falling market, an up day that closes in the top fifth of its range is followed by a weaker next day the wider its range against its 20-day mean. The next-day unusual move steps from +0.08 % (range multiple ≤0.8, 325 cases, 172 days, t 0.16) to −0.79 % (0.8–1.2, t −0.98), −0.72 % (1.2–1.7, t −0.93) and −1.96 % (>1.7, 58 cases, 32 days, t −2.27). The widest bucket is about nine times the 0.22 % trade cost.
- **F2:** The grading of F1 points the same way in both halves of the explored windows. On up days closing above 70 % of their range, the widest bucket gives −2.43 % (w7–w12, t −2.35) and −1.85 % (w13–w18, t −1.44); the narrowest gives −0.56 % and +0.49 %. The rank correlation of range multiple with the next-day move over these 736 days is −0.145.
- **F3:** Without a close condition, the width grading the tested idea claims is absent. Falling-market up days give next-day unusual moves of −0.86 % (0.6–0.8, t −2.67), −0.45 % (0.8–1.0), −0.91 % (1.0–1.3), −0.42 % (1.3–1.7) and −0.97 % (>1.7, t −1.26). The test's t of 1.18 comes from this mix of wide days closing anywhere.
- **F4:** Across all falling-market up days the next day is weaker than usual: −0.54 % (1,883 cases, 520 days, t −2.15). The fade grows as the 60-day fall gets shallower: −0.40 % (60-day return below −50 %, t −0.43), −0.19 % (−50 to −35 %), −0.61 % (−35 to −25 %, t −1.81), −0.71 % (−25 to −15 %, t −2.00) and −1.06 % (−15 to −10 %, 169 cases, 123 days, t −2.85).
- **F5:** The shallow-fall fade of F4 (60-day return from −25 % to −10 %) has the same sign in both halves: −1.14 % in w7–w12 (t −2.84) and −0.51 % in w13–w18 (t −1.10). Up days in rising coins (60-day return above +10 %) do not fade: +0.57 %, +0.19 % and +0.06 % next day.
- **F6:** Two days after a falling-market up day that closes high on a range above 1.7 times its 20-day mean, the coin rises: +2.19 % (65 cases, 30 days, t 2.52). The next-day fade of F1 is given back, not the start of a further fall.
- **F7:** Wide days closing in the bottom fifth of their range rebound the next day: +1.62 % in falling markets (t 1.64) and +1.49 % elsewhere (t 2.48). Wide down days of 1.3–1.7 times the mean range in falling markets give +1.36 % (t 2.21). These are low-close and fall rebounds the profile map already holds in the agitated and falling agitated cells, so they are not a discovery.
- **F8:** No weekday shows a next-day move with |t| above 1.66 in either profile, and the scaled 5-day return shows no grading in falling markets (all six buckets within |t| 1.56), so those angles give nothing.

## Ideas
- `074-01.b1.b1.b1.g1_falling-wide-high-close-fade` (from F1, F2, F3, F6): In a falling market, an up day that closes near its high on a high-to-low range wide against the coin's average daily range over the past 20 days is followed by a fall over the next day, the wider that range against its 20-day average, the larger the next day's fall.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `074-01.b1.b1.b1.g2_shallow-downtrend-rally-fade` (from F4, F5): In a falling market, an up day is followed by a fall over the next day, the smaller the coin's 60-day fall, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
