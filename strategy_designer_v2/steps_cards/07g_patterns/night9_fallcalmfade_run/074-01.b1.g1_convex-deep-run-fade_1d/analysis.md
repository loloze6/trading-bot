---
line: 7.g patterns
backtest: 074-01.b1.g1_convex-deep-run-fade_1d
idea tested: 074-01.b1.g1_convex-deep-run-fade
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5146 USD
---
## Findings
- **F1:** The fade after a run-breaking up day lives in falling markets only. There the next day's excess return is −0.97 % (t −3.33, 912 cases on 349 days). In choppy markets it is −0.60 % (t −1.39, 183 cases on 120 days). In rising markets it is +0.36 % (t 0.98, 447 cases on 179 days). The tested idea's theory and its brief already say this.
- **F2:** The fade belongs to the run break, not to the up day. In falling markets, small up days of 0 to 1 usual swing that end a run are followed by −1.02 % (t −2.94, 279 days). The same up days without a prior down run are followed by +0.09 % (t 0.25, 209 days). The idea already holds this.
- **F3:** Within falling markets, calm and agitated fade alike: −0.76 % (t −2.62, 217 days) against −1.16 % (t −2.53, 194 days). The effect needs no agitation split, which agrees with the brief.
- **F4:** By depth quartile in falling markets, the deepest quartile fades most: −2.00 % (t −5.76, 202 cases) against −0.82 %, −0.18 % and −1.00 % for the other three. The growth is not steady across quartiles, but it supports the convex sizing the idea already uses.
- **F5:** Run-breaking up days in falling markets fade on Wednesday to Friday and Sunday: −1.74 % (t −4.62, 207 days). They do not fade on Monday, Tuesday or Saturday: +0.19 % (t 0.47, 142 days). This is a weekday split found after many groupings. It has no graded form and no reason given, so it does not count as a finding to build on.
- **F6:** After a fall of more than 2 usual swings, the next day rebounds. Outside falling markets the rebound is +2.26 % (t 3.89, 83 cases). In falling agitated markets it is +4.96 % (t 1.90, 31 cases on 15 days). This repeats the long rebound ideas the profile map already holds in many cells, so it is not a discovery.
- **F7:** In choppy markets, the longest runs (3 to 4 down days) and the deepest quartile fade by −2.21 % (t −1.33, 25 days) and −1.40 % (t −1.04, 42 days). Neither can be told from chance, so the empty choppy agitated short cell gets no support here.

## Ideas
- No ideas: Every pattern that stands out repeats the tested idea (F1 to F4, already in the map as 074-01.b1.g1, falling short) or long rebounds the map already holds (F6). What remains is an ungraded weekday split (F5) or choppy-market fades too weak to tell from chance (F7), after looking at run length, depth, up-day size, close position, agitation, trend, weekday, window and large moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
