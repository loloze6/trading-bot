---
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3882 USD
---
## Findings
- **F1:** The check failed on Calmar (0.575 against 0.75). The rebuilt book's deepest fall is -48.3 % against a yearly return of +27.8 %, and its worst episode runs from w12 to w16 (456 days), while the coins held fell -51.2 %. The book stays long whenever the 20-day return is positive, so it also buys short rebounds inside long declines.
- **F2:** The idea's effect sits only where the coin's 60-day return is also positive. There, signal cases end +2.56 % above the coin's normal 10-day drift (t 2.43, 295 independent cases), and with the 60-day return negative they end -0.14 % (t -0.11, 123 cases). The condition alone does not earn: grid bars with a positive 60-day return and no signal end -2.31 % (t -1.77, 128 cases). The longer rise is therefore part of the idea's own situation, a range expansion inside a rise, and not a separate effect.
- **F3:** Taking the same positions only while the 60-day return is positive improves the book before costs on the failing measure:
- **F4:** The 100-day average gives the same picture. Signal cases above it end +1.66 % above drift (t 1.87, 369 cases), and those below it end +0.07 % (t 0.05, 113 cases). Bars above it without the signal end -1.15 % (t -0.90, 108 cases), so the condition alone does not earn. The book's mean daily gain is 0.216 % on days with the price above its 50-day average, against 0.017 % below it.
- **F5:** Inside the regime the grading by range is weak and not monotone:
- **F6:** Costs do not explain the failure. Per case the total move is +1.93 %, 10.0 times the 0.19 % a trade costs, and the unusual move is +0.75 % (strength 0.047), 3.9 times that cost. The losses come from being long inside longer declines, not from fees.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise.d1_range-expansion-in-long-rise` (from F1, F2, F3, F6): The wider a coin's daily high-low range is relative to its average range over the past 30 days, while its 20-day return is positive and its 60-day return is also positive, the higher that coin's return over the next 10 days.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise.d2_range-expansion-above-long-average` (from F1, F4, F5): The wider a coin's daily high-low range is relative to its average range over the past 30 days, while its 20-day return is positive and its close is above its 100-day average close, the higher that coin's return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
