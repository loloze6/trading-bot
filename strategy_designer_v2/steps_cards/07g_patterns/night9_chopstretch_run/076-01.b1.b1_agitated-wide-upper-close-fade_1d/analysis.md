---
line: 7.g patterns
backtest: 076-01.b1.b1_agitated-wide-upper-close-fade_1d
idea tested: 076-01.b1.b1_agitated-wide-upper-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6180 USD
---
## Findings
- **F1:** The tested situation does not fade in agitated markets as a whole: wide (top range-multiple quartile), high-closing (top fifth of the range) agitated days move only -0.41 % the next day against the coin's drift (t -0.70, 223 cases, 137 days). The top fifth of the range-multiple × close-height score moves -0.43 % (t -1.03, 714 cases, 359 days), well inside chance.
- **F2:** Split by the 60-day trend, the fade lives only in falling agitated markets. There the next-day unusual move falls steadily across the quartiles of range multiple × close height: +1.88 % (t 2.23, 209 cases, 82 days), +0.26 % (t 0.53), -0.72 % (t -1.15), -0.94 % (t -1.52, 209 cases, 92 days). In rising agitated markets the quartiles show no order (-0.28, +0.63, -0.36, +0.15 %, top quartile t 0.23).
- **F3:** The top quartile of that score in falling agitated markets is negative in every one of the 7 windows with at least 6 cases, from -0.26 % (w16) to -2.74 % (w15). The strong up days there (daily return over the 20-day swing above its 60th percentile) are negative in all 7 windows with cases, -0.02 % to -3.05 %.
- **F4:** The book's own shorts follow the same split. Bars it held short in falling markets were followed by a next-day unusual move of -1.94 % (t -2.22, 99 cases, 47 days), a gain for the short. Bars held short in rising markets gave -0.08 % (t -0.10, 193 cases, 111 days), so the rising-market half of its positions carried nothing.
- **F5:** Within falling agitated markets, the grading by the up day's size alone is weak. Among up days the correlation of the return-over-swing with the next-day unusual move is -0.06 (408 cases), and its quartiles sit flat at -0.86, -1.38, -1.19 and -1.30 %. The grading in F2 comes from the range-width × close-height product, not from the size of the rise.
- **F6:** Wide days closing low rebound in agitated markets: +2.51 % (t 2.52, 144 cases) for the widest quartile closing in the bottom fifth, and +1.16 % (t 2.64, 714 cases, 289 days) for the top fifth of (1 − close height) × range multiple. The profile map already holds this pattern (039-02, 044-01, 045-01), so it is not a discovery.
- **F7:** The other angles showed nothing beyond chance across the roughly 150 cells examined:

## Ideas
- `076-01.b1.b1.g1_falling-agitated-wide-high-close-fade` (from F2, F3, F4, F5): In a falling, agitated market, a day whose high-low range is wide against the coin's average range over the past 20 days and which closes high in that range is followed by a fall over the next day. The fall grows with the product of the range's width and the close's height in it, and wide days closing low in that market instead rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
