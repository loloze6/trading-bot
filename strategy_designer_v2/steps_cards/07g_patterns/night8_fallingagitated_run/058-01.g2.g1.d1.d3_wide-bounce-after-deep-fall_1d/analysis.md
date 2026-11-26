---
line: 7.g patterns
backtest: 058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d
idea tested: 058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4672 USD
---
## Findings
- **F1:** In the falling, agitated profile, the next day follows today's return against its 30-day swing in reverse, in order across the quintiles: the deepest-fall fifth is followed by an excess +2.18 % (t 5.08, 221 cases), the next by +1.02 % (t 2.96), the middle by −0.25 %, and the two largest-rise fifths by −0.77 % (t −2.01) and −0.81 % (t −1.86). Outside the profile the same split is nearly flat: +0.37 % (t 2.29) for the deepest falls, and −0.11 % to −0.18 % with |t| under 1.4 for the rest.
- **F2:** In the profile, where the day closes in its own range orders the next day the same way: closes in the lowest fifth are followed by +2.02 % (t 4.87, 260 cases), and closes in the fourth and top fifths by −0.96 % (t −2.75) and −0.58 % (t −1.71). The long half of F1 and F2, the low-close and deep-fall rebound in falling agitated markets, is already held by 12 strategies in the map. The short half sits in the map's empty cell, falling agitated short.
- **F3:** The days the tested forecast shorts most, the widest-range days in the profile, are followed by a rebound, not a fall: the top range fifth gains +1.53 % next day (t 2.78, 221 cases), against −0.50 % to +0.25 % (|t| under 1.3) for the other fifths. Among up days in the profile, the next-day give-back shrinks as the up day grows: 1.16 %, 0.98 % and 0.43 % short excess by tercile of the day's rise against swing (t 1.65, 1.84, 0.66; about 180 cases each). The tested size grading ("wider bounce, larger fall") points against the bars.
- **F4:** The brief's own form, a 3-day rise in the profile followed by a give-back over the next 3 days, shows only in the largest third of rises. On non-overlapping 3-day steps the three terciles give a short excess of −0.49 %, −0.78 % and +3.21 % (the last with t 1.82, 53 cases, clustered by day). The rank correlation of rise size with the next 3 days is −0.18 over 157 rises, but only 20 of those fall in w7–w12, so the pattern rests on w13–w18.
- **F5:** The tested book's shorts earned before costs on every coin (mean position gain per active bar 0.09 % to 0.56 %, t 0.26 to 1.81, 47 to 83 bars per coin), with XRP the weakest (−0.15 % short excess). The book's mean daily return stayed between −0.02 % and +0.07 % in every window from w7 to w18. Its small yearly return (+3.3 %) comes from being in the market on only 8 % of coin-days, not from losses.
- **F6:** Outside the profile the opposite holds over 3 days: the largest-rise fifth of 3-day moves is followed by a further +1.43 % over the next 3 days (t 3.02, 380 cases, rank correlation +0.08). This continuation outside falling agitated markets repeats the rising-market and breakout continuation books the map already holds, so it is not a discovery. Weekday effects (all days: Wednesday −0.50 % t −2.78, Thursday +0.41 % t 2.80) were one of many angles and repeat the held late-week idea 045-01.

## Ideas
- `058-01.g2.g1.d1.d3.g1_high-close-next-day-giveback` (from F2, F1, F3, F5): In a falling, agitated market, a day that closes in the upper part of its high-to-low range is followed by a fall over the next day, and the nearer its close sits to its high, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
