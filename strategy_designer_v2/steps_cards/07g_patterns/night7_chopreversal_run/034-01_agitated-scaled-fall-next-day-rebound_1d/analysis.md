---
line: 7.g patterns
backtest: 034-01_agitated-scaled-fall-next-day-rebound_1d
idea tested: 034-01_agitated-scaled-fall-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4643 USD
---
## Findings
- **F1:** In agitated markets the next-day rebound after a one-day fall is convex, not linear. Regressing the next-day excess return on the fall (in 30-day swings) and its square, falls only, t clustered by day: fall² +0.0124 (t 5.94), fall −0.0223 (t −2.76).
- **F2:** Only the deepest agitated falls carry that rebound. Next-day excess return, day-clustered:
- **F3:** The rebound after deep agitated falls also shows over two days and after three-day falls:
- **F4:** Contrary to the brief, calm markets also show a graded next-day rebound after falls. Among calm falls the linear slope is +0.0150 (t 2.64, day-clustered); calm falls of 1 to 1.5 swings return +0.77 % (t 1.94, 138 days). By year this is uneven: 2018 +0.16 %, 2019 +0.23 %, 2020 +1.66 % (t 3.14), 2021 +1.12 %.
- **F5:** In agitated markets, ordinary days within one usual swing are partly reversed the next day, and in calm markets they are not.
- **F6:** Rebounds after falls closing in the lowest quarter of their range look stronger, but not reliably once cases of one day are taken together. Falls beyond 1.5 swings closing low: agitated +2.52 % (t 2.06, 51 days) against +2.05 % (t 1.65) for the others; calm +0.82 % (t 1.23).
- **F7:** Falls beyond one swing made on a Thursday rebound +2.70 % the next day (t 2.66, 41 days), against +0.32 % to +0.45 % on other weekdays (t ≤ 1.1). This is one of seven weekdays checked and no single year reaches t 2, so it is not used for an idea.
- **F8:** The book earned +0.045 % a day over 1449 days, with 1 % tails of −2.05 % and +2.80 %. Window means range from −0.011 % to +0.179 %, so a few windows (w11, w14, w18) carry most of the gain, consistent with a profit concentrated in rare deep-fall days (F2).

## Ideas
- `034-01.g1_agitated-extreme-fall-convex-rebound` (from F1, F2, F8): In an agitated market, a coin's next-day rise after a one-day fall grows faster than the fall itself, measured against its 30-day daily swing. A fall of a few usual swings is followed by a rise many times larger than a fall of about one swing, which is followed by almost none.
- `034-01.g2_agitated-deep-fall-two-day-rebound` (from F1, F3): In an agitated market, the larger a coin's one-day fall against its 30-day daily swing, the larger its rise over the next two days, growing faster than the fall.
- `034-01.g3_agitated-three-day-fall-rebound` (from F3, F1): In an agitated market, the larger a coin's three-day fall measured against its 30-day daily swing, the larger its rise over the next day, growing faster than the fall.
- `034-01.g4_scaled-fall-rebound-every-market` (from F4, F2): The larger a coin's one-day fall measured against its 30-day daily swing, the larger its rise over the next day, in calm as in agitated markets.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `034-01.g5_agitated-ordinary-rise-gives-back` (from F5): In an agitated market, a coin's ordinary one-day rise is partly given back the next day, and the larger the rise within its usual daily swing, the larger the give-back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
