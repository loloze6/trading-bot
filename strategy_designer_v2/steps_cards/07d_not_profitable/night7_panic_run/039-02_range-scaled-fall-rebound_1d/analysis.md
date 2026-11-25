---
line: 7.d confirmed, not profitable
backtest: 039-02_range-scaled-fall-rebound_1d
idea tested: 039-02_range-scaled-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4040 USD
---
## Findings
- **F1:** The Calmar failure comes from one fall. The book's deepest fall was -27.9 % over 120 days in windows w8 to w9 (w9 alone lost 18.8 %, with its worst day at -17.7 %). The book moved with the coins there (correlation 0.72; the book summed -29.7 % against -43.3 % for holding), and on all 30 of the book's worst days the coins fell too (book -5.8 %, coins -10.2 % on average).
- **F2:** The effect lives only where the coin's recent swing has risen. On down days in the top two-fifths of the scaled fall:
- **F3:** The rising-swing condition is not an effect of its own. Without the idea's signal, on the same horizon, bars with that condition earn nothing or lose:
- **F4:** Inside the rising-swing state the rebound stays graded. By quintile of the scaled fall, the next-day excess return runs from -0.16 % and -0.41 % in the two smallest to +1.51 % and +1.95 % in the two largest. In the calm state no quintile is clearly positive (from -0.52 % to +0.36 %).
- **F5:** The losses in the deepest fall came from the calm-swing bars. In windows w8 to w9 the position's summed gains were:
- **F6:** In an approximate rebuild with costs, the rising-swing condition repairs the failing measure. Holding the book only while the 10-day swing exceeds the 60-day swing:
- **F7:** Most of the book's gain comes from the large falls. The two top quintiles of the scaled fall carry 93 % of the position gain on down days, with mean next-day excess returns of +0.57 % and +0.87 %, against +0.15 %, +0.01 % and +0.03 % in the lower three.

## Ideas
- `039-02.d1_rising-swing-scaled-fall-rebound` (from F1, F2, F3, F4, F5, F6, F7): After a down day, a coin rises over the next day, more so the larger that day's fall measured in units of its 30-day average daily high-to-low range, only while its daily swing over the last 10 days is larger than its swing over the last 60 days, the larger the fall the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
