---
line: 7.g patterns
backtest: 058-02.b1.b2.b1.b2_calm-market-range-position_1d
idea tested: 058-02.b1.b2.b1.b2_calm-market-range-position
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3958 USD
---
## Findings
- **F1:** In calm bars the 5-day excess return rises steadily with the close's place in its 20-day high-low range. The bottom fifth gives −2.41 % (t −3.14, 163 cases), the low fifth −2.38 % (t −3.78), the middle −0.17 %, the high fifth +0.68 % and the top fifth +4.40 % (t 4.40, 177 cases). In agitated bars the same sort shows no reliable step: the top gives +1.78 % (t 1.16) and the bottom +0.28 % (t 0.18). This is continuation, the opposite of the brief's reversion.
- **F2:** The continuation is concentrated in the coin's quietest bars.
- **F3:** The range position carries the effect, not the plain 5-day move. In a joint regression on calm bars, the range position's slope is +2.40 % per standard deviation (day-clustered t 2.29). The scaled 5-day move's slope is +1.16 % (t 0.94).
- **F4:** Most of the book's gain comes from longs.
- **F5:** Closes low in the range keep falling when the trend is down.
- **F6:** In a rising 60-day trend, calm closes high in the range give +5.31 % (day-clustered t 2.93, 94 cases on 37 days). Choppy calm high closes give +6.97 % (t 1.58, only 28 cases). This rising-calm long side is already held in the map (034-01.b1, 035-01.b1), so it is not a discovery.
- **F7:** High-minus-low range position in calm bars is positive in 9 of the 11 windows that can be measured, from +0.79 % to +14.47 %. Two windows are negative: w7 (−2.78 %) and w12 (−0.54 %). The calm correlation between range position and the 5-day excess return is positive in every year (2018 0.06, 2019 0.20, 2020 0.19, 2021 0.17) and for every coin (0.05 to 0.35).

## Ideas
- `058-02.b1.b2.b1.b2.g1_falling-calm-range-low-continuation` (from F5, F4, F1): In a falling, calm market, the lower a coin's close sits within its 20-day high-low range, the larger its fall over the next 5 days.
- `058-02.b1.b2.b1.b2.g2_quietness-scaled-range-continuation` (from F2, F1, F3, F7): The less a coin has been swinging over the last 20 days compared with its usual swing, the larger its move over the next 5 days in the direction of its close's place in its 20-day high-low range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
