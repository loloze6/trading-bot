---
line: 7.g patterns
backtest: 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d
idea tested: 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5225 USD
---
## Findings
- **F1:** In calm markets the range-edge effect grows with the horizon. On a 5-day non-overlapping grid, closes in the top fifth of the 20-day range are followed by +4.40 % above the coin's drift (t 3.10, 177 cases, 69 days), and closes in the two bottom fifths by -2.41 % (t -1.91) and -2.38 % (t -2.38). At 2 days the top fifth gives only +1.20 % (t 2.21) and the bottom fifth -0.67 % (t -1.23).
- **F2:** The profile in the brief, choppy calm, carries the strongest version of this continuation at longer horizons. The signed move above drift, in the direction of the close's side of mid-range, is:
- **F3:** In agitated markets the range position predicts nothing graded at any horizon tested. At 5 days the fifths run +0.28, -0.54, -0.77, +0.95, +1.78 % with every |t| below 1, and the signed move is -0.45 % in falling agitated and +1.97 % (t 1.26) in rising agitated.
- **F4:** The book's profit comes from long, trend-riding holds rather than the 2-day bet:
- **F5:** The book earns on the market's extreme days in both directions. On the market's worst-fifth days it makes +0.30 % and on its best-fifth days +0.32 %, against -0.10 %, -0.01 % and +0.08 % on the middle three fifths: the convex profile of a continuation book.
- **F6:** No other angle stood out against the number looked at:

## Ideas
- `058-02.b1.b2.b1.b2.b2.e1.g1_choppy-calm-edge-continuation` (from F1, F2, F4, F5): In a choppy, calm market, the nearer a coin's close sits to the top of its 20-day high-low range, the larger its rise over the next 10 days, and the nearer to the bottom, the larger its fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
