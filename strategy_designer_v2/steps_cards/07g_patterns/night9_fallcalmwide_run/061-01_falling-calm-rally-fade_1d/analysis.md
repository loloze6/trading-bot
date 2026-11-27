---
line: 7.g patterns
backtest: 061-01_falling-calm-rally-fade_1d
idea tested: 061-01_falling-calm-rally-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4065 USD
---
## Findings
- **F1:** The tested fade is not in the data. In falling calm, the next day after a scaled rise above 2 is -1.04 % unusual (t -1.27, 35 cases, 26 days), and after a rise of 1 to 2 it is -0.96 % (t -1.97, 165 cases, 100 days). After flat days (|z| ≤ 0.3) it is already -0.54 % (t -2.05, 600 cases, 337 days), so rises fall no more than flat days, the brief's own first test of falsity. The scaled rise and the next day correlate at only -0.033, and step 5 found the larger-half minus smaller-half difference at -0.14 %.
- **F2:** The brief's lopsided half holds only as an absence. In falling calm, scaled falls below -2 do not rebound the next day (-0.55 %, t -0.51, 75 cases, 34 days) or over the next 3 days (-1.80 %, t -1.28).
- **F3:** Outside falling calm, scaled one-day falls rebound the next day, and the rebound is graded:
- **F4:** A close near the day's low is followed by a next-day rise of +0.63 % (t 2.13, 1402 cases, 509 days). In a falling agitated market it is +2.90 % (t 2.43, 148 cases, 67 days); in falling calm it is only +0.13 % (t 0.35).
- **F5:** The other angles show nothing that stands out against the number of bins looked at (about 60):
- **F6:** The book's result is carried by single windows. w14 earned +0.69 summed gain and w18 lost -0.70 (w16 -0.28, w17 -0.17), with no coin standing out beyond about ±0.3.

## Ideas
- No ideas: The tested rally fade is only the falling calm market's own next-day drift (F1, F2). The one pattern that stands out, the graded next-day rebound after scaled falls and low closes outside falling calm (F3, F4), is already held in the map's agitated and falling agitated long cells (038-01, 047-01, 051-01, 045-01, 039-02). Nothing else stands out among the angles examined (F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
