---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded_1d
idea tested: 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6407 USD
---
## Findings
- **F1:** In a choppy market (60-day return between -10 % and +10 %), the 20-day return scaled by its usual 20-day swing predicts the next 5 days' unusual move in the same direction, with slope 0.060 per unit and t 3.71 (152 non-overlapping cases on 68 days, cases of one day together). In falling markets the slope is only 0.009 (t 0.79) and in rising markets 0.014 (t 1.34), so the continuation lives in the choppy market.
- **F2:** The effect in F1 is graded at both ends inside the choppy market. Its lowest scaled 20-day quintile is followed by an unusual 5-day move of -12.5 % (t -2.30, 25 cases, 15 days), and its highest by +8.1 % (t 1.44, 20 cases, 10 days), with the middle quintiles in order: -2.5 %, -1.8 %, +1.8 %.
- **F3:** The same continuation holds on a shorter past period in the choppy market: the 5-day return scaled by its usual swing has slope 0.066 on the next 5 days' unusual move (t 2.71, 152 cases, 68 days).
- **F4:** The choppy continuation does not depend on agitation, so it is no agitated-only effect. Measured with a proxy of 30-day against 90-day swing, its slope is 0.054 (t 3.87, 103 cases, 50 days) in the calmer bars and 0.069 (t 1.25, 49 cases, 38 days) in the more agitated ones.
- **F5:** Among choppy-market high closes (close in the top quarter of the day's range), the next 5 days follow the 5-day return's sign rather than the high close. After a negative 5-day return the unusual move is -4.3 % (t -1.22, 13 cases); after a positive one it is +5.3 % (t 1.40, 35 cases). This suggests the tested idea's short gain comes from continuation of the recent fall, not from fading the high close.
- **F6:** The book's profit is carried by a few days and a few coins.
- **F7:** Not distinct from chance, so none of these becomes an idea:

## Ideas
- `061-01.b1.b1.b1.d1.d2.g1_choppy-market-twenty-day-continuation` (from F1, F2, F4, F5): In a choppy market, a coin's 20-day return continues over the next five days. The further the coin has moved over those 20 days, measured against its usual 20-day swing, the larger the move in the same direction, up after a rise and down after a fall.
- `061-01.b1.b1.b1.d1.d2.g2_choppy-market-five-day-continuation` (from F3, F5): In a choppy market, a coin's 5-day return continues over the next five days. The larger that 5-day move against its usual 5-day swing, the larger the move in the same direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
