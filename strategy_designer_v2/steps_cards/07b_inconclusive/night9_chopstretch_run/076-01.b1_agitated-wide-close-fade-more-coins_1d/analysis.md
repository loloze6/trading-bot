---
line: 7.b inconclusive
backtest: 076-01.b1_agitated-wide-close-fade-more-coins_1d
idea tested: 076-01.b1_agitated-wide-close-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3493 USD
---
## Findings
- **F1:** The test's result is on the side opposite to the idea. Mean short-side move was −0.55 % with t −1.85 (866 days). In the folds shown, the 482 cases gave a short-side mean of −0.50 % (t −0.85, 256 days), and −1.21 % over 3 days (t −1.46). So the wrong sign is not a matter of horizon.
- **F2:** The cases mix two opposite groups, sorted by where the close sits in the day's range. In the lowest quarter of close location, the coin rose next day: short-side mean −2.74 %, t −2.41, 121 cases. The top two quarters fell: +1.17 % (t 1.39) and +0.78 % (t 1.02). The product quartiles show the same, from −2.13 % (t −2.06) up to +1.37 % (t 1.37). This matches the step-5 supporting check, larger half minus smaller half +0.98 %.
- **F3:** On all agitated days, wide days (range at least 1.5 times the 20-day mean range) split by close:
- **F4:** The fade is weaker in calm markets, as the brief predicts. Wide, high-closing calm days gave +0.35 % (t 0.65, 224 cases), against +1.31 % in agitated markets. Narrow high-closing agitated days gave +0.53 % (t 1.51).
- **F5:** Among the cases, days that fell on the day rebounded next day: −1.58 %, t −1.83, 237 cases. Days that rose faded: +0.55 %, t 0.79, 245 cases. The idea's push-up-and-give-back shows only on true high closes.
- **F6:** No single coin or year carries the negative mean. Every year from 2018 to 2021 is between −0.06 % and −0.59 % with |t| under 0.9. Every coin has |t| at or under 1.55. So the result comes from the case definition, not from one part of the data.

## Ideas
- `076-01.b1.b1_agitated-wide-upper-close-fade` (from F2, F3, F4, F5): In an agitated market, a day whose high-low range is wide against the coin's average range over the past 20 days and which closes in the upper part of its range, near its high, is followed by a fall over the next day. The fall is larger the wider the day's range and the farther above the middle of its range it closes, the two multiplying.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
