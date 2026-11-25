---
line: 7.g patterns
backtest: 058-01.b2.b1_quiet-calm-fall-more-coins_1d
idea tested: 058-01.b2.b1_quiet-calm-fall-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4423 USD
---
## Findings
- **F1:** The 30-day return carries on over the next 5 days only in choppy markets (60-day return between -10 % and +10 %). Across its 30-day-return quintiles, the drift-adjusted 5-day move rises in order: -14.96 % (13 cases, 9 days, t -2.06), -6.13 % (34 cases, 25 days, t -3.02), -1.56 % (58 cases, t -1.21), +4.35 % (37 cases, t 1.88), +6.96 % (9 cases, t 0.97). Each of these moves is far larger than the 0.22 % a trade costs.
- **F2:** In falling markets (60-day return below -10 %) the same quintiles are not graded. The deepest 30-day falls (bottom quintile, 181 cases) are followed by +0.74 % (t 0.39), while the next quintile is followed by -3.52 % (130 cases, 55 days, t -2.76). In the tested regime, the bottom quartile gives +0.21 % and the third gives -4.58 % (t -3.80). In this profile, "the deeper the fall, the more it continues" does not hold.
- **F3:** The brief's volume dimension shows no grading. The forecast's slope has t 0.46 (931 grid bars). The 30-to-90-day volume ratio quintiles are not monotone: from +1.39 % at the quietest to -0.57 % at the heaviest, with the most negative value, -2.07 % (t -2.83), in the middle. Today's volume against its 30-day mean is not graded either: -0.90 %, +0.27 %, -0.35 %, -0.30 %, +0.78 %.
- **F4:** A close at the top of the 30-day range (top 10 % of it) is followed by +3.23 % over 5 days (252 cases, 84 days, t 2.38), and by +4.65 % in rising markets (t 2.24). This repeats the nearness-to-high ideas the map already holds (034-01.b1, 035-01.b1), so it is not a discovery.
- **F5:** The book earned almost nothing. Its trades lose on most coins: mean net P/L is -4.93 % on XRP, -4.22 % on ZEC and -2.44 % on BTC, and only ETH (+6.86 %) and LTC/XMR are positive. Its window means range from -0.096 % to +0.100 % a day. Its short sits in falling markets, where F2 shows the deepest falls do not continue.
- **F6:** The worst one-day falls (bottom decile) are followed by a +0.97 % next-day rebound (727 cases, 218 days, t 2.24). The many falling-agitated rebound ideas in the map already hold this. Wednesday's -0.75 % (t -1.67) is not distinguishable from chance.

## Ideas
- `058-01.b2.b1.g1_choppy-market-decline-continues` (from F1, F2, F3): In a choppy market, the more a coin has fallen over its last 30 days, the more it keeps falling over the next 5 days.
- `058-01.b2.b1.g2_steady-calm-fall-continues` (from F2, F5): In a falling, calm market, the more a coin's 30-day return falls short of its 60-day return's pace, the more it keeps falling over the next 5 days. A decline that is steady relative to the longer fall carries on more than one already stretched far below it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
