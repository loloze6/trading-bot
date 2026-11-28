---
line: 7.g patterns
backtest: 086-01.c1_forceful-turn-day-continues_1d
idea tested: 086-01.c1_forceful-turn-day-continues
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5887 USD
---
## Findings
- **F1:** Inside the rising agitated profile, the day's high-to-low range measured against the coin's 30-day swing predicts the next 3 days. The slope of the unusual 3-day move on this range has t 3.34 over 359 non-overlapping cases. The widest fifth of days is followed by an unusual move of +4.19 % (strength 0.39 of a usual move, t 1.84 with the cases of one day together, 56 days). The other four fifths range from -2.05 % to +1.05 %.
- **F2:** The range effect is absent outside the profile. There the same slope has t 0.15 over 1,117 cases, against t 3.34 inside it, so it belongs to rising agitated markets.
- **F3:** Inside the profile the range effect sits on up days. The slope has t 3.86 over 185 up-day cases against t 0.84 over 174 down-day cases. In the widest fifth, days closing in the upper half of their range are followed by +5.46 % (strength 0.50, t 1.55, 33 days), against +2.52 % for those closing in the lower half.
- **F4:** The range effect does not come from volume or from the prior 5-day run. In a joint least-squares fit the range keeps t 2.74, while volume against its 30-day mean falls to t -1.09 and the 5-day return in usual swings gets t 1.96. On a log scale the range slope still has t 2.83.
- **F5:** The range slope is positive on all four coins (LTC t 2.79, XRP t 1.55, ETH t 0.56, XMR t 0.57). It is also positive in every year with more than 7 cases (2017 t 3.58, 2021 t 1.97, 2018, 2019 and 2020 between t 0.18 and t 1.10).
- **F6:** The tested situation adds nothing on its own. Break-day cases have a mean unusual move of -0.18 % (t -0.28, 245 days). The length of the preceding down run has a slope t of only 1.08 across all in-profile grid bars (483). Up-day size in usual swings has a slope t of 2.24, but its quintiles are not monotone (+2.63 %, +0.11 %, -1.18 %, +2.21 %).
- **F7:** The tested book is mostly the coin's own drift. Over 610 days with a position it earns +0.047 % a day, its return correlates 0.68 with the coin's, and only 37 % of those days are positive. The total move per case (+0.22 %) is 0.8 times the 0.26 % cost of a trade, while the widest-range fifth in F1 moves about 16 times that cost.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `086-01.c1.g1_wide-up-day-continues` (from F1, F2, F3, F4, F5, F7): In a rising, agitated market, after an up day whose high-to-low range is wide against the coin's usual daily swing over the past 30 days, the coin rises over the next 3 days, and the wider that range, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
