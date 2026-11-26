---
line: 7.d confirmed, not profitable
backtest: 067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues_1d
idea tested: 067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4227 USD
---
## Findings
- **F1:** Inside the choppy regime, the short signal (forecast at or below -2, one case per 10-day grid cell) pays only when the coin is agitated. On agitated cases the 10-day short earns a total +10.59 % (t 3.72, n 19; unusual +12.36 %). On calm cases it earns -0.34 % (t -0.12, n 44; unusual +2.59 %). The book spends most of its cases in the calm state, where the effect is about zero before costs. Agitation here is the coin's 30-day swing above its median over all its explored windows, which stands in for the profile's past-year median.
- **F2:** Agitation is not an effect of its own. Shorting every agitated 10-day grid cell, signal or not, earns -2.54 % (t -2.58, n 444). Shorting agitated choppy falls without the signal earns -1.68 % (t -0.37, n 13). So the gain on agitated cases comes from the idea's own month-slide signal. This fits the brief's theory: a coin that has just turned in a flat two-month market is the case where the newly repositioned crowd is still acting.
- **F3:** The cube puts the size on the wrong slides. Choppy cells with a 30-day fall of 15 to 25 % continue down by +8.57 % short over 10 days (t 4.13, n 32). Falls deeper than 25 % give -1.17 % (t -0.26, n 22). Falls of 8 to 15 % give -0.94 % (n 15). Among signal cases, the middle forecast third earns +6.88 % (t 1.96), against +1.40 % for the largest third and +0.89 % for the smallest.
- **F4:** The book's 424 short trades lose 2.36 % gross and 2.46 % net each, with 38 % winners and 10.8 days held. Every entry-forecast third loses (small -3.05 %, mid -1.21 %, large -3.12 % net). The trade loss is therefore mostly a timing loss, not a fee loss. The fee is 0.22 % against a -2.36 % gross loss. Many trades enter on small forecasts after the signal, and those miss the move the grid cases capture (+2.96 % on average over the 63 signal cases).
- **F5:** Shorting fights the coins' rise. Over all grid cells, a 10-day short earns -2.71 % (t -2.99, n 756) in calm cells and -2.54 % in agitated cells. The worst windows of the book are those where the coins rose: w10 had a coin mean of +55 bp a day and the book -9.2 bp; w11 had +193 bp and the book -5.0 bp. In those two windows the signal's shorts lost 27.5 % each over 10 days (n 3 each). This is what sinks the Sharpe against holding and the run with one window left out.

## Ideas
- `067-01.b1.g1.b1.d1.d1_agitated-chop-slide-continues` (from F1, F2, F5): In a choppy, agitated market, the larger a coin's plain percentage fall over the past 30 days, the more it keeps falling over the next 10 days.
- `067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues` (from F3, F4): In a choppy market, the larger a coin's plain percentage fall over the past 30 days, the more it keeps falling over the next 10 days, in proportion to the depth of the slide rather than steeply, so that moderate and deep slides both carry the move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
