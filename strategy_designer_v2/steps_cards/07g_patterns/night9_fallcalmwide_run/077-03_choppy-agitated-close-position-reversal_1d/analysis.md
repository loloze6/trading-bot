---
line: 7.g patterns
backtest: 077-03_choppy-agitated-close-position-reversal_1d
idea tested: 077-03_choppy-agitated-close-position-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4400 USD
---
## Findings
- **F1:** Inside the tested profile (choppy agitated, as the backtest's regime marks it), the reversal lives on wide days and is stronger after high closes, the opposite of the brief's claim. Wide days closing in the upper half were followed by a next-day excess return of −3.94 % (t −2.76, 69 cases). Wide days closing in the lower half were followed by +1.40 % (t 1.57, 69 cases). Narrow days showed +0.54 % (t 1.18, 127 cases) after high closes and −0.01 % (t −0.01, 92 cases) after low closes.
- **F2:** Inside the profile, the result is graded only at the low-close extreme. The lowest quintile of the forecast's product (close's distance from mid-range × range in usual moves) was followed by +2.06 % (t 2.61, 72 cases). The highest quintile was followed by −1.29 % (t −1.41, 72 cases), and the middle quintiles were mixed: q2 −0.68 % (t −1.23), q3 −0.10 %, q4 −1.51 % (t −1.47). The book earned about the same per in-position bar on each side: long +0.51 % (t 3.45, 157 bars) and short +0.56 % (t 1.99, 180 bars).
- **F3:** Over all bars, with the profile approximated as the 60-day return and the 30-day swing against the 120-day swing, the product's reversal appears only in agitated markets that are not rising. The correlation of the reversed product with next-day excess return in usual moves was 0.25 in falling agitated (t 7.19, 780 bars) and 0.20 in choppy agitated (t 3.03, 227 bars). It was between −0.01 and 0.03 in every calm profile and in rising agitated (|t| ≤ 1.06). The falling agitated part is already held as 058-02.b1.g1.b1.b1, "falling agitated next day reversal".
- **F4:** Choppy agitated high-close days under the approximate profile fell the next day in every product tercile: −1.66 %, −2.44 % and −2.48 % (t_day −0.86, −1.31, −1.71; 40, 41 and 40 cases). The fall grows weakly with the product.
- **F5:** The septile of largest down days (in usual moves) was followed by +0.97 % next day (t 5.49, 1181 cases) and +1.15 % over three days (t 3.88). It was largest in falling agitated: +2.08 % (t_day 1.70, 51 days). This is the falling agitated rebound family that the map already holds 16 times.
- **F6:** In falling agitated markets, the larger an up day against its 30-day swing, the larger the next-day fall: rank correlation −0.12 (t −2.37, 384 up days). High-close days there fell in all three terciles: −1.03 %, −1.12 % and −1.34 % (t_day −1.44, −1.36, −1.66). This lies inside the two strategies already held for falling agitated short (058-02.b1.g1.b1.b1 and 060-01.g1.d2.d1), so it is not a discovery.
- **F7:** The other angles do not stand out given how many were tried:

## Ideas
- `077-03.g1_choppy-agitated-high-close-fall` (from F1, F2, F4): In a choppy, agitated market, a day closing near its high falls over the next day, and the fall is larger the closer the close sits to the high and the wider the day's range against the coin's 30-day swing of daily returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
