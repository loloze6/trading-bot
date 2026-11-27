---
line: 7.g patterns
backtest: 077-03.d1_choppy-agitated-low-close-rebound_1d
idea tested: 077-03.d1_choppy-agitated-low-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4483 USD
---
## Findings
- **F1:** Across all bars of folds B and C, a wide day closing near its low (top width tercile, close in the bottom fifth of the range) was followed by a next-day excess return of +1.346 % (t 5.58, n 545). The same close on a mid-width day gave −0.168 % (t −0.62, n 373), and on a narrow day −0.004 % (t −0.02, n 351), so the rebound grows with the day's width against the 30-day swing.
- **F2:** The wide-low-close rebound was not specific to the choppy agitated profile. For the top fifth of the low-close signal (distance below mid × width), the next-day excess return was:
- **F3:** In a rising market (60-day return above +10 %), a down day of 1 to 2 of the coin's 30-day swings was followed by a rise. The excess return was:
- **F4:** The tested idea's effect, inside its own profile, could not be told from chance. In-profile low closes rose +1.298 % the next day (t 2.57, only 68 bars), but the step-5 size was +0.03 % unusual move per case (0.006 of a usual move, t 0.15, 465 days). The total move per case was +0.17 %, against a trade cost of 0.22 %, so it was 0.7 times the cost. The book held a position on 5 % of coin-days, for a yearly return of +1.6 % and a Calmar of 0.25.
- **F5:** Up moves in falling markets faded over 3 days but did not stand out once same-day cases were taken together. A 1-to-2-swing up day gave −3.006 % (t −2.92, n 62) without clustering, but in falling agitated it was −3.113 % with t −1.50 over 19 days, and 2021 reversed to +2.848 %. The map's falling agitated cell already holds a next-day reversal and a close-height fade, so I propose no idea from it.
- **F6:** The weekday pattern does not count as a finding given the number of angles examined. Wednesday's next-day excess was −0.445 % (t −2.60) and Friday's +0.371 % (t 2.85), but only 2 of 7 weekdays reached |t| > 2, and the in-profile weekday readings did not line up with these.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `077-03.d1.g1_rising-calm-pullback-rebound` (from F3): In a rising, calm market, a day that falls by more than usual against the coin's 30-day swing is followed by a rise over the next three days, larger the larger that day's fall in units of the swing.
- `077-03.d1.g2_rising-calm-low-close-rebound` (from F1, F2): In a rising, calm market, a day closing below the middle of its range is followed by a rise over the next day, larger the further the close sits below the middle multiplied by the day's range against its 30-day swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
