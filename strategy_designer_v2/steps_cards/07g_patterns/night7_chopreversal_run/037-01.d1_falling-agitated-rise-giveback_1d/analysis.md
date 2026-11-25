---
line: 7.g patterns
backtest: 037-01.d1_falling-agitated-rise-giveback_1d
idea tested: 037-01.d1_falling-agitated-rise-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3792 USD
---
## Findings
- **F1:** In the falling agitated profile (bars not sent to chop), the next day's return beyond drift falls steadily as the day's close moves up its own high-low range: +2.33 % (t 5.22, n 201) after closes in the bottom fifth, then +0.38 % (t 1.26), +0.11 %, -0.71 % (t -1.84) and -0.60 % (t -1.55, n 203) in the top fifth. Out of the profile the same ladder is flat, from +0.20 % (t 1.13, n 831) to -0.32 % (t -2.28, n 1324). These t's are not day-pooled, but 5.2 stands well clear of the roughly 40 cells looked at.
- **F2:** Within the profile, next-day returns beyond drift fall in order across the day's own scaled move. After falls: +6.02 % (z ≤ -2, t 3.47, n 26), +1.94 % (t 2.90), +1.21 % (t 3.40), +0.79 % (t 2.18). After rises: -0.89 % (z in (0, 0.5], t -2.74, n 292) and -1.27 % ((0.5, 1], t -2.20, n 141). Beyond one usual swing the give-back is gone: -0.18 % (t -0.34) and -0.56 % (t -0.38). The tested idea is the up half of a wider same-day-reversal ladder.
- **F3:** The give-back of an ordinary rise (z in (0, 1]) grows with the coin's own 30-day swing level, inside and outside the profile. In the highest swing tercile it is -1.11 % (t -3.20, n 346) in the profile and -0.54 % (t -2.30, n 549) outside it. In the lowest tercile it is +0.02 % (t 0.16, n 848) outside the profile, so the effect follows agitation rather than the falling trend alone.
- **F4:** The give-back lasts one day only: over two days (grid 2) the in-profile rises show -0.16 % (t -0.25) and -0.82 % (t -0.61).
- **F5:** It is uneven across coins and years:
- **F6:** The tested book's total move per case (+0.43 %) is only 2.2 times the 0.19 % trade cost. The low-close rebound in F1 (+2.33 %) is about 12 times that cost, a move large enough to pay.

## Ideas
- `037-01.d1.g2_agitation-scaled-ordinary-rise-giveback` (from F3, F2, F4): In an agitated market, a coin's one-day rise that stays within its 30-day daily swing is given back over the next day. The give-back is larger the larger the rise within that swing and the more the coin's 30-day swing exceeds its past year's usual swing.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `037-01.d1.g1_low-close-next-day-rebound` (from F1, F6): In a falling, agitated market, the lower a coin closes within its day's high-low range, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
