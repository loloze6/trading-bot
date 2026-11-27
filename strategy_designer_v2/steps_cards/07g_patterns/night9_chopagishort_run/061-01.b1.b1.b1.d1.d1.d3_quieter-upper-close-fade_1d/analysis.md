---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4452 USD
---
## Findings
- **F1:** The book's gain sits almost entirely in one window: summed daily book returns are +0.2439 over 1,449 days in folds B and C, of which w16 alone gives +0.2337. The other eleven windows sum between -0.0152 and +0.0160. The 10 best days sum to +0.4086, more than the whole total.
- **F2:** In choppy markets (60-day return within ±10 %), the coin's 5-day unusual move follows its own volatility-scaled 5-day return, correlation 0.444 over 152 grid cases. The lowest quartile of that scaled return is followed by a further unusual fall of -9.42 % over 5 days (t -2.32 with cases of one day together, 25 days). The top quartile is followed by +2.84 %. In falling and rising markets the same quartiles only reach -1.78 % and -0.87 % (t -0.69 and -0.48).
- **F3:** In choppy markets, the fall after a negative 5-day return is larger when the last 20 days' swings are high against the last 60 days'. With the 20/60 swing ratio above its median, the unusual 5-day move is -8.46 % (t -2.25, 29 days, 42 cases); below it, -1.34 % (t -0.70). Over all choppy cases the correlation of the 5-day unusual move with that ratio is -0.217. This is the opposite of the tested idea's "quieter swings, larger fall" grading.
- **F4:** In choppy markets, a close in the top quarter of the day's range does not fade. It is followed by +2.68 % unusual over 5 days (t 1.22, 48 cases), and by +5.29 % (t 2.06, 35 cases) when the 5-day return was positive. A close in the bottom quarter is followed by -4.75 % (t -3.59, 23 cases). The short's edge comes from the prior fall, not from the high close.
- **F5:** How long the book's trades lasted splits their result. The 26 trades closed after 1 day lost -4.83 % on average. The 57 trades held the full 5 days gained +3.95 %, and the 12 held 7 days gained +6.20 %. Trades in the top third of |entry forecast| gained +5.72 %, against +1.07 % and -1.69 % for the lower two thirds.
- **F6:** The edge fades across the years in choppy markets: unusual 5-day move -7.33 % in 2018 (t -2.61) and -2.17 % in 2019 (t -2.16), then -2.47 % in 2020 (t -0.48) and +1.66 % in 2021 (t 0.43). Trades entered in 2021 lost -3.01 % on average (44 trades).

## Ideas
- `061-01.b1.b1.b1.d1.d1.d3.g1_choppy-scaled-fall-continuation` (from F2, F4): In a choppy market, a coin whose 5-day return is negative keeps falling over the next five days, and the larger that 5-day fall in units of its last 20 days' daily swing, the larger the further fall.
- `061-01.b1.b1.b1.d1.d1.d3.g2_widening-swings-fall-continuation` (from F3, F2): In a choppy market, after a negative 5-day return, a coin falls further over the next five days the more its last 20 days' daily swings exceed its last 60 days' swings.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
