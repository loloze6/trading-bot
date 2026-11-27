---
line: 7.g patterns
backtest: 077-03.d1.b1_widest-low-close-next-day-rebound_1d
idea tested: 077-03.d1.b1_widest-low-close-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4369 USD
---
## Findings
- **F1:** The day's own move reverses the next day, and only when the coin is swinging hard. Across all bars of folds B and C, the day's return measured in 30-day return standard deviations is followed by an opposite next-day excess return:
- **F2:** The tested idea's profile is too rare to judge it, and the strongest version of its effect sits outside that profile.
- **F3:** The long side of F2 is already held. In the high-swing tercile with a falling 60-day trend:
- **F4:** The fall after up days in the high-swing tercile is not one coin or one year, though its t over days is weaker than its per-case t.
- **F5:** On the brief's own short side, in choppy, high-swing bars, wide days closing in the top fifth of their range fell -4.16 % the next day (t over days -2.27, 11 days). Narrow ones rose +0.61 % (6 days). Inside the recorded profile, the widest quarter of high closes fell -3.59 % (t -2.19, 13 cases). Choppy agitated short is empty on the profile map, but these case counts are very small.
- **F6:** I looked at many angles, and some patterns did not stand out enough to count.

## Ideas
- `077-03.d1.b1.g1_choppy-agitated-high-close-fade` (from F5, F1, F2): In a choppy, agitated market, a day that closes near its high on a range wide against the coin's 30-day swing is followed by a fall over the next day, larger the wider the day against that swing and the nearer the close sits to the high.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `077-03.d1.b1.g2_agitated-wide-high-close-fade` (from F1, F4, F6): In an agitated market, a day that closes near its high on a range wide against the coin's 30-day swing is followed by a fall over the next day, larger the wider the day and the nearer the close sits to its high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
